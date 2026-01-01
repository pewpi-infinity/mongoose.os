/**
 * Basic BMX Tricks
 * Individual trick definitions and behaviors
 */

class BasicTricks {
  constructor() {
    this.tricks = {
      // Simple tricks
      wheelie: {
        name: 'Wheelie',
        description: 'Lift front wheel and balance on rear',
        difficulty: 1,
        energyCost: 10,
        multiplier: 1.0,
        animation: '🚴‍♂️',
        duration: 500,
        requirements: []
      },
      
      manual: {
        name: 'Manual',
        description: 'Lift rear wheel and balance on front',
        difficulty: 2,
        energyCost: 15,
        multiplier: 1.3,
        animation: '🚴',
        duration: 600,
        requirements: []
      },
      
      bunnyhop: {
        name: 'Bunny Hop',
        description: 'Jump with both wheels off ground',
        difficulty: 2,
        energyCost: 20,
        multiplier: 1.2,
        animation: '🚴‍♂️⬆️',
        duration: 700,
        requirements: []
      },
      
      // Intermediate tricks
      tailwhip: {
        name: 'Tailwhip',
        description: 'Spin frame 360° around handlebars',
        difficulty: 3,
        energyCost: 30,
        multiplier: 1.5,
        animation: '🚴🌀',
        duration: 900,
        requirements: ['bunnyhop']
      },
      
      grind: {
        name: 'Grind',
        description: 'Slide along rail or edge',
        difficulty: 3,
        energyCost: 25,
        multiplier: 1.8,
        animation: '🚴⚡',
        duration: 1000,
        requirements: ['bunnyhop']
      },
      
      barspin: {
        name: 'Barspin',
        description: 'Spin handlebars 360° while airborne',
        difficulty: 3,
        energyCost: 28,
        multiplier: 1.6,
        animation: '🚴💫',
        duration: 800,
        requirements: ['bunnyhop']
      },
      
      // Advanced tricks
      backflip: {
        name: 'Backflip',
        description: 'Rotate backward 360° in air',
        difficulty: 4,
        energyCost: 40,
        multiplier: 2.0,
        animation: '🚴🔄',
        duration: 1200,
        requirements: ['bunnyhop', 'wheelie']
      },
      
      '360': {
        name: '360',
        description: 'Spin rider and bike 360° horizontally',
        difficulty: 4,
        energyCost: 35,
        multiplier: 2.2,
        animation: '🚴🌪️',
        duration: 1100,
        requirements: ['bunnyhop']
      },
      
      // Expert tricks
      flair: {
        name: 'Flair',
        description: 'Backflip + 180° rotation',
        difficulty: 5,
        energyCost: 50,
        multiplier: 3.0,
        animation: '🚴🌟',
        duration: 1500,
        requirements: ['backflip', '360']
      },
      
      superman: {
        name: 'Superman',
        description: 'Extend body backward off bike',
        difficulty: 5,
        energyCost: 45,
        multiplier: 2.8,
        animation: '🦸‍♂️🚴',
        duration: 1400,
        requirements: ['backflip']
      }
    };
  }
  
  getTrick(name) {
    return this.tricks[name] || null;
  }
  
  getAllTricks() {
    return Object.keys(this.tricks);
  }
  
  getTricksByDifficulty(difficulty) {
    return Object.entries(this.tricks)
      .filter(([_, trick]) => trick.difficulty === difficulty)
      .map(([name, _]) => name);
  }
  
  canPerformTrick(trickName, unlockedTricks = []) {
    const trick = this.tricks[trickName];
    if (!trick) return false;
    return trick.requirements.every(req => unlockedTricks.includes(req));
  }
  
  getProgressionPath(targetTrick) {
    const trick = this.tricks[targetTrick];
    if (!trick) return [];
    
    const path = [...trick.requirements];
    trick.requirements.forEach(req => {
      const reqTrick = this.tricks[req];
      if (reqTrick && reqTrick.requirements.length > 0) {
        path.unshift(...reqTrick.requirements);
      }
    });
    
    return [...new Set(path), targetTrick];
  }
  
  calculateScore(trickName, comboMultiplier = 1.0, themeBonus = 0) {
    const trick = this.tricks[trickName];
    if (!trick) return 0;
    
    const baseScore = trick.difficulty * 100;
    const trickScore = baseScore * trick.multiplier;
    const comboScore = trickScore * comboMultiplier;
    const finalScore = comboScore + themeBonus;
    
    return Math.floor(finalScore);
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = BasicTricks;
}
