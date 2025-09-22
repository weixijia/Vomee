"""
Basic example of using the Vomee platform for multimodal data capture.
"""

import time
import numpy as np
from vomee import VomeeCapture
from vomee.capture import CaptureConfig


def main():
    """Main example function."""
    print("Vomee Multimodal Sensing Platform - Basic Example")
    print("=" * 50)
    
    # Create configuration
    config = CaptureConfig(
        video_enabled=True,
        audio_enabled=True,
        mmwave_enabled=True,
        skeleton_enabled=True,
        video_resolution=(1920, 1080),
        video_fps=30,
        audio_sample_rate=44100,
        sync_tolerance_ms=1.0
    )
    
    # Initialize capture system
    print("Initializing Vomee capture system...")
    capture = VomeeCapture(config)
    
    try:
        # Start the capture system
        if not capture.start():
            print("Failed to start capture system")
            return
        
        print("Capture system started successfully!")
        print("Starting 5-second recording session...")
        
        # Record for 5 seconds
        data = capture.record(duration=5.0)
        
        print(f"Recording completed! Captured {len(data.get('frames', []))} frames")
        
        # Save the data
        output_path = "output/example_session"
        capture.save(data, output_path)
        print(f"Data saved to {output_path}")
        
        # Display some statistics
        frames = data.get('frames', [])
        if frames:
            print("\nCapture Statistics:")
            print(f"- Total frames: {len(frames)}")
            
            # Count frames per modality
            video_frames = sum(1 for f in frames if 'video' in f)
            audio_frames = sum(1 for f in frames if 'audio' in f)
            mmwave_frames = sum(1 for f in frames if 'mmwave' in f)
            skeleton_frames = sum(1 for f in frames if 'skeleton' in f)
            
            print(f"- Video frames: {video_frames}")
            print(f"- Audio frames: {audio_frames}")
            print(f"- mmWave frames: {mmwave_frames}")
            print(f"- Skeleton frames: {skeleton_frames}")
            
            # Timing analysis
            timestamps = [f.get('timestamp', 0) for f in frames]
            if timestamps:
                duration = max(timestamps) - min(timestamps)
                fps = len(frames) / duration if duration > 0 else 0
                print(f"- Recording duration: {duration:.2f} seconds")
                print(f"- Average capture rate: {fps:.2f} FPS")
        
    except KeyboardInterrupt:
        print("\nRecording interrupted by user")
        
    except Exception as e:
        print(f"Error during capture: {e}")
        
    finally:
        # Clean shutdown
        print("Shutting down capture system...")
        capture.shutdown()
        print("Shutdown complete!")


if __name__ == "__main__":
    main()