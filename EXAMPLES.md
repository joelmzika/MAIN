# TouchDesigner Math CHOP Idle Return - Example Configurations

This file contains example configurations for different use cases.

## Configuration 1: Smooth Particle System Reset
```python
TARGET_VALUE = 0.0
RETURN_SPEED = 0.02       # Slow, organic return
INACTIVITY_DELAY = 90     # 3 seconds at 30 FPS
ACTIVITY_THRESHOLD = 0.005 # Medium sensitivity
```
**Use Case**: Particle systems or fluid simulations that should gently settle when no interaction is detected.

## Configuration 2: Quick UI Reset
```python
TARGET_VALUE = 0.0
RETURN_SPEED = 0.15       # Fast return
INACTIVITY_DELAY = 30     # 1 second at 30 FPS
ACTIVITY_THRESHOLD = 0.001 # High sensitivity
```
**Use Case**: UI elements or menus that should quickly return to default positions after interaction.

## Configuration 3: Audio-Reactive Baseline
```python
TARGET_VALUE = 0.1        # Return to slight baseline
RETURN_SPEED = 0.05       # Medium speed
INACTIVITY_DELAY = 120    # 4 seconds at 30 FPS
ACTIVITY_THRESHOLD = 0.01  # Low sensitivity (ignore small audio fluctuations)
```
**Use Case**: Audio-reactive visuals that should maintain a slight baseline when music is quiet.

## Configuration 4: Camera Position Reset
```python
TARGET_VALUE = 0.0
RETURN_SPEED = 0.03       # Slow, camera-like movement
INACTIVITY_DELAY = 180    # 6 seconds at 30 FPS
ACTIVITY_THRESHOLD = 0.002 # Medium sensitivity
```
**Use Case**: Camera position/rotation that should smoothly return to default view after user interaction.

## Configuration 5: High-Frequency Data Smoothing
```python
TARGET_VALUE = 0.5        # Middle value
RETURN_SPEED = 0.01       # Very slow
INACTIVITY_DELAY = 60     # 2 seconds at 30 FPS
ACTIVITY_THRESHOLD = 0.05  # Very low sensitivity (filters noise)
```
**Use Case**: Noisy sensor data that needs heavy smoothing and should settle to a middle ground.

## Configuration 6: Instant Snap (No Interpolation)
```python
TARGET_VALUE = 0.0
RETURN_SPEED = 1.0        # Immediate
INACTIVITY_DELAY = 45     # 1.5 seconds at 30 FPS
ACTIVITY_THRESHOLD = 0.001 # High sensitivity
```
**Use Case**: Toggle-like behavior where values should snap immediately to target after delay.

## Configuration 7: Gentle Fade Out
```python
TARGET_VALUE = 0.0
RETURN_SPEED = 0.008      # Very slow fade
INACTIVITY_DELAY = 150    # 5 seconds at 30 FPS
ACTIVITY_THRESHOLD = 0.003 # Medium sensitivity
```
**Use Case**: Visual effects or opacity that should very gradually fade out after activity stops.

## Frame Rate Reference Table

Converting delay times for different frame rates:

| Seconds | 30 FPS | 60 FPS | 120 FPS |
|---------|--------|--------|---------|
| 0.5s    | 15     | 30     | 60      |
| 1s      | 30     | 60     | 120     |
| 2s      | 60     | 120    | 240     |
| 3s      | 90     | 180    | 360     |
| 5s      | 150    | 300    | 600     |
| 10s     | 300    | 600    | 1200    |

## Return Speed Visual Guide

- **0.001 - 0.01**: Ultra slow, almost imperceptible (meditation apps, subtle ambiance)
- **0.01 - 0.05**: Slow, organic (natural movement, particle systems)
- **0.05 - 0.15**: Medium, responsive (UI elements, interactive installations)
- **0.15 - 0.3**: Fast, snappy (game-like interactions, quick resets)
- **0.3 - 1.0**: Very fast to instant (toggle behaviors, binary states)

## Advanced: Multiple Target Values per Channel

If you need different channels to return to different values, you can modify the script:

```python
# In the onCook function, replace target_value with a list:
target_values = [0.0, 0.5, 1.0]  # Different target for each channel

for chan_idx in range(scriptOp.numChans):
    target = target_values[chan_idx] if chan_idx < len(target_values) else 0.0
    # ... rest of interpolation logic
```

## Performance Considerations

- **Low overhead**: < 1% CPU for typical setups (1-10 channels, 30 FPS)
- **Moderate overhead**: 1-3% CPU for complex setups (50+ channels, 60 FPS)
- **Optimization tip**: Use only on channels that need idle return behavior
- **Optimization tip**: Increase activity threshold to reduce false positives

## Testing Your Configuration

1. Start with default values
2. Trigger activity in your CHOP (move values)
3. Stop activity and observe:
   - Does it wait the right amount of time?
   - Does it return at the right speed?
   - Does it reach the target value?
4. Adjust parameters incrementally
5. Test edge cases (rapid on/off, very slow changes)
