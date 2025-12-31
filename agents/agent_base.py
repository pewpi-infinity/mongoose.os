#!/usr/bin/env python3
"""
Base Agent Architecture for Mongoose.OS Multi-Agent Ecosystem

This module provides the foundation for all autonomous agents in the system.
Each agent has a specific role in the token-to-webpage-to-sale pipeline.

Philosophy: Sound reasoning and logic for operating a healthy internet ecosystem.
"""

import json
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional


class AgentBase(ABC):
    """
    Base class for all autonomous agents in the Mongoose.OS ecosystem.
    
    Every agent must:
    1. Have a clear purpose and role
    2. Report metrics about its activities
    3. Communicate with other agents via the orchestrator
    4. Maintain logs of all actions
    5. Contribute to the health of the internet ecosystem
    """
    
    def __init__(self, agent_id: str, agent_name: str, agent_role: str):
        """
        Initialize agent with identity and purpose.
        
        Args:
            agent_id: Unique identifier for this agent
            agent_name: Human-readable name
            agent_role: Description of agent's purpose in the ecosystem
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.created_at = datetime.now().isoformat()
        self.metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "pages_created": 0,
            "tokens_generated": 0,
            "last_activity": None
        }
        self.log_file = f"logs/agent_{agent_id}.log"
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        os.makedirs("logs", exist_ok=True)
    
    def log(self, message: str, level: str = "INFO"):
        """
        Log agent activity with timestamp.
        
        Args:
            message: Log message
            level: Log level (INFO, WARNING, ERROR, SUCCESS)
        """
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {self.agent_name}: {message}\n"
        
        # Write to agent-specific log
        with open(self.log_file, "a") as f:
            f.write(log_entry)
        
        # Also write to master log
        with open("logs/agent_master.log", "a") as f:
            f.write(log_entry)
        
        print(log_entry.strip())
    
    def update_metrics(self, metric: str, value: Any):
        """Update agent metrics"""
        self.metrics[metric] = value
        self.metrics["last_activity"] = datetime.now().isoformat()
    
    def increment_metric(self, metric: str, amount: int = 1):
        """Increment a numeric metric"""
        if metric in self.metrics and isinstance(self.metrics[metric], (int, float)):
            self.metrics[metric] += amount
        else:
            self.metrics[metric] = amount
        self.metrics["last_activity"] = datetime.now().isoformat()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current agent metrics"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_role": self.agent_role,
            "created_at": self.created_at,
            "metrics": self.metrics
        }
    
    def export_metrics(self, output_file: Optional[str] = None) -> str:
        """
        Export metrics to JSON file.
        
        Args:
            output_file: Optional custom output file path
            
        Returns:
            Path to exported metrics file
        """
        if output_file is None:
            output_file = f"metrics/agent_{self.agent_id}_metrics.json"
        
        os.makedirs("metrics", exist_ok=True)
        
        with open(output_file, "w") as f:
            json.dump(self.get_metrics(), f, indent=2)
        
        self.log(f"Metrics exported to {output_file}", "SUCCESS")
        return output_file
    
    @abstractmethod
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task assigned to this agent.
        
        Args:
            task: Task dictionary containing task details
            
        Returns:
            Result dictionary with task outcome
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Return list of capabilities this agent provides.
        
        Returns:
            List of capability strings
        """
        pass
    
    def create_token_page(self, token_id: str, token_data: Dict[str, Any]) -> str:
        """
        Create a webpage for a token (used by all agents).
        
        Args:
            token_id: Unique token identifier
            token_data: Token data to display
            
        Returns:
            Path to created page
        """
        page_path = f"token_{token_id}.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Token {token_id} - Mongoose.OS</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            background: #0b0b0b;
            color: #e6e6e6;
            font-family: system-ui, sans-serif;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{
            color: #00e5ff;
            margin-bottom: 20px;
        }}
        .token-info {{
            background: rgba(0, 229, 255, 0.05);
            border: 2px solid rgba(0, 229, 255, 0.3);
            border-radius: 12px;
            padding: 30px;
            margin: 20px 0;
        }}
        .buy-button {{
            background: #00e5ff;
            color: #0b0b0b;
            border: none;
            padding: 15px 40px;
            font-size: 1.2rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 20px;
        }}
        .buy-button:hover {{
            background: #00b8cc;
        }}
        pre {{
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🪙 Token {token_id}</h1>
        
        <div class="token-info">
            <h2>Token Information</h2>
            <p><strong>Token ID:</strong> {token_id}</p>
            <p><strong>Created:</strong> {token_data.get('created_at', 'N/A')}</p>
            <p><strong>Agent:</strong> {token_data.get('agent', 'N/A')}</p>
            <p><strong>Type:</strong> {token_data.get('type', 'N/A')}</p>
            
            {self._render_token_data(token_data)}
        </div>
        
        <button class="buy-button" onclick="alert('Purchase system integration coming soon!')">
            💰 Buy This Token
        </button>
        
        <p style="margin-top: 20px; opacity: 0.7;">
            <a href="/" style="color: #00e5ff;">← Back to Home</a>
        </p>
    </div>
</body>
</html>
"""
        
        with open(page_path, "w") as f:
            f.write(html_content)
        
        self.log(f"Created token page: {page_path}", "SUCCESS")
        self.increment_metric("pages_created")
        self.increment_metric("tokens_generated")
        
        return page_path
    
    def _render_token_data(self, token_data: Dict[str, Any]) -> str:
        """Render token data as HTML"""
        html = "<h3>Details</h3><pre>"
        for key, value in token_data.items():
            if key not in ['created_at', 'agent', 'type']:
                html += f"{key}: {value}\n"
        html += "</pre>"
        return html


class AgentHealth:
    """
    Monitor and report on the health of the agent ecosystem.
    
    Philosophy: A healthy internet requires transparent, accountable systems
    that can self-monitor and report their status honestly.
    """
    
    @staticmethod
    def check_system_health() -> Dict[str, Any]:
        """
        Check overall system health.
        
        Returns:
            Health report dictionary
        """
        health = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "agents_active": 0,
            "total_tasks": 0,
            "total_pages": 0,
            "total_tokens": 0,
            "issues": []
        }
        
        # Check if logs directory exists and has recent activity
        if not os.path.exists("logs"):
            health["issues"].append("Logs directory not found")
            health["status"] = "warning"
        
        # Check if metrics directory exists
        if not os.path.exists("metrics"):
            health["issues"].append("Metrics directory not found")
            health["status"] = "warning"
        
        # Aggregate metrics from all agents
        if os.path.exists("metrics"):
            for filename in os.listdir("metrics"):
                if filename.startswith("agent_") and filename.endswith("_metrics.json"):
                    try:
                        with open(os.path.join("metrics", filename)) as f:
                            metrics = json.load(f)
                            health["agents_active"] += 1
                            health["total_tasks"] += metrics["metrics"]["tasks_completed"]
                            health["total_pages"] += metrics["metrics"]["pages_created"]
                            health["total_tokens"] += metrics["metrics"]["tokens_generated"]
                    except Exception as e:
                        health["issues"].append(f"Error reading {filename}: {str(e)}")
        
        return health
    
    @staticmethod
    def generate_health_report() -> str:
        """
        Generate HTML health report.
        
        Returns:
            Path to health report HTML file
        """
        health = AgentHealth.check_system_health()
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent System Health - Mongoose.OS</title>
    <style>
        body {{
            background: #0b0b0b;
            color: #e6e6e6;
            font-family: system-ui, sans-serif;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        h1 {{
            color: #00e5ff;
        }}
        .status-card {{
            background: rgba(0, 229, 255, 0.05);
            border: 2px solid rgba(0, 229, 255, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }}
        .metric {{
            font-size: 2rem;
            font-weight: bold;
            color: #00e5ff;
        }}
        .healthy {{
            color: #00ff88;
        }}
        .warning {{
            color: #ffaa00;
        }}
        .error {{
            color: #ff4444;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Agent System Health Dashboard</h1>
        
        <div class="status-card">
            <h2>System Status: <span class="{health['status']}">{health['status'].upper()}</span></h2>
            <p>Last Updated: {health['timestamp']}</p>
        </div>
        
        <div class="status-card">
            <h2>Active Agents</h2>
            <p class="metric">{health['agents_active']}</p>
        </div>
        
        <div class="status-card">
            <h2>Total Tasks Completed</h2>
            <p class="metric">{health['total_tasks']}</p>
        </div>
        
        <div class="status-card">
            <h2>Pages Created</h2>
            <p class="metric">{health['total_pages']}</p>
        </div>
        
        <div class="status-card">
            <h2>Tokens Generated</h2>
            <p class="metric">{health['total_tokens']}</p>
        </div>
        
        {AgentHealth._render_issues(health['issues'])}
        
        <p style="margin-top: 20px;">
            <a href="/" style="color: #00e5ff;">← Back to Home</a>
        </p>
    </div>
</body>
</html>
"""
        
        report_path = "agent_health.html"
        with open(report_path, "w") as f:
            f.write(html_content)
        
        return report_path
    
    @staticmethod
    def _render_issues(issues: List[str]) -> str:
        """Render issues list as HTML"""
        if not issues:
            return ""
        
        html = '<div class="status-card"><h2>Issues</h2><ul>'
        for issue in issues:
            html += f"<li>{issue}</li>"
        html += "</ul></div>"
        return html


if __name__ == "__main__":
    # Test the base agent architecture
    print("Testing Agent Base Architecture...")
    print("=" * 60)
    
    # Check system health
    health = AgentHealth.check_system_health()
    print(json.dumps(health, indent=2))
    
    # Generate health report
    report_path = AgentHealth.generate_health_report()
    print(f"\nHealth report generated: {report_path}")
