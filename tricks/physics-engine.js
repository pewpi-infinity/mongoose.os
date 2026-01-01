/**
 * Physics Engine for BMX Terminal
 * Handles capacitor charging and energy discharge
 */

class BMXPhysicsEngine {
  constructor() {
    // Capacitor state
    this.capacitor = {
      charge: 0,
      maxCharge: 100,
      chargeRate: 5,
      decayRate: 0.5, // Passive decay per second
      voltage: 0
    };
    
    // Physics constants
    this.constants = {
      gravity: 9.81,
      airResistance: 0.1,
      friction: 0.05,
      pedalEfficiency: 0.9
    };
    
    // State
    this.isCharging = false;
    this.lastUpdate = Date.now();
    this.pedalPower = 0;
    
    // Start passive decay loop
    this.startDecayLoop();
  }
  
  /**
   * Charge capacitor by pedaling
   */
  pedalCharge(intensity = 1) {
    if (intensity < 0.1 || intensity > 10) {
      return {
        success: false,
        error: 'Intensity must be between 0.1 and 10'
      };
    }
    
    const chargeAmount = this.capacitor.chargeRate * intensity * this.constants.pedalEfficiency;
    const newCharge = Math.min(this.capacitor.charge + chargeAmount, this.capacitor.maxCharge);
    const actualCharge = newCharge - this.capacitor.charge;
    
    this.capacitor.charge = newCharge;
    this.capacitor.voltage = this.calculateVoltage(newCharge);
    this.pedalPower = intensity;
    
    return {
      success: true,
      charged: actualCharge,
      currentCharge: this.capacitor.charge,
      voltage: this.capacitor.voltage,
      percentFull: (this.capacitor.charge / this.capacitor.maxCharge) * 100
    };
  }
  
  /**
   * Discharge energy for trick
   */
  discharge(energyCost) {
    if (this.capacitor.charge < energyCost) {
      return {
        success: false,
        error: `Insufficient energy! Need ${energyCost}, have ${this.capacitor.charge}`,
        shortage: energyCost - this.capacitor.charge
      };
    }
    
    this.capacitor.charge -= energyCost;
    this.capacitor.voltage = this.calculateVoltage(this.capacitor.charge);
    
    return {
      success: true,
      discharged: energyCost,
      remaining: this.capacitor.charge,
      voltage: this.capacitor.voltage
    };
  }
  
  /**
   * Calculate trick height based on energy
   */
  performTrick(trickType, energy) {
    const baseHeight = 1.0; // meters
    const energyFactor = energy / 10;
    
    // Calculate height with physics
    const velocity = Math.sqrt(2 * this.constants.gravity * baseHeight * energyFactor);
    const trickHeight = (velocity * velocity) / (2 * this.constants.gravity);
    
    // Apply air resistance
    const actualHeight = trickHeight * (1 - this.constants.airResistance);
    
    return {
      height: actualHeight,
      velocity: velocity,
      energy: energy,
      hangTime: Math.sqrt((2 * actualHeight) / this.constants.gravity)
    };
  }
  
  /**
   * Calculate voltage from charge
   */
  calculateVoltage(charge) {
    // V = Q/C, simplified model
    const capacitance = 1.0; // Farads
    return charge / capacitance;
  }
  
  /**
   * Check if enough energy available
   */
  hasEnergy(required) {
    return this.capacitor.charge >= required;
  }
  
  /**
   * Get current energy level
   */
  getEnergy() {
    return this.capacitor.charge;
  }
  
  /**
   * Get energy percentage
   */
  getEnergyPercent() {
    return (this.capacitor.charge / this.capacitor.maxCharge) * 100;
  }
  
  /**
   * Get capacitor status
   */
  getStatus() {
    return {
      charge: this.capacitor.charge,
      maxCharge: this.capacitor.maxCharge,
      voltage: this.capacitor.voltage,
      percentFull: this.getEnergyPercent(),
      pedalPower: this.pedalPower,
      isCharging: this.isCharging
    };
  }
  
  /**
   * Start passive energy decay
   */
  startDecayLoop() {
    setInterval(() => {
      const now = Date.now();
      const deltaTime = (now - this.lastUpdate) / 1000; // seconds
      this.lastUpdate = now;
      
      // Apply passive decay
      if (this.capacitor.charge > 0 && !this.isCharging) {
        const decay = this.capacitor.decayRate * deltaTime;
        this.capacitor.charge = Math.max(0, this.capacitor.charge - decay);
        this.capacitor.voltage = this.calculateVoltage(this.capacitor.charge);
      }
    }, 1000);
  }
  
  /**
   * Calculate momentum for tricks
   */
  calculateMomentum(mass, velocity) {
    return mass * velocity;
  }
  
  /**
   * Calculate force required for trick
   */
  calculateForce(mass, acceleration) {
    return mass * acceleration;
  }
  
  /**
   * Calculate rotational energy
   */
  calculateRotationalEnergy(momentOfInertia, angularVelocity) {
    return 0.5 * momentOfInertia * angularVelocity * angularVelocity;
  }
  
  /**
   * Simulate trick physics
   */
  simulateTrickPhysics(trickName, energy) {
    // Default bike + rider values
    const mass = 75; // kg (rider) + 10 kg (bike)
    const bikeLength = 1.8; // meters
    const momentOfInertia = mass * bikeLength * bikeLength / 12;
    
    // Get trick result
    const trick = this.performTrick(trickName, energy);
    
    // Calculate angular velocity for spins
    const rotations = trickName.includes('360') ? 1 : trickName.includes('flip') ? 1 : 0;
    const angularVelocity = rotations > 0 ? (2 * Math.PI * rotations) / trick.hangTime : 0;
    
    // Calculate forces
    const takeoffVelocity = trick.velocity;
    const takeoffAcceleration = takeoffVelocity / 0.1; // Assume 0.1s takeoff time
    const force = this.calculateForce(mass, takeoffAcceleration);
    
    return {
      ...trick,
      force: force,
      momentum: this.calculateMomentum(mass, takeoffVelocity),
      angularVelocity: angularVelocity,
      rotationalEnergy: this.calculateRotationalEnergy(momentOfInertia, angularVelocity),
      gForce: takeoffAcceleration / this.constants.gravity
    };
  }
  
  /**
   * Get physics constants
   */
  getConstants() {
    return { ...this.constants };
  }
  
  /**
   * Reset capacitor
   */
  reset() {
    this.capacitor.charge = 0;
    this.capacitor.voltage = 0;
    this.pedalPower = 0;
    this.isCharging = false;
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = BMXPhysicsEngine;
}
