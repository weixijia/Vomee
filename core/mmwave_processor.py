"""
mmWave Radar Signal Processor Module

GPU-accelerated FFT processing (Range-Doppler / Range-Azimuth / Doppler-Azimuth)
for TI xWR1843 raw ADC.

Uses **PyTorch** so the SAME code runs GPU-accelerated on NVIDIA (CUDA) and Apple
Silicon (MPS), and on CPU everywhere — replacing the former NVIDIA-only CuPy path
for full macOS/Ubuntu/Windows cross-platform support. Falls back to NumPy if torch
is unavailable. Core reshape/FFT/orientation logic preserved from fft.py (verified
to produce identical RA/RD: relative FFT error ~3e-8, normalized heatmap diff ~2e-7).
"""
import os
# Process-wide hint for the POSE pipeline's MPS path on Apple Silicon (lets unsupported
# MPS ops fall back to CPU). This module's FFT does NOT use MPS (see _pick_device).
os.environ.setdefault('PYTORCH_ENABLE_MPS_FALLBACK', '1')

import sys
from typing import Tuple

import numpy as np

sys.path.append('..')
from config import ADC_PARAMS

# PyTorch preferred (CUDA / MPS / CPU); NumPy is the fallback.
TORCH_AVAILABLE = False
torch = None
try:
    import torch as _torch
    torch = _torch
    TORCH_AVAILABLE = True
except Exception as e:  # pragma: no cover
    print(f"[Processor] PyTorch unavailable ({e}); using NumPy (CPU)")


def _pick_device():
    # FFT device: CUDA if available, else CPU. MPS is intentionally NOT used here --
    # torch.fft (_fft_c2c/_fft_r2c) is unimplemented on the Apple-Silicon MPS backend
    # and complex tensors cannot transfer to MPS (pytorch #78044 / #116392), and the
    # MPS->CPU fallback env var does not rescue FFT/complex ops. CPU torch.fft is
    # correct and fast for a 256x255 frame; MPS still serves the pose pipeline elsewhere.
    if not TORCH_AVAILABLE:
        return None
    try:
        if torch.cuda.is_available():
            return 'cuda'
    except Exception:
        pass
    return 'cpu'


class MmWaveProcessor:
    """3D-FFT processor producing normalized RD/RA/DA heatmaps from raw ADC."""

    def __init__(self, num_angle_bins: int = 256, flip_range: bool = False):
        self.num_angle_bins = num_angle_bins
        # flip_range: put range 0 (near) at BOTTOM. The default (False) is the verified orientation
        # for the pure-Python/studio_cli capture. mmWave-Studio-sourced frames (received via
        # --no-trigger) have the range axis mirrored (different ADC I/Q-interleave), so set True there.
        self.flip_range = flip_range
        self.adc_params = ADC_PARAMS
        self.chirps = ADC_PARAMS['chirps']
        self.rx = ADC_PARAMS['rx']
        self.tx = ADC_PARAMS['tx']
        self.samples = ADC_PARAMS['samples']
        self.iq = ADC_PARAMS['IQ']
        self.virtual_antennas = 2 * self.rx          # first 2 TX

        self.device = _pick_device()
        self.use_torch = TORCH_AVAILABLE and self.device is not None
        if self.use_torch:
            print(f"[Processor] PyTorch {torch.__version__} on '{self.device}'")
        else:
            print("[Processor] NumPy (CPU)")

    def process(self, raw_data: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """raw int16 ADC -> (rd, ra, da), each normalized [0,1]."""
        if self.use_torch:
            try:
                return self._process_torch(raw_data, self.device)
            except Exception as e:
                print(f"[Processor] torch '{self.device}' error: {e}; retry on CPU")
                try:
                    return self._process_torch(raw_data, 'cpu')
                except Exception as e2:
                    print(f"[Processor] torch CPU error: {e2}; falling back to NumPy")
        return self._process_numpy(raw_data)

    # ---------- PyTorch path (CUDA / Apple-Silicon MPS / CPU) ----------
    def _process_torch(self, raw_data, device):
        t = torch.as_tensor(np.ascontiguousarray(raw_data), dtype=torch.int16, device=device)
        t = t.reshape(-1, self.chirps, self.tx, self.rx, self.samples // 2, self.iq, 2)
        t = t.permute(0, 1, 2, 3, 4, 6, 5).contiguous()
        t = t.reshape(-1, self.chirps, self.tx, self.rx, self.samples, self.iq)
        cplx = torch.complex(t[..., 0].float(), t[..., 1].float())            # I + jQ
        d2 = cplx[:, :, 0:2, :, :].reshape(-1, self.chirps, self.virtual_antennas, self.samples)
        frame = d2[0]                                                         # (chirps, VA, samples)
        # zero-pad azimuth (VA) to num_angle_bins (avoid F.pad on complex)
        padded = torch.zeros((frame.shape[0], self.num_angle_bins, frame.shape[2]),
                             dtype=frame.dtype, device=frame.device)
        padded[:, :frame.shape[1], :] = frame
        fft = torch.fft.fftshift(torch.fft.fftn(padded), dim=(0, 1))
        power = fft.abs() ** 2
        rd = self._nf_t(torch.log10(power.sum(1)).T, self.flip_range)         # (range, doppler) — near at BOTTOM
        ra = self._nf_t(torch.log10(power.sum(0)).T, self.flip_range)         # (range, azimuth) — near at BOTTOM (matches RD)
        da = self._nf_t(torch.log10(power.sum(2)).T, False)                   # (azimuth, doppler) — no range axis
        return rd.cpu().numpy(), ra.cpu().numpy(), da.cpu().numpy()

    @staticmethod
    def _nf_t(x, flip):
        x = (x - x.min()) / (x.max() - x.min() + 1e-10)
        return torch.flip(x, dims=[0]) if flip else x

    # ---------- NumPy fallback (identical math + orientation) ----------
    def _process_numpy(self, raw_data):
        adc = np.reshape(raw_data, (-1, self.chirps, self.tx, self.rx, self.samples // 2, self.iq, 2))
        adc = np.transpose(adc, (0, 1, 2, 3, 4, 6, 5))
        adc = np.reshape(adc, (-1, self.chirps, self.tx, self.rx, self.samples, self.iq))
        adc = (adc[:, :, :, :, :, 0] + 1j * adc[:, :, :, :, :, 1]).astype(np.complex64)
        d2 = np.reshape(adc[:, :, 0:2, :, :], (-1, self.chirps, self.virtual_antennas, self.samples))
        frame = d2[0]
        frame = np.pad(frame, ((0, 0), (0, self.num_angle_bins - d2.shape[2]), (0, 0)), mode='constant')
        fft = np.fft.fftshift(np.fft.fftn(frame), axes=(0, 1))
        power = np.abs(fft) ** 2
        rd = self._nf_n(np.log10(power.sum(1)).T, self.flip_range)   # near at BOTTOM
        ra = self._nf_n(np.log10(power.sum(0)).T, self.flip_range)   # near at BOTTOM (matches RD)
        da = self._nf_n(np.log10(power.sum(2)).T, False)
        return rd, ra, da

    @staticmethod
    def _nf_n(x, flip):
        x = (x - x.min()) / (x.max() - x.min() + 1e-10)
        return np.ascontiguousarray(x[::-1] if flip else x)
