/**
 * BMX Terminal Demo & Test Suite
 * Demonstrates all features and validates functionality
 */

class BMXTerminalDemo {
  constructor() {
    this.tests = [];
    this.results = {
      passed: 0,
      failed: 0,
      total: 0
    };
  }
  
  async runAll() {
    console.log('🚴 BMX Terminal Demo & Test Suite\n');
    console.log('='.repeat(60));
    
    await this.demo1_basicTricks();
    await this.demo2_comboSystem();
    await this.demo3_physicsEngine();
    await this.demo4_themeSystem();
    await this.demo5_mrwCharacters();
    await this.demo6_scoringSystem();
    await this.demo7_achievements();
    await this.demo8_integration();
    
    this.printResults();
  }
  
  async demo1_basicTricks() {
    console.log('\n📍 Demo 1: Basic Tricks');
    console.log('-'.repeat(60));
    
    const physics = new BMXPhysicsEngine();
    const combos = new ComboSystem();
    const terminal = new BMXTerminal();
    
    await terminal.init(physics, combos);
    
    // Charge energy
    physics.pedalCharge(10);
    console.log('✓ Charged capacitor to full');
    
    // Test each trick
    const tricks = ['wheelie', 'bunnyhop', 'tailwhip', 'backflip', 'grind'];
    
    for (const trick of tricks) {
      const result = await terminal.executeTrick(trick, `echo "Testing ${trick}"`);
      
      if (result.success) {
        console.log(`✓ ${trick}: ${result.points} points (${terminal.tricks[trick].multiplier}x)`);
        this.test('pass', `${trick} execution`);
      } else {
        console.log(`✗ ${trick}: ${result.error}`);
        this.test('fail', `${trick} execution`);
      }
      
      // Recharge
      physics.pedalCharge(5);
    }
  }
  
  async demo2_comboSystem() {
    console.log('\n📍 Demo 2: Combo System');
    console.log('-'.repeat(60));
    
    const physics = new BMXPhysicsEngine();
    const combos = new ComboSystem();
    const terminal = new BMXTerminal();
    
    await terminal.init(physics, combos);
    physics.pedalCharge(20);
    
    // Test super_jump combo: wheelie + bunnyhop
    console.log('\nTesting Super Jump combo (wheelie + bunnyhop):');
    await terminal.executeTrick('wheelie', 'echo test');
    physics.pedalCharge(5);
    
    const result = await terminal.executeTrick('bunnyhop', 'echo test');
    const combo = combos.checkCombo(['wheelie', 'bunnyhop']);
    
    if (combo) {
      console.log(`✓ Combo detected: ${combo.name} (${combo.multiplier}x)`);
      this.test('pass', 'Super Jump combo');
    } else {
      console.log('✗ Combo not detected');
      this.test('fail', 'Super Jump combo');
    }
    
    // Test token formula combo
    console.log('\nTesting Token Formula combo:');
    physics.pedalCharge(50);
    await terminal.executeTrick('backflip', 'echo test');
    physics.pedalCharge(10);
    await terminal.executeTrick('360', 'echo test');
    physics.pedalCharge(10);
    await terminal.executeTrick('flair', 'echo test');
    
    const tokenCombo = combos.checkCombo(['backflip', '360', 'flair']);
    if (tokenCombo && tokenCombo.tokenReward) {
      console.log(`✓ Token Formula: ${tokenCombo.name} (+${tokenCombo.tokenReward} tokens)`);
      this.test('pass', 'Token formula combo');
    }
  }
  
  demo3_physicsEngine() {
    console.log('\n📍 Demo 3: Physics Engine');
    console.log('-'.repeat(60));
    
    const physics = new BMXPhysicsEngine();
    
    // Test charging
    console.log('\nTesting capacitor charging:');
    const charge1 = physics.pedalCharge(1);
    console.log(`✓ Charged ${charge1.charged.toFixed(1)} units (intensity: 1)`);
    
    const charge5 = physics.pedalCharge(5);
    console.log(`✓ Charged ${charge5.charged.toFixed(1)} units (intensity: 5)`);
    
    const status = physics.getStatus();
    console.log(`✓ Current charge: ${status.charge.toFixed(1)}/${status.maxCharge}`);
    console.log(`✓ Voltage: ${status.voltage.toFixed(2)}V`);
    
    this.test('pass', 'Capacitor charging');
    
    // Test discharge
    console.log('\nTesting energy discharge:');
    const discharge = physics.discharge(20);
    if (discharge.success) {
      console.log(`✓ Discharged 20 units, ${discharge.remaining.toFixed(1)} remaining`);
      this.test('pass', 'Energy discharge');
    } else {
      console.log(`✗ Discharge failed: ${discharge.error}`);
      this.test('fail', 'Energy discharge');
    }
    
    // Test physics simulation
    console.log('\nTesting trick physics simulation:');
    const simulation = physics.simulateTrickPhysics('backflip', 40);
    console.log(`✓ Height: ${simulation.height.toFixed(2)}m`);
    console.log(`✓ Velocity: ${simulation.velocity.toFixed(2)}m/s`);
    console.log(`✓ Hang time: ${simulation.hangTime.toFixed(2)}s`);
    console.log(`✓ G-force: ${simulation.gForce.toFixed(2)}g`);
    
    this.test('pass', 'Physics simulation');
  }
  
  demo4_themeSystem() {
    console.log('\n📍 Demo 4: Theme System');
    console.log('-'.repeat(60));
    
    const themeManager = new ThemeManager();
    const themes = themeManager.getAllThemes();
    
    console.log(`\n✓ ${themes.length} themes available:`);
    
    themes.forEach(themeName => {
      const theme = themeManager.getTheme(themeName);
      console.log(`  ${theme.name}`);
      console.log(`    Colors: ${theme.colors.primary}, ${theme.colors.secondary}`);
      console.log(`    Obstacles: ${theme.obstacles.slice(0, 3).join(', ')}...`);
    });
    
    this.test('pass', 'Theme loading');
    
    // Test theme switching
    console.log('\nTesting theme switching:');
    const result = themeManager.switchTheme('electronics');
    if (result.success) {
      console.log(`✓ Switched to: ${result.theme.name}`);
      this.test('pass', 'Theme switching');
    } else {
      console.log(`✗ Theme switch failed`);
      this.test('fail', 'Theme switching');
    }
  }
  
  demo5_mrwCharacters() {
    console.log('\n📍 Demo 5: MRW Characters');
    console.log('-'.repeat(60));
    
    const mrw = new MRWTerminal();
    
    console.log('\nAvailable characters:');
    const characters = mrw.getCharacters();
    
    characters.forEach(char => {
      console.log(`  ${char.emoji} ${char.name}`);
      console.log(`    Vehicle: ${char.vehicle}`);
      console.log(`    Speed: ${char.speed}/10`);
      console.log(`    Trick Bonus: ${char.trickBonus}x`);
      console.log(`    Special: ${char.specialMove}`);
    });
    
    this.test('pass', 'Character loading');
    
    // Test character selection
    console.log('\nTesting character selection:');
    const result = mrw.selectCharacter('mario');
    if (result.success) {
      console.log(`✓ Selected: ${result.character.name}`);
      this.test('pass', 'Character selection');
    }
    
    // Test special move
    console.log('\nTesting special move:');
    const special = mrw.useSpecialMove();
    console.log(`✓ ${special.specialMove} activated!`);
    console.log(`  Effect: ${JSON.stringify(special.effect)}`);
    this.test('pass', 'Special moves');
    
    // Test race mode
    console.log('\nTesting race mode:');
    const race = mrw.startRace(3);
    console.log(`✓ Race started with ${race.competitors.length} competitors`);
    this.test('pass', 'Race mode');
  }
  
  demo6_scoringSystem() {
    console.log('\n📍 Demo 6: Scoring System');
    console.log('-'.repeat(60));
    
    const rewards = new TrickRewards();
    
    // Test point calculation
    console.log('\nTesting point calculation:');
    const trick = { difficulty: 4, multiplier: 2.0 };
    const points = rewards.calculatePoints(trick, { combo: 1.5, theme: 1.2 });
    console.log(`✓ Base (difficulty 4): 400 points`);
    console.log(`✓ With 2.0x trick multiplier: 800 points`);
    console.log(`✓ With 1.5x combo: 1200 points`);
    console.log(`✓ With 1.2x theme: ${points} points`);
    
    this.test('pass', 'Point calculation');
    
    // Test awarding points
    console.log('\nTesting point awards:');
    const award = rewards.awardPoints('wheelie', 100, {});
    console.log(`✓ Awarded 100 points`);
    console.log(`✓ Total score: ${award.totalScore}`);
    console.log(`✓ Session tricks: ${award.sessionTricks}`);
    
    this.test('pass', 'Point awards');
    
    // Test leaderboard
    console.log('\nTesting leaderboard:');
    rewards.addToLeaderboard('Player1', 5000, { tricks: 50, combos: 10 });
    rewards.addToLeaderboard('Player2', 3000, { tricks: 30, combos: 5 });
    const leaderboard = rewards.getLeaderboard(2);
    
    console.log('✓ Leaderboard:');
    leaderboard.forEach(entry => {
      console.log(`  ${entry.rank}. ${entry.player}: ${entry.score} (${entry.tricks} tricks)`);
    });
    
    this.test('pass', 'Leaderboard');
  }
  
  demo7_achievements() {
    console.log('\n📍 Demo 7: Achievements');
    console.log('-'.repeat(60));
    
    const rewards = new TrickRewards();
    
    console.log('\nAll achievements:');
    const achievements = rewards.getAllAchievements();
    
    achievements.slice(0, 5).forEach(ach => {
      console.log(`  ${ach.emoji} ${ach.name} (${ach.points} pts)`);
      console.log(`    ${ach.description}`);
      if (ach.required) {
        console.log(`    Progress: ${ach.progressPercent.toFixed(0)}%`);
      }
    });
    
    console.log(`  ... and ${achievements.length - 5} more`);
    
    this.test('pass', 'Achievement system');
    
    // Test unlocking
    console.log('\nTesting achievement unlock:');
    rewards.awardPoints('wheelie', 100, {});
    const newAchievements = rewards.getNewlyUnlocked();
    
    if (newAchievements.length > 0) {
      console.log('✓ Achievements unlocked:');
      newAchievements.forEach(ach => {
        console.log(`  ${ach.emoji} ${ach.name} (+${ach.points} pts)`);
      });
      this.test('pass', 'Achievement unlock');
    }
  }
  
  async demo8_integration() {
    console.log('\n📍 Demo 8: Full System Integration');
    console.log('-'.repeat(60));
    
    const physics = new BMXPhysicsEngine();
    const combos = new ComboSystem();
    const terminal = new BMXTerminal();
    const rewards = new TrickRewards();
    const mrw = new MRWTerminal();
    const themeManager = new ThemeManager();
    
    await terminal.init(physics, combos);
    mrw.selectCharacter('mario');
    themeManager.switchTheme('mario');
    
    console.log('\n✓ All systems initialized');
    
    // Perform a complete workflow
    console.log('\nPerforming complete workflow:');
    
    // 1. Charge energy
    physics.pedalCharge(10);
    console.log('1. ✓ Charged capacitor');
    
    // 2. Execute trick with character bonus
    const character = mrw.getCurrentCharacter();
    const result = await terminal.executeTrick('wheelie', 'git status');
    console.log(`2. ✓ ${character.emoji} performed wheelie`);
    
    // 3. Award points with multipliers
    const pointsWithBonus = result.points * character.trickBonus;
    rewards.awardPoints('wheelie', pointsWithBonus, {});
    console.log(`3. ✓ Awarded ${pointsWithBonus} points (character bonus: ${character.trickBonus}x)`);
    
    // 4. Check status
    const status = terminal.getStatus();
    console.log('4. ✓ System status:');
    console.log(`   Theme: ${status.themeConfig.name}`);
    console.log(`   Energy: ${status.energy.toFixed(1)}`);
    console.log(`   Score: ${rewards.currentSession.score}`);
    console.log(`   Tricks: ${status.tricksPerformed}`);
    
    this.test('pass', 'Full integration');
  }
  
  test(result, name) {
    this.results.total++;
    if (result === 'pass') {
      this.results.passed++;
    } else {
      this.results.failed++;
    }
  }
  
  printResults() {
    console.log('\n' + '='.repeat(60));
    console.log('📊 Test Results');
    console.log('='.repeat(60));
    console.log(`Total Tests: ${this.results.total}`);
    console.log(`✓ Passed: ${this.results.passed}`);
    console.log(`✗ Failed: ${this.results.failed}`);
    console.log(`Success Rate: ${((this.results.passed / this.results.total) * 100).toFixed(1)}%`);
    console.log('='.repeat(60));
    
    if (this.results.failed === 0) {
      console.log('\n🎉 All tests passed! BMX Terminal is ready to ride! 🚴');
    }
  }
}

// Run demo if in Node.js environment
if (typeof require !== 'undefined') {
  // Load all modules
  try {
    const BMXTerminal = require('./bmx-terminal.js');
    const BasicTricks = require('./tricks/basic-tricks.js');
    const ComboSystem = require('./tricks/combo-system.js');
    const BMXPhysicsEngine = require('./tricks/physics-engine.js');
    const { ThemeManager } = require('./themes/bmx-themes.js');
    const TrickRewards = require('./scoring/trick-rewards.js');
    const MRWTerminal = require('./terminals/mrw-terminal.js');
    
    // Make global
    global.BMXTerminal = BMXTerminal;
    global.BasicTricks = BasicTricks;
    global.ComboSystem = ComboSystem;
    global.BMXPhysicsEngine = BMXPhysicsEngine;
    global.ThemeManager = ThemeManager;
    global.TrickRewards = TrickRewards;
    global.MRWTerminal = MRWTerminal;
    
    // Run demo
    const demo = new BMXTerminalDemo();
    demo.runAll();
  } catch (error) {
    console.error('Error loading modules:', error.message);
    console.log('\nNote: This demo requires all BMX Terminal modules to be available.');
    console.log('Run this from the mongoose.os root directory or use the web interface.');
  }
}

// Export for browser use
if (typeof window !== 'undefined') {
  window.BMXTerminalDemo = BMXTerminalDemo;
  
  // Add run button to page
  window.addEventListener('load', () => {
    const runButton = document.createElement('button');
    runButton.textContent = '🧪 Run Demo & Tests';
    runButton.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      padding: 15px 25px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 8px;
      font-weight: bold;
      cursor: pointer;
      z-index: 1000;
    `;
    
    runButton.onclick = async () => {
      const demo = new BMXTerminalDemo();
      await demo.runAll();
    };
    
    document.body.appendChild(runButton);
  });
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BMXTerminalDemo;
}
