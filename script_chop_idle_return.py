"""
Script CHOP - Idle Return Implementation

This script is designed to be used in a Script CHOP in TouchDesigner.
It monitors input values and smoothly returns them to a target value
when no activity is detected.

USAGE:
1. Create a Script CHOP in TouchDesigner
2. Connect your Math CHOP (or any CHOP) as input to the Script CHOP
3. In the Script CHOP's 'Script' parameter, reference this DAT
4. Set the parameters in the Script CHOP's parameter page
5. Use the output of the Script CHOP for your visualizations/controls

The Script CHOP will pass through input values when active,
and smoothly transition to the target value when inactive.
"""

# Store persistent state
if not hasattr(me, 'idleState'):
    me.idleState = {
        'inactive_frames': 0,
        'last_values': None,
        'target_value': 0.0,
        'return_speed': 0.05,
        'inactivity_delay': 60,
        'activity_threshold': 0.001
    }


def onSetupParameters(scriptOp):
    """
    Called when setting up custom parameters for the Script CHOP
    """
    page = scriptOp.appendCustomPage('Idle Return')
    
    p = page.appendFloat('Targetvalue', label='Target Value')
    p[0].default = 0.0
    p[0].normMin = -1.0
    p[0].normMax = 1.0
    
    p = page.appendFloat('Returnspeed', label='Return Speed')
    p[0].default = 0.05
    p[0].normMin = 0.001
    p[0].normMax = 0.5
    p[0].clampMin = True
    p[0].clampMax = True
    
    p = page.appendInt('Inactivitydelay', label='Inactivity Delay (frames)')
    p[0].default = 60
    p[0].normMin = 0
    p[0].normMax = 300
    
    p = page.appendFloat('Activitythreshold', label='Activity Threshold')
    p[0].default = 0.001
    p[0].normMin = 0.0001
    p[0].normMax = 0.1


def onCook(scriptOp):
    """
    Called every frame to process the CHOP data
    """
    state = me.idleState
    
    # Get parameters
    target_value = scriptOp.par.Targetvalue.eval()
    return_speed = scriptOp.par.Returnspeed.eval()
    inactivity_delay = int(scriptOp.par.Inactivitydelay.eval())
    activity_threshold = scriptOp.par.Activitythreshold.eval()
    
    # Update state with current parameters
    state['target_value'] = target_value
    state['return_speed'] = return_speed
    state['inactivity_delay'] = inactivity_delay
    state['activity_threshold'] = activity_threshold
    
    # Get input
    if scriptOp.numInputs > 0:
        input_chop = scriptOp.inputs[0]
        
        # Copy input structure to output
        scriptOp.copy(input_chop)
        
        # Check for activity
        activity_detected = False
        current_values = []
        
        # Sample all channels to detect activity
        for chan_idx in range(scriptOp.numChans):
            if scriptOp.numSamples > 0:
                current_val = scriptOp[chan_idx][0]
                current_values.append(current_val)
                
                # Compare with last frame
                if state['last_values'] is not None and chan_idx < len(state['last_values']):
                    delta = abs(current_val - state['last_values'][chan_idx])
                    if delta > activity_threshold:
                        activity_detected = True
        
        # Update activity state
        if activity_detected:
            state['inactive_frames'] = 0
        else:
            state['inactive_frames'] += 1
        
        # Apply idle return if inactive for long enough
        if state['inactive_frames'] >= inactivity_delay:
            # Smoothly interpolate all channels towards target
            for chan_idx in range(scriptOp.numChans):
                for sample_idx in range(scriptOp.numSamples):
                    current_val = scriptOp[chan_idx][sample_idx]
                    
                    # Linear interpolation towards target
                    new_val = current_val + (target_value - current_val) * return_speed
                    
                    # Update the sample
                    scriptOp[chan_idx][sample_idx] = new_val
        
        # Store current values for next frame
        state['last_values'] = current_values
    else:
        # No input, create a single channel at target value
        scriptOp.numChans = 1
        scriptOp.numSamples = 1
        scriptOp[0][0] = target_value


def onPulse(par):
    """
    Called when custom pulse parameters are triggered
    """
    pass
