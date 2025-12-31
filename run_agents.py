#!/usr/bin/env python3
"""
Master Runner - Executes the multi-agent ecosystem

This script initializes all agents and demonstrates the
token-to-webpage-to-sale pipeline in action.

Philosophy: Orchestration brings order from complexity.
"""

import sys
import os

# Add agents directory to path
sys.path.insert(0, os.path.dirname(__file__))

from agents.agent_base import AgentHealth
from agents.agent_code_review import CodeReviewAgent
from agents.agent_orchestrator import OrchestratorAgent
from agents.agent_token_manager import TokenManagerAgent


def main():
    """Run the multi-agent system"""
    print("=" * 60)
    print("🤖 MONGOOSE.OS MULTI-AGENT ECOSYSTEM")
    print("=" * 60)
    print()
    
    # Initialize agents
    print("Initializing agents...")
    orchestrator = OrchestratorAgent()
    code_reviewer = CodeReviewAgent()
    token_manager = TokenManagerAgent()
    
    # Register agents with orchestrator
    print("\nRegistering agents with orchestrator...")
    orchestrator.execute_task({
        "action": "register_agent",
        "agent_info": {
            "agent_id": code_reviewer.agent_id,
            "agent_name": code_reviewer.agent_name,
            "agent_role": code_reviewer.agent_role,
            "capabilities": code_reviewer.get_capabilities()
        }
    })
    
    orchestrator.execute_task({
        "action": "register_agent",
        "agent_info": {
            "agent_id": token_manager.agent_id,
            "agent_name": token_manager.agent_name,
            "agent_role": token_manager.agent_role,
            "capabilities": token_manager.get_capabilities()
        }
    })
    
    # Demonstrate token creation
    print("\n" + "=" * 60)
    print("🪙 DEMONSTRATING TOKEN-TO-WEBPAGE-TO-SALE PIPELINE")
    print("=" * 60)
    print()
    
    # Create a token for a git push action
    print("Creating token for 'push' action...")
    push_result = token_manager.execute_task({
        "action": "create_token",
        "action_data": {
            "type": "push",
            "data": {
                "files_changed": 4,
                "commit_message": "Add multi-agent system",
                "branch": "main"
            }
        }
    })
    
    if push_result.get("success"):
        token = push_result["token"]
        print(f"✅ Token created: {token['token_id']}")
        print(f"   Webpage: {token['webpage']}")
        print(f"   Sales Page: {token['sales_page']}")
        print(f"   Price: ${token['price_usd']:.2f}")
    
    # Perform code review
    print("\n" + "=" * 60)
    print("👁️  PERFORMING CODE REVIEW")
    print("=" * 60)
    print()
    
    review_result = code_reviewer.execute_task({
        "action": "security_scan",
        "directory": "agents"
    })
    
    if review_result.get("success"):
        result = review_result["result"]
        print(f"✅ Security scan complete")
        print(f"   Vulnerabilities: {result['vulnerabilities_found']}")
    
    # Generate system report
    print("\n" + "=" * 60)
    print("📊 GENERATING SYSTEM REPORT")
    print("=" * 60)
    print()
    
    report_result = orchestrator.execute_task({"action": "generate_report"})
    if report_result.get("success"):
        print(f"✅ System report generated: {report_result['html_report']}")
    
    # Generate health report
    print("\n" + "=" * 60)
    print("🏥 SYSTEM HEALTH CHECK")
    print("=" * 60)
    print()
    
    health_report = AgentHealth.generate_health_report()
    print(f"✅ Health report generated: {health_report}")
    
    # Export all metrics
    print("\n" + "=" * 60)
    print("📈 EXPORTING METRICS")
    print("=" * 60)
    print()
    
    orchestrator.export_metrics()
    code_reviewer.export_metrics()
    token_manager.export_metrics()
    
    print("\n✅ All metrics exported to metrics/ directory")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 EXECUTION SUMMARY")
    print("=" * 60)
    print()
    print(f"Agents Active: 3")
    print(f"Tasks Completed: {orchestrator.metrics['tasks_completed'] + code_reviewer.metrics['tasks_completed'] + token_manager.metrics['tasks_completed']}")
    print(f"Tokens Generated: {token_manager.metrics['tokens_generated']}")
    print(f"Pages Created: {token_manager.metrics['pages_created']}")
    print()
    print("🌐 Visit generated pages:")
    print("   - agent_health.html - Agent health dashboard")
    print("   - system_report.html - Complete system report")
    print("   - Sale pages and token pages in root directory")
    print()
    print("=" * 60)
    print("✨ MULTI-AGENT ECOSYSTEM OPERATIONAL")
    print("=" * 60)


if __name__ == "__main__":
    main()
