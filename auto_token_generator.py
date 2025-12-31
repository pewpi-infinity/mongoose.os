#!/usr/bin/env python3
"""
Auto Token Generator - Creates tokens for repository actions

This script monitors repository activity and automatically
creates tokens and sales pages for various actions.

Usage: python3 auto_token_generator.py [action_type]
"""

import sys
import os
import json
import subprocess
from datetime import datetime

# Add agents directory to path
sys.path.insert(0, os.path.dirname(__file__))

from agents.agent_token_manager import TokenManagerAgent


def get_git_info():
    """Get current git repository information"""
    try:
        # Get last commit info
        commit_hash = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        ).stdout.strip()
        
        commit_msg = subprocess.run(
            ['git', 'log', '-1', '--pretty=%B'],
            capture_output=True,
            text=True,
            timeout=5
        ).stdout.strip()
        
        branch = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        ).stdout.strip()
        
        # Get files changed in last commit
        files_changed = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        ).stdout.strip().split('\n')
        
        return {
            "commit_hash": commit_hash,
            "commit_message": commit_msg,
            "branch": branch,
            "files_changed": len([f for f in files_changed if f]),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Warning: Could not get git info: {e}")
        return {
            "timestamp": datetime.now().isoformat()
        }


def create_token_for_push():
    """Create token for git push action"""
    print("🚀 Creating token for GIT PUSH action...")
    
    agent = TokenManagerAgent()
    git_info = get_git_info()
    
    result = agent.execute_task({
        "action": "create_token",
        "action_data": {
            "type": "push",
            "data": git_info
        }
    })
    
    if result.get("success"):
        token = result["token"]
        print(f"\n✅ Token created successfully!")
        print(f"   Token ID: {token['token_id']}")
        print(f"   Price: ${token['price_usd']:.2f}")
        print(f"   Token Page: {token['webpage']}")
        print(f"   Sales Page: {token['sales_page']}")
        
        # Export metrics
        agent.export_metrics()
        
        return token
    else:
        print(f"❌ Failed to create token: {result.get('error')}")
        return None


def create_token_for_import(module_name):
    """Create token for import action"""
    print(f"📥 Creating token for IMPORT action: {module_name}")
    
    agent = TokenManagerAgent()
    
    result = agent.execute_task({
        "action": "create_token",
        "action_data": {
            "type": "import",
            "data": {
                "module": module_name,
                "timestamp": datetime.now().isoformat()
            }
        }
    })
    
    if result.get("success"):
        token = result["token"]
        print(f"\n✅ Token created successfully!")
        print(f"   Token ID: {token['token_id']}")
        print(f"   Price: ${token['price_usd']:.2f}")
        print(f"   Token Page: {token['webpage']}")
        print(f"   Sales Page: {token['sales_page']}")
        
        agent.export_metrics()
        return token
    else:
        print(f"❌ Failed to create token: {result.get('error')}")
        return None


def create_token_for_research(topic):
    """Create token for research action"""
    print(f"🔬 Creating token for RESEARCH action: {topic}")
    
    agent = TokenManagerAgent()
    
    result = agent.execute_task({
        "action": "create_token",
        "action_data": {
            "type": "research",
            "data": {
                "topic": topic,
                "timestamp": datetime.now().isoformat()
            }
        }
    })
    
    if result.get("success"):
        token = result["token"]
        print(f"\n✅ Token created successfully!")
        print(f"   Token ID: {token['token_id']}")
        print(f"   Price: ${token['price_usd']:.2f}")
        print(f"   Token Page: {token['webpage']}")
        print(f"   Sales Page: {token['sales_page']}")
        
        agent.export_metrics()
        return token
    else:
        print(f"❌ Failed to create token: {result.get('error')}")
        return None


def create_token_for_license(license_type):
    """Create token for license action"""
    print(f"📜 Creating token for LICENSE action: {license_type}")
    
    agent = TokenManagerAgent()
    
    result = agent.execute_task({
        "action": "create_token",
        "action_data": {
            "type": "license",
            "data": {
                "license_type": license_type,
                "timestamp": datetime.now().isoformat()
            }
        }
    })
    
    if result.get("success"):
        token = result["token"]
        print(f"\n✅ Token created successfully!")
        print(f"   Token ID: {token['token_id']}")
        print(f"   Price: ${token['price_usd']:.2f}")
        print(f"   Token Page: {token['webpage']}")
        print(f"   Sales Page: {token['sales_page']}")
        
        agent.export_metrics()
        return token
    else:
        print(f"❌ Failed to create token: {result.get('error')}")
        return None


def main():
    """Main function"""
    print("=" * 60)
    print("🪙 AUTO TOKEN GENERATOR")
    print("=" * 60)
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python3 auto_token_generator.py <action> [args]")
        print()
        print("Available actions:")
        print("  push           - Create token for git push")
        print("  import <name>  - Create token for import action")
        print("  research <topic> - Create token for research")
        print("  license <type> - Create token for license")
        print()
        print("Example: python3 auto_token_generator.py push")
        return
    
    action = sys.argv[1].lower()
    
    if action == "push":
        create_token_for_push()
    elif action == "import" and len(sys.argv) > 2:
        create_token_for_import(sys.argv[2])
    elif action == "research" and len(sys.argv) > 2:
        create_token_for_research(sys.argv[2])
    elif action == "license" and len(sys.argv) > 2:
        create_token_for_license(sys.argv[2])
    else:
        print(f"❌ Unknown action or missing arguments: {action}")
        print("Run without arguments for usage info")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
