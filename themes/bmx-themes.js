/**
 * Theme Manager for BMX Terminal
 * All 11 themes with their configurations
 */

const BMXThemes = {
  mario: {
    name: '🍄 Mushroom Kingdom',
    description: 'Trick bike through the Mushroom Kingdom',
    colors: {
      primary: '#ff0000',
      secondary: '#00ff00',
      accent: '#ffff00',
      background: '#5c94fc',
      text: '#ffffff'
    },
    obstacles: ['pipe', 'mushroom', 'coin_block', 'goomba', 'koopa', 'star'],
    ramps: ['green_pipe', 'question_block', 'brick_platform'],
    characters: ['mario', 'luigi', 'toad', 'peach'],
    effects: {
      jump: 'coin_sound',
      trick: 'power_up',
      combo: 'star_music',
      fail: 'pipe_sound'
    },
    bgPattern: 'brick',
    music: 'overworld_theme'
  },
  
  electronics: {
    name: '🔌 Circuit Board',
    description: 'Circuit board ramps and electronic obstacles',
    colors: {
      primary: '#00ff00',
      secondary: '#0000ff',
      accent: '#ff00ff',
      background: '#001a00',
      text: '#00ff00'
    },
    obstacles: ['resistor', 'capacitor', 'transistor', 'diode', 'ic_chip'],
    ramps: ['circuit_trace', 'pcb_edge', 'solder_pad'],
    characters: ['electron', 'current_flow', 'voltage_meter'],
    effects: {
      jump: 'spark',
      trick: 'circuit_pulse',
      combo: 'voltage_surge',
      fail: 'short_circuit'
    },
    bgPattern: 'pcb',
    music: 'electronic_beats'
  },
  
  chemistry: {
    name: '🧪 Laboratory',
    description: 'Lab equipment obstacles and chemical reactions',
    colors: {
      primary: '#00ffff',
      secondary: '#ff00ff',
      accent: '#ffff00',
      background: '#ffffff',
      text: '#000000'
    },
    obstacles: ['beaker', 'flask', 'bunsen_burner', 'test_tube', 'petri_dish'],
    ramps: ['lab_bench', 'fume_hood', 'periodic_table'],
    characters: ['scientist', 'molecule', 'atom'],
    effects: {
      jump: 'bubble',
      trick: 'reaction',
      combo: 'explosion',
      fail: 'spill'
    },
    bgPattern: 'lab_tiles',
    music: 'experimental'
  },
  
  robotics: {
    name: '🤖 Robot Assembly',
    description: 'Robot assembly line course',
    colors: {
      primary: '#808080',
      secondary: '#ff6600',
      accent: '#00ccff',
      background: '#1a1a1a',
      text: '#ffffff'
    },
    obstacles: ['robot_arm', 'conveyor', 'servo', 'sensor', 'actuator'],
    ramps: ['assembly_line', 'robotic_platform', 'mechanical_ramp'],
    characters: ['robot', 'ai_core', 'drone'],
    effects: {
      jump: 'servo_whir',
      trick: 'mechanical_click',
      combo: 'assembly_complete',
      fail: 'malfunction'
    },
    bgPattern: 'factory_floor',
    music: 'industrial'
  },
  
  construction: {
    name: '🏗️ Building Site',
    description: 'Building site stunts and construction obstacles',
    colors: {
      primary: '#ff6600',
      secondary: '#ffff00',
      accent: '#000000',
      background: '#87ceeb',
      text: '#000000'
    },
    obstacles: ['scaffold', 'crane', 'beam', 'barrier', 'cement_mixer'],
    ramps: ['steel_beam', 'construction_slope', 'crane_arm'],
    characters: ['worker', 'foreman', 'excavator'],
    effects: {
      jump: 'metal_clang',
      trick: 'construction_horn',
      combo: 'building_complete',
      fail: 'crash'
    },
    bgPattern: 'concrete',
    music: 'construction_sounds'
  },
  
  space: {
    name: '🚀 Space Station',
    description: 'Zero-gravity BMX tricks in space',
    colors: {
      primary: '#000033',
      secondary: '#ffffff',
      accent: '#00ffff',
      background: '#000000',
      text: '#ffffff'
    },
    obstacles: ['satellite', 'asteroid', 'space_station', 'meteor', 'planet'],
    ramps: ['solar_panel', 'satellite_dish', 'space_module'],
    characters: ['astronaut', 'alien', 'robot'],
    effects: {
      jump: 'thruster',
      trick: 'zero_g',
      combo: 'warp_speed',
      fail: 'depressurize'
    },
    bgPattern: 'stars',
    music: 'space_ambient'
  },
  
  nature: {
    name: '🌳 Forest Trail',
    description: 'Natural terrain and forest obstacles',
    colors: {
      primary: '#228b22',
      secondary: '#8b4513',
      accent: '#ffff00',
      background: '#87ceeb',
      text: '#000000'
    },
    obstacles: ['tree', 'rock', 'log', 'bush', 'stream'],
    ramps: ['hill', 'fallen_tree', 'rock_formation'],
    characters: ['deer', 'bird', 'squirrel'],
    effects: {
      jump: 'rustle',
      trick: 'wind',
      combo: 'nature_harmony',
      fail: 'splash'
    },
    bgPattern: 'grass',
    music: 'forest_sounds'
  },
  
  cyber: {
    name: '💻 Cyberspace',
    description: 'Digital realm with data streams',
    colors: {
      primary: '#00ff00',
      secondary: '#000000',
      accent: '#ff00ff',
      background: '#001100',
      text: '#00ff00'
    },
    obstacles: ['firewall', 'data_stream', 'node', 'glitch', 'virus'],
    ramps: ['data_highway', 'network_bridge', 'server_rack'],
    characters: ['hacker', 'ai', 'program'],
    effects: {
      jump: 'digital_pulse',
      trick: 'code_execution',
      combo: 'system_breach',
      fail: '404_error'
    },
    bgPattern: 'matrix',
    music: 'cyberpunk'
  },
  
  ocean: {
    name: '🌊 Underwater',
    description: 'Aquatic BMX in underwater world',
    colors: {
      primary: '#0066cc',
      secondary: '#00ccff',
      accent: '#ffff00',
      background: '#003366',
      text: '#ffffff'
    },
    obstacles: ['coral', 'fish', 'bubble', 'treasure', 'seaweed'],
    ramps: ['coral_reef', 'shipwreck', 'underwater_cave'],
    characters: ['mermaid', 'dolphin', 'submarine'],
    effects: {
      jump: 'splash',
      trick: 'bubble_burst',
      combo: 'tidal_wave',
      fail: 'sink'
    },
    bgPattern: 'waves',
    music: 'ocean_ambient'
  },
  
  retro: {
    name: '👾 8-bit Arcade',
    description: 'Pixel-perfect retro gaming world',
    colors: {
      primary: '#ff00ff',
      secondary: '#00ffff',
      accent: '#ffff00',
      background: '#000000',
      text: '#ffffff'
    },
    obstacles: ['pixel_block', 'sprite', 'power_up', 'enemy', 'coin'],
    ramps: ['platform', 'ladder', 'pixel_ramp'],
    characters: ['player_one', 'boss', 'npc'],
    effects: {
      jump: '8bit_jump',
      trick: 'power_up_sound',
      combo: 'level_complete',
      fail: 'game_over'
    },
    bgPattern: 'pixels',
    music: 'chiptune'
  },
  
  neon: {
    name: '✨ Neon City',
    description: 'Futuristic neon cityscape',
    colors: {
      primary: '#ff1493',
      secondary: '#00ffff',
      accent: '#ffff00',
      background: '#0a0a1a',
      text: '#ffffff'
    },
    obstacles: ['neon_sign', 'hologram', 'light_beam', 'skyscraper', 'billboard'],
    ramps: ['neon_rail', 'rooftop', 'light_bridge'],
    characters: ['cyberpunk', 'android', 'hover_car'],
    effects: {
      jump: 'neon_flash',
      trick: 'hologram_flicker',
      combo: 'city_lights',
      fail: 'blackout'
    },
    bgPattern: 'neon_grid',
    music: 'synthwave'
  }
};

/**
 * Theme Manager class
 */
class ThemeManager {
  constructor() {
    this.themes = BMXThemes;
    this.currentTheme = 'mario';
  }
  
  /**
   * Get theme by name
   */
  getTheme(name) {
    return this.themes[name] || null;
  }
  
  /**
   * Get all themes
   */
  getAllThemes() {
    return Object.keys(this.themes);
  }
  
  /**
   * Switch to theme
   */
  switchTheme(name) {
    if (!this.themes[name]) {
      return { success: false, error: `Theme '${name}' not found` };
    }
    
    this.currentTheme = name;
    return {
      success: true,
      theme: this.themes[name]
    };
  }
  
  /**
   * Get current theme
   */
  getCurrentTheme() {
    return this.themes[this.currentTheme];
  }
  
  /**
   * Apply theme to terminal
   */
  applyTheme(terminalElement) {
    const theme = this.getCurrentTheme();
    
    if (!terminalElement) return;
    
    // Apply colors
    terminalElement.style.setProperty('--primary-color', theme.colors.primary);
    terminalElement.style.setProperty('--secondary-color', theme.colors.secondary);
    terminalElement.style.setProperty('--accent-color', theme.colors.accent);
    terminalElement.style.setProperty('--background-color', theme.colors.background);
    terminalElement.style.setProperty('--text-color', theme.colors.text);
    
    // Apply background pattern
    terminalElement.classList.add(`bg-${theme.bgPattern}`);
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { BMXThemes, ThemeManager };
} else if (typeof window !== 'undefined') {
  window.BMXThemes = BMXThemes;
  window.ThemeManager = ThemeManager;
}
