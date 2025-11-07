# Quick Start Guide - Math CHOP Idle Return

Get your Math CHOP returning to a target value in 5 minutes!

## What You'll Need
- TouchDesigner (any recent version)
- A Math CHOP or any CHOP with values you want to control
- 5 minutes

## Step-by-Step Setup

### Method 1: Script CHOP (Easiest - Recommended)

#### 1. Prepare Your Network
```
Create or locate your Math CHOP
Let's say it's called "math1"
```

#### 2. Create the Script CHOP
- In your network, press `Tab` and type `Script CHOP`
- Press Enter to create it
- Position it after your Math CHOP

#### 3. Connect the Network
- Connect your Math CHOP → Script CHOP
- Your network should look like:
```
[math1] → [script1]
```

#### 4. Create the Script DAT
- Press `Tab` and type `Text DAT`
- Press Enter to create it
- Double-click the Text DAT to open it
- Copy and paste the entire contents of `script_chop_idle_return.py`
- Name it something like "idle_return_script"

#### 5. Link Script to Script CHOP
- Click on your Script CHOP
- In the parameters panel (right side), find the **Script** section
- Click on the **DAT** parameter
- Type the name of your Text DAT (e.g., `idle_return_script`)
- Press Enter

#### 6. Configure Parameters
After linking, a new **Custom** page will appear in the Script CHOP parameters:
- Click on the **Custom** page
- You'll see:
  - **Target Value**: Set this to where you want values to return (default: 0.0)
  - **Return Speed**: Set this to how fast (default: 0.05 is good)
  - **Inactivity Delay**: Set this to frames to wait (default: 60 = 2 seconds)
  - **Activity Threshold**: Leave default (0.001) initially

#### 7. Test It!
- Make your Math CHOP values change (use a mouse CHOP, OSC input, etc.)
- Stop changing the values
- Wait for the inactivity delay
- Watch the values smoothly return to your target value!

#### 8. Fine-tune
- **Too fast?** Reduce Return Speed (try 0.02)
- **Too slow?** Increase Return Speed (try 0.1)
- **Starts returning too soon?** Increase Inactivity Delay (try 120)
- **Doesn't detect activity?** Reduce Activity Threshold (try 0.0001)

---

## Method 2: Copy-Paste Quick Setup

If you just want to test quickly without external files:

#### 1. Create Script CHOP
- Create a Script CHOP and connect your input

#### 2. Create Inline Script
- Right-click the Script CHOP
- Select **Customize Component** → **Add Python Callbacks**
- You'll see a DAT appear inside

#### 3. Paste This Minimal Code
```python
# Minimal idle return - paste this in the callbacks DAT

if not hasattr(me, 'state'):
    me.state = {'inactive': 0, 'last': None}

def onCook(scriptOp):
    # Config
    TARGET = 0.0
    SPEED = 0.05
    DELAY = 60
    THRESHOLD = 0.001
    
    # Copy input
    if scriptOp.numInputs > 0:
        scriptOp.copy(scriptOp.inputs[0])
        
        # Check activity
        active = False
        curr = [scriptOp[i][0] for i in range(scriptOp.numChans)]
        
        if me.state['last']:
            for i, val in enumerate(curr):
                if abs(val - me.state['last'][i]) > THRESHOLD:
                    active = True
        
        me.state['inactive'] = 0 if active else me.state['inactive'] + 1
        me.state['last'] = curr
        
        # Return to target
        if me.state['inactive'] >= DELAY:
            for i in range(scriptOp.numChans):
                for s in range(scriptOp.numSamples):
                    scriptOp[i][s] += (TARGET - scriptOp[i][s]) * SPEED
```

#### 4. Adjust the Config Values
Edit these lines in the code above:
```python
TARGET = 0.0    # Your target value
SPEED = 0.05    # 0.01 = slow, 0.2 = fast
DELAY = 60      # Frames to wait
THRESHOLD = 0.001  # Activity detection sensitivity
```

---

## Common Patterns

### Pattern: Mouse-Controlled Visual That Resets
```
[Mouse CHOP] → [Math CHOP] → [Script CHOP + idle return] → [Null CHOP] → [Visuals]
```

### Pattern: Audio-Reactive With Baseline
```
[Audio CHOP] → [Filter] → [Math CHOP] → [Script CHOP + idle return] → [Output]
```

### Pattern: Multiple Independent Returns
```
[Multi-channel Input] → [Select CHOP (chan 0)] → [Script CHOP] → [Combine]
                     → [Select CHOP (chan 1)] → [Script CHOP] → [Combine]
```

---

## Troubleshooting

### "Nothing happens"
✓ Check that your Script DAT is properly linked
✓ Verify the Script CHOP has input connected
✓ Make sure values are actually changing in the input

### "Returns immediately"
✓ Increase INACTIVITY_DELAY (try 120 or 180)
✓ Check that ACTIVITY_THRESHOLD isn't too high

### "Never returns"
✓ Decrease ACTIVITY_THRESHOLD (try 0.0001)
✓ Make sure input values actually stop changing
✓ Check for noisy input signals

### "Returns too fast/slow"
✓ Adjust RETURN_SPEED (lower = slower, higher = faster)

---

## Next Steps

Once you have the basic setup working:

1. **Read** `README.md` for full documentation
2. **Check** `EXAMPLES.md` for configuration recipes
3. **Experiment** with different parameter values
4. **Combine** with other TouchDesigner features

---

## Need Help?

- Check the README.md for detailed explanations
- Review EXAMPLES.md for common configurations
- TouchDesigner Forum: forum.derivative.ca
- TouchDesigner Discord: community channels

Happy creating! 🎨
