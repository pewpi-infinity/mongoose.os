# mongoose.os
Trick bike Freestyle BMX scripting

## Logged Octave Shell

This repository provides a logged wrapper for GNU Octave that captures all inputs and outputs with timestamps.

### Files

- **`run_octave_logged.py`** - Main script to run Octave with logging
- **`log_server.py`** - HTTP server to view logs via web interface
- **`index.html`** - Web UI for log viewing
- **`logs/txt.log`** - Log file (created automatically)

### Installation

1. Install GNU Octave:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install octave
   
   # macOS
   brew install octave
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/pewpi-infinity/mongoose.os.git
   cd mongoose.os
   ```

### Usage

#### Running the Logged Octave Shell

```bash
python3 run_octave_logged.py
```

**Behavior:**
- Every user input is logged as `[TIMESTAMP] [IN] ...`
- Every Octave response is logged as `[TIMESTAMP] [OUT] ...`
- Logs are saved to `logs/txt.log`

**Example:**
```
octave> x = 5
x = 5
octave> y = x * 2
y = 10
octave> quit
```

This will create log entries like:
```
[2025-12-06 02:05:41] [IN] x = 5
[2025-12-06 02:05:41] [OUT] x = 5
[2025-12-06 02:05:45] [IN] y = x * 2
[2025-12-06 02:05:45] [OUT] y = 10
[2025-12-06 02:05:48] [IN] quit
```

#### Viewing Logs via Web Interface

In a separate terminal, start the log server:

```bash
python3 log_server.py
```

Then open your browser to: `http://localhost:8000/`

**Features:**
- Real-time log viewing
- Auto-refresh option (every 5 seconds)
- Syntax highlighting for inputs/outputs
- Clear logs functionality
- Responsive dark theme interface

### Mathematical Context

This tool is designed to help explore complex mathematical problems and equations, including:

1. **Three-body problem** - Gravitational interactions
2. **Navier-Stokes equations** - Fluid dynamics
3. **Yang-Mills theory** - Quantum field theory
4. **Riemann hypothesis** - Number theory
5. **And many more...**

The logged shell allows you to experiment with numerical solutions and maintain a complete history of your computational experiments.

### API Endpoints

The log server provides the following API endpoints:

- `GET /` - Serves the web interface
- `GET /api/logs` - Returns log content as JSON
- `GET /api/clear` - Clears the log file

### Development

To contribute or modify:

1. Fork the repository
2. Make your changes
3. Test with Octave installed
4. Submit a pull request

### License

See repository license for details.
