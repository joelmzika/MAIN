# Visual Architecture Guide

## How It Works - Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT STAGE: Your Math CHOP or any CHOP                    │
│  - Mouse movements, audio, OSC, sensors, etc.               │
│  - Values change based on your input                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  MONITORING STAGE: Script CHOP with Idle Return             │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 1. Check Activity:                                  │    │
│  │    - Compare current values with last frame        │    │
│  │    - If change > threshold → ACTIVE                │    │
│  │    - If change < threshold → increment counter     │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 2. Decision:                                        │    │
│  │    IF inactive_frames < DELAY:                     │    │
│  │       → Pass through input values unchanged        │    │
│  │    ELSE:                                            │    │
│  │       → Apply interpolation to target              │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 3. Interpolation (when returning):                 │    │
│  │    new_val = current + (target - current) * speed  │    │
│  │    - Creates smooth exponential curve              │    │
│  │    - Starts fast, slows down near target           │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT STAGE: Clean values for your visualization          │
│  - Smooth, controlled values                                │
│  - No sudden jumps                                           │
│  - Returns to baseline when idle                            │
└─────────────────────────────────────────────────────────────┘
```

## State Machine Diagram

```
                    ┌──────────────┐
                    │   ACTIVE     │
                    │ (Passing     │
         ┌─────────>│  through     │<─────────┐
         │          │  input)      │          │
         │          └──────┬───────┘          │
         │                 │                  │
         │                 │ No activity      │
    Activity               │ detected         │ Activity
    detected               │                  │ detected
         │                 ▼                  │
         │          ┌──────────────┐          │
         │          │   WAITING    │          │
         │          │ (Counter     │          │
         └──────────│  < delay)    │          │
                    └──────┬───────┘          │
                           │                  │
                           │ Counter          │
                           │ >= delay         │
                           ▼                  │
                    ┌──────────────┐          │
                    │  RETURNING   │          │
                    │ (Interpolate │──────────┘
                    │  to target)  │
                    └──────────────┘
```

## Value Behavior Over Time

```
Value
  │
1.0│     ╱╲                                    User stops
   │    ╱  ╲                                   interacting
   │   ╱    ╲    ╱╲                                ↓
   │  ╱      ╲  ╱  ╲                           ┌──────┐
0.5│ ╱        ╲╱    ╲    ╱╲                    │      │
   │╱                 ╲  ╱  ╲                  │Wait  │
   │                   ╲╱    ╲                 │delay │
0.0├─────────────────────────╲────────────────┴──────┴────────→
   │                          ╲                       ╲
   │                           ╲                       ╲  Smooth
   │                            ╲                       ╲ interpolation
   │                             ╲                       ╲ to target
   │                              ╲                       ╲
-1.0│                               ━━━━━━━━━━━━━━━━━━━━━━→ Target (0.0)
   └────────────────────────────────────────────────────────> Time
   
   └─ Active ─┘  └─ Active ─┘  └──── Inactive ────┘  └─ Returning ─┘
```

## Parameter Effects Visualization

### Return Speed Effect
```
speed = 0.01 (slow)    speed = 0.05 (medium)   speed = 0.2 (fast)
      
Value     Value     Value
  │         │         │
  │╲        │╲        │╲___
  │ ╲       │ ╲       │
  │  ╲      │  ╲      │
  │   ╲     │   ╲__   │
  │    ╲    │         │
  │     ╲_  │         │
  └─────────└─────────└──────> Time
  
  Gradual    Normal     Quick
```

### Activity Threshold Effect
```
threshold = 0.0001     threshold = 0.001      threshold = 0.01
(very sensitive)       (normal)               (less sensitive)

Detects tiny changes   Balanced detection     Ignores small changes
Good for precise       Good for most cases    Good for noisy inputs
control                                       or deliberate motion
```

### Inactivity Delay Effect
```
delay = 30 frames      delay = 60 frames      delay = 180 frames
(1 sec @ 30fps)        (2 sec @ 30fps)        (6 sec @ 30fps)

Activity stops ↓       Activity stops ↓       Activity stops ↓
    │                      │                      │
    └─ Quick return        └─── Delayed return   └──────────── Long delay
```

## Network Topology Examples

### Single Channel Control
```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Mouse   │───>│  Script  │───>│  Null    │
│  CHOP    │    │  CHOP    │    │  CHOP    │
└──────────┘    └──────────┘    └──────────┘
                 (idle return)
```

### Multi-Channel Processing
```
                 ┌──────────┐
                 │ Select   │───┐
                 │ (chan 0) │   │
┌──────────┐    ├──────────┤   │    ┌──────────┐
│ Multi-   │───>│ Select   │───┼───>│ Merge    │
│ channel  │    │ (chan 1) │   │    │ CHOP     │
│  Input   │    ├──────────┤   │    └──────────┘
└──────────┘    │ Select   │───┘
                 │ (chan 2) │
                 └──────────┘
                 Each with own
                 idle return
                 settings
```

### Audio-Reactive with Idle
```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Audio   │───>│  Filter  │───>│  Script  │───>│ Visuals  │
│  In      │    │  CHOP    │    │  CHOP    │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                 (returns to
                                  baseline when
                                  quiet)
```

### Feedback Loop with Control
```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Script  │───>│  Math    │───>│  Null    │
│  CHOP    │<───│  CHOP    │    │  CHOP    │
└──────────┘    └──────────┘    └──────────┘
 (idle return    (feedback
  provides        calculations)
  stability)
```

## Implementation Comparison

```
┌─────────────────┬─────────────┬──────────────┬─────────────┐
│                 │ Script CHOP │ CHOP Execute │ Python Class│
├─────────────────┼─────────────┼──────────────┼─────────────┤
│ Ease of Use     │   ★★★★★     │    ★★★☆☆    │   ★★☆☆☆     │
│ Flexibility     │   ★★★★☆     │    ★★★★☆    │   ★★★★★     │
│ Performance     │   ★★★★☆     │    ★★★★★    │   ★★★☆☆     │
│ Real-time Mods  │   ★★★★★     │    ★★☆☆☆    │   ★★★★☆     │
│ Recommended For │   Everyone  │  Monitoring  │  Advanced   │
└─────────────────┴─────────────┴──────────────┴─────────────┘
```

## Quick Reference - When to Use What

```
Your Situation                        → Recommended Solution
─────────────────────────────────────────────────────────────
Need it to work quickly               → Script CHOP
Want visual parameter control         → Script CHOP
Need to process values                → Script CHOP
Just need activity monitoring         → CHOP Execute
Building custom Python tools          → Python Class
Need maximum flexibility              → Python Class
Working with complex logic            → Python Class
```

## Troubleshooting Flow

```
Problem: Values not returning?
    │
    ├─> Check: Input connected? ──No──> Connect input CHOP
    │                  │
    │                 Yes
    │                  │
    ├─> Check: Activity threshold too high? ──Yes──> Lower it (try 0.0001)
    │                  │
    │                 No
    │                  │
    └─> Check: Delay too long? ──Yes──> Reduce delay (try 30)
                       │
                      No
                       │
                   Working! ──> Fine-tune parameters
```
