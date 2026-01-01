# 🚴 BMX Terminal - Freestyle Command Scripting

A revolutionary terminal interface that combines BMX freestyle tricks with command execution. Perform tricks to execute commands, chain combos for bonuses, and compete with Mario characters on bikes!

## 🎯 Features

### Trick-Based Commands
Execute any command by prefixing it with a BMX trick:
```bash
wheelie git push           # Simple execution (1x multiplier)
bunnyhop cd ~/projects     # Jump to directories (1.2x)
tailwhip ls -la            # Spin through files (1.5x)
backflip npm install       # Complex operations (2.0x)
grind python script.py     # Process data (1.8x)
```

### Combo System
Chain tricks together for massive multipliers:
- **Super Jump**: wheelie + bunnyhop → 1.5x
- **Ultra Fast Compile**: tailwhip + backflip → 2.0x
- **Quantum Optimization**: grind + manual + bunnyhop → 2.5x
- **Mushroom Code Compression**: 360 + tailwhip + barspin → 3.0x

### Special Token Formula Combos
Unlock legendary combos:
- **👑📶⚪ Crown Orchestrator Flip**: backflip + 360 + flair (3.5x, 100 tokens)
- **🗄️🧵📶 Memory Thread Grind**: grind + manual + tailwhip (3.2x, 80 tokens)
- **🪡🤓⭐ Smart Weaver Spin**: tailwhip + barspin + 360 (3.8x, 120 tokens)

### 11 Themes
Each theme transforms the BMX terminal experience:

1. **🍄 Mushroom Kingdom** - Mario's world with pipes and mushrooms
2. **🔌 Circuit Board** - Electronic components and circuit traces
3. **🧪 Laboratory** - Scientific equipment and chemical reactions
4. **🤖 Robot Assembly** - Futuristic robot factory
5. **🏗️ Building Site** - Construction zone with cranes
6. **🚀 Space Station** - Zero-gravity cosmic tricks
7. **🌳 Forest Trail** - Natural terrain and obstacles
8. **💻 Cyberspace** - Digital realm with data streams
9. **🌊 Underwater** - Aquatic BMX adventure
10. **👾 8-bit Arcade** - Retro pixel-perfect world
11. **✨ Neon City** - Futuristic neon cityscape

### Capacitor Physics Engine
- Pedal to charge your capacitor
- Each trick consumes energy
- Higher difficulty = more energy needed
- Realistic physics calculations for trick height, velocity, and forces

### MRW Terminal Characters
Compete with Mario Racing World characters:
- **🍄🚴 Mario** - BMX bike specialist (1.2x trick bonus)
- **👻🛹 Luigi** - Skateboard expert (1.3x trick bonus)
- **👑🚴 Peach** - Royal tricks (1.5x trick bonus)
- **🍄🛹 Toad** - Speed demon (1.1x trick bonus)
- **🦖🚴 Yoshi** - Egg throw special (1.4x trick bonus)
- **🐲🚙 Bowser** - Monster power (2.0x trick bonus)

### Scoring & Achievements
- Points based on trick difficulty
- Combo multipliers
- 15+ achievements to unlock
- Global leaderboard integration

## 🚀 Quick Start

### Web Interface
Open `terminals/bmx-terminal.html` in your browser for the full interactive experience.

### Command Line Usage
```javascript
// Initialize system
const physics = new BMXPhysicsEngine();
const combos = new ComboSystem();
const terminal = new BMXTerminal();
await terminal.init(physics, combos);

// Execute tricks
terminal.executeTrick('wheelie', 'git status');
terminal.executeTrick('backflip', 'npm test');

// Switch themes
terminal.switchTheme('electronics');

// Charge energy
physics.pedalCharge(5);
```

## 📋 File Structure

```
mongoose.os/
├── bmx-terminal.js           # Main BMX terminal class
├── tricks/
│   ├── basic-tricks.js       # Individual trick definitions
│   ├── combo-system.js       # Combo detection and rewards
│   └── physics-engine.js     # Capacitor and physics calculations
├── themes/
│   └── bmx-themes.js         # All 11 theme configurations
├── scoring/
│   └── trick-rewards.js      # Points, achievements, leaderboard
└── terminals/
    ├── bmx-terminal.html     # Web interface
    └── mrw-terminal.js       # Mario Racing World characters
```

## 🎮 Commands

### Basic Tricks
```bash
wheelie <command>      # 1x multiplier, 10 energy
manual <command>       # 1.3x multiplier, 15 energy
bunnyhop <command>     # 1.2x multiplier, 20 energy
tailwhip <command>     # 1.5x multiplier, 30 energy
grind <command>        # 1.8x multiplier, 25 energy
barspin <command>      # 1.6x multiplier, 28 energy
backflip <command>     # 2.0x multiplier, 40 energy
360 <command>          # 2.2x multiplier, 35 energy
```

### BMX Commands
```bash
bmx help               # Show help
bmx status             # Show current stats
bmx theme <name>       # Switch theme
bmx pedal [power]      # Charge capacitor
```

### MRW Commands
```javascript
// Select character
mrw.selectCharacter('mario');

// Start race
mrw.startRace(3);

// Use special move
mrw.useSpecialMove();

// Joystick controls
mrw.handleJoystick('up');     // Accelerate
mrw.handleJoystick('button1'); // Trick
```

## 🏆 Achievements

### Beginner
- **First Trick** - Perform your first BMX trick (50 pts)
- **Pedal Master** - Fully charge capacitor 10 times (100 pts)

### Tricks
- **Wheelie Warrior** - 50 wheelies (150 pts)
- **Flip Master** - 20 backflips (300 pts)
- **Grind King** - 30 grinds (250 pts)

### Combos
- **Combo Novice** - First combo (200 pts)
- **Combo Master** - 10 different combos (500 pts)
- **Token Formula** - Unlock special combo (1000 pts)

### Score
- **Point Collector** - 10,000 points (300 pts)
- **Score Legend** - 50,000 points (1000 pts)

### Advanced
- **Perfect Run** - 20 tricks without failing (800 pts)
- **Energy Efficient** - 10 tricks with minimal energy (500 pts)
- **Speed Demon** - 5 tricks in under 10 seconds (600 pts)

## 🎨 Theme Customization

Each theme includes:
- Custom color palette
- Theme-specific obstacles
- Unique ramps and platforms
- Character skins
- Sound effects
- Background patterns
- Music themes

## ⚡ Physics Simulation

The physics engine calculates:
- Capacitor charge/discharge
- Trick height based on energy
- Velocity and acceleration
- G-forces during tricks
- Rotational energy for spins
- Air resistance and friction
- Momentum calculations

## 🔧 Advanced Usage

### Custom Combos
```javascript
combos.combos['my_combo'] = {
  name: 'My Custom Combo',
  tricks: ['wheelie', 'manual', 'grind'],
  multiplier: 2.5,
  description: 'Custom combination',
  emoji: '🎯'
};
```

### Custom Themes
```javascript
terminal.themes['my_theme'] = {
  name: '🎯 My Theme',
  colors: { primary: '#ff0000', secondary: '#00ff00', accent: '#0000ff' },
  obstacles: ['obstacle1', 'obstacle2'],
  ramps: ['ramp1', 'ramp2'],
  bgPattern: 'custom_pattern'
};
```

### Energy Management
```javascript
// Check energy
const hasEnergy = physics.hasEnergy(30);

// Get status
const status = physics.getStatus();

// Simulate trick physics
const simulation = physics.simulateTrickPhysics('backflip', 40);
```

## 🎯 Tips & Tricks

1. **Charge Smart**: Keep your capacitor above 50% for big combos
2. **Theme Bonuses**: Some themes give bonus multipliers
3. **Combo Chains**: Plan your trick sequence for maximum points
4. **Energy Conservation**: Lower tricks for simple commands
5. **Special Moves**: Use character specials at the right time
6. **Practice Mode**: Try combos in Mario theme first

## 🔒 Safety

- Commands are simulated by default for safety
- Enable real execution with caution
- Always validate commands before execution
- Energy limits prevent accidental spam

## 📊 Statistics Tracking

```javascript
// Get session stats
const stats = rewards.getSessionStats();

// View leaderboard
const top10 = rewards.getLeaderboard(10);

// Check achievements
const achievements = rewards.getAllAchievements();

// Combo history
const history = combos.getStats();
```

## 🌟 Contributing

This is an additive-only system. All features are designed to:
- ✅ Add new functionality without breaking existing code
- ✅ Support all 11 themes equally
- ✅ Integrate with existing terminal infrastructure
- ✅ Maintain backward compatibility

## 📝 License

Part of the Mongoose.OS ecosystem - Freestyle your way to productivity!

---

**Made with ❤️ for developers who want to make commands fun again!**

🚴 **Keep riding, keep coding!** 🚴
