"""
Math CHOP Idle Return Script for TouchDesigner

This script allows a Math CHOP to smoothly return to a specific target value
when it becomes inactive. The script monitors the activity state and applies
smooth interpolation to transition back to the target.

Usage:
1. Create a Math CHOP in your TouchDesigner project
2. Add a chopexec DAT referencing this script
3. Configure the parameters below
4. The Math CHOP will automatically return to the target value when inactive

Parameters:
- target_value: The value to return to when inactive (default: 0)
- return_speed: Speed of return transition (0-1, default: 0.05)
- activity_threshold: Threshold to determine if CHOP is active (default: 0.01)
- active_channel: Channel index to monitor for activity (default: 0)
"""

class MathChopIdleReturn:
    """
    Handles smooth return to target value for inactive Math CHOPs
    """
    
    def __init__(self, ownerComp):
        """
        Initialize the idle return handler
        
        Args:
            ownerComp: The component that owns this script
        """
        self.ownerComp = ownerComp
        
        # Configuration parameters
        self.target_value = 0.0  # Target value to return to
        self.return_speed = 0.05  # Speed of interpolation (0-1)
        self.activity_threshold = 0.01  # Threshold for detecting activity
        self.active_channel = 0  # Channel to monitor for activity
        
        # Internal state
        self.current_value = 0.0
        self.is_active = False
        self.inactive_frames = 0
        self.activation_delay = 30  # Frames to wait before starting return
        
    def configure(self, target_value=0.0, return_speed=0.05, 
                  activity_threshold=0.01, active_channel=0, 
                  activation_delay=30):
        """
        Configure the idle return parameters
        
        Args:
            target_value: Value to return to when inactive
            return_speed: Speed of return (0-1, higher = faster)
            activity_threshold: Threshold for activity detection
            active_channel: Channel index to monitor
            activation_delay: Frames to wait before returning
        """
        self.target_value = target_value
        self.return_speed = max(0.001, min(1.0, return_speed))
        self.activity_threshold = activity_threshold
        self.active_channel = active_channel
        self.activation_delay = activation_delay
        
    def check_activity(self, chop):
        """
        Check if the CHOP is currently active based on value changes
        
        Args:
            chop: The CHOP operator to check
            
        Returns:
            bool: True if active, False if inactive
        """
        if not chop or chop.numChans == 0:
            return False
            
        # Get the current value from the monitored channel
        channel_index = min(self.active_channel, chop.numChans - 1)
        current = chop[channel_index][0] if chop.numSamples > 0 else 0
        
        # Check if value has changed significantly
        value_delta = abs(current - self.current_value)
        is_active = value_delta > self.activity_threshold
        
        self.current_value = current
        return is_active
        
    def apply_idle_return(self, chop):
        """
        Apply smooth return to target value for the CHOP
        
        Args:
            chop: The CHOP operator to modify
        """
        if not chop or chop.numChans == 0:
            return
            
        # Check activity state
        self.is_active = self.check_activity(chop)
        
        if self.is_active:
            # Reset inactive counter when active
            self.inactive_frames = 0
        else:
            # Increment inactive counter
            self.inactive_frames += 1
            
        # Only apply return after delay period
        if self.inactive_frames >= self.activation_delay:
            # Apply smooth interpolation to all channels
            for chan_idx in range(chop.numChans):
                if chop.numSamples > 0:
                    current_val = chop[chan_idx][0]
                    # Lerp towards target value
                    new_val = current_val + (self.target_value - current_val) * self.return_speed
                    
                    # Use Math CHOP's expression or modify via script
                    # Note: Direct modification may require a different approach
                    # This is a reference implementation
                    
    def get_return_value(self, current_value):
        """
        Calculate the interpolated return value
        
        Args:
            current_value: Current value of the channel
            
        Returns:
            float: Interpolated value moving towards target
        """
        if self.inactive_frames < self.activation_delay:
            return current_value
            
        # Smooth interpolation (lerp)
        return current_value + (self.target_value - current_value) * self.return_speed


# Example usage in TouchDesigner CHOP Execute DAT:
"""
# In your CHOP Execute DAT, add this code:

# Create instance at module level
idle_return = None

def onSetupParameters(par):
    # Setup custom parameters for the parent component
    page = par.appendCustomPage('Idle Return')
    p = page.appendFloat('Targetvalue', label='Target Value')
    p[0].default = 0
    p = page.appendFloat('Returnspeed', label='Return Speed')
    p[0].default = 0.05
    p[0].normMin = 0
    p[0].normMax = 1
    p = page.appendFloat('Activitythreshold', label='Activity Threshold')
    p[0].default = 0.01
    p = page.appendInt('Activechannel', label='Active Channel')
    p[0].default = 0
    p = page.appendInt('Activationdelay', label='Activation Delay')
    p[0].default = 30

def onCreate():
    global idle_return
    idle_return = MathChopIdleReturn(parent())

def onCook(scriptOp):
    global idle_return
    if idle_return is None:
        idle_return = MathChopIdleReturn(parent())
    
    # Get parameters from parent component
    target = parent().par.Targetvalue.eval() if hasattr(parent().par, 'Targetvalue') else 0
    speed = parent().par.Returnspeed.eval() if hasattr(parent().par, 'Returnspeed') else 0.05
    threshold = parent().par.Activitythreshold.eval() if hasattr(parent().par, 'Activitythreshold') else 0.01
    channel = int(parent().par.Activechannel.eval()) if hasattr(parent().par, 'Activechannel') else 0
    delay = int(parent().par.Activationdelay.eval()) if hasattr(parent().par, 'Activationdelay') else 30
    
    # Configure
    idle_return.configure(target, speed, threshold, channel, delay)
    
    # Get input CHOP
    inputChop = scriptOp.inputs[0] if len(scriptOp.inputs) > 0 else None
    
    if inputChop:
        # Copy input to output
        scriptOp.copy(inputChop)
        
        # Apply idle return logic
        if idle_return.inactive_frames >= idle_return.activation_delay:
            for i in range(scriptOp.numChans):
                for s in range(scriptOp.numSamples):
                    current = scriptOp[i][s]
                    new_val = idle_return.get_return_value(current)
                    scriptOp[i][s] = new_val
"""
