# Deployment & Usage Instructions

## For TouchDesigner Users

### Option 1: Use the Script CHOP (Recommended)

This is the easiest and most feature-rich approach.

**Steps:**
1. Download `script_chop_idle_return.py` from this repository
2. Open your TouchDesigner project
3. Create a **Text DAT** in your network
4. Open the Text DAT and paste the entire contents of `script_chop_idle_return.py`
5. Name the Text DAT something memorable (e.g., `idle_return_script`)
6. Create a **Script CHOP** in your network
7. Connect your Math CHOP (or any CHOP) to the Script CHOP's input
8. In the Script CHOP parameters:
   - Set **DAT** parameter to point to your Text DAT
   - A **Custom** page will appear
9. Configure the parameters in the Custom page:
   - **Target Value**: Your desired return value
   - **Return Speed**: How fast to return (start with 0.05)
   - **Inactivity Delay**: Frames to wait (60 = 2 seconds @ 30fps)
   - **Activity Threshold**: Sensitivity (start with 0.001)
10. Done! Your CHOP will now smoothly return to the target when inactive

### Option 2: Use the CHOP Execute DAT

For event-driven monitoring and detection.

**Steps:**
1. Download `chopexec_idle_return.py`
2. Create a **CHOP Execute DAT**
3. Paste the contents into the DAT
4. In the DAT parameters, set **CHOPs** to your Math CHOP
5. Modify the configuration constants at the top:
   ```python
   TARGET_VALUE = 0.0
   RETURN_SPEED = 0.05
   INACTIVITY_DELAY = 60
   ACTIVITY_THRESHOLD = 0.001
   ```

### Option 3: Use the Python Class

For advanced users who want to integrate into custom Python scripts.

**Steps:**
1. Download `math_chop_idle_return.py`
2. Create a **Text DAT** with the contents
3. In your custom Python scripts:
   ```python
   import math_chop_idle_return
   
   handler = math_chop_idle_return.MathChopIdleReturn(parent())
   handler.configure(target_value=0.0, return_speed=0.05)
   ```

## File Organization in TouchDesigner

Suggested network organization:

```
/project1
  ├─ /data
  │   ├─ idle_return_script (Text DAT with script_chop_idle_return.py)
  │   └─ idle_return_class (Text DAT with math_chop_idle_return.py)
  │
  ├─ /processing
  │   ├─ math1 (Your Math CHOP)
  │   ├─ script1 (Script CHOP with idle return)
  │   └─ null1 (Output)
  │
  └─ /output
      └─ ...
```

## Configuration Presets

### Preset 1: Interactive Installation (Slow Return)
```
Target Value: 0.0
Return Speed: 0.02
Inactivity Delay: 120 frames (4 seconds @ 30fps)
Activity Threshold: 0.005
```

### Preset 2: UI Control (Fast Return)
```
Target Value: 0.0
Return Speed: 0.15
Inactivity Delay: 30 frames (1 second @ 30fps)
Activity Threshold: 0.001
```

### Preset 3: Audio Reactive (Balanced)
```
Target Value: 0.1
Return Speed: 0.05
Inactivity Delay: 90 frames (3 seconds @ 30fps)
Activity Threshold: 0.01
```

## Integration with Existing Projects

### Adding to Existing Math CHOP
1. Create Script CHOP after your existing Math CHOP
2. Connect: `[Your Math CHOP] → [Script CHOP] → [Your Output]`
3. Configure as described above
4. Your existing downstream operators will work unchanged

### Multiple CHOPs with Different Settings
Create separate Script CHOPs for each channel group:
```
[Source] → [Select chan0] → [Script CHOP (fast return)] → [Merge]
        → [Select chan1] → [Script CHOP (slow return)] → [Merge]
```

### Feedback Loops
Safe to use in feedback loops:
```
[Script CHOP] → [Math CHOP] → [Null] → back to Script CHOP input
```

## Testing Your Setup

1. **Test Activity Detection**:
   - Change your input values
   - Verify the output follows the input

2. **Test Inactivity Detection**:
   - Stop changing input values
   - Wait for the inactivity delay
   - Verify values start returning to target

3. **Test Return Speed**:
   - Adjust Return Speed parameter
   - Observe how fast values return
   - Fine-tune to your preference

4. **Test Threshold**:
   - If using noisy input, increase threshold
   - If values don't detect activity, decrease threshold

## Performance Optimization

### For High Frame Rates (60+ FPS)
- Consider increasing inactivity delay proportionally
- Example: 60 frames @ 30fps = 2 seconds → 120 frames @ 60fps

### For Many Channels (50+)
- Use Select CHOPs to split channels
- Apply idle return only to channels that need it
- Merge back together

### For Real-Time Performance
- Keep return speed ≤ 0.2 for smooth results
- Avoid excessive parameter changes per frame
- Use Null CHOPs to cache processed results

## Common Network Patterns

### Pattern: Mouse-Controlled Parameter
```
[Mouse CHOP] → [Script CHOP] → [CHOP to DAT] → [Parameter]
```

### Pattern: Audio-Reactive Visual
```
[Audio In] → [Analysis] → [Math] → [Script CHOP] → [Visual]
```

### Pattern: Multiple Inputs, Single Return
```
[Input A] ┐
[Input B] ├→ [Math CHOP] → [Script CHOP] → [Output]
[Input C] ┘
```

## Troubleshooting Integration

**Q: Script CHOP shows error "Invalid DAT"**
- A: Make sure you've set the DAT parameter to point to your Text DAT
- A: Verify the Text DAT contains the script code

**Q: Custom parameters don't appear**
- A: Close and reopen the Script CHOP parameters panel
- A: Check that the script has no syntax errors

**Q: Values don't change**
- A: Verify input is connected to Script CHOP
- A: Check that Script CHOP is cooking (green dot)
- A: Look at the Script CHOP info DAT for errors

**Q: Return happens immediately**
- A: Increase the Inactivity Delay parameter
- A: Check that Activity Threshold isn't too high

## Updating the Script

To update to a newer version:
1. Download the new script file
2. Open your Text DAT
3. Replace the entire contents with the new version
4. Save
5. The Script CHOP will automatically reload

## Backup Your Configuration

Save your parameter settings:
1. Right-click the Script CHOP
2. Select **Copy Parameters**
3. Save to a Text DAT or file for reference
4. To restore: **Paste Parameters**

## Support

- **Documentation**: See README.md
- **Quick Setup**: See QUICKSTART.md
- **Examples**: See EXAMPLES.md
- **Troubleshooting**: See README.md "Troubleshooting" section

## Version Compatibility

- Tested with TouchDesigner 2020.20000+
- Compatible with TouchDesigner 2021.x, 2022.x, 2023.x
- Should work with any Python 3.7+ (included in TouchDesigner)

---

**Ready to deploy?** Start with the Script CHOP method (Option 1) for the best experience! 🚀
