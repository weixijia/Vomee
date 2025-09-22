"""
Visualization module for Vomee platform.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, Optional, List


class Visualizer:
    """Visualization tools for multimodal data."""
    
    def __init__(self):
        """Initialize visualizer."""
        plt.style.use('default')
    
    def plot_multimodal_timeline(self, data: Dict[str, Any], save_path: Optional[str] = None):
        """
        Plot timeline of multimodal data capture.
        
        Args:
            data: Multimodal data dictionary
            save_path: Path to save the plot
        """
        fig, axes = plt.subplots(4, 1, figsize=(12, 10))
        fig.suptitle('Vomee Multimodal Data Timeline', fontsize=16)
        
        # Extract timestamps
        frames = data.get('frames', [])
        if not frames:
            return
            
        timestamps = [frame.get('timestamp', 0) for frame in frames]
        
        # Video data visualization
        if any('video' in frame for frame in frames):
            video_activity = [1 if 'video' in frame else 0 for frame in frames]
            axes[0].plot(timestamps, video_activity, 'b-', linewidth=2)
            axes[0].set_ylabel('Video')
            axes[0].set_ylim(-0.1, 1.1)
            axes[0].grid(True, alpha=0.3)
        
        # Audio data visualization
        if any('audio' in frame for frame in frames):
            audio_activity = [1 if 'audio' in frame else 0 for frame in frames]
            axes[1].plot(timestamps, audio_activity, 'g-', linewidth=2)
            axes[1].set_ylabel('Audio')
            axes[1].set_ylim(-0.1, 1.1)
            axes[1].grid(True, alpha=0.3)
        
        # mmWave data visualization
        if any('mmwave' in frame for frame in frames):
            mmwave_activity = [1 if 'mmwave' in frame else 0 for frame in frames]
            axes[2].plot(timestamps, mmwave_activity, 'r-', linewidth=2)
            axes[2].set_ylabel('mmWave')
            axes[2].set_ylim(-0.1, 1.1)
            axes[2].grid(True, alpha=0.3)
        
        # Skeleton data visualization
        if any('skeleton' in frame for frame in frames):
            skeleton_activity = [1 if 'skeleton' in frame else 0 for frame in frames]
            axes[3].plot(timestamps, skeleton_activity, 'm-', linewidth=2)
            axes[3].set_ylabel('Skeleton')
            axes[3].set_ylim(-0.1, 1.1)
            axes[3].grid(True, alpha=0.3)
        
        axes[3].set_xlabel('Time (s)')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def plot_skeleton_joints(self, skeleton_data: Dict[str, Any], save_path: Optional[str] = None):
        """
        Plot skeleton joint positions.
        
        Args:
            skeleton_data: Skeleton tracking data
            save_path: Path to save the plot
        """
        if 'joints_3d' not in skeleton_data:
            return
            
        joints_3d = skeleton_data['joints_3d']
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot joints
        ax.scatter(joints_3d[:, 0], joints_3d[:, 1], joints_3d[:, 2], 
                  c='red', s=50, alpha=0.8)
        
        # Add joint indices
        for i, (x, y, z) in enumerate(joints_3d):
            ax.text(x, y, z, str(i), fontsize=8)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Skeleton Joints')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def plot_mmwave_pointcloud(self, mmwave_data: Dict[str, Any], save_path: Optional[str] = None):
        """
        Plot mmWave point cloud data.
        
        Args:
            mmwave_data: mmWave radar data
            save_path: Path to save the plot
        """
        if 'point_cloud' not in mmwave_data:
            return
            
        point_cloud = mmwave_data['point_cloud']
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot point cloud (x, y, z, intensity)
        scatter = ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2],
                           c=point_cloud[:, 3], cmap='viridis', s=20, alpha=0.7)
        
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('mmWave Point Cloud')
        
        plt.colorbar(scatter, label='Intensity')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def plot_audio_spectrogram(self, audio_data: np.ndarray, sample_rate: int = 44100,
                             save_path: Optional[str] = None):
        """
        Plot audio spectrogram.
        
        Args:
            audio_data: Audio samples
            sample_rate: Audio sample rate
            save_path: Path to save the plot
        """
        plt.figure(figsize=(12, 6))
        
        # Compute spectrogram
        plt.specgram(audio_data, Fs=sample_rate, cmap='viridis')
        plt.colorbar(label='Power (dB)')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Audio Spectrogram')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def create_summary_dashboard(self, data: Dict[str, Any], save_path: Optional[str] = None):
        """
        Create a comprehensive dashboard of all modalities.
        
        Args:
            data: Multimodal data dictionary
            save_path: Path to save the dashboard
        """
        fig = plt.figure(figsize=(16, 12))
        
        # Timeline plot
        ax1 = plt.subplot(3, 2, (1, 2))
        self._plot_timeline_compact(data, ax1)
        
        # Individual modality plots
        frames = data.get('frames', [])
        if frames:
            # Get sample data from first available frame
            sample_frame = frames[0]
            
            if 'skeleton' in sample_frame:
                ax2 = plt.subplot(3, 2, 3, projection='3d')
                self._plot_skeleton_compact(sample_frame['skeleton'], ax2)
            
            if 'mmwave' in sample_frame:
                ax3 = plt.subplot(3, 2, 4, projection='3d')
                self._plot_mmwave_compact(sample_frame['mmwave'], ax3)
            
            if 'audio' in sample_frame:
                ax4 = plt.subplot(3, 2, 5)
                self._plot_audio_compact(sample_frame['audio'], ax4)
            
            if 'video' in sample_frame:
                ax5 = plt.subplot(3, 2, 6)
                self._plot_video_compact(sample_frame['video'], ax5)
        
        plt.suptitle('Vomee Multimodal Sensing Dashboard', fontsize=16)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def _plot_timeline_compact(self, data: Dict[str, Any], ax):
        """Compact timeline plot for dashboard."""
        frames = data.get('frames', [])
        if not frames:
            return
            
        timestamps = [frame.get('timestamp', 0) for frame in frames]
        modalities = ['video', 'audio', 'mmwave', 'skeleton']
        colors = ['blue', 'green', 'red', 'magenta']
        
        for i, modality in enumerate(modalities):
            activity = [1 if modality in frame else 0 for frame in frames]
            ax.plot(timestamps, np.array(activity) + i, color=colors[i], 
                   linewidth=2, label=modality)
        
        ax.set_ylabel('Modalities')
        ax.set_xlabel('Time (s)')
        ax.set_title('Data Capture Timeline')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_skeleton_compact(self, skeleton_data: Dict[str, Any], ax):
        """Compact skeleton plot for dashboard."""
        if 'joints_3d' in skeleton_data:
            joints = skeleton_data['joints_3d']
            ax.scatter(joints[:, 0], joints[:, 1], joints[:, 2], c='red', s=10)
            ax.set_title('Skeleton Joints')
    
    def _plot_mmwave_compact(self, mmwave_data: Dict[str, Any], ax):
        """Compact mmWave plot for dashboard."""
        if 'point_cloud' in mmwave_data:
            pc = mmwave_data['point_cloud']
            ax.scatter(pc[:, 0], pc[:, 1], pc[:, 2], c=pc[:, 3], s=5, cmap='viridis')
            ax.set_title('mmWave Point Cloud')
    
    def _plot_audio_compact(self, audio_data: np.ndarray, ax):
        """Compact audio plot for dashboard."""
        ax.plot(audio_data)
        ax.set_title('Audio Waveform')
        ax.set_xlabel('Samples')
    
    def _plot_video_compact(self, video_data: np.ndarray, ax):
        """Compact video plot for dashboard."""
        if len(video_data.shape) == 3:  # Single frame
            ax.imshow(video_data)
            ax.set_title('Video Frame')
            ax.axis('off')