#!/usr/bin/env python3
"""
Orchestrator Agent - Coordinates all agents and manages workflow

This agent is the conductor of the multi-agent symphony, ensuring
all agents work together harmoniously toward common goals.

Philosophy: Coordination creates synergy; synergy creates value.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from agents.agent_base import AgentBase, AgentHealth


class OrchestratorAgent(AgentBase):
    """
    Central coordinator for the multi-agent ecosystem.
    
    Capabilities:
    - Register and manage agents
    - Assign tasks to appropriate agents
    - Monitor agent health and performance
    - Coordinate complex workflows
    - Generate system-wide reports
    """
    
    def __init__(self):
        super().__init__(
            agent_id="orchestrator",
            agent_name="Orchestrator Agent",
            agent_role="Coordinates all agents and manages system-wide workflows"
        )
        self.registered_agents = {}
        self.task_queue = []
        self.completed_tasks = []
    
    def get_capabilities(self) -> List[str]:
        """Return agent capabilities"""
        return [
            "register_agent",
            "assign_task",
            "monitor_agents",
            "coordinate_workflow",
            "generate_reports"
        ]
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an orchestration task.
        
        Args:
            task: Dictionary with 'action' and task-specific parameters
            
        Returns:
            Result dictionary
        """
        action = task.get("action")
        
        if action == "register_agent":
            return self.register_agent(task.get("agent_info"))
        elif action == "assign_task":
            return self.assign_task(task.get("task_data"))
        elif action == "health_check":
            return self.check_all_agents()
        elif action == "generate_report":
            return self.generate_system_report()
        else:
            self.log(f"Unknown action: {action}", "WARNING")
            self.increment_metric("tasks_failed")
            return {"success": False, "error": f"Unknown action: {action}"}
    
    def register_agent(self, agent_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new agent with the orchestrator.
        
        Args:
            agent_info: Agent information dictionary
            
        Returns:
            Registration result
        """
        agent_id = agent_info.get("agent_id")
        
        if not agent_id:
            self.log("Agent registration failed: missing agent_id", "ERROR")
            return {"success": False, "error": "Missing agent_id"}
        
        self.registered_agents[agent_id] = {
            **agent_info,
            "registered_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.log(f"Agent registered: {agent_info.get('agent_name', agent_id)}", "SUCCESS")
        self.increment_metric("tasks_completed")
        
        return {"success": True, "agent_id": agent_id}
    
    def assign_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assign a task to the most appropriate agent.
        
        Args:
            task_data: Task information
            
        Returns:
            Assignment result
        """
        task_type = task_data.get("type")
        
        # Simple routing logic based on task type
        agent_routing = {
            "code_review": "code_reviewer",
            "build": "builder",
            "research": "researcher",
            "sales_page": "sales_generator",
            "token_management": "token_manager"
        }
        
        target_agent = agent_routing.get(task_type)
        
        if not target_agent or target_agent not in self.registered_agents:
            self.log(f"No agent available for task type: {task_type}", "WARNING")
            self.task_queue.append(task_data)
            return {"success": False, "error": "No suitable agent found", "queued": True}
        
        # In a real implementation, this would actually send the task to the agent
        # For now, we just log and track it
        task_id = f"task_{int(datetime.now().timestamp())}"
        task_record = {
            "task_id": task_id,
            "assigned_to": target_agent,
            "task_data": task_data,
            "assigned_at": datetime.now().isoformat(),
            "status": "assigned"
        }
        
        self.completed_tasks.append(task_record)
        self.log(f"Task {task_id} assigned to {target_agent}", "SUCCESS")
        self.increment_metric("tasks_completed")
        
        return {"success": True, "task_id": task_id, "assigned_to": target_agent}
    
    def check_all_agents(self) -> Dict[str, Any]:
        """
        Check health of all registered agents.
        
        Returns:
            Health check results
        """
        self.log("Performing system-wide health check...")
        
        system_health = AgentHealth.check_system_health()
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "system_health": system_health,
            "registered_agents": len(self.registered_agents),
            "agents": list(self.registered_agents.keys()),
            "task_queue_length": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks)
        }
        
        self.increment_metric("tasks_completed")
        self.log(f"Health check complete: {len(self.registered_agents)} agents active")
        
        return {"success": True, "result": results}
    
    def generate_system_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive system report.
        
        Returns:
            Report generation result
        """
        self.log("Generating system report...")
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "orchestrator_metrics": self.get_metrics(),
            "registered_agents": self.registered_agents,
            "task_statistics": {
                "queued": len(self.task_queue),
                "completed": len(self.completed_tasks)
            },
            "system_health": AgentHealth.check_system_health()
        }
        
        # Save report
        report_file = f"metrics/system_report_{int(datetime.now().timestamp())}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        # Generate HTML report
        html_report = self._generate_html_report(report)
        
        self.increment_metric("tasks_completed")
        self.log(f"System report generated: {report_file}")
        
        return {
            "success": True,
            "report_file": report_file,
            "html_report": html_report
        }
    
    def _generate_html_report(self, report: Dict[str, Any]) -> str:
        """Generate HTML version of system report"""
        html_path = "system_report.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Report - Mongoose.OS</title>
    <style>
        body {{
            background: #0b0b0b;
            color: #e6e6e6;
            font-family: system-ui, sans-serif;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #00e5ff;
        }}
        .report-card {{
            background: rgba(0, 229, 255, 0.05);
            border: 2px solid rgba(0, 229, 255, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }}
        .agent-list {{
            list-style: none;
            padding: 0;
        }}
        .agent-item {{
            padding: 10px;
            margin: 5px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Multi-Agent System Report</h1>
        
        <div class="report-card">
            <h2>System Overview</h2>
            <p><strong>Generated:</strong> {report['generated_at']}</p>
            <p><strong>Active Agents:</strong> {len(report['registered_agents'])}</p>
            <p><strong>Tasks Queued:</strong> {report['task_statistics']['queued']}</p>
            <p><strong>Tasks Completed:</strong> {report['task_statistics']['completed']}</p>
        </div>
        
        <div class="report-card">
            <h2>Registered Agents</h2>
            <ul class="agent-list">
                {self._render_agent_list(report['registered_agents'])}
            </ul>
        </div>
        
        <div class="report-card">
            <h2>System Health</h2>
            <p><strong>Status:</strong> {report['system_health']['status'].upper()}</p>
            <p><strong>Total Pages:</strong> {report['system_health']['total_pages']}</p>
            <p><strong>Total Tokens:</strong> {report['system_health']['total_tokens']}</p>
        </div>
        
        <p style="margin-top: 20px;">
            <a href="/" style="color: #00e5ff;">← Back to Home</a>
        </p>
    </div>
</body>
</html>
"""
        
        with open(html_path, "w") as f:
            f.write(html_content)
        
        return html_path
    
    def _render_agent_list(self, agents: Dict[str, Any]) -> str:
        """Render agent list as HTML"""
        html = ""
        for agent_id, info in agents.items():
            html += f'<li class="agent-item">'
            html += f'<strong>{info.get("agent_name", agent_id)}</strong><br>'
            html += f'{info.get("agent_role", "No role defined")}<br>'
            html += f'<small>Status: {info.get("status", "unknown")}</small>'
            html += '</li>'
        return html


if __name__ == "__main__":
    # Test the orchestrator
    agent = OrchestratorAgent()
    print(f"Agent initialized: {agent.agent_name}")
    print(f"Capabilities: {agent.get_capabilities()}")
    
    # Test agent registration
    test_agent = {
        "agent_id": "test_agent",
        "agent_name": "Test Agent",
        "agent_role": "Testing purposes"
    }
    result = agent.execute_task({"action": "register_agent", "agent_info": test_agent})
    print(json.dumps(result, indent=2))
    
    # Generate report
    report_result = agent.execute_task({"action": "generate_report"})
    print(json.dumps(report_result, indent=2))
    
    # Export metrics
    agent.export_metrics()
