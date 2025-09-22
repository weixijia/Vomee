"""
Example demonstrating real-time visualization of captured data.
"""

import time
import threading
from vomee import VomeeCapture, Visualizer
from vomee.capture import CaptureConfig


class RealTimeVisualizer:
    """Real-time data visualization for Vomee platform."""
    
    def __init__(self):
        self.visualizer = Visualizer()
        self.capture_data = {'frames': []}
        self.is_running = False
        
    def start_visualization(self, capture: VomeeCapture):
        """Start real-time visualization."""
        self.is_running = True
        
        # Start visualization thread
        vis_thread = threading.Thread(target=self._visualization_loop)
        vis_thread.start()
        
        return vis_thread
    
    def stop_visualization(self):
        """Stop real-time visualization."""
        self.is_running = False
    
    def update_data(self, new_data):
        """Update data for visualization."""
        self.capture_data = new_data
    
    def _visualization_loop(self):
        """Main visualization loop."""
        while self.is_running:
            if self.capture_data.get('frames'):
                try:
                    # Create and display dashboard
                    self.visualizer.create_summary_dashboard(
                        self.capture_data, 
                        save_path='output/realtime_dashboard.png'
                    )
                except Exception as e:
                    print(f"Visualization error: {e}")
            
            time.sleep(2.0)  # Update every 2 seconds


def main():
    """Main function for real-time visualization example."""
    print("Vomee Real-Time Visualization Example")
    print("=" * 40)
    
    # Configuration for shorter capture sessions
    config = CaptureConfig(
        video_enabled=True,
        audio_enabled=True,
        mmwave_enabled=True,
        skeleton_enabled=True,
        sync_tolerance_ms=1.0
    )
    
    # Initialize systems
    capture = VomeeCapture(config)
    visualizer_rt = RealTimeVisualizer()
    
    try:
        # Start capture system
        if not capture.start():
            print("Failed to start capture system")
            return
        
        print("Starting real-time capture and visualization...")
        print("Press Ctrl+C to stop")
        
        # Start visualization
        vis_thread = visualizer_rt.start_visualization(capture)
        
        # Continuous capture loop
        while True:
            # Capture for 2 seconds
            data = capture.record(duration=2.0)
            
            # Update visualization data
            visualizer_rt.update_data(data)
            
            print(f"Captured {len(data.get('frames', []))} frames")
            
    except KeyboardInterrupt:
        print("\nStopping real-time capture...")
        
    finally:
        # Clean shutdown
        visualizer_rt.stop_visualization()
        capture.shutdown()
        print("Real-time visualization stopped")


if __name__ == "__main__":
    main()