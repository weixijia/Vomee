# API Reference

## VomeeCapture

Main class for coordinating multimodal data capture.

### Constructor

```python
VomeeCapture(config: Optional[CaptureConfig] = None)
```

**Parameters:**
- `config`: Configuration object with capture parameters

### Methods

#### start()
```python
start() -> bool
```
Start the capture system.

**Returns:** `bool` - True if all sensors started successfully

#### record()
```python
record(duration: Optional[float] = None) -> Dict[str, Any]
```
Start recording data from all sensors.

**Parameters:**
- `duration`: Recording duration in seconds (None for manual stop)

**Returns:** `Dict` containing captured data from all sensors

#### stop()
```python
stop() -> Dict[str, Any]
```
Stop recording and return captured data.

**Returns:** `Dict` containing all captured data

#### save()
```python
save(data: Dict[str, Any], output_path: str)
```
Save captured data to file.

**Parameters:**
- `data`: Data dictionary from capture
- `output_path`: Path to save the data

#### shutdown()
```python
shutdown()
```
Gracefully shutdown the capture system.

## CaptureConfig

Configuration class for capture sessions.

### Constructor

```python
CaptureConfig(
    video_enabled: bool = True,
    audio_enabled: bool = True,
    mmwave_enabled: bool = True,
    skeleton_enabled: bool = True,
    video_resolution: tuple = (1920, 1080),
    video_fps: int = 30,
    audio_sample_rate: int = 44100,
    audio_channels: int = 2,
    sync_tolerance_ms: float = 1.0,
    output_format: str = "hdf5"
)
```

## DataProcessor

Main data processing class for multimodal data.

### Methods

#### process_video()
```python
process_video(video_data: np.ndarray) -> np.ndarray
```
Process video frames.

#### process_audio()
```python
process_audio(audio_data: np.ndarray) -> np.ndarray
```
Process audio data.

#### process_mmwave()
```python
process_mmwave(mmwave_data: Dict[str, Any]) -> Dict[str, Any]
```
Process mmWave radar data.

#### process_skeleton()
```python
process_skeleton(skeleton_data: Dict[str, Any]) -> Dict[str, Any]
```
Process skeleton tracking data.

#### fuse_multimodal_data()
```python
fuse_multimodal_data(
    video_data: Optional[np.ndarray] = None,
    audio_data: Optional[np.ndarray] = None,
    mmwave_data: Optional[Dict[str, Any]] = None,
    skeleton_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```
Fuse data from multiple modalities.

## Visualizer

Visualization tools for multimodal data.

### Methods

#### plot_multimodal_timeline()
```python
plot_multimodal_timeline(data: Dict[str, Any], save_path: Optional[str] = None)
```
Plot timeline of multimodal data capture.

#### plot_skeleton_joints()
```python
plot_skeleton_joints(skeleton_data: Dict[str, Any], save_path: Optional[str] = None)
```
Plot skeleton joint positions.

#### plot_mmwave_pointcloud()
```python
plot_mmwave_pointcloud(mmwave_data: Dict[str, Any], save_path: Optional[str] = None)
```
Plot mmWave point cloud data.

#### create_summary_dashboard()
```python
create_summary_dashboard(data: Dict[str, Any], save_path: Optional[str] = None)
```
Create a comprehensive dashboard of all modalities.

## SyncManager

Manages timestamp synchronization across multiple sensors.

### Constructor

```python
SyncManager(tolerance_ms: float = 1.0)
```

### Methods

#### start()
```python
start()
```
Start the synchronization manager.

#### stop()
```python
stop()
```
Stop the synchronization manager.

#### get_timestamp()
```python
get_timestamp() -> float
```
Get current synchronized timestamp.

## ConfigManager

Manages configuration for the Vomee platform.

### Constructor

```python
ConfigManager(config_path: Optional[str] = None)
```

### Methods

#### load_config()
```python
load_config(config_path: str)
```
Load configuration from file.

#### save_config()
```python
save_config(config_path: str)
```
Save current configuration to file.

#### get_config()
```python
get_config() -> SystemConfig
```
Get current configuration.

## Example Usage

### Basic Capture

```python
from vomee import VomeeCapture, CaptureConfig

# Create configuration
config = CaptureConfig(
    video_enabled=True,
    audio_enabled=True,
    mmwave_enabled=True,
    skeleton_enabled=True
)

# Initialize and start capture
capture = VomeeCapture(config)
capture.start()

# Record for 10 seconds
data = capture.record(duration=10)

# Save data
capture.save(data, 'output/session_001')
capture.shutdown()
```

### Data Processing

```python
from vomee import DataProcessor, Visualizer

processor = DataProcessor()
visualizer = Visualizer()

# Process captured data
processed_data = processor.fuse_multimodal_data(
    video_data=video_frames,
    audio_data=audio_samples,
    mmwave_data=radar_data,
    skeleton_data=pose_data
)

# Create visualizations
visualizer.create_summary_dashboard(processed_data, 'dashboard.png')
```

### CLI Usage

```bash
# Basic capture
vomee capture --duration 10 --output session_001

# List available devices
vomee list-devices

# Create configuration file
vomee config --create config.json
```