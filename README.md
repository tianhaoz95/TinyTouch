# TinyTouch 🧸 (ToddlerPlay for watchOS)

A child-development play experience and accidental-touch shield designed specifically for parents holding an 18-month-old toddler with an Apple Watch.

---

## 🌟 The Core Problem & The Dual Solution

When holding a one-and-a-half-year-old toddler, their hands naturally reach for whatever is glowing on your wrist. On standard watchOS:
- Random taps hit watch face complications that dial recent phone numbers or emergency SOS.
- Swiping down pulls Notification Center; swiping up / side button opens Control Center.
- Turning the Digital Crown scrolls away into Smart Stack.
- Short screen timeouts turn the display black within seconds, triggering toddler frustration.

**TinyTouch provides a dual solution:**
1. **Accidental-Touch Shield ("Toddler Lock")**: Captures 100% of edge-to-edge screen interactions. Disables system navigation bars, dismiss gestures, and complication triggers. Tames the Digital Crown so turning it acts as an interactive musical toy rather than scrolling out of the app. Returning to settings requires a continuous **3-second hold** on a discreet Parent Shield with animated countdown and haptic feedback—something an 18-month-old cannot do.
2. **Developmentally Grounded Play (18-Month Focus)**: Designed according to pediatric developmental principles (AAP low-stimulation recommendations). No fast flashing, no predatory reward loops, no losing states. Delivers immediate cause-and-effect auditory chimes (pentatonic scale), gentle tactile haptics, friendly animal speech recognition, and a calm bedtime lullaby transition when the session ends.

---

## 🎮 The 5 Toddler Play Modes

### 1. 🫧 Bubble Pop (Motor Coordination & Cause-and-Effect)
- Gentle floating translucent bubbles with glowing rims and cute shapes (Stars, Hearts, Circles).
- Tapping any bubble bursts it with an authentic bubble pop sound, expanding particle rings, and tactile pops.
- Tapping empty space spawns a brand new bubble right under their finger.
- Turning the **Digital Crown** inflates a giant centerpiece bubble until it pops into rainbow confetti!

### 2. 🐶 Animal Friends & Peekaboo (Speech & Language Discovery)
- High-contrast, expressive animal characters (Puppy, Kitty, Duck, Cow, Frog, Bunny).
- Tapping an animal makes them do a springy squish/bounce animation with floating hearts.
- Plays characteristic animal sounds (Woof, Meow, Quack, Moo, Ribbit).
- Spoken voice cues ("Duck! Quack quack!") support early speech mimicry and word association.
- Digital Crown spins the animal carousel with mechanical click haptics.

### 3. 🎹 Sound Garden / Xylophone (Harmonic Sensory & Rhythm)
- 6 colorful vertical chime bars (Do, Re, Mi, Sol, La, Do).
- Uses the **Pentatonic Scale (C, D, E, G, A, C5)**: mathematically consonant and impossible to create harsh or discordant notes—every random tap sounds like a harmonious melody.
- Tapping or sliding fingers lights up bars with vertical ripples and plays glockenspiel chimes.
- Turning the Digital Crown performs a sweeping musical glissando.

### 4. ✨ Magic Sparkles (Free Motor & Sensory Exploration)
- Pure open OLED-black canvas.
- Drags leave glowing rainbow stardust and sparkling chime cascades.
- Accommodates whole-palm slaps and multi-finger explorations without errors or menus.
- Crown rotation creates a spinning kaleidoscope galaxy in the center.

### 5. 🌙 Sleepy Moon Lullaby (Calm Transition & Bedtime Wind-Down)
- Deep midnight sky with soft twinkling stars and a gentle smiling crescent moon.
- Plays a soothing music box melody (*Twinkle Twinkle* motif).
- Tapping the moon gently brightens its blushing cheeks with a soft pulse.
- **Tear-Free Transitions**: Automatically activates when the Parent Play Timer expires, signaling to the toddler that it is "time to rest" rather than an abrupt screen cutoff.

---

## 🛡️ Parental Controls & Safety Features

- **Parent Shield (3-Second Hold Gate)**:
  Positioned in the top-left corner. Holding for 3 continuous seconds fills a progress ring with rhythmic haptic ticks. If released early, it resets immediately.
- **Session Play Timer**:
  Configure 3 min, 5 min, 10 min, or unlimited play. When the timer ends, the app gently transitions to the Sleepy Lullaby mode.
- **Sensory Toggles**:
  Toggle Sound Effects, Spoken Words, Taptic Engine pulses, and Low-Stimulation mode (slows movement speeds and mutes contrast).
- **Co-Play Prompts**:
  Displays rotating caregiver prompts (e.g., *"What sound does the duck make? Quack quack!"*) to foster parent-child interaction while holding the toddler.
- **Water Lock & Guided Access Integration**:
  Built-in guide explaining how parents can activate watchOS Water Lock (swipe Control Center -> Water Droplet) if they want 100% hardware touch lockdown while the child watches the screen.

---

## 🛠️ Project Architecture

```
ToddlerPlay/
├── Sources/
│   ├── ToddlerPlayApp.swift            # App entry point & scene lifecycle
│   ├── Models/
│   │   └── GameMode.swift              # Game mode definitions & metadata
│   ├── Services/
│   │   ├── SoundManager.swift          # Low-latency AVAudioPlayer pool & AVSpeechSynthesizer
│   │   ├── HapticsManager.swift        # Taptic Engine semantic patterns
│   │   └── SessionKeeper.swift         # WKExtendedRuntimeSession screen wake manager
│   ├── ViewModels/
│   │   └── AppState.swift              # Observable central state & session timer
│   └── Views/
│       ├── MainContainerView.swift     # Full-screen container, shield, and co-play banner
│       ├── Components/
│       │   └── ShapeViews.swift        # Custom vector shapes (Star, Heart, Moon, Bubble)
│       ├── ParentLock/
│       │   ├── ParentShieldButton.swift# 3-second hold circular progress lock
│       │   ├── ParentDashboardView.swift# Activity picker, timers, and sensory options
│       │   └── ParentGuideView.swift   # Safety guide and Water Lock instructions
│       └── Games/
│           ├── BubblePopView.swift     # Bubble pop game
│           ├── AnimalFriendsView.swift # Animals, bounces, sounds, and speech
│           ├── SoundGardenView.swift   # Pentatonic xylophone & glissando
│           ├── SparkleCanvasView.swift # Rainbow touch sparkles & crown vortex
│           └── SleepyMoonView.swift    # Soothing lullaby wind-down
├── Resources/
│   ├── Assets.xcassets/                # 1024x1024 AppIcon and AccentColor
│   └── Sounds/                         # 16 synthesized 16-bit 44.1kHz PCM WAV assets
├── tools/
│   ├── generate_project.py             # Generates standalone watchOS .xcodeproj
│   ├── generate_sounds.py              # Mathematical sound synthesis script
│   ├── capture_screens.py              # Automated screenshot test harness
│   └── run_tests.swift                 # Unit test suite (51/51 passing)
└── screenshots/                        # High-resolution Apple Watch UI screenshots
```

---

## 🚀 Building & Running

### Requirements
- macOS with Xcode 15+ (tested on Xcode 26.6 / watchOS 26.5 SDK)
- Apple Watch running watchOS 10.0 or later

### From the Command Line
```bash
# Build the watchOS app
xcodebuild -scheme ToddlerPlay -destination 'platform=watchOS Simulator,name=Apple Watch Ultra 3 (49mm)' clean build

# Run unit tests
swift tools/run_tests.swift

# Install and launch on booted simulator
xcrun simctl install booted /Users/tianhaoz/Library/Developer/Xcode/DerivedData/ToddlerPlay-*/Build/Products/Debug-watchsimulator/ToddlerPlay.app
xcrun simctl launch booted com.tianhaoz.tinytouch
```

### In Xcode
1. Open `ToddlerPlay.xcodeproj` in Xcode.
2. Select the `ToddlerPlay` scheme and your target Apple Watch or Simulator.
3. Press `Cmd + R` to run!
