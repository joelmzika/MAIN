# TouchDesigner Math CHOP Idle Return

A collection of scripts for TouchDesigner that allow a Math CHOP (or any CHOP) to smoothly return to a specific target value when it becomes inactive.

## Problem Statement

When working with interactive installations or real-time visualizations in TouchDesigner, you often need values to smoothly return to a "rest" or "idle" state when there's no active input. For example:
- A particle system should calm down when there's no interaction
- A visual effect should fade to a baseline when inactive
- Control values should reset to defaults after a period of inactivity

This repository provides multiple implementation approaches for this common pattern.

## Solutions Provided

### 1. Script CHOP Implementation (Recommended)

**File:** `script_chop_idle_return.py`

The Script CHOP approach is the most flexible and easiest to use.

#### Setup:
1. In TouchDesigner, create a **Script CHOP**
2. Connect your Math CHOP (or any CHOP) as input to the Script CHOP
3. Create a **Text DAT** and paste the contents of `script_chop_idle_return.py`
4. In the Script CHOP's parameters:
   - Set the **DAT** parameter to reference your Text DAT
   - Go to the **Custom** page (it will appear after setup)
5. Configure the parameters:
   - **Target Value**: The value to return to (default: 0.0)
   - **Return Speed**: How fast to interpolate (0.001-0.5, default: 0.05)
   - **Inactivity Delay**: Frames to wait before starting return (default: 60)
   - **Activity Threshold**: Minimum change to detect activity (default: 0.001)

#### How It Works:
- Monitors all input channels for value changes
- If changes exceed the activity threshold, reset the inactivity timer
- After the inactivity delay period, smoothly interpolates all channels toward the target value
- Uses linear interpolation (lerp) for smooth transitions

#### Example Use Cases:
```
Input CHOP → Script CHOP (with idle return) → Output to visuals
Math CHOP → Script CHOP (with idle return) → Null CHOP → Other operators
```

### 2. CHOP Execute Implementation

**File:** `chopexec_idle_return.py`

This approach uses CHOP Execute callbacks for event-driven behavior.

#### Setup:
1. Create a **CHOP Execute DAT**
2. Paste the contents of `chopexec_idle_return.py`
3. In the CHOP Execute DAT parameters:
   - Set the **CHOPs** parameter to reference your Math CHOP
4. Modify the configuration constants at the top of the script:
   ```python
   TARGET_VALUE = 0.0
   RETURN_SPEED = 0.05
   INACTIVITY_DELAY = 60
   ACTIVITY_THRESHOLD = 0.001
   ```

#### Limitations:
This is more of a monitoring/detection script. For actual value modification, combine it with the Script CHOP approach.

### 3. Python Class Implementation

**File:** `math_chop_idle_return.py`

A reusable Python class that can be imported and used in various contexts.

#### Setup:
1. Create a **Text DAT** with the contents of `math_chop_idle_return.py`
2. Import and use in your scripts:
   ```python
   import math_chop_idle_return
   idle_handler = math_chop_idle_return.MathChopIdleReturn(parent())
   idle_handler.configure(target_value=0.0, return_speed=0.05)
   ```

## Parameters Explained

### Target Value
The value that all channels will return to when inactive.
- **Range**: Any float value
- **Default**: 0.0
- **Example**: Set to 0.5 for a mid-point rest state

### Return Speed
Controls how quickly values interpolate toward the target.
- **Range**: 0.001 (very slow) to 0.5 (very fast)
- **Default**: 0.05 (smooth transition)
- **Formula**: `new_value = current + (target - current) * speed`
- **Tip**: Lower values create more gradual, organic-feeling returns

### Inactivity Delay (frames)
Number of frames to wait before starting the return transition.
- **Range**: 0 to any positive integer
- **Default**: 60 frames (2 seconds at 30 FPS, 1 second at 60 FPS)
- **Example**: Set to 90 for a 3-second delay at 30 FPS

### Activity Threshold
Minimum value change required to be considered "active."
- **Range**: 0.0001 to 0.1
- **Default**: 0.001
- **Tip**: Increase if noisy inputs are preventing idle return
- **Tip**: Decrease for more sensitive activity detection

## Network Setup Examples

### Basic Setup
```
[Math CHOP] → [Script CHOP with idle return] → [Null CHOP] → [Your operators]
```

### With Monitoring
```
[Math CHOP] → [Script CHOP with idle return] → [Null CHOP]
                                                      ↓
                                                [Trail CHOP]
                                                      ↓
                                                [Analysis]
```

### Multiple Channels
```
[Multi-channel CHOP] → [Script CHOP] → [Output]
                            ↓
                    Returns all channels
                    to same target value
```

## Tips and Best Practices

1. **Tuning Return Speed**: Start with 0.05 and adjust based on feel. Slower (0.01-0.03) for organic, faster (0.1-0.2) for responsive.

2. **Frame Rate Consideration**: The inactivity delay is in frames, so adjust based on your project's FPS.

3. **Noise Handling**: If your input has noise, increase the activity threshold to prevent false activity detection.

4. **Multiple Targets**: To return different channels to different values, use multiple Script CHOPs with select CHOPs.

5. **Performance**: The Script CHOP approach is efficient and runs every frame. For complex networks, consider using it only where needed.

## Troubleshooting

**Problem**: Values never return to target
- **Solution**: Check that input values are actually changing less than the activity threshold
- **Solution**: Verify the inactivity delay isn't too long

**Problem**: Return happens too quickly
- **Solution**: Reduce the return speed parameter (try 0.01-0.03)

**Problem**: Return starts too soon
- **Solution**: Increase the inactivity delay parameter

**Problem**: Activity detection is too sensitive
- **Solution**: Increase the activity threshold parameter

## Technical Details

The implementation uses linear interpolation (lerp) for smooth transitions:
```
new_value = current_value + (target_value - current_value) * return_speed
```

This creates an exponential decay curve toward the target, resulting in smooth, natural-looking transitions.

## Requirements

- TouchDesigner 2020.20000 or later (tested)
- No external dependencies

## License

This code is provided as-is for use in TouchDesigner projects.

## Contributing

Feel free to modify and extend these scripts for your specific use cases.

## Support

For issues or questions, please refer to the TouchDesigner documentation or community forums.
