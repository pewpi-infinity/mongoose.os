/**
 * Machine Operating System (MOS) Core
 * 
 * This module manages all 287+ machines as an integrated operating system.
 * Each repository is a machine. The system itself is a machine containing machines.
 */

class MachineOS {
  constructor() {
    this.machines = [];
    this.activeMachines = new Map();
    this.machineConnections = new Map();
    this.systemState = {
      initialized: false,
      totalMachines: 0,
      activeMachines: 0,
      targetMachines: 601
    };
  }

  /**
   * Initialize the Machine OS
   */
  async initialize() {
    console.log('🚀 Initializing Machine OS...');
    
    try {
      // Load machine registry
      await this.loadMachineRegistry();
      
      // Establish inter-machine connections
      this.establishConnections();
      
      // Initialize quantum portal
      this.initializeQuantumPortal();
      
      this.systemState.initialized = true;
      console.log(`✅ Machine OS initialized with ${this.systemState.totalMachines} machines`);
      
      return true;
    } catch (error) {
      console.error('❌ Failed to initialize Machine OS:', error);
      return false;
    }
  }

  /**
   * Load all machines from the registry
   */
  async loadMachineRegistry() {
    const response = await fetch('/GLOBAL_REPO_CENSUS.json');
    this.machines = await response.json();
    this.systemState.totalMachines = this.machines.length;
    
    // Categorize machines
    this.machines.forEach(machine => {
      machine.category = this.categorizeMachine(machine);
      machine.status = 'ready';
      machine.connections = [];
    });
    
    console.log(`📦 Loaded ${this.machines.length} machines`);
  }

  /**
   * Categorize a machine based on its name and properties
   */
  categorizeMachine(machine) {
    const name = machine.name.toLowerCase();
    
    if (name.includes('brain-')) return 'brain_node';
    if (name.includes('sandbox-')) return 'sandbox';
    if (name.match(/^[a-z]$/)) return 'alphabet';
    if (name === 'mongoose.os') return 'core_hub';
    if (['z', 'banksy', 'gpt-vector-design', 'i', 'j', 'k', 'infinity-portal'].includes(name)) {
      return 'core_machine';
    }
    
    return 'utility';
  }

  /**
   * Establish connections between machines
   */
  establishConnections() {
    console.log('🔗 Establishing inter-machine connections...');
    
    // Every machine connects to the hub (mongoose.os)
    const hub = this.machines.find(m => m.name === 'mongoose.os');
    
    this.machines.forEach(machine => {
      // Connect to hub
      if (machine.name !== 'mongoose.os') {
        this.connectMachines(machine.name, hub.name);
      }
      
      // Brain nodes connect to each other in clusters
      if (machine.category === 'brain_node') {
        this.connectBrainNodes(machine);
      }
      
      // Alphabet machines form a chain
      if (machine.category === 'alphabet') {
        this.connectAlphabetMachines(machine);
      }
    });
    
    console.log('✅ Inter-machine connections established');
  }

  /**
   * Connect two machines
   */
  connectMachines(machineA, machineB) {
    if (!this.machineConnections.has(machineA)) {
      this.machineConnections.set(machineA, []);
    }
    this.machineConnections.get(machineA).push(machineB);
  }

  /**
   * Connect brain nodes in clusters for distributed processing
   */
  connectBrainNodes(brainNode) {
    const brainNodes = this.machines.filter(m => m.category === 'brain_node');
    const nodeNumber = parseInt(brainNode.name.match(/\d+/)?.[0] || 0);
    
    // Connect to adjacent brain nodes (cluster of 5)
    for (let i = -2; i <= 2; i++) {
      if (i !== 0) {
        const adjacentNum = nodeNumber + i;
        const adjacent = brainNodes.find(m => m.name.includes(`-${String(adjacentNum).padStart(3, '0')}`));
        if (adjacent) {
          this.connectMachines(brainNode.name, adjacent.name);
        }
      }
    }
  }

  /**
   * Connect alphabet machines in a chain
   */
  connectAlphabetMachines(machine) {
    const alpha = this.machines.filter(m => m.category === 'alphabet');
    const currentIndex = alpha.findIndex(m => m.name === machine.name);
    
    // Connect to previous and next
    if (currentIndex > 0) {
      this.connectMachines(machine.name, alpha[currentIndex - 1].name);
    }
    if (currentIndex < alpha.length - 1) {
      this.connectMachines(machine.name, alpha[currentIndex + 1].name);
    }
  }

  /**
   * Initialize quantum portal connections
   */
  initializeQuantumPortal() {
    console.log('⚡ Initializing quantum portal...');
    // Quantum portal provides distributed rendering and storage
    this.quantumPortal = {
      active: true,
      connections: this.machines.length,
      renderingNodes: this.machines.filter(m => m.category === 'brain_node').length
    };
  }

  /**
   * Get a machine by name
   */
  getMachine(name) {
    return this.machines.find(m => m.name === name);
  }

  /**
   * Get all machines by category
   */
  getMachinesByCategory(category) {
    return this.machines.filter(m => m.category === category);
  }

  /**
   * Get machine connections
   */
  getConnections(machineName) {
    return this.machineConnections.get(machineName) || [];
  }

  /**
   * Activate a machine (for future use with token licensing)
   */
  activateMachine(machineName, tokenId) {
    const machine = this.getMachine(machineName);
    if (machine) {
      machine.status = 'active';
      machine.tokenId = tokenId;
      machine.activatedAt = new Date().toISOString();
      this.activeMachines.set(machineName, machine);
      this.systemState.activeMachines = this.activeMachines.size;
      return true;
    }
    return false;
  }

  /**
   * Get system status
   */
  getStatus() {
    return {
      ...this.systemState,
      categories: {
        brain_nodes: this.getMachinesByCategory('brain_node').length,
        sandbox: this.getMachinesByCategory('sandbox').length,
        alphabet: this.getMachinesByCategory('alphabet').length,
        core_machines: this.getMachinesByCategory('core_machine').length,
        utility: this.getMachinesByCategory('utility').length
      },
      quantumPortal: this.quantumPortal
    };
  }

  /**
   * Send command to a machine (for i terminal)
   */
  sendCommand(machineName, command) {
    const machine = this.getMachine(machineName);
    if (!machine) {
      return { success: false, error: 'Machine not found' };
    }

    // Log command
    console.log(`📥 Command to ${machineName}: ${command}`);
    
    return {
      success: true,
      machine: machineName,
      command: command,
      response: `Command received by ${machineName}`,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Get machine output (for j terminal)
   */
  getMachineOutput(machineName) {
    const machine = this.getMachine(machineName);
    if (!machine) {
      return null;
    }

    return {
      machine: machineName,
      status: machine.status,
      category: machine.category,
      connections: this.getConnections(machineName).length,
      lastUpdate: machine.updatedAt
    };
  }
}

// Create global Machine OS instance
window.MachineOS = new MachineOS();

// Auto-initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.MachineOS.initialize();
  });
} else {
  window.MachineOS.initialize();
}

// Expose to console for debugging
console.log('💻 Machine OS loaded. Access via window.MachineOS');
console.log('📊 Try: MachineOS.getStatus()');
console.log('🔍 Try: MachineOS.getMachine("mongoose.os")');
console.log('🌐 Try: MachineOS.getConnections("mongoose.os")');
