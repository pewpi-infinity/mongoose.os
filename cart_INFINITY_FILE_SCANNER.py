#!/usr/bin/env python3
"""
∞ Infinity File Scanner
Scans all files in mongoose.os and catalogs them by type
Organizes token files, index files, txt files, and all other files of interest
"""

import os
import json
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class InfinityFileScanner:
    """Scans and catalogs all files in the repository"""
    
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.catalog = {
            "scan_time": datetime.now().isoformat(),
            "total_files": 0,
            "by_type": defaultdict(list),
            "by_category": {
                "tokens": [],
                "indexes": [],
                "texts": [],
                "configs": [],
                "scripts": [],
                "html": [],
                "json": [],
                "other": []
            },
            "duplicates": defaultdict(list),
            "machines": []
        }
    
    def scan(self):
        """Scan all files in repository"""
        print("🔍 Starting Infinity File Scan...")
        
        # Ignore directories
        ignore_dirs = {'.git', '__pycache__', 'node_modules', '.infinity'}
        
        for root, dirs, files in os.walk(self.root_dir):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                filepath = Path(root) / file
                self.catalog_file(filepath)
        
        # Find duplicates
        self.find_duplicates()
        
        # Identify machines
        self.identify_machines()
        
        print(f"✅ Scan complete: {self.catalog['total_files']} files cataloged")
        return self.catalog
    
    def catalog_file(self, filepath):
        """Catalog a single file"""
        try:
            relative_path = filepath.relative_to(self.root_dir)
            file_info = {
                "path": str(relative_path),
                "name": filepath.name,
                "size": filepath.stat().st_size,
                "extension": filepath.suffix,
                "modified": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
            }
            
            # Categorize by extension
            ext = filepath.suffix.lower()
            self.catalog['by_type'][ext].append(file_info)
            
            # Categorize by purpose
            filename_lower = filepath.name.lower()
            
            if 'token' in filename_lower or 'inf' in filename_lower:
                self.catalog['by_category']['tokens'].append(file_info)
            
            if 'index' in filename_lower:
                self.catalog['by_category']['indexes'].append(file_info)
            
            if ext in ['.txt', '.md']:
                self.catalog['by_category']['texts'].append(file_info)
            
            if ext in ['.json', '.yaml', '.yml', '.toml']:
                self.catalog['by_category']['configs'].append(file_info)
            
            if ext in ['.py', '.sh', '.js']:
                self.catalog['by_category']['scripts'].append(file_info)
            
            if ext in ['.html', '.htm']:
                self.catalog['by_category']['html'].append(file_info)
            
            if ext == '.json':
                self.catalog['by_category']['json'].append(file_info)
            
            self.catalog['total_files'] += 1
            
        except Exception as e:
            print(f"⚠️  Error cataloging {filepath}: {e}")
    
    def find_duplicates(self):
        """Find duplicate files by content hash"""
        print("🔍 Finding duplicates...")
        hashes = defaultdict(list)
        
        for ext, files in self.catalog['by_type'].items():
            for file_info in files:
                try:
                    filepath = self.root_dir / file_info['path']
                    if filepath.stat().st_size < 10 * 1024 * 1024:  # Only hash files < 10MB
                        with open(filepath, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                            hashes[file_hash].append(file_info['path'])
                except Exception:
                    pass
        
        # Store duplicates
        for hash_val, paths in hashes.items():
            if len(paths) > 1:
                self.catalog['duplicates'][hash_val] = paths
        
        print(f"   Found {len(self.catalog['duplicates'])} sets of duplicates")
    
    def identify_machines(self):
        """Identify machine scripts (cart files and other machines)"""
        print("🤖 Identifying machines...")
        
        machines = []
        for file_info in self.catalog['by_category']['scripts']:
            filename = file_info['name']
            
            # Cart files are machines
            if filename.startswith('cart') and filename.endswith('.py'):
                machines.append({
                    "name": filename,
                    "path": file_info['path'],
                    "type": "cart_machine",
                    "size": file_info['size']
                })
            
            # Shell scripts that run things
            elif filename.endswith('.sh') and any(word in filename.lower() for word in ['infinity', 'run', 'start', 'engine']):
                machines.append({
                    "name": filename,
                    "path": file_info['path'],
                    "type": "shell_machine",
                    "size": file_info['size']
                })
        
        self.catalog['machines'] = machines
        print(f"   Found {len(machines)} machine scripts")
    
    def save_catalog(self, output_file="INFINITY_FILE_CATALOG.json"):
        """Save catalog to JSON file"""
        # Convert defaultdicts to regular dicts for JSON serialization
        catalog_copy = dict(self.catalog)
        catalog_copy['by_type'] = dict(catalog_copy['by_type'])
        catalog_copy['duplicates'] = dict(catalog_copy['duplicates'])
        
        with open(output_file, 'w') as f:
            json.dump(catalog_copy, f, indent=2)
        
        print(f"💾 Catalog saved to {output_file}")
    
    def generate_summary(self):
        """Generate human-readable summary"""
        summary = f"""
═══════════════════════════════════════════════════════════
         ∞ INFINITY FILE CATALOG SUMMARY
═══════════════════════════════════════════════════════════
Scan Time: {self.catalog['scan_time']}
Total Files: {self.catalog['total_files']:,}

📊 BY CATEGORY:
  • Tokens:  {len(self.catalog['by_category']['tokens']):,}
  • Indexes: {len(self.catalog['by_category']['indexes']):,}
  • Texts:   {len(self.catalog['by_category']['texts']):,}
  • Configs: {len(self.catalog['by_category']['configs']):,}
  • Scripts: {len(self.catalog['by_category']['scripts']):,}
  • HTML:    {len(self.catalog['by_category']['html']):,}
  • JSON:    {len(self.catalog['by_category']['json']):,}

🔧 MACHINES FOUND: {len(self.catalog['machines'])}
  
📁 TOP FILE TYPES:
"""
        # Sort by count
        sorted_types = sorted(self.catalog['by_type'].items(), 
                            key=lambda x: len(x[1]), reverse=True)[:10]
        
        for ext, files in sorted_types:
            summary += f"  {ext or '(no ext)':15s} : {len(files):>6,} files\n"
        
        summary += f"\n🔄 DUPLICATE SETS: {len(self.catalog['duplicates'])}\n"
        summary += "═══════════════════════════════════════════════════════════\n"
        
        return summary


def main():
    """Main execution"""
    scanner = InfinityFileScanner()
    scanner.scan()
    scanner.save_catalog()
    
    # Generate and print summary
    summary = scanner.generate_summary()
    print(summary)
    
    # Save summary to file
    with open("INFINITY_FILE_CATALOG_SUMMARY.txt", 'w') as f:
        f.write(summary)
    
    print("✅ Complete! Check INFINITY_FILE_CATALOG.json and INFINITY_FILE_CATALOG_SUMMARY.txt")


if __name__ == "__main__":
    main()
