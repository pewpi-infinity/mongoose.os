/**
 * Combo System for BMX Terminal
 * Detects and rewards trick combinations
 */

class ComboSystem {
  constructor() {
    // Special combo definitions
    this.combos = {
      // Basic combos
      'super_jump': {
        name: 'Super Jump',
        tricks: ['wheelie', 'bunnyhop'],
        multiplier: 1.5,
        description: 'Quick elevation gain',
        emoji: '🚀'
      },
      
      'ultra_fast_compile': {
        name: 'Ultra Fast Compile',
        tricks: ['tailwhip', 'backflip'],
        multiplier: 2.0,
        description: 'Lightning speed compilation',
        emoji: '⚡'
      },
      
      'quantum_optimization': {
        name: 'Quantum Optimization',
        tricks: ['grind', 'manual', 'bunnyhop'],
        multiplier: 2.5,
        description: 'Reality-bending optimization',
        emoji: '🌀'
      },
      
      'mushroom_code_compression': {
        name: 'Mushroom Code Compression',
        tricks: ['360', 'tailwhip', 'barspin'],
        multiplier: 3.0,
        description: 'Mario-powered compression',
        emoji: '🍄'
      },
      
      // Token formula combos
      'crown_orchestrator_flip': {
        name: 'Crown Orchestrator Flip 👑📶⚪',
        tricks: ['backflip', '360', 'flair'],
        multiplier: 3.5,
        description: 'Royal orchestration technique',
        emoji: '👑',
        tokenReward: 100
      },
      
      'memory_thread_grind': {
        name: 'Memory Thread Grind 🗄️🧵📶',
        tricks: ['grind', 'manual', 'tailwhip'],
        multiplier: 3.2,
        description: 'Thread through memory banks',
        emoji: '🗄️',
        tokenReward: 80
      },
      
      'smart_weaver_spin': {
        name: 'Smart Weaver Spin 🪡🤓⭐',
        tricks: ['tailwhip', 'barspin', '360'],
        multiplier: 3.8,
        description: 'Weave code intelligently',
        emoji: '🪡',
        tokenReward: 120
      },
      
      // Advanced combos
      'gravity_defiance': {
        name: 'Gravity Defiance',
        tricks: ['backflip', 'backflip', 'superman'],
        multiplier: 4.0,
        description: 'Physics? What physics?',
        emoji: '🌌'
      },
      
      'circuit_breaker': {
        name: 'Circuit Breaker',
        tricks: ['grind', 'barspin', 'manual', 'grind'],
        multiplier: 3.5,
        description: 'Overload the circuits',
        emoji: '🔌'
      },
      
      'time_warp': {
        name: 'Time Warp',
        tricks: ['360', '360', '360'],
        multiplier: 4.5,
        description: 'Bend time itself',
        emoji: '⏰'
      }
    };
    
    this.comboHistory = [];
    this.activeCombo = null;
    this.comboTimer = null;
    this.comboWindow = 5000; // 5 seconds to complete combo
  }
  
  /**
   * Check if current trick chain matches any combos
   */
  checkCombo(trickChain) {
    if (!trickChain || trickChain.length < 2) {
      return null;
    }
    
    // Check each combo pattern
    for (const [key, combo] of Object.entries(this.combos)) {
      if (this.matchesCombo(trickChain, combo.tricks)) {
        this.recordCombo(key, combo);
        return {
          name: combo.name,
          multiplier: combo.multiplier,
          description: combo.description,
          emoji: combo.emoji,
          tokenReward: combo.tokenReward || 0
        };
      }
    }
    
    return null;
  }
  
  /**
   * Check if trick chain matches combo pattern
   */
  matchesCombo(chain, pattern) {
    if (chain.length < pattern.length) {
      return false;
    }
    
    // Check if pattern exists at end of chain
    const chainEnd = chain.slice(-pattern.length);
    return pattern.every((trick, index) => trick === chainEnd[index]);
  }
  
  /**
   * Record combo achievement
   */
  recordCombo(comboKey, combo) {
    const comboRecord = {
      key: comboKey,
      name: combo.name,
      timestamp: Date.now(),
      multiplier: combo.multiplier,
      tricks: combo.tricks
    };
    
    this.comboHistory.push(comboRecord);
    this.activeCombo = comboRecord;
    
    // Clear active combo after window
    if (this.comboTimer) {
      clearTimeout(this.comboTimer);
    }
    
    this.comboTimer = setTimeout(() => {
      this.activeCombo = null;
    }, this.comboWindow);
  }
  
  /**
   * Get all possible combos for current chain
   */
  getPossibleCombos(currentChain) {
    const possible = [];
    
    for (const [key, combo] of Object.entries(this.combos)) {
      // Check if current chain is a partial match
      const remainingTricks = this.getRemainingTricks(currentChain, combo.tricks);
      
      if (remainingTricks.length > 0 && remainingTricks.length < combo.tricks.length) {
        possible.push({
          key: key,
          name: combo.name,
          remaining: remainingTricks,
          progress: ((combo.tricks.length - remainingTricks.length) / combo.tricks.length) * 100
        });
      }
    }
    
    return possible;
  }
  
  /**
   * Get remaining tricks needed for combo
   */
  getRemainingTricks(currentChain, comboPattern) {
    let matchIndex = 0;
    
    for (let i = 0; i < currentChain.length && matchIndex < comboPattern.length; i++) {
      if (currentChain[i] === comboPattern[matchIndex]) {
        matchIndex++;
      }
    }
    
    return comboPattern.slice(matchIndex);
  }
  
  /**
   * Get combo statistics
   */
  getStats() {
    const stats = {
      totalCombos: this.comboHistory.length,
      uniqueCombos: new Set(this.comboHistory.map(c => c.key)).size,
      totalMultiplier: this.comboHistory.reduce((sum, c) => sum + c.multiplier, 0),
      bestCombo: null,
      recentCombos: this.comboHistory.slice(-5)
    };
    
    if (this.comboHistory.length > 0) {
      stats.bestCombo = this.comboHistory.reduce((best, current) => 
        current.multiplier > best.multiplier ? current : best
      );
    }
    
    return stats;
  }
  
  /**
   * Get combo leaderboard
   */
  getLeaderboard() {
    const comboCount = {};
    
    this.comboHistory.forEach(combo => {
      comboCount[combo.key] = (comboCount[combo.key] || 0) + 1;
    });
    
    return Object.entries(comboCount)
      .map(([key, count]) => ({
        combo: this.combos[key].name,
        count: count,
        multiplier: this.combos[key].multiplier
      }))
      .sort((a, b) => b.count - a.count);
  }
  
  /**
   * Get available combos list
   */
  getAvailableCombos() {
    return Object.entries(this.combos).map(([key, combo]) => ({
      key: key,
      name: combo.name,
      tricks: combo.tricks,
      multiplier: combo.multiplier,
      description: combo.description,
      emoji: combo.emoji,
      tokenReward: combo.tokenReward || 0
    }));
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = ComboSystem;
}
