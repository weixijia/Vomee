"""
Simple verification script to check installation and basic functionality.
"""

import sys
import importlib


def check_python_version():
    """Check Python version compatibility."""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {sys.version}")
    return True


def check_dependencies():
    """Check if core dependencies are available."""
    dependencies = {
        'numpy': 'numpy',
        'matplotlib': 'matplotlib', 
        # Optional dependencies - don't fail if missing
        'cv2': 'opencv-python (optional)',
        'pyaudio': 'pyaudio (optional)',
        'serial': 'pyserial (optional)'
    }
    
    print("\nChecking dependencies...")
    results = {}
    
    for module, name in dependencies.items():
        try:
            importlib.import_module(module)
            print(f"✅ {name}")
            results[module] = True
        except ImportError:
            if module in ['cv2', 'pyaudio', 'serial']:
                print(f"⚠️  {name} - not installed (optional)")
                results[module] = False
            else:
                print(f"❌ {name} - required")
                results[module] = False
    
    return results


def check_vomee_import():
    """Check if Vomee package can be imported."""
    print("\nChecking Vomee package...")
    try:
        # Try importing without hardware dependencies
        import vomee
        print(f"✅ Vomee version {vomee.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Vomee import failed: {e}")
        return False


def run_basic_test():
    """Run basic functionality test."""
    print("\nRunning basic tests...")
    try:
        from vomee.utils.sync_manager import SyncManager
        from vomee.utils.config_manager import ConfigManager
        from vomee.processing import DataProcessor
        
        # Test sync manager
        sync = SyncManager()
        sync.start()
        timestamp = sync.get_timestamp()
        sync.stop()
        print(f"✅ Sync manager: timestamp = {timestamp:.3f}")
        
        # Test config manager
        config = ConfigManager()
        print("✅ Config manager: initialized")
        
        # Test data processor
        processor = DataProcessor()
        print("✅ Data processor: initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False


def main():
    """Main verification function."""
    print("Vomee Installation Verification")
    print("=" * 35)
    
    results = []
    
    # Check Python version
    results.append(check_python_version())
    
    # Check dependencies
    dep_results = check_dependencies()
    results.append(all(dep_results[dep] for dep in ['numpy', 'matplotlib']))
    
    # Check Vomee import
    results.append(check_vomee_import())
    
    # Run basic tests
    results.append(run_basic_test())
    
    # Summary
    print("\n" + "=" * 35)
    if all(results):
        print("✅ Verification PASSED - Vomee is ready to use!")
        print("\nNext steps:")
        print("1. Install optional dependencies for your hardware")
        print("2. Run: python examples/basic_capture.py")
        print("3. Check hardware setup: docs/hardware_setup.md")
    else:
        print("❌ Verification FAILED - Please check the issues above")
        print("\nTroubleshooting:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Check Python version compatibility")
        print("3. Consult installation guide: docs/installation.md")
    
    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)