/**
 * BMX Terminal - Freestyle BMX-style terminal scripting system
 * Execute commands with bike tricks and combos
 */

class BMXTerminal {
  constructor() {
    this.currentTheme = 'mario';
    this.trickHistory = [];
    this.comboChain = [];
    this.score = 0;
    this.achievements = [];
    this.physicsEngine = null;
    this.comboSystem = null;
    
    // Basic tricks mapping
    this.tricks = {
      wheelie: { difficulty: 1, energyCost: 10, multiplier: 1.0 },
      bunnyhop: { difficulty: 2, energyCost: 20, multiplier: 1.2 },
      tailwhip: { difficulty: 3, energyCost: 30, multiplier: 1.5 },
      backflip: { difficulty: 4, energyCost: 40, multiplier: 2.0 },
      grind: { difficulty: 3, energyCost: 25, multiplier: 1.8 },
      manual: { difficulty: 2, energyCost: 15, multiplier: 1.3 },
      '360': { difficulty: 4, energyCost: 35, multiplier: 2.2 },
      barspin: { difficulty: 3, energyCost: 28, multiplier: 1.6 }
    };
    
    // Theme configurations
    this.themes = {
      mario: {
        name: '🍄 Mushroom Kingdom',
        colors: { primary: '#ff0000', secondary: '#00ff00', accent: '#ffff00' },
        obstacles: ['pipe', 'mushroom', 'coin_block', 'goomba'],
        bgPattern: 'brick'
      },
      electronics: {
        name: '🔌 Circuit Board',
        colors: { primary: '#00ff00', secondary: '#0000ff', accent: '#ff00ff' },
        obstacles: ['resistor', 'capacitor', 'transistor', 'circuit_trace'],
        bgPattern: 'pcb'
      },
      chemistry: {
        name: '🧪 Laboratory',
        colors: { primary: '#00ffff', secondary: '#ff00ff', accent: '#ffff00' },
        obstacles: ['beaker', 'flask', 'bunsen_burner', 'test_tube'],
        bgPattern: 'lab_tiles'
      },
      robotics: {
        name: '🤖 Robot Assembly',
        colors: { primary: '#808080', secondary: '#ff6600', accent: '#00ccff' },
        obstacles: ['robot_arm', 'conveyor', 'servo', 'sensor'],
        bgPattern: 'factory_floor'
      },
      construction: {
        name: '🏗️ Building Site',
        colors: { primary: '#ff6600', secondary: '#ffff00', accent: '#000000' },
        obstacles: ['scaffold', 'crane', 'beam', 'barrier'],
        bgPattern: 'concrete'
      },
      space: {
        name: '🚀 Space Station',
        colors: { primary: '#000033', secondary: '#ffffff', accent: '#00ffff' },
        obstacles: ['satellite', 'asteroid', 'space_station', 'star'],
        bgPattern: 'stars'
      },
      nature: {
        name: '🌳 Forest Trail',
        colors: { primary: '#228b22', secondary: '#8b4513', accent: '#ffff00' },
        obstacles: ['tree', 'rock', 'log', 'bush'],
        bgPattern: 'grass'
      },
      cyber: {
        name: '💻 Cyberspace',
        colors: { primary: '#00ff00', secondary: '#000000', accent: '#ff00ff' },
        obstacles: ['firewall', 'data_stream', 'node', 'glitch'],
        bgPattern: 'matrix'
      },
      ocean: {
        name: '🌊 Underwater',
        colors: { primary: '#0066cc', secondary: '#00ccff', accent: '#ffff00' },
        obstacles: ['coral', 'fish', 'bubble', 'treasure'],
        bgPattern: 'waves'
      },
      retro: {
        name: '👾 8-bit Arcade',
        colors: { primary: '#ff00ff', secondary: '#00ffff', accent: '#ffff00' },
        obstacles: ['pixel_block', 'sprite', 'power_up', 'enemy'],
        bgPattern: 'pixels'
      },
      neon: {
        name: '✨ Neon City',
        colors: { primary: '#ff1493', secondary: '#00ffff', accent: '#ffff00' },
        obstacles: ['neon_sign', 'hologram', 'light_beam', 'skyscraper'],
        bgPattern: 'neon_grid'
      }
    };
  }
  
  /**
   * Initialize BMX terminal system
   */
  async init(physicsEngine, comboSystem) {
    this.physicsEngine = physicsEngine;
    this.comboSystem = comboSystem;
    console.log('🚴 BMX Terminal initialized');
    console.log(`Current theme: ${this.themes[this.currentTheme].name}`);
    return true;
  }
  
  /**
   * Execute command with BMX trick wrapper
   */
  async executeTrick(trickName, command) {
    const trick = this.tricks[trickName];
    
    if (!trick) {
      return {
        success: false,
        error: `Unknown trick: ${trickName}. Available: ${Object.keys(this.tricks).join(', ')}`
      };
    }
    
    // Check energy with physics engine
    if (this.physicsEngine) {
      const hasEnergy = this.physicsEngine.hasEnergy(trick.energyCost);
      if (!hasEnergy) {
        return {
          success: false,
          error: `Not enough energy! Need ${trick.energyCost}, pedal to charge capacitor!`
        };
      }
    }
    
    // Add to combo chain
    this.comboChain.push(trickName);
    if (this.comboChain.length > 5) {
      this.comboChain.shift(); // Keep last 5 tricks
    }
    
    // Check for combo bonus
    let comboBonus = 1.0;
    if (this.comboSystem) {
      const combo = this.comboSystem.checkCombo(this.comboChain);
      if (combo) {
        comboBonus = combo.multiplier;
        console.log(`🎮 COMBO: ${combo.name} (${comboBonus}x)`);
      }
    }
    
    // Perform trick animation
    this.performTrickAnimation(trickName, trick);
    
    // Discharge energy
    if (this.physicsEngine) {
      this.physicsEngine.discharge(trick.energyCost);
    }
    
    // Execute the actual command
    const result = await this.executeCommand(command);
    
    // Calculate points
    const points = Math.floor(trick.difficulty * 100 * trick.multiplier * comboBonus);
    this.score += points;
    
    // Record trick
    this.trickHistory.push({
      trick: trickName,
      command: command,
      points: points,
      timestamp: Date.now(),
      theme: this.currentTheme
    });
    
    return {
      success: true,
      trick: trickName,
      command: command,
      points: points,
      totalScore: this.score,
      combo: comboBonus > 1.0,
      result: result
    };
  }
  
  /**
   * Perform trick animation
   */
  performTrickAnimation(trickName, trick) {
    const theme = this.themes[this.currentTheme];
    console.log(`🚴 ${trickName.toUpperCase()}! [${theme.name}]`);
    
    // Animation based on difficulty
    const stars = '⭐'.repeat(trick.difficulty);
    const energy = '⚡'.repeat(Math.ceil(trick.energyCost / 10));
    
    console.log(`  ${stars} Difficulty: ${trick.difficulty}`);
    console.log(`  ${energy} Energy: ${trick.energyCost}`);
    console.log(`  💯 Multiplier: ${trick.multiplier}x`);
    
    // Theme-specific celebration
    if (trick.difficulty >= 4) {
      console.log(`  🎆 SPECTACULAR ${trickName.toUpperCase()}!`);
    }
  }
  
  /**
   * Execute the actual shell command
   */
  async executeCommand(command) {
    try {
      // In a real implementation, this would execute the shell command
      // For safety, we'll just simulate it
      console.log(`  📟 Executing: ${command}`);
      return {
        stdout: `Command executed: ${command}`,
        stderr: '',
        exitCode: 0
      };
    } catch (error) {
      return {
        stdout: '',
        stderr: error.message,
        exitCode: 1
      };
    }
  }
  
  /**
   * Switch theme
   */
  switchTheme(themeName) {
    if (!this.themes[themeName]) {
      return {
        success: false,
        error: `Unknown theme: ${themeName}. Available: ${Object.keys(this.themes).join(', ')}`
      };
    }
    
    this.currentTheme = themeName;
    const theme = this.themes[themeName];
    
    console.log(`🎨 Theme switched to: ${theme.name}`);
    console.log(`  Colors: ${JSON.stringify(theme.colors)}`);
    console.log(`  Obstacles: ${theme.obstacles.join(', ')}`);
    
    return {
      success: true,
      theme: themeName,
      config: theme
    };
  }
  
  /**
   * Get current status
   */
  getStatus() {
    return {
      theme: this.currentTheme,
      themeConfig: this.themes[this.currentTheme],
      score: this.score,
      tricksPerformed: this.trickHistory.length,
      comboChain: this.comboChain,
      recentTricks: this.trickHistory.slice(-5),
      achievements: this.achievements,
      energy: this.physicsEngine ? this.physicsEngine.getEnergy() : 0
    };
  }
  
  /**
   * Get help text
   */
  getHelp() {
    return `
🚴 BMX Terminal - Freestyle Command Execution

BASIC TRICKS:
  wheelie <command>    - Simple command execution (1x)
  bunnyhop <command>   - Jump to directories (1.2x)
  tailwhip <command>   - Spin through files (1.5x)
  backflip <command>   - Complex operations (2.0x)
  grind <command>      - Process data (1.8x)
  manual <command>     - Balance operations (1.3x)
  360 <command>        - Rotate operations (2.2x)
  barspin <command>    - Handle rotation (1.6x)

COMBOS:
  Chain tricks together for bonus multipliers!
  Example: wheelie + bunnyhop = super_jump_command
  
THEMES (${Object.keys(this.themes).length} available):
  ${Object.entries(this.themes).map(([key, t]) => `${key.padEnd(15)} - ${t.name}`).join('\n  ')}

COMMANDS:
  bmx theme <name>     - Switch theme
  bmx status           - Show current stats
  bmx pedal [power]    - Charge capacitor
  bmx help             - Show this help
  
ENERGY SYSTEM:
  - Pedal to charge capacitor
  - Tricks consume energy
  - Higher tricks = more energy needed
  - Combos = bonus multipliers

Current Score: ${this.score} points
Theme: ${this.themes[this.currentTheme].name}
    `;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BMXTerminal;
}
