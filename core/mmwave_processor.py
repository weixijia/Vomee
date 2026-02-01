"""
mmWave Radar Signal Processor Module

Handles GPU-accelerated FFT processing for TI IWR1843 mmWave radar data.
Generates Range-Doppler, Range-Azimuth, and Doppler-Azimuth heatmaps.

Preserved core logic from fft.py.
"""

import numpy as np
from typing import Tuple

import sys
sys.path.append('..')
from config import ADC_PARAMS

# Try to import CuPy with error handling
CUPY_AVAILABLE = False
cp = None

try:
    import cupy as cp
    # Test GPU availability
    cp.cuda.Device(0).compute_capability
    CUPY_AVAILABLE = True
    print(f"[Processor] CuPy {cp.__version__} with CUDA ready")
except Exception as e:
    print(f"[Processor] CuPy/CUDA not available: {e}")
    print("[Processor] Falling back to NumPy (slower)")


class MmWaveProcessor:
    """
    GPU-accelerated mmWave radar signal processor.

    Uses CuPy for FFT processing to generate heatmaps from raw ADC data.
    """

    def __init__(self, num_angle_bins: int = 256):
        """
        Initialize the processor.

        Args:
            num_angle_bins: Number of angle bins for azimuth FFT (default 256)
        """
        self.num_angle_bins = num_angle_bins
        self.adc_params = ADC_PARAMS
        self.use_gpu = CUPY_AVAILABLE

        # Pre-calculate shapes
        self.chirps = ADC_PARAMS['chirps']
        self.rx = ADC_PARAMS['rx']
        self.tx = ADC_PARAMS['tx']
        self.samples = ADC_PARAMS['samples']
        self.iq = ADC_PARAMS['IQ']

        # Virtual antenna count (tx * rx for first 2 tx)
        self.virtual_antennas = 2 * self.rx  # Using tx 0:2

        # Select array library (CuPy for GPU, NumPy for CPU)
        self._xp = cp if self.use_gpu else np
        self._fft = cp.fft if self.use_gpu else np.fft

    def process(self, raw_data: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Process raw ADC data and generate heatmaps.

        Args:
            raw_data: Raw ADC data as int16 numpy array

        Returns:
            Tuple of (rd_heatmap, ra_heatmap, da_heatmap), all normalized [0,1]
        """
        xp = self._xp

        try:
            # Transfer to GPU if using CuPy
            if self.use_gpu:
                adc_data = xp.asarray(raw_data)
            else:
                adc_data = raw_data

            # Reshape: (chirps, tx, rx, samples/2, IQ, 2)
            adc_data = xp.reshape(adc_data, (-1, self.chirps, self.tx, self.rx,
                                              self.samples // 2, self.iq, 2))

            # Transpose to interleave properly
            adc_data = xp.transpose(adc_data, (0, 1, 2, 3, 4, 6, 5))

            # Reshape to: (chirps, tx, rx, samples, IQ)
            adc_data = xp.reshape(adc_data, (-1, self.chirps, self.tx, self.rx,
                                              self.samples, self.iq))

            # Convert I/Q to complex: I + jQ
            adc_data = (adc_data[:, :, :, :, :, 0] + 1j * adc_data[:, :, :, :, :, 1]).astype(xp.complex64)

            # Extract 2D data: (chirps, virtual_antennas, samples) using first 2 TX
            adc_data_2d = xp.reshape(adc_data[:, :, 0:2, :, :],
                                      (-1, self.chirps, self.virtual_antennas, self.samples))

            # Use first frame
            adc_data_frame = adc_data_2d[0]

            # Zero-pad azimuth dimension to num_angle_bins
            padding = ((0, 0), (0, self.num_angle_bins - adc_data_2d.shape[2]), (0, 0))
            adc_data_padded = xp.pad(adc_data_frame, padding, mode='constant')

            # 3D FFT
            fft_data = self._fft.fftn(adc_data_padded)  # Shape: (255, 256, 256)

            # FFT shift on doppler and azimuth axes
            fft_data = self._fft.fftshift(fft_data, axes=(0, 1))

            # Generate heatmaps
            rd_img = self._compute_range_doppler(fft_data, xp)
            ra_img = self._compute_range_azimuth(fft_data, xp)
            da_img = self._compute_doppler_azimuth(fft_data, xp)

            # Transfer back to CPU if using CuPy
            if self.use_gpu:
                return xp.asnumpy(rd_img), xp.asnumpy(ra_img), xp.asnumpy(da_img)
            else:
                return rd_img, ra_img, da_img

        except Exception as e:
            # If GPU fails, try falling back to CPU
            if self.use_gpu:
                print(f"[Processor] GPU error: {e}, falling back to CPU")
                self.use_gpu = False
                self._xp = np
                self._fft = np.fft
                return self.process(raw_data)  # Retry with CPU
            else:
                raise

    def _compute_range_doppler(self, fft_data, xp) -> np.ndarray:
        """
        Compute Range-Doppler heatmap.

        Args:
            fft_data: 3D FFT output (doppler, azimuth, range)
            xp: Array library (cupy or numpy)

        Returns:
            Normalized Range-Doppler heatmap
        """
        # Sum over azimuth, log scale, transpose
        range_doppler = xp.log10((xp.abs(fft_data)**2).sum(1)).T

        # Normalize to [0, 1]
        range_doppler = (range_doppler - xp.min(range_doppler)) / (xp.max(range_doppler) - xp.min(range_doppler) + 1e-10)

        # Flip vertically
        range_doppler = range_doppler[::-1]

        return range_doppler

    def _compute_range_azimuth(self, fft_data, xp) -> np.ndarray:
        """
        Compute Range-Azimuth heatmap.

        Args:
            fft_data: 3D FFT output (doppler, azimuth, range)
            xp: Array library (cupy or numpy)

        Returns:
            Normalized Range-Azimuth heatmap
        """
        # Sum over doppler, log scale, transpose
        range_azimuth = xp.log10((xp.abs(fft_data)**2).sum(0)).T

        # Normalize to [0, 1]
        range_azimuth = (range_azimuth - xp.min(range_azimuth)) / (xp.max(range_azimuth) - xp.min(range_azimuth) + 1e-10)

        # Flip vertically
        range_azimuth = range_azimuth[::-1]

        return range_azimuth

    def _compute_doppler_azimuth(self, fft_data, xp) -> np.ndarray:
        """
        Compute Doppler-Azimuth heatmap.

        Args:
            fft_data: 3D FFT output (doppler, azimuth, range)
            xp: Array library (cupy or numpy)

        Returns:
            Normalized Doppler-Azimuth heatmap
        """
        # Sum over range, log scale, transpose
        doppler_azimuth = xp.log10((xp.abs(fft_data)**2).sum(2)).T

        # Normalize to [0, 1]
        doppler_azimuth = (doppler_azimuth - xp.min(doppler_azimuth)) / (xp.max(doppler_azimuth) - xp.min(doppler_azimuth) + 1e-10)

        return doppler_azimuth

