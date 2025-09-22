"""
Basic tests for Vomee platform components.
"""

import pytest
import numpy as np
from vomee import VomeeCapture
from vomee.capture import CaptureConfig
from vomee.processing import DataProcessor
from vomee.visualization import Visualizer
from vomee.utils.sync_manager import SyncManager
from vomee.utils.config_manager import ConfigManager


class TestCaptureConfig:
    """Test capture configuration."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = CaptureConfig()
        assert config.video_enabled is True
        assert config.audio_enabled is True
        assert config.mmwave_enabled is True
        assert config.skeleton_enabled is True
        assert config.video_resolution == (1920, 1080)
        assert config.video_fps == 30
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = CaptureConfig(
            video_enabled=False,
            video_resolution=(1280, 720),
            video_fps=60
        )
        assert config.video_enabled is False
        assert config.video_resolution == (1280, 720)
        assert config.video_fps == 60


class TestSyncManager:
    """Test synchronization manager."""
    
    def test_sync_manager_initialization(self):
        """Test sync manager initialization."""
        sync_manager = SyncManager(tolerance_ms=2.0)
        assert sync_manager.tolerance_ms == 2.0
        assert not sync_manager.is_running
    
    def test_sync_manager_lifecycle(self):
        """Test sync manager start/stop lifecycle."""
        sync_manager = SyncManager()
        
        # Start sync manager
        sync_manager.start()
        assert sync_manager.is_running
        assert sync_manager.start_time is not None
        
        # Get timestamp
        timestamp = sync_manager.get_timestamp()
        assert isinstance(timestamp, float)
        assert timestamp >= 0
        
        # Stop sync manager
        sync_manager.stop()
        assert not sync_manager.is_running
        assert sync_manager.start_time is None


class TestDataProcessor:
    """Test data processing components."""
    
    def test_processor_initialization(self):
        """Test processor initialization."""
        processor = DataProcessor()
        assert processor is not None
    
    def test_video_processing(self):
        """Test video data processing."""
        processor = DataProcessor()
        
        # Create dummy video data
        video_data = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Process video
        processed = processor.process_video(video_data)
        assert processed is not None
        assert processed.shape == video_data.shape
    
    def test_audio_processing(self):
        """Test audio data processing."""
        processor = DataProcessor()
        
        # Create dummy audio data
        audio_data = np.random.randn(1024).astype(np.float32)
        
        # Process audio
        processed = processor.process_audio(audio_data)
        assert processed is not None
        assert len(processed) == len(audio_data)
    
    def test_multimodal_fusion(self):
        """Test multimodal data fusion."""
        processor = DataProcessor()
        
        # Create dummy data
        video_data = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        audio_data = np.random.randn(1024).astype(np.float32)
        mmwave_data = {
            'point_cloud': np.random.rand(50, 4),
            'range_doppler': np.random.rand(128, 64)
        }
        skeleton_data = {
            'joints_3d': np.random.rand(33, 3),
            'confidence': np.random.rand(33)
        }
        
        # Fuse data
        fused = processor.fuse_multimodal_data(
            video_data=video_data,
            audio_data=audio_data,
            mmwave_data=mmwave_data,
            skeleton_data=skeleton_data
        )
        
        assert 'video_features' in fused
        assert 'audio_features' in fused
        assert 'mmwave_features' in fused
        assert 'skeleton_features' in fused


class TestVisualizer:
    """Test visualization components."""
    
    def test_visualizer_initialization(self):
        """Test visualizer initialization."""
        visualizer = Visualizer()
        assert visualizer is not None
    
    def test_timeline_plotting(self):
        """Test timeline plotting functionality."""
        visualizer = Visualizer()
        
        # Create dummy data
        dummy_data = {
            'frames': [
                {'timestamp': 0.0, 'video': np.random.rand(100, 100, 3)},
                {'timestamp': 0.1, 'audio': np.random.rand(1024)},
                {'timestamp': 0.2, 'mmwave': {'point_cloud': np.random.rand(10, 4)}},
                {'timestamp': 0.3, 'skeleton': {'joints_3d': np.random.rand(33, 3)}}
            ]
        }
        
        # This should not raise an exception
        try:
            visualizer.plot_multimodal_timeline(dummy_data)
        except Exception as e:
            # Allow for missing display in CI environment
            if "DISPLAY" not in str(e):
                raise


class TestConfigManager:
    """Test configuration management."""
    
    def test_config_manager_initialization(self):
        """Test config manager initialization."""
        config_manager = ConfigManager()
        assert config_manager.config is not None
    
    def test_default_configuration(self):
        """Test default configuration values."""
        config_manager = ConfigManager()
        config = config_manager.get_config()
        
        assert config.video.enabled is True
        assert config.audio.enabled is True
        assert config.video.resolution == (1920, 1080)
        assert config.audio.sample_rate == 44100


class TestVomeeCapture:
    """Test main capture class."""
    
    def test_capture_initialization(self):
        """Test capture system initialization."""
        config = CaptureConfig(
            video_enabled=False,  # Disable to avoid hardware dependencies
            audio_enabled=False,
            mmwave_enabled=False,
            skeleton_enabled=False
        )
        
        capture = VomeeCapture(config)
        assert capture.config == config
        assert not capture.is_recording
    
    def test_capture_lifecycle_mock(self):
        """Test capture lifecycle with mocked sensors."""
        # This test would require mocking the sensor interfaces
        # For now, just test initialization
        config = CaptureConfig(
            video_enabled=False,
            audio_enabled=False,
            mmwave_enabled=False,
            skeleton_enabled=False
        )
        
        capture = VomeeCapture(config)
        assert len(capture.sensors) == 0  # No sensors enabled


# Integration tests (these might require hardware)
class TestIntegration:
    """Integration tests for the complete system."""
    
    @pytest.mark.integration
    def test_full_capture_pipeline(self):
        """Test complete capture pipeline."""
        # This would test with actual hardware
        # Skip in CI environments without hardware
        pytest.skip("Requires hardware setup")
    
    @pytest.mark.integration
    def test_synchronization_accuracy(self):
        """Test timestamp synchronization accuracy."""
        # This would test actual synchronization performance
        pytest.skip("Requires hardware setup")


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__])