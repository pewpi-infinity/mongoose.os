# Mongoose.OS - Login & Token Wallet

A web application for Trick bike Freestyle BMX scripting with login functionality, token wallet management, and server-side commit logging.

## Features

### 1. **Login Page**
- User authentication with username and password
- Automatic user registration on first login
- Login events saved as server-side commits
- Session token generation

### 2. **Token Wallet**
- View total token balance
- Add tokens of different types:
  - Trick Token
  - Freestyle Token
  - BMX Token
  - Reward Token
- Track all tokens with timestamps
- Visual token display with color-coded types

### 3. **Colored Project Links**
- 8 colorful navigation links for co-pilot project integration:
  - **FREESTYLE** - Freestyle BMX Project
  - **BMX** - BMX Core System
  - **TRICKS** - Tricks Library
  - **MONGOOSE** - Mongoose OS
  - **SCRIPTING** - Scripting Engine
  - **COPILOT** - CoPilot Integration
  - **INTEGRATION** - Project Integration Hub
  - **PROJECTS** - All Projects Dashboard
- Each word link has a unique gradient color scheme
- Interactive hover effects
- Links prepared for integration with other co-pilot repositories

### 4. **Server-Side Commit Log**
- All user actions (login, token additions) are logged server-side
- Commit log stored in `commit-log.txt`
- Real-time commit history display
- Includes:
  - Username
  - Action type
  - Timestamp
  - Additional metadata (token type, amount, etc.)

## Installation

```bash
# Install dependencies
npm install

# Start the server
npm start
```

The server will run on `http://localhost:3000` by default.

## Usage

1. **Login**: Enter any username and password. First-time users are automatically registered.
2. **Add Tokens**: Select token type and amount, then click "Add Tokens"
3. **View Wallet**: See your token balance and all tokens you've collected
4. **Explore Links**: Click on the colored project links to see project information
5. **Check Commits**: View the server-side commit log to see all actions

## API Endpoints

### POST `/api/login`
Login or register a user
```json
{
  "username": "string",
  "password": "string"
}
```

### GET `/api/wallet/:username`
Get user's token wallet

### POST `/api/wallet/add`
Add tokens to wallet
```json
{
  "username": "string",
  "tokenType": "string",
  "amount": "number"
}
```

### GET `/api/commits`
Get all server-side commits

## Technologies

- **Backend**: Node.js, Express
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS with gradient backgrounds and animations
- **Storage**: In-memory storage with file-based commit logging

## Project Integration

The colored word links are designed to facilitate integration with other co-pilot repository projects. Each link can be configured to point to related repositories or project sections for seamless collaboration across multiple BMX-related projects.

## Future Enhancements

- Persistent database storage
- Secure password hashing
- User profile management
- Token trading/transfer between users
- Real GitHub repository integration for project links
- OAuth authentication
- Token redemption system

## License

ISC
