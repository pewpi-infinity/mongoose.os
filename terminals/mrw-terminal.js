/**
 * MRW Terminal - Mario Racing World Terminal
 * BMX characters including Mario, Luigi on bikes and skateboards
 */

class MRWTerminal {
  constructor() {
    this.characters = {
      mario: {
        name: 'Mario',
        vehicle: 'BMX',
        emoji: '🍄🚴',
        speed: 8,
        trickBonus: 1.2,
        specialMove: 'Mushroom Boost',
        color: '#ff0000'
      },
      luigi: {
        name: 'Luigi',
        vehicle: 'Skateboard',
        emoji: '👻🛹',
        speed: 7,
        trickBonus: 1.3,
        specialMove: 'Ghost Jump',
        color: '#00ff00'
      },
      peach: {
        name: 'Peach',
        vehicle: 'BMX',
        emoji: '👑🚴',
        speed: 6,
        trickBonus: 1.5,
        specialMove: 'Royal Flip',
        color: '#ff69b4'
      },
      toad: {
        name: 'Toad',
        vehicle: 'Skateboard',
        emoji: '🍄🛹',
        speed: 9,
        trickBonus: 1.1,
        specialMove: 'Spore Dash',
        color: '#ff6600'
      },
      yoshi: {
        name: 'Yoshi',
        vehicle: 'BMX',
        emoji: '🦖🚴',
        speed: 7,
        trickBonus: 1.4,
        specialMove: 'Egg Throw',
        color: '#00ff00'
      },
      bowser: {
        name: 'Bowser',
        vehicle: 'Monster Truck',
        emoji: '🐲🚙',
        speed: 5,
        trickBonus: 2.0,
        specialMove: 'Fire Breath',
        color: '#ff6600'
      }
    };
    
    this.vehicles = {
      car1: { emoji: '🏎️', speed: 10, type: 'competition' },
      car2: { emoji: '🚗', speed: 8, type: 'competition' },
      car3: { emoji: '🚙', speed: 7, type: 'competition' },
      bike: { emoji: '🏍️', speed: 9, type: 'competition' }
    };
    
    this.obstacles = {
      mushroom: { emoji: '🍄', type: 'ramp', boost: 1.5 },
      pipe: { emoji: '🟢', type: 'obstacle', height: 2 },
      coin: { emoji: '🪙', type: 'collectible', points: 10 },
      star: { emoji: '⭐', type: 'powerup', duration: 5000 }
    };
    
    this.currentCharacter = 'mario';
    this.competitors = [];
    this.raceState = {
      inRace: false,
      position: 1,
      lap: 0,
      totalLaps: 3
    };
    
    this.joystickControls = {
      up: 'accelerate',
      down: 'brake',
      left: 'lean_left',
      right: 'lean_right',
      button1: 'trick',
      button2: 'special_move'
    };
  }
  
  /**
   * Select character
   */
  selectCharacter(characterName) {
    if (!this.characters[characterName]) {
      return {
        success: false,
        error: `Character '${characterName}' not found. Available: ${Object.keys(this.characters).join(', ')}`
      };
    }
    
    this.currentCharacter = characterName;
    const character = this.characters[characterName];
    
    console.log(`${character.emoji} ${character.name} selected!`);
    console.log(`  Vehicle: ${character.vehicle}`);
    console.log(`  Speed: ${character.speed}/10`);
    console.log(`  Trick Bonus: ${character.trickBonus}x`);
    console.log(`  Special: ${character.specialMove}`);
    
    return {
      success: true,
      character: character
    };
  }
  
  /**
   * Get current character
   */
  getCurrentCharacter() {
    return this.characters[this.currentCharacter];
  }
  
  /**
   * Start race mode
   */
  startRace(numCompetitors = 3) {
    // Select random competitors
    const availableChars = Object.keys(this.characters)
      .filter(c => c !== this.currentCharacter);
    
    this.competitors = [];
    for (let i = 0; i < numCompetitors && i < availableChars.length; i++) {
      const charName = availableChars[Math.floor(Math.random() * availableChars.length)];
      this.competitors.push({
        name: charName,
        character: this.characters[charName],
        position: i + 2,
        speed: Math.random() * 10
      });
    }
    
    this.raceState = {
      inRace: true,
      position: 1,
      lap: 1,
      totalLaps: 3,
      startTime: Date.now()
    };
    
    console.log('🏁 Race Started!');
    console.log(`  You: ${this.getCurrentCharacter().emoji} ${this.getCurrentCharacter().name}`);
    console.log('  Competitors:');
    this.competitors.forEach(comp => {
      console.log(`    ${comp.character.emoji} ${comp.character.name}`);
    });
    
    return {
      success: true,
      raceState: this.raceState,
      competitors: this.competitors
    };
  }
  
  /**
   * Perform trick with character
   */
  performCharacterTrick(trickName) {
    const character = this.getCurrentCharacter();
    const trickBonus = character.trickBonus;
    
    console.log(`${character.emoji} ${character.name} performs ${trickName}!`);
    console.log(`  Bonus multiplier: ${trickBonus}x`);
    
    // Animate character
    this.animateCharacter(trickName);
    
    return {
      character: character.name,
      trick: trickName,
      bonus: trickBonus
    };
  }
  
  /**
   * Animate character trick
   */
  animateCharacter(trickName) {
    const character = this.getCurrentCharacter();
    const frames = [
      `${character.emoji} `,
      `${character.emoji}⬆️`,
      `${character.emoji}🌀`,
      `${character.emoji}⭐`,
      `${character.emoji}✨`
    ];
    
    // In a real implementation, this would animate in the terminal
    console.log(`Animation: ${frames.join(' → ')}`);
  }
  
  /**
   * Use special move
   */
  useSpecialMove() {
    const character = this.getCurrentCharacter();
    
    console.log(`✨ ${character.name} uses ${character.specialMove}!`);
    
    // Special move effects
    const effects = {
      'Mushroom Boost': { speedBoost: 2.0, duration: 3000 },
      'Ghost Jump': { jumpHeight: 2.0, duration: 2000 },
      'Royal Flip': { trickBonus: 2.0, duration: 4000 },
      'Spore Dash': { speedBoost: 1.5, trickBonus: 1.5, duration: 3000 },
      'Egg Throw': { obstacleRemove: true, duration: 5000 },
      'Fire Breath': { clearPath: true, duration: 4000 }
    };
    
    const effect = effects[character.specialMove];
    
    return {
      specialMove: character.specialMove,
      effect: effect
    };
  }
  
  /**
   * Handle joystick input
   */
  handleJoystick(direction, button = null) {
    const character = this.getCurrentCharacter();
    let action = '';
    
    if (button) {
      action = this.joystickControls[button];
    } else {
      action = this.joystickControls[direction];
    }
    
    console.log(`🕹️ ${direction || button}: ${action}`);
    
    // Execute action
    switch(action) {
      case 'trick':
        return this.performCharacterTrick('freestyle');
      case 'special_move':
        return this.useSpecialMove();
      case 'accelerate':
        return { action: 'accelerate', speed: character.speed + 2 };
      case 'brake':
        return { action: 'brake', speed: Math.max(0, character.speed - 2) };
      case 'lean_left':
      case 'lean_right':
        return { action: action, trickSetup: true };
      default:
        return { action: 'none' };
    }
  }
  
  /**
   * Update race position
   */
  updateRacePosition() {
    if (!this.raceState.inRace) return;
    
    // Random position changes
    const positionChange = Math.floor(Math.random() * 3) - 1; // -1, 0, or 1
    this.raceState.position = Math.max(1, Math.min(
      this.raceState.position + positionChange,
      this.competitors.length + 1
    ));
    
    return this.raceState.position;
  }
  
  /**
   * Get race status
   */
  getRaceStatus() {
    if (!this.raceState.inRace) {
      return { inRace: false };
    }
    
    return {
      inRace: true,
      position: this.raceState.position,
      lap: this.raceState.lap,
      totalLaps: this.raceState.totalLaps,
      competitors: this.competitors,
      elapsed: Date.now() - this.raceState.startTime
    };
  }
  
  /**
   * Place obstacle on track
   */
  placeObstacle(obstacleType, position) {
    const obstacle = this.obstacles[obstacleType];
    
    if (!obstacle) {
      return { success: false, error: 'Unknown obstacle type' };
    }
    
    console.log(`${obstacle.emoji} Placed at position ${position}`);
    
    return {
      success: true,
      obstacle: obstacle,
      position: position
    };
  }
  
  /**
   * Collect item
   */
  collectItem(itemType) {
    const item = this.obstacles[itemType];
    
    if (!item) return { success: false };
    
    console.log(`Collected ${item.emoji}!`);
    
    if (item.type === 'collectible') {
      return { success: true, points: item.points };
    } else if (item.type === 'powerup') {
      return { success: true, powerup: itemType, duration: item.duration };
    } else if (item.type === 'ramp') {
      return { success: true, boost: item.boost };
    }
    
    return { success: true };
  }
  
  /**
   * Get available characters
   */
  getCharacters() {
    return Object.entries(this.characters).map(([key, char]) => ({
      id: key,
      ...char
    }));
  }
  
  /**
   * Get MRW status
   */
  getStatus() {
    return {
      currentCharacter: this.getCurrentCharacter(),
      raceState: this.raceState,
      competitors: this.competitors,
      joystickEnabled: true
    };
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MRWTerminal;
} else if (typeof window !== 'undefined') {
  window.MRWTerminal = MRWTerminal;
}
