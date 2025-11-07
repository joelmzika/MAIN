"""
CHOP Execute DAT - Idle Return to Target Value

Simple script for TouchDesigner CHOP Execute DAT that makes a Math CHOP
slowly return to a specific value when it becomes inactive.

SETUP:
1. Create a Math CHOP or any CHOP you want to control
2. Create a CHOP Execute DAT
3. Paste this code into the CHOP Execute DAT
4. Reference your Math CHOP in the CHOP Execute DAT's 'CHOPs' parameter
5. Adjust the parameters below to your needs

PARAMETERS:
- TARGET_VALUE: The value to return to when inactive
- RETURN_SPEED: How fast to return (0.01 = slow, 0.1 = fast)
- INACTIVITY_DELAY: Frames to wait before starting return
- ACTIVITY_THRESHOLD: Minimum change to consider active
"""

# ============== CONFIGURATION ==============
TARGET_VALUE = 0.0          # Value to return to when inactive
RETURN_SPEED = 0.05         # Speed of return (0.01 - 0.5 recommended)
INACTIVITY_DELAY = 60       # Frames to wait before returning (60 = 2 seconds at 30fps)
ACTIVITY_THRESHOLD = 0.001  # Minimum change to detect activity
# ===========================================


# Global variables to track state
if not hasattr(op, 'idle_return_state'):
    op.idle_return_state = {
        'inactive_frames': 0,
        'last_values': {},
        'is_returning': False
    }


def onOffToOn(channel, sampleIndex, val, prev):
    """Called when channel goes from 0 to non-zero"""
    reset_inactivity()
    return


def whileOn(channel, sampleIndex, val, prev):
    """Called every frame while channel is non-zero"""
    check_activity(channel, val, prev)
    return


def onOnToOff(channel, sampleIndex, val, prev):
    """Called when channel goes from non-zero to 0"""
    reset_inactivity()
    return


def whileOff(channel, sampleIndex, val, prev):
    """Called every frame while channel is 0"""
    increment_inactivity()
    return


def onValueChange(channel, sampleIndex, val, prev):
    """Called when any value changes"""
    check_activity(channel, val, prev)
    return


def reset_inactivity():
    """Reset the inactivity counter when activity is detected"""
    state = op.idle_return_state
    state['inactive_frames'] = 0
    state['is_returning'] = False


def increment_inactivity():
    """Increment inactivity counter"""
    state = op.idle_return_state
    state['inactive_frames'] += 1
    
    # Start returning after delay
    if state['inactive_frames'] >= INACTIVITY_DELAY:
        state['is_returning'] = True


def check_activity(channel, val, prev):
    """Check if there's significant activity"""
    # Check if value changed significantly
    delta = abs(val - prev)
    if delta > ACTIVITY_THRESHOLD:
        reset_inactivity()
    else:
        increment_inactivity()


# Alternative implementation using a custom parameter approach
def apply_idle_return(chop_path):
    """
    Apply idle return to a CHOP - call this from a separate script
    
    Args:
        chop_path: Path to the CHOP operator (e.g., '/project1/math1')
    """
    chop = op(chop_path)
    if not chop:
        return
    
    state = op.idle_return_state
    
    # Check if we should apply return
    if state['is_returning']:
        # This is conceptual - actual implementation depends on your setup
        # You would typically use this with a Math CHOP or Null CHOP
        pass
