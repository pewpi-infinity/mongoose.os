/**
 * Trick Rewards System
 * Scoring, achievements, and leaderboard
 */

class TrickRewards {
  constructor() {
    this.achievements = {
      // Beginner achievements
      'first_trick': {
        name: 'First Trick',
        description: 'Perform your first BMX trick',
        emoji: '🎯',
        points: 50,
        unlocked: false
      },
      'pedal_master': {
        name: 'Pedal Master',
        description: 'Fully charge capacitor 10 times',
        emoji: '⚡',
        points: 100,
        unlocked: false,
        progress: 0,
        required: 10
      },
      
      // Trick achievements
      'wheelie_warrior': {
        name: 'Wheelie Warrior',
        description: 'Perform 50 wheelies',
        emoji: '🚴‍♂️',
        points: 150,
        unlocked: false,
        progress: 0,
        required: 50
      },
      'flip_master': {
        name: 'Flip Master',
        description: 'Land 20 backflips',
        emoji: '🔄',
        points: 300,
        unlocked: false,
        progress: 0,
        required: 20
      },
      'grind_king': {
        name: 'Grind King',
        description: 'Complete 30 grinds',
        emoji: '⚡',
        points: 250,
        unlocked: false,
        progress: 0,
        required: 30
      },
      
      // Combo achievements
      'combo_novice': {
        name: 'Combo Novice',
        description: 'Complete your first combo',
        emoji: '🌟',
        points: 200,
        unlocked: false
      },
      'combo_master': {
        name: 'Combo Master',
        description: 'Complete 10 different combos',
        emoji: '💫',
        points: 500,
        unlocked: false,
        progress: 0,
        required: 10
      },
      'token_formula_unlocked': {
        name: 'Token Formula Unlocked',
        description: 'Unlock a special token formula combo',
        emoji: '👑',
        points: 1000,
        unlocked: false
      },
      
      // Score achievements
      'point_collector': {
        name: 'Point Collector',
        description: 'Reach 10,000 points',
        emoji: '💯',
        points: 300,
        unlocked: false
      },
      'score_legend': {
        name: 'Score Legend',
        description: 'Reach 50,000 points',
        emoji: '🏆',
        points: 1000,
        unlocked: false
      },
      
      // Theme achievements
      'theme_explorer': {
        name: 'Theme Explorer',
        description: 'Try all 11 themes',
        emoji: '🎨',
        points: 400,
        unlocked: false,
        progress: 0,
        required: 11
      },
      'mario_champion': {
        name: 'Mario Champion',
        description: 'Score 5,000 points in Mario theme',
        emoji: '🍄',
        points: 300,
        unlocked: false
      },
      
      // Advanced achievements
      'no_falls': {
        name: 'Perfect Run',
        description: 'Complete 20 tricks without failing',
        emoji: '✨',
        points: 800,
        unlocked: false,
        progress: 0,
        required: 20
      },
      'energy_efficient': {
        name: 'Energy Efficient',
        description: 'Complete 10 tricks with minimal energy',
        emoji: '🔋',
        points: 500,
        unlocked: false,
        progress: 0,
        required: 10
      },
      'speed_demon': {
        name: 'Speed Demon',
        description: 'Complete 5 tricks in under 10 seconds',
        emoji: '⚡',
        points: 600,
        unlocked: false
      }
    };
    
    this.leaderboard = [];
    this.currentSession = {
      score: 0,
      tricks: 0,
      combos: 0,
      startTime: Date.now()
    };
  }
  
  /**
   * Calculate points for a trick
   */
  calculatePoints(trick, multipliers = {}) {
    const basePoints = trick.difficulty * 100;
    const trickMultiplier = trick.multiplier || 1.0;
    const comboMultiplier = multipliers.combo || 1.0;
    const themeMultiplier = multipliers.theme || 1.0;
    
    const points = basePoints * trickMultiplier * comboMultiplier * themeMultiplier;
    return Math.floor(points);
  }
  
  /**
   * Award points and check achievements
   */
  awardPoints(trickName, points, context = {}) {
    this.currentSession.score += points;
    this.currentSession.tricks += 1;
    
    if (context.combo) {
      this.currentSession.combos += 1;
    }
    
    // Check achievements
    this.checkAchievements(trickName, context);
    
    return {
      totalScore: this.currentSession.score,
      sessionTricks: this.currentSession.tricks,
      newAchievements: this.getNewlyUnlocked()
    };
  }
  
  /**
   * Check and unlock achievements
   */
  checkAchievements(trickName, context) {
    // First trick
    if (!this.achievements.first_trick.unlocked && this.currentSession.tricks === 1) {
      this.unlockAchievement('first_trick');
    }
    
    // Combo achievements
    if (context.combo && !this.achievements.combo_novice.unlocked) {
      this.unlockAchievement('combo_novice');
    }
    
    // Token formula
    if (context.tokenCombo && !this.achievements.token_formula_unlocked.unlocked) {
      this.unlockAchievement('token_formula_unlocked');
    }
    
    // Score achievements
    if (this.currentSession.score >= 10000 && !this.achievements.point_collector.unlocked) {
      this.unlockAchievement('point_collector');
    }
    if (this.currentSession.score >= 50000 && !this.achievements.score_legend.unlocked) {
      this.unlockAchievement('score_legend');
    }
    
    // Trick-specific achievements
    this.updateTrickProgress(trickName);
  }
  
  /**
   * Update progress for trick-specific achievements
   */
  updateTrickProgress(trickName) {
    if (trickName === 'wheelie') {
      this.updateProgress('wheelie_warrior');
    } else if (trickName === 'backflip') {
      this.updateProgress('flip_master');
    } else if (trickName === 'grind') {
      this.updateProgress('grind_king');
    }
  }
  
  /**
   * Update achievement progress
   */
  updateProgress(achievementKey) {
    const achievement = this.achievements[achievementKey];
    if (!achievement || achievement.unlocked) return;
    
    achievement.progress = (achievement.progress || 0) + 1;
    
    if (achievement.progress >= achievement.required) {
      this.unlockAchievement(achievementKey);
    }
  }
  
  /**
   * Unlock an achievement
   */
  unlockAchievement(key) {
    const achievement = this.achievements[key];
    if (!achievement || achievement.unlocked) return;
    
    achievement.unlocked = true;
    achievement.unlockedAt = Date.now();
    
    console.log(`🏆 Achievement Unlocked: ${achievement.name} ${achievement.emoji}`);
    console.log(`   ${achievement.description}`);
    console.log(`   +${achievement.points} points`);
    
    this.currentSession.score += achievement.points;
  }
  
  /**
   * Get newly unlocked achievements
   */
  getNewlyUnlocked() {
    return Object.entries(this.achievements)
      .filter(([_, achievement]) => 
        achievement.unlocked && 
        achievement.unlockedAt > Date.now() - 5000 // Last 5 seconds
      )
      .map(([key, achievement]) => ({
        key: key,
        name: achievement.name,
        emoji: achievement.emoji,
        points: achievement.points
      }));
  }
  
  /**
   * Get all achievements
   */
  getAllAchievements() {
    return Object.entries(this.achievements).map(([key, achievement]) => ({
      key: key,
      ...achievement,
      progressPercent: achievement.required ? 
        (achievement.progress || 0) / achievement.required * 100 : 100
    }));
  }
  
  /**
   * Add score to leaderboard
   */
  addToLeaderboard(playerName, score, stats = {}) {
    const entry = {
      player: playerName,
      score: score,
      tricks: stats.tricks || 0,
      combos: stats.combos || 0,
      achievements: stats.achievements || 0,
      timestamp: Date.now()
    };
    
    this.leaderboard.push(entry);
    this.leaderboard.sort((a, b) => b.score - a.score);
    
    // Keep top 100
    if (this.leaderboard.length > 100) {
      this.leaderboard = this.leaderboard.slice(0, 100);
    }
    
    return this.leaderboard.indexOf(entry) + 1; // Return rank
  }
  
  /**
   * Get leaderboard
   */
  getLeaderboard(limit = 10) {
    return this.leaderboard.slice(0, limit).map((entry, index) => ({
      rank: index + 1,
      ...entry
    }));
  }
  
  /**
   * Get session stats
   */
  getSessionStats() {
    const duration = Date.now() - this.currentSession.startTime;
    const unlockedCount = Object.values(this.achievements).filter(a => a.unlocked).length;
    
    return {
      score: this.currentSession.score,
      tricks: this.currentSession.tricks,
      combos: this.currentSession.combos,
      achievements: unlockedCount,
      duration: duration,
      avgPointsPerTrick: this.currentSession.tricks > 0 ? 
        this.currentSession.score / this.currentSession.tricks : 0
    };
  }
  
  /**
   * Reset session
   */
  resetSession() {
    this.currentSession = {
      score: 0,
      tricks: 0,
      combos: 0,
      startTime: Date.now()
    };
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = TrickRewards;
}
