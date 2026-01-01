/**
 * BMX Terminal Integration Example
 * Shows how to integrate BMX Terminal with existing terminal systems
 */

// Example 1: Standalone Usage
async function standaloneExample() {
  const physics = new BMXPhysicsEngine();
  const combos = new ComboSystem();
  const terminal = new BMXTerminal();
  const rewards = new TrickRewards();
  
  await terminal.init(physics, combos);
  
  // Charge up
  physics.pedalCharge(5);
  
  // Execute command with trick
  const result = await terminal.executeTrick('wheelie', 'git status');
  console.log('Trick result:', result);
  
  // Award points
  rewards.awardPoints('wheelie', result.points, { combo: result.combo });
}

// Example 2: Integration with Existing i-Terminal
function iTerminalIntegration() {
  // Wrap i-terminal commands with BMX tricks
  const originalSendCommand = window.sendICommand;
  
  window.sendICommand = async function() {
    const input = document.getElementById('iTerminalInput');
    const command = input.value.trim();
    
    // Check if command starts with trick
    const tricks = ['wheelie', 'bunnyhop', 'tailwhip', 'backflip', 'grind'];
    const firstWord = command.split(' ')[0].toLowerCase();
    
    if (tricks.includes(firstWord)) {
      // Use BMX terminal
      const trickName = firstWord;
      const actualCommand = command.substring(firstWord.length).trim();
      
      const result = await window.bmxTerminal.executeTrick(trickName, actualCommand);
      
      // Display in i-terminal
      const output = document.getElementById('iTerminalOutput');
      const resultLine = document.createElement('div');
      resultLine.className = 'terminal-line success';
      resultLine.textContent = `🚴 ${trickName}: +${result.points} points!`;
      output.appendChild(resultLine);
      
      input.value = '';
    } else {
      // Use original i-terminal command
      originalSendCommand();
    }
  };
}

// Example 3: Theme-Synchronized Terminals
function syncThemeAcrossTerminals(themeName) {
  // Update BMX terminal theme
  window.bmxTerminal.switchTheme(themeName);
  
  // Update i-terminal colors
  const theme = window.bmxTerminal.themes[themeName];
  const iTerminal = document.getElementById('iTerminal');
  if (iTerminal) {
    iTerminal.style.borderColor = theme.colors.primary;
    iTerminal.style.setProperty('--theme-color', theme.colors.primary);
  }
  
  // Update j-terminal colors
  const jTerminal = document.getElementById('jTerminal');
  if (jTerminal) {
    jTerminal.style.borderColor = theme.colors.secondary;
    jTerminal.style.setProperty('--theme-color', theme.colors.secondary);
  }
}

// Example 4: Combo Achievement Notifications
function setupAchievementNotifications() {
  setInterval(() => {
    const newAchievements = window.rewards.getNewlyUnlocked();
    
    newAchievements.forEach(achievement => {
      showAchievementPopup(achievement);
    });
  }, 1000);
}

function showAchievementPopup(achievement) {
  const popup = document.createElement('div');
  popup.className = 'achievement-popup';
  popup.innerHTML = `
    <div style="font-size: 1.5rem; margin-bottom: 10px;">${achievement.emoji}</div>
    <div style="font-weight: bold; margin-bottom: 5px;">Achievement Unlocked!</div>
    <div>${achievement.name}</div>
    <div style="color: gold; margin-top: 5px;">+${achievement.points} points</div>
  `;
  
  document.body.appendChild(popup);
  
  setTimeout(() => {
    popup.style.animation = 'slideOut 0.5s ease-out';
    setTimeout(() => popup.remove(), 500);
  }, 3000);
}

// Example 5: MRW Character Integration
async function setupMRWCharacters() {
  const mrw = new MRWTerminal();
  
  // Let user select character
  const characterSelect = document.createElement('select');
  characterSelect.innerHTML = `
    <option value="mario">🍄 Mario</option>
    <option value="luigi">👻 Luigi</option>
    <option value="peach">👑 Peach</option>
    <option value="toad">🍄 Toad</option>
    <option value="yoshi">🦖 Yoshi</option>
    <option value="bowser">🐲 Bowser</option>
  `;
  
  characterSelect.addEventListener('change', (e) => {
    mrw.selectCharacter(e.target.value);
    
    // Apply character bonus to BMX terminal
    const character = mrw.getCurrentCharacter();
    window.bmxTerminal.characterBonus = character.trickBonus;
  });
  
  return mrw;
}

// Example 6: Real-time Energy Monitoring
function setupEnergyMonitor() {
  const energyDisplay = document.createElement('div');
  energyDisplay.id = 'energy-monitor';
  energyDisplay.style.cssText = `
    position: fixed;
    top: 20px;
    left: 20px;
    background: rgba(0, 0, 0, 0.8);
    padding: 15px;
    border-radius: 8px;
    border: 2px solid #00ff00;
    z-index: 999;
  `;
  
  document.body.appendChild(energyDisplay);
  
  setInterval(() => {
    const status = window.physics.getStatus();
    energyDisplay.innerHTML = `
      <div style="color: #00ff00; font-weight: bold; margin-bottom: 5px;">⚡ ENERGY</div>
      <div style="font-size: 1.5rem; color: white;">${Math.round(status.charge)}/${status.maxCharge}</div>
      <div style="color: #ffff00; font-size: 0.8rem;">${Math.round(status.percentFull)}%</div>
      <div style="color: #00ffff; font-size: 0.8rem; margin-top: 5px;">
        ${status.voltage.toFixed(2)}V
      </div>
    `;
  }, 100);
}

// Example 7: Auto-Pedal System
function setupAutoPedal(targetEnergy = 80) {
  setInterval(() => {
    const currentEnergy = window.physics.getEnergy();
    
    if (currentEnergy < targetEnergy) {
      // Auto-charge to maintain minimum energy
      const needed = targetEnergy - currentEnergy;
      const intensity = Math.min(needed / 5, 5);
      window.physics.pedalCharge(intensity);
    }
  }, 2000);
}

// Example 8: Command History with Tricks
class BMXCommandHistory {
  constructor() {
    this.history = [];
    this.maxHistory = 100;
  }
  
  add(trick, command, result) {
    this.history.push({
      trick: trick,
      command: command,
      result: result,
      timestamp: Date.now()
    });
    
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    }
  }
  
  getRecent(count = 10) {
    return this.history.slice(-count);
  }
  
  getTrickStats() {
    const stats = {};
    this.history.forEach(entry => {
      stats[entry.trick] = (stats[entry.trick] || 0) + 1;
    });
    return stats;
  }
  
  getMostUsedTrick() {
    const stats = this.getTrickStats();
    return Object.entries(stats).reduce((a, b) => a[1] > b[1] ? a : b)[0];
  }
}

// Example 9: Combo Suggestions
function suggestNextTrick() {
  const currentChain = window.bmxTerminal.comboChain;
  const possible = window.combos.getPossibleCombos(currentChain);
  
  if (possible.length > 0) {
    console.log('💡 Combo Suggestions:');
    possible.forEach(combo => {
      console.log(`  ${combo.name}: ${combo.remaining.join(' → ')} (${combo.progress.toFixed(0)}%)`);
    });
  }
}

// Example 10: Full Integration Setup
async function setupBMXTerminalIntegration() {
  // Initialize all systems
  window.physics = new BMXPhysicsEngine();
  window.combos = new ComboSystem();
  window.bmxTerminal = new BMXTerminal();
  window.rewards = new TrickRewards();
  window.mrw = new MRWTerminal();
  window.themeManager = new ThemeManager();
  window.commandHistory = new BMXCommandHistory();
  
  await window.bmxTerminal.init(window.physics, window.combos);
  
  // Set up integrations
  iTerminalIntegration();
  setupAchievementNotifications();
  setupEnergyMonitor();
  setupAutoPedal(70); // Maintain 70% energy
  
  // Add global BMX command
  window.bmx = {
    trick: (name, cmd) => window.bmxTerminal.executeTrick(name, cmd),
    theme: (name) => syncThemeAcrossTerminals(name),
    pedal: (power) => window.physics.pedalCharge(power),
    status: () => window.bmxTerminal.getStatus(),
    help: () => console.log(window.bmxTerminal.getHelp()),
    suggest: () => suggestNextTrick(),
    character: (name) => window.mrw.selectCharacter(name)
  };
  
  console.log('🚴 BMX Terminal Integration Complete!');
  console.log('Use window.bmx for quick access:');
  console.log('  bmx.trick("wheelie", "ls")');
  console.log('  bmx.theme("electronics")');
  console.log('  bmx.pedal(5)');
  console.log('  bmx.status()');
  console.log('  bmx.suggest()');
}

// Auto-initialize if in browser
if (typeof window !== 'undefined') {
  window.addEventListener('load', () => {
    if (window.BMXTerminal && window.BMXPhysicsEngine) {
      setupBMXTerminalIntegration();
    }
  });
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    setupBMXTerminalIntegration,
    iTerminalIntegration,
    syncThemeAcrossTerminals,
    setupAchievementNotifications,
    setupMRWCharacters,
    BMXCommandHistory
  };
}
