#!/usr/bin/env python3
"""
Code Review Agent - Audits all code changes and ensures quality

This agent reviews code commits, pull requests, and file changes
to ensure quality standards and security best practices.

Philosophy: Quality code creates a healthier internet ecosystem.
"""

import os
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Any
from agents.agent_base import AgentBase


class CodeReviewAgent(AgentBase):
    """
    Autonomous agent responsible for code quality and security review.
    
    Capabilities:
    - Review code changes
    - Check for security vulnerabilities
    - Ensure coding standards
    - Generate review reports
    - Create tokens for reviewed code
    """
    
    def __init__(self):
        super().__init__(
            agent_id="code_reviewer",
            agent_name="Code Review Agent",
            agent_role="Ensures code quality and security across the ecosystem"
        )
        self.review_count = 0
        self.vulnerabilities_found = 0
    
    def get_capabilities(self) -> List[str]:
        """Return agent capabilities"""
        return [
            "review_code",
            "check_security",
            "enforce_standards",
            "generate_reports",
            "create_review_tokens"
        ]
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a code review task.
        
        Args:
            task: Dictionary with 'action' and task-specific parameters
            
        Returns:
            Result dictionary
        """
        action = task.get("action")
        
        if action == "review_file":
            return self.review_file(task.get("file_path"))
        elif action == "review_changes":
            return self.review_git_changes()
        elif action == "security_scan":
            return self.security_scan(task.get("directory", "."))
        else:
            self.log(f"Unknown action: {action}", "WARNING")
            self.increment_metric("tasks_failed")
            return {"success": False, "error": f"Unknown action: {action}"}
    
    def review_file(self, file_path: str) -> Dict[str, Any]:
        """
        Review a single file for quality and security.
        
        Args:
            file_path: Path to file to review
            
        Returns:
            Review result dictionary
        """
        self.log(f"Reviewing file: {file_path}")
        
        if not os.path.exists(file_path):
            self.log(f"File not found: {file_path}", "ERROR")
            self.increment_metric("tasks_failed")
            return {"success": False, "error": "File not found"}
        
        issues = []
        
        # Basic checks
        with open(file_path, 'r', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            
            # Check for common issues
            for i, line in enumerate(lines, 1):
                # Check for hardcoded secrets (very basic)
                if any(keyword in line.lower() for keyword in ['password', 'api_key', 'secret']):
                    if '=' in line and not line.strip().startswith('#'):
                        issues.append({
                            "line": i,
                            "type": "security",
                            "message": "Possible hardcoded secret"
                        })
                        self.vulnerabilities_found += 1
                
                # Check line length
                if len(line) > 120:
                    issues.append({
                        "line": i,
                        "type": "style",
                        "message": "Line exceeds 120 characters"
                    })
        
        # Create review report
        review_result = {
            "file": file_path,
            "timestamp": datetime.now().isoformat(),
            "issues_found": len(issues),
            "issues": issues,
            "reviewed_by": self.agent_name
        }
        
        # Create token for this review
        token_id = f"review_{int(datetime.now().timestamp())}"
        token_data = {
            "type": "code_review",
            "file": file_path,
            "issues": len(issues),
            "created_at": review_result["timestamp"],
            "agent": self.agent_name
        }
        
        page_path = self.create_token_page(token_id, token_data)
        review_result["token_page"] = page_path
        
        self.review_count += 1
        self.increment_metric("tasks_completed")
        self.log(f"Review complete: {len(issues)} issues found")
        
        return {"success": True, "result": review_result}
    
    def review_git_changes(self) -> Dict[str, Any]:
        """
        Review recent git changes.
        
        Returns:
            Review result dictionary
        """
        self.log("Reviewing git changes...")
        
        try:
            # Get list of changed files
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD~1'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                self.log("No git changes to review", "WARNING")
                return {"success": True, "result": {"files": [], "message": "No changes"}}
            
            changed_files = [f for f in result.stdout.strip().split('\n') if f]
            
            # Review each changed file
            all_issues = []
            for file_path in changed_files:
                if os.path.exists(file_path):
                    review = self.review_file(file_path)
                    if review.get("success"):
                        all_issues.extend(review["result"]["issues"])
            
            summary = {
                "files_reviewed": len(changed_files),
                "total_issues": len(all_issues),
                "timestamp": datetime.now().isoformat()
            }
            
            self.increment_metric("tasks_completed")
            return {"success": True, "result": summary}
            
        except Exception as e:
            self.log(f"Error reviewing git changes: {str(e)}", "ERROR")
            self.increment_metric("tasks_failed")
            return {"success": False, "error": str(e)}
    
    def security_scan(self, directory: str) -> Dict[str, Any]:
        """
        Perform security scan on directory.
        
        Args:
            directory: Directory to scan
            
        Returns:
            Scan result dictionary
        """
        self.log(f"Performing security scan on: {directory}")
        
        vulnerabilities = []
        
        # Scan Python files for common issues
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories and common excludes
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    review = self.review_file(file_path)
                    if review.get("success"):
                        security_issues = [
                            issue for issue in review["result"]["issues"]
                            if issue["type"] == "security"
                        ]
                        if security_issues:
                            vulnerabilities.append({
                                "file": file_path,
                                "issues": security_issues
                            })
        
        scan_result = {
            "directory": directory,
            "vulnerabilities_found": len(vulnerabilities),
            "details": vulnerabilities,
            "timestamp": datetime.now().isoformat(),
            "scanned_by": self.agent_name
        }
        
        self.increment_metric("tasks_completed")
        self.log(f"Security scan complete: {len(vulnerabilities)} vulnerabilities found")
        
        return {"success": True, "result": scan_result}
    
    def get_review_stats(self) -> Dict[str, Any]:
        """Get review statistics"""
        return {
            "reviews_completed": self.review_count,
            "vulnerabilities_found": self.vulnerabilities_found,
            **self.get_metrics()
        }


if __name__ == "__main__":
    # Test the code review agent
    agent = CodeReviewAgent()
    print(f"Agent initialized: {agent.agent_name}")
    print(f"Capabilities: {agent.get_capabilities()}")
    
    # Test review
    test_task = {"action": "security_scan", "directory": "agents"}
    result = agent.execute_task(test_task)
    print(json.dumps(result, indent=2))
    
    # Export metrics
    agent.export_metrics()
