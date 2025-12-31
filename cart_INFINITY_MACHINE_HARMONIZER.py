#!/usr/bin/env python3
"""
∞ Infinity Machine Harmonizer
Handles duplicate machines by creating complementary variations
Instead of culling, transforms duplicates into octave variations
"""

import json
import os
from pathlib import Path
from collections import defaultdict
import re

class InfinityMachineHarmonizer:
    """Harmonizes duplicate machines into complementary variations"""
    
    def __init__(self, catalog_file="INFINITY_FILE_CATALOG.json"):
        with open(catalog_file, 'r') as f:
            self.catalog = json.load(f)
        
        self.variations = {
            "base": ["alpha", "beta", "gamma", "delta", "epsilon"],
            "octave": ["octave1", "octave2", "octave3", "octave4", "octave5"],
            "frequency": ["low_freq", "mid_freq", "high_freq", "ultra_freq"],
            "dimension": ["3d", "4d", "5d", "quantum_d"],
            "power": ["standard", "enhanced", "turbo", "quantum"]
        }
        
        self.harmonized = {
            "machines": [],
            "variations_created": 0,
            "duplicates_harmonized": 0
        }
    
    def harmonize(self):
        """Harmonize all duplicate machines"""
        print("🎵 Starting Infinity Machine Harmonization...")
        
        # Group machines by base name
        machine_groups = self.group_machines()
        
        # Harmonize each group
        for base_name, machines in machine_groups.items():
            if len(machines) > 1:
                print(f"   Harmonizing {len(machines)} instances of '{base_name}'...")
                self.harmonize_group(base_name, machines)
        
        print(f"\n✅ Harmonization complete!")
        print(f"   • {self.harmonized['duplicates_harmonized']} duplicate groups harmonized")
        print(f"   • {self.harmonized['variations_created']} variations created")
        
        return self.harmonized
    
    def group_machines(self):
        """Group machines by base functionality"""
        groups = defaultdict(list)
        
        for machine in self.catalog['machines']:
            # Extract base name (remove numbers, version suffixes)
            base_name = re.sub(r'[0-9]+|_v\d+|_\d+$', '', machine['name'])
            base_name = base_name.replace('.py', '').replace('.sh', '')
            groups[base_name].append(machine)
        
        return groups
    
    def harmonize_group(self, base_name, machines):
        """Harmonize a group of duplicate machines"""
        
        # Sort by size (larger might be more feature-rich)
        machines_sorted = sorted(machines, key=lambda x: x['size'], reverse=True)
        
        # Assign variations
        for idx, machine in enumerate(machines_sorted):
            if idx == 0:
                # First (largest) is the base
                harmonized = {
                    "original": machine,
                    "variation": "base",
                    "purpose": "Primary implementation",
                    "active": True
                }
            else:
                # Others get octave variations
                variation_type = list(self.variations.keys())[idx % len(self.variations)]
                variation_name = self.variations[variation_type][idx % len(self.variations[variation_type])]
                
                harmonized = {
                    "original": machine,
                    "variation": variation_name,
                    "purpose": self.generate_purpose(base_name, variation_name),
                    "active": True
                }
                
                self.harmonized['variations_created'] += 1
            
            self.harmonized['machines'].append(harmonized)
        
        self.harmonized['duplicates_harmonized'] += 1
    
    def generate_purpose(self, base_name, variation):
        """Generate purpose for variation"""
        purpose_map = {
            "octave1": "Operates at first octave frequency for harmonic resonance",
            "octave2": "Operates at second octave for dimensional shift",
            "octave3": "Operates at third octave for quantum entanglement",
            "octave4": "Operates at fourth octave for consciousness interface",
            "octave5": "Operates at fifth octave for transcendence layer",
            "low_freq": "Processes low-frequency patterns",
            "mid_freq": "Processes mid-range frequency patterns",
            "high_freq": "Processes high-frequency patterns",
            "ultra_freq": "Processes ultra-high frequency quantum patterns",
            "3d": "Operates in 3-dimensional space",
            "4d": "Operates in 4-dimensional spacetime",
            "5d": "Operates in 5-dimensional quantum space",
            "quantum_d": "Operates in quantum dimensional superposition",
            "enhanced": "Enhanced version with additional features",
            "turbo": "High-performance optimized version",
            "quantum": "Quantum-enhanced implementation"
        }
        
        return purpose_map.get(variation, f"Specialized {variation} implementation of {base_name}")
    
    def save_harmony(self, output_file="INFINITY_MACHINE_HARMONY.json"):
        """Save harmonization results"""
        with open(output_file, 'w') as f:
            json.dump(self.harmonized, f, indent=2)
        
        print(f"💾 Harmony saved to {output_file}")
    
    def generate_harmony_report(self):
        """Generate human-readable harmony report"""
        report = f"""
═══════════════════════════════════════════════════════════
     ∞ INFINITY MACHINE HARMONY REPORT
═══════════════════════════════════════════════════════════
Duplicates Harmonized: {self.harmonized['duplicates_harmonized']}
Variations Created: {self.harmonized['variations_created']}
Total Machines Active: {len(self.harmonized['machines'])}

🎵 HARMONY PRINCIPLE:
Instead of culling duplicates, each instance operates at a
different frequency/octave/dimension, creating a harmonic
resonance network where all machines complement each other.

📊 HARMONIZED MACHINES:
"""
        # Group by variation type
        by_variation = defaultdict(list)
        for machine in self.harmonized['machines']:
            by_variation[machine['variation']].append(machine)
        
        for variation, machines in sorted(by_variation.items()):
            report += f"\n  {variation.upper()}:\n"
            for machine in machines[:5]:  # Show first 5 of each
                report += f"    • {machine['original']['name']}\n"
                report += f"      {machine['purpose']}\n"
            
            if len(machines) > 5:
                report += f"    ... and {len(machines) - 5} more\n"
        
        report += "\n═══════════════════════════════════════════════════════════\n"
        return report


def main():
    """Main execution"""
    print("🎵 Infinity Machine Harmonizer\n")
    
    # Check if catalog exists
    if not os.path.exists("INFINITY_FILE_CATALOG.json"):
        print("❌ Error: INFINITY_FILE_CATALOG.json not found!")
        print("   Run cart_INFINITY_FILE_SCANNER.py first.")
        return
    
    harmonizer = InfinityMachineHarmonizer()
    harmonizer.harmonize()
    harmonizer.save_harmony()
    
    # Generate and print report
    report = harmonizer.generate_harmony_report()
    print(report)
    
    # Save report
    with open("INFINITY_MACHINE_HARMONY_REPORT.txt", 'w') as f:
        f.write(report)
    
    print("✅ Complete! Check INFINITY_MACHINE_HARMONY.json and INFINITY_MACHINE_HARMONY_REPORT.txt")


if __name__ == "__main__":
    main()
