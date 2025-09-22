"""
Example demonstrating data processing and analysis with Vomee.
"""

import numpy as np
from vomee import VomeeCapture, DataProcessor, Visualizer
from vomee.capture import CaptureConfig


def main():
    """Demonstrate data processing pipeline."""
    print("Vomee Data Processing Example")
    print("=" * 35)
    
    # Configuration for processing example
    config = CaptureConfig(
        video_enabled=True,
        audio_enabled=True,
        mmwave_enabled=True,
        skeleton_enabled=True
    )
    
    # Initialize components
    capture = VomeeCapture(config)
    processor = DataProcessor()
    visualizer = Visualizer()
    
    try:
        # Start capture
        if not capture.start():
            print("Failed to start capture system")
            return
        
        print("Recording 5 seconds of data for processing...")
        data = capture.record(duration=5.0)
        
        print("Processing captured data...")
        processed_data = process_multimodal_data(data, processor)
        
        print("Creating visualizations...")
        create_visualizations(data, processed_data, visualizer)
        
        print("Analysis complete!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        capture.shutdown()


def process_multimodal_data(data, processor):
    """Process data from all modalities."""
    frames = data.get('frames', [])
    if not frames:
        return {}
    
    processed_frames = []
    
    for i, frame in enumerate(frames):
        processed_frame = {'timestamp': frame.get('timestamp', 0)}
        
        # Process video data
        if 'video' in frame:
            video_data = frame['video']
            processed_video = processor.process_video(video_data)
            processed_frame['video'] = processed_video
        
        # Process audio data
        if 'audio' in frame:
            audio_data = frame['audio']
            processed_audio = processor.process_audio(audio_data)
            processed_frame['audio'] = processed_audio
        
        # Process mmWave data
        if 'mmwave' in frame:
            mmwave_data = frame['mmwave']
            processed_mmwave = processor.process_mmwave(mmwave_data)
            processed_frame['mmwave'] = processed_mmwave
        
        # Process skeleton data
        if 'skeleton' in frame:
            skeleton_data = frame['skeleton']
            processed_skeleton = processor.process_skeleton(skeleton_data)
            processed_frame['skeleton'] = processed_skeleton
        
        processed_frames.append(processed_frame)
        
        if i % 10 == 0:
            print(f"Processed frame {i+1}/{len(frames)}")
    
    return {'frames': processed_frames, 'metadata': data.get('metadata', {})}


def create_visualizations(raw_data, processed_data, visualizer):
    """Create visualizations for the data."""
    
    # Timeline visualization
    print("Creating timeline visualization...")
    visualizer.plot_multimodal_timeline(
        raw_data, 
        save_path='output/timeline.png'
    )
    
    # Dashboard visualization
    print("Creating dashboard...")
    visualizer.create_summary_dashboard(
        processed_data,
        save_path='output/dashboard.png'
    )
    
    # Individual modality visualizations
    frames = raw_data.get('frames', [])
    if frames and len(frames) > 0:
        sample_frame = frames[0]
        
        # Skeleton visualization
        if 'skeleton' in sample_frame:
            print("Creating skeleton visualization...")
            visualizer.plot_skeleton_joints(
                sample_frame['skeleton'],
                save_path='output/skeleton.png'
            )
        
        # mmWave visualization
        if 'mmwave' in sample_frame:
            print("Creating mmWave visualization...")
            visualizer.plot_mmwave_pointcloud(
                sample_frame['mmwave'],
                save_path='output/mmwave.png'
            )
        
        # Audio visualization
        if 'audio' in sample_frame:
            print("Creating audio visualization...")
            visualizer.plot_audio_spectrogram(
                sample_frame['audio'],
                save_path='output/audio.png'
            )


def analyze_activity_patterns(data):
    """Analyze activity patterns from multimodal data."""
    frames = data.get('frames', [])
    if not frames:
        return
    
    print("\nActivity Pattern Analysis:")
    print("-" * 30)
    
    # Analyze data availability
    video_frames = sum(1 for f in frames if 'video' in f)
    audio_frames = sum(1 for f in frames if 'audio' in f)
    mmwave_frames = sum(1 for f in frames if 'mmwave' in f)
    skeleton_frames = sum(1 for f in frames if 'skeleton' in f)
    
    total_frames = len(frames)
    
    print(f"Data completeness:")
    print(f"  Video: {video_frames/total_frames*100:.1f}%")
    print(f"  Audio: {audio_frames/total_frames*100:.1f}%")
    print(f"  mmWave: {mmwave_frames/total_frames*100:.1f}%")
    print(f"  Skeleton: {skeleton_frames/total_frames*100:.1f}%")
    
    # Temporal analysis
    timestamps = [f.get('timestamp', 0) for f in frames]
    if len(timestamps) > 1:
        time_gaps = np.diff(timestamps)
        avg_interval = np.mean(time_gaps)
        max_gap = np.max(time_gaps)
        
        print(f"\nTemporal characteristics:")
        print(f"  Average frame interval: {avg_interval*1000:.2f} ms")
        print(f"  Maximum gap: {max_gap*1000:.2f} ms")
        print(f"  Effective frame rate: {1/avg_interval:.2f} FPS")


if __name__ == "__main__":
    main()