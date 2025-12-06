const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

// In-memory storage for tokens and users (in production, use a database)
let users = {};
let tokenWallets = {};

// Login endpoint
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    
    // Simple authentication (in production, use proper password hashing)
    if (!users[username]) {
        users[username] = { password, tokens: 0 };
        tokenWallets[username] = [];
    } else if (users[username].password !== password) {
        return res.status(401).json({ success: false, message: 'Invalid credentials' });
    }
    
    // Create a simple token
    const token = Buffer.from(`${username}:${Date.now()}`).toString('base64');
    
    // Save login as server-side commit
    const commitLog = {
        timestamp: new Date().toISOString(),
        username: username,
        action: 'login',
        token: token
    };
    
    // Append to commit log file
    const logEntry = JSON.stringify(commitLog) + '\n';
    fs.appendFileSync(path.join(__dirname, 'commit-log.txt'), logEntry);
    
    res.json({ 
        success: true, 
        token: token,
        username: username,
        tokens: users[username].tokens
    });
});

// Token wallet endpoints
app.get('/api/wallet/:username', (req, res) => {
    const { username } = req.params;
    
    if (!tokenWallets[username]) {
        tokenWallets[username] = [];
    }
    
    res.json({ 
        success: true,
        tokens: tokenWallets[username],
        balance: users[username]?.tokens || 0
    });
});

app.post('/api/wallet/add', (req, res) => {
    const { username, tokenType, amount } = req.body;
    
    if (!tokenWallets[username]) {
        tokenWallets[username] = [];
    }
    
    const newToken = {
        id: Date.now(),
        type: tokenType,
        amount: amount,
        timestamp: new Date().toISOString()
    };
    
    tokenWallets[username].push(newToken);
    
    if (!users[username]) {
        users[username] = { tokens: 0 };
    }
    users[username].tokens += parseInt(amount);
    
    // Log the token addition as a commit
    const commitLog = {
        timestamp: new Date().toISOString(),
        username: username,
        action: 'add_token',
        tokenType: tokenType,
        amount: amount
    };
    
    fs.appendFileSync(path.join(__dirname, 'commit-log.txt'), JSON.stringify(commitLog) + '\n');
    
    res.json({ 
        success: true,
        wallet: tokenWallets[username],
        balance: users[username].tokens
    });
});

// Get commit log
app.get('/api/commits', (req, res) => {
    try {
        const logPath = path.join(__dirname, 'commit-log.txt');
        if (!fs.existsSync(logPath)) {
            return res.json({ success: true, commits: [] });
        }
        
        const logContent = fs.readFileSync(logPath, 'utf8');
        const commits = logContent
            .split('\n')
            .filter(line => line.trim())
            .map(line => JSON.parse(line));
        
        res.json({ success: true, commits: commits });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Serve the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
