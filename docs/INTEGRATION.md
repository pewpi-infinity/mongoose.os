# Pewpi Shared Library Integration

This repository integrates the canonical pewpi unified auth + wallet + token shared library from [GPT-Vector-Design](https://github.com/pewpi-infinity/GPT-Vector-Design).

## Quick Reference

The shared library is located at: [`src/pewpi-shared/`](../src/pewpi-shared/)

For complete integration documentation, see: [`src/pewpi-shared/INTEGRATION.md`](../src/pewpi-shared/INTEGRATION.md)

## What's Included

The pewpi-shared library provides:

- **TokenService**: Token management with IndexedDB (Dexie) + localStorage fallback
- **LoginComponent**: Passwordless login (magic-link) + optional GitHub OAuth
- **WalletComponent**: Wallet UI with balance, token list, and live feed
- **IntegrationListener**: Event-based integration for cross-repo state sync
- **P2PSyncManager**: Optional WebRTC-based peer-to-peer synchronization

## Initialization

The shared services are initialized in [`app.js`](../app.js) with:

```javascript
// Initialize token service auto-tracking
if (window.pewpiShared.tokenService) {
    window.pewpiShared.tokenService.initAutoTracking();
}

// Restore authentication session
if (window.pewpiShared.authService) {
    window.pewpiShared.authService.restoreSession();
}

// Setup event listeners
window.addEventListener('pewpi.token.created', (event) => {
    console.log('[Pewpi] Token created:', event.detail);
});

window.addEventListener('pewpi.token.updated', (event) => {
    console.log('[Pewpi] Token updated:', event.detail);
});

window.addEventListener('pewpi.login.changed', (event) => {
    console.log('[Pewpi] Login changed:', event.detail);
});
```

## Dependencies

Required npm packages (added to `package.json`):

```json
{
  "dependencies": {
    "dexie": "^3.2.4",
    "crypto-js": "^4.2.0"
  }
}
```

Install with:

```bash
npm install
```

## Usage Examples

### Creating Tokens

```javascript
// Award a token when user contributes
const token = await tokenService.createToken({
  type: 'bronze',
  value: 1,
  userId: 'user_123',
  metadata: { action: 'research_published' }
});
```

### Listening to Events

```javascript
// Listen for token events across the application
window.addEventListener('pewpi.token.created', (event) => {
  const token = event.detail;
  updateUserBalance(token.userId);
  showNotification(`You earned a ${token.type} token!`);
});
```

### Integration with Existing Features

The pewpi-shared library is designed to be backward-compatible. Existing authentication and wallet features remain intact. The shared library adds a standardized layer that can be incrementally adopted.

## Migration Notes

### Optional: Migrating Existing Auth

If you have existing authentication, you can:

1. Keep both systems running in parallel
2. Gradually migrate users to pewpi auth
3. Use migration utilities in the shared library

### Optional: Migrating Existing Tokens

If you have existing tokens in localStorage:

```javascript
// TokenService automatically uses localStorage as fallback
// Your existing data remains intact
```

## Testing Locally

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Open browser to `http://localhost:3000`

4. Open DevTools Console to see pewpi initialization logs

## Backward Compatibility

The initialization is wrapped in try/catch blocks to ensure:
- No breaking changes to existing builds
- Graceful degradation if shared services are unavailable
- Console warnings for debugging

## TODOs for Maintainers

- [ ] Test pewpi-shared integration with existing features
- [ ] Decide whether to adopt ES6 modules or script tags for imports
- [ ] Consider enabling P2P sync for multi-device token synchronization
- [ ] Review token creation logic for research contributions
- [ ] Update UI to display wallet component (optional)
- [ ] Add login component to existing auth flow (optional)

## Support

For questions about the pewpi-shared library:
- See the main integration guide: [`src/pewpi-shared/INTEGRATION.md`](../src/pewpi-shared/INTEGRATION.md)
- Check the source repository: https://github.com/pewpi-infinity/GPT-Vector-Design
- Review test examples in the GPT-Vector-Design `tests/` directory
