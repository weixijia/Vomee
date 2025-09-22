"""
Command line interface for Vomee platform.
"""

import argparse
import json
import sys
from vomee import VomeeCapture
from vomee.capture import CaptureConfig
from vomee.utils.config_manager import ConfigManager


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Vomee Multimodal Sensing Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  vomee capture --duration 10 --output session_001
  vomee capture --config config.json
  vomee list-devices
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Capture command
    capture_parser = subparsers.add_parser('capture', help='Start data capture')
    capture_parser.add_argument('--duration', type=float, default=10.0,
                               help='Recording duration in seconds (default: 10.0)')
    capture_parser.add_argument('--output', type=str, default='vomee_session',
                               help='Output session name (default: vomee_session)')
    capture_parser.add_argument('--config', type=str,
                               help='Configuration file path')
    capture_parser.add_argument('--video', action='store_true', default=True,
                               help='Enable video capture')
    capture_parser.add_argument('--audio', action='store_true', default=True,
                               help='Enable audio capture')
    capture_parser.add_argument('--mmwave', action='store_true', default=False,
                               help='Enable mmWave capture')
    capture_parser.add_argument('--skeleton', action='store_true', default=True,
                               help='Enable skeleton tracking')
    
    # List devices command
    list_parser = subparsers.add_parser('list-devices', help='List available devices')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_parser.add_argument('--create', type=str,
                              help='Create default config file')
    config_parser.add_argument('--validate', type=str,
                              help='Validate config file')
    
    args = parser.parse_args()
    
    if args.command == 'capture':
        run_capture(args)
    elif args.command == 'list-devices':
        list_devices()
    elif args.command == 'config':
        handle_config(args)
    else:
        parser.print_help()


def run_capture(args):
    """Run data capture with given arguments."""
    print("Starting Vomee capture session...")
    
    try:
        # Load configuration
        if args.config:
            config_manager = ConfigManager(args.config)
            config = config_manager.get_config()
        else:
            config = CaptureConfig(
                video_enabled=args.video,
                audio_enabled=args.audio,
                mmwave_enabled=args.mmwave,
                skeleton_enabled=args.skeleton
            )
        
        # Initialize capture
        capture = VomeeCapture(config)
        
        if not capture.start():
            print("Failed to start capture system")
            sys.exit(1)
        
        print(f"Recording for {args.duration} seconds...")
        data = capture.record(duration=args.duration)
        
        # Save data
        output_path = f"output/{args.output}"
        capture.save(data, output_path)
        
        print(f"Capture completed! Data saved to {output_path}")
        print(f"Captured {len(data.get('frames', []))} frames")
        
    except KeyboardInterrupt:
        print("\nCapture interrupted by user")
    except Exception as e:
        print(f"Capture failed: {e}")
        sys.exit(1)
    finally:
        capture.shutdown()


def list_devices():
    """List available capture devices."""
    print("Vomee Device Detection")
    print("=" * 30)
    
    try:
        import cv2
        print("Video Devices:")
        for i in range(5):  # Check first 5 indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"  [{i}] Camera device found")
                cap.release()
        
        import pyaudio
        p = pyaudio.PyAudio()
        print(f"\nAudio Devices ({p.get_device_count()} total):")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"  [{i}] {info['name']} (Input)")
        p.terminate()
        
        print("\nmmWave Devices:")
        print("  Check USB serial ports for connected radar devices")
        
        print("\nSkeleton Tracking:")
        try:
            import pyrealsense2 as rs
            ctx = rs.context()
            devices = ctx.query_devices()
            print(f"  Found {len(devices)} RealSense device(s)")
        except ImportError:
            print("  RealSense SDK not installed")
        
    except Exception as e:
        print(f"Device detection failed: {e}")


def handle_config(args):
    """Handle configuration commands."""
    if args.create:
        create_default_config(args.create)
    elif args.validate:
        validate_config(args.validate)


def create_default_config(filepath):
    """Create default configuration file."""
    default_config = {
        "video": {
            "enabled": True,
            "resolution": [1920, 1080],
            "fps": 30,
            "device_id": 0
        },
        "audio": {
            "enabled": True,
            "sample_rate": 44100,
            "channels": 2
        },
        "mmwave": {
            "enabled": False,
            "device_port": "/dev/ttyUSB0",
            "config_port": "/dev/ttyUSB1"
        },
        "skeleton": {
            "enabled": True,
            "tracking_method": "mediapipe"
        },
        "system": {
            "output_dir": "./output",
            "sync_tolerance_ms": 1.0
        }
    }
    
    try:
        with open(filepath, 'w') as f:
            json.dump(default_config, f, indent=2)
        print(f"Default configuration created: {filepath}")
    except Exception as e:
        print(f"Failed to create config: {e}")


def validate_config(filepath):
    """Validate configuration file."""
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
        
        required_sections = ['video', 'audio', 'mmwave', 'skeleton']
        for section in required_sections:
            if section not in config:
                print(f"Missing section: {section}")
                return False
        
        print(f"Configuration valid: {filepath}")
        return True
        
    except Exception as e:
        print(f"Config validation failed: {e}")
        return False


if __name__ == "__main__":
    main()