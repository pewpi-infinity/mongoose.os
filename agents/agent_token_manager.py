#!/usr/bin/env python3
"""
Token Manager Agent - Manages token generation and sales pages

This agent ensures every action in the repository creates:
1. A unique token
2. A dedicated webpage for that token  
3. A sales interface with buy button
4. Integration with pricing system

Philosophy: Every action has value; every value deserves a market.
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Any
from agents.agent_base import AgentBase


class TokenManagerAgent(AgentBase):
    """
    Manages token lifecycle from creation to sale.
    
    Capabilities:
    - Generate unique tokens for actions
    - Create token webpages
    - Build sales interfaces
    - Track token ownership
    - Generate pricing data
    """
    
    def __init__(self):
        super().__init__(
            agent_id="token_manager",
            agent_name="Token Manager Agent",
            agent_role="Manages token-to-webpage-to-sale pipeline"
        )
        self.tokens_db_file = "tokens_database.json"
        self.load_tokens_db()
    
    def load_tokens_db(self):
        """Load existing tokens database"""
        if os.path.exists(self.tokens_db_file):
            with open(self.tokens_db_file, 'r') as f:
                self.tokens_db = json.load(f)
        else:
            self.tokens_db = {"tokens": [], "total_value": 0}
    
    def save_tokens_db(self):
        """Save tokens database"""
        with open(self.tokens_db_file, 'w') as f:
            json.dump(self.tokens_db, f, indent=2)
    
    def get_capabilities(self) -> List[str]:
        """Return agent capabilities"""
        return [
            "create_token",
            "create_sales_page",
            "track_token",
            "generate_pricing",
            "list_tokens"
        ]
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a token management task"""
        action = task.get("action")
        
        if action == "create_token":
            return self.create_token_for_action(task.get("action_data"))
        elif action == "create_sales_page":
            return self.create_sales_page(task.get("token_id"))
        elif action == "list_tokens":
            return self.list_all_tokens()
        else:
            self.log(f"Unknown action: {action}", "WARNING")
            self.increment_metric("tasks_failed")
            return {"success": False, "error": f"Unknown action: {action}"}
    
    def create_token_for_action(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a token for any repository action.
        
        Args:
            action_data: Dictionary with action details (type, data, etc.)
            
        Returns:
            Token creation result
        """
        action_type = action_data.get("type", "unknown")
        self.log(f"Creating token for action: {action_type}")
        
        # Generate unique token ID
        token_data_str = json.dumps(action_data, sort_keys=True)
        token_hash = hashlib.sha256(token_data_str.encode()).hexdigest()[:16]
        token_id = f"TOKEN_{action_type.upper()}_{token_hash}"
        
        # Create token record
        token_record = {
            "token_id": token_id,
            "action_type": action_type,
            "created_at": datetime.now().isoformat(),
            "action_data": action_data,
            "price_usd": self._calculate_price(action_type),
            "status": "active"
        }
        
        # Create token webpage
        page_path = self.create_token_page(token_id, token_record)
        token_record["webpage"] = page_path
        
        # Create sales page
        sales_page = self._create_sales_page(token_record)
        token_record["sales_page"] = sales_page
        
        # Add to database
        self.tokens_db["tokens"].append(token_record)
        self.tokens_db["total_value"] += token_record["price_usd"]
        self.save_tokens_db()
        
        self.increment_metric("tasks_completed")
        self.increment_metric("tokens_generated")
        self.log(f"Token created: {token_id}", "SUCCESS")
        
        return {"success": True, "token": token_record}
    
    def _calculate_price(self, action_type: str) -> float:
        """Calculate price for an action type"""
        base_prices = {
            "push": 0.01,
            "import": 0.05,
            "extract": 0.03,
            "thread": 0.02,
            "license": 0.10,
            "research": 0.08,
            "build": 0.15,
            "unknown": 0.01
        }
        return base_prices.get(action_type, 0.01)
    
    def _create_sales_page(self, token_record: Dict[str, Any]) -> str:
        """Create a sales page for a token"""
        token_id = token_record["token_id"]
        sales_page_path = f"sale_{token_id}.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buy {token_id} - Mongoose.OS Marketplace</title>
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
            max-width: 900px;
            margin: 0 auto;
        }}
        h1 {{
            color: #00e5ff;
            margin-bottom: 10px;
        }}
        .price-tag {{
            font-size: 3rem;
            color: #00ff88;
            font-weight: bold;
            margin: 20px 0;
        }}
        .product-info {{
            background: rgba(0, 229, 255, 0.05);
            border: 2px solid rgba(0, 229, 255, 0.3);
            border-radius: 12px;
            padding: 30px;
            margin: 20px 0;
        }}
        .buy-section {{
            background: rgba(0, 255, 136, 0.1);
            border: 2px solid #00ff88;
            border-radius: 12px;
            padding: 30px;
            margin: 30px 0;
            text-align: center;
        }}
        .buy-button {{
            background: linear-gradient(135deg, #00e5ff, #00ff88);
            color: #0b0b0b;
            border: none;
            padding: 20px 60px;
            font-size: 1.5rem;
            border-radius: 12px;
            cursor: pointer;
            font-weight: bold;
            margin: 20px 0;
            transition: transform 0.2s;
        }}
        .buy-button:hover {{
            transform: scale(1.05);
        }}
        .features {{
            list-style: none;
            padding: 0;
        }}
        .features li {{
            padding: 10px 0;
            border-bottom: 1px solid rgba(0, 229, 255, 0.2);
        }}
        .features li:before {{
            content: "✓ ";
            color: #00ff88;
            font-weight: bold;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛒 Purchase Token</h1>
        
        <div class="price-tag">
            ${token_record["price_usd"]:.2f} USD
        </div>
        
        <div class="product-info">
            <h2>Token Details</h2>
            <p><strong>Token ID:</strong> {token_id}</p>
            <p><strong>Action Type:</strong> {token_record["action_type"]}</p>
            <p><strong>Created:</strong> {token_record["created_at"]}</p>
            <p><strong>Status:</strong> <span style="color: #00ff88;">● {token_record["status"]}</span></p>
            
            <h3 style="margin-top: 20px;">What You Get:</h3>
            <ul class="features">
                <li>Unique token ownership certificate</li>
                <li>Permanent access to token webpage</li>
                <li>Contribution to internet ecosystem health</li>
                <li>Support for autonomous agent development</li>
                <li>Transaction recorded on blockchain</li>
            </ul>
        </div>
        
        <div class="buy-section">
            <h2>Ready to Purchase?</h2>
            <p style="margin: 15px 0;">Secure payment via crypto or traditional methods</p>
            
            <button class="buy-button" onclick="initiateurchase()">
                💎 Buy Now for ${token_record["price_usd"]:.2f}
            </button>
            
            <p style="margin-top: 20px; opacity: 0.7; font-size: 0.9rem;">
                Contact: marvaseater@gmail.com • 808-342-9975<br>
                All purchases support the Mongoose.OS ecosystem
            </p>
        </div>
        
        <p style="margin-top: 20px;">
            <a href="/{token_record['webpage']}" style="color: #00e5ff;">View Token Page</a> |
            <a href="/" style="color: #00e5ff;">Back to Home</a>
        </p>
    </div>
    
    <script>
        function initiatePurchase() {{
            alert('Purchase system integration in progress!\\n\\nContact: marvaseater@gmail.com\\nPhone: 808-342-9975\\n\\nToken: {token_id}\\nPrice: ${token_record["price_usd"]:.2f} USD');
        }}
    </script>
</body>
</html>
"""
        
        with open(sales_page_path, "w") as f:
            f.write(html_content)
        
        self.log(f"Sales page created: {sales_page_path}")
        self.increment_metric("pages_created")
        
        return sales_page_path
    
    def list_all_tokens(self) -> Dict[str, Any]:
        """List all tokens in the system"""
        self.log(f"Listing all tokens: {len(self.tokens_db['tokens'])} total")
        self.increment_metric("tasks_completed")
        
        return {
            "success": True,
            "total_tokens": len(self.tokens_db["tokens"]),
            "total_value": self.tokens_db["total_value"],
            "tokens": self.tokens_db["tokens"]
        }
    
    def create_sales_page(self, token_id: str) -> Dict[str, Any]:
        """Create sales page for existing token"""
        # Find token in database
        token = next((t for t in self.tokens_db["tokens"] if t["token_id"] == token_id), None)
        
        if not token:
            self.log(f"Token not found: {token_id}", "ERROR")
            return {"success": False, "error": "Token not found"}
        
        sales_page = self._create_sales_page(token)
        
        self.increment_metric("tasks_completed")
        return {"success": True, "sales_page": sales_page}


if __name__ == "__main__":
    # Test the token manager
    agent = TokenManagerAgent()
    print(f"Agent initialized: {agent.agent_name}")
    print(f"Capabilities: {agent.get_capabilities()}")
    
    # Create a test token
    test_action = {
        "type": "push",
        "data": {
            "files_changed": 5,
            "commit_message": "Test commit"
        }
    }
    
    result = agent.execute_task({
        "action": "create_token",
        "action_data": test_action
    })
    
    print(json.dumps(result, indent=2))
    
    # Export metrics
    agent.export_metrics()
