# Chrome Extension Configuration

## API Server URL

The extension uses the API server URL configured in the popup UI. By default, it's set to `http://localhost:5000`.

### For Development

The default `http://localhost:5000` works when running the Flask API locally:
```bash
python src/api.py
```

### For Production

To use a production API server:

1. Update the default URL in `popup.html` line 155:
```html
<input type="text" id="apiUrl" placeholder="https://your-api-server.com" value="https://your-api-server.com">
```

2. Update the `host_permissions` in `manifest.json` to include your production domain:
```json
"host_permissions": [
  "http://localhost:5000/*",
  "https://your-api-server.com/*"
]
```

3. Users can also manually change the API URL in the extension popup without reinstalling.

### Security Note

The extension only requests permissions for the API server it needs to communicate with. Users can review and approve these permissions during installation.
