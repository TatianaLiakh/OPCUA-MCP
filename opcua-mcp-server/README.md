# OPC UA MCP Server

A Model Context Protocol (MCP) server that provides seamless integration with OPC UA servers. This server enables AI assistants and other MCP clients to interact with industrial automation systems through standardized OPC UA communication protocols.

## Overview

This MCP server acts as a bridge between AI assistants and OPC UA servers, allowing for:
- Reading sensor data and system variables
- Writing control values to actuators and systems
- Browsing OPC UA node hierarchies
- Calling OPC UA methods for system operations
- Batch operations for multiple nodes

## Features

### Core Tools

- **`read_opcua_node`** - Read the current value of any OPC UA node
- **`write_opcua_node`** - Write values to OPC UA nodes with automatic type conversion
- **`browse_opcua_node_children`** - Explore the OPC UA address space and discover available nodes
- **`call_opcua_method`** - Execute OPC UA methods on server objects
- **`read_multiple_opcua_nodes`** - Batch read multiple nodes in a single operation
- **`write_multiple_opcua_nodes`** - Batch write to multiple nodes efficiently

### Key Capabilities

- **Automatic Connection Management**: Handles OPC UA client lifecycle with proper connection setup and teardown
- **Type-Safe Operations**: Automatic type conversion based on existing node data types
- **Error Handling**: Comprehensive error reporting for debugging and monitoring
- **Async Support**: Built on FastMCP for efficient asynchronous operations
- **Configurable**: Environment-based server URL configuration

## Installation

### Prerequisites

- Python 3.13 or higher
- Access to an OPC UA server (local or remote)
- UV package manager (recommended) or pip

### Setup

1. **Clone or download the project:**
   ```bash
   cd opcua-mcp-server
   ```

2. **Install dependencies using UV:**
   ```bash
   uv sync
   ```

   **Or using pip:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the OPC UA server URL:**
   ```bash
   export OPCUA_SERVER_URL="opc.tcp://localhost:4840"
   ```

## Usage

### Running the Server

**With UV:**
```bash
uv run opcua-mcp-server.py
```

**With Python:**
```bash
python opcua-mcp-server.py
```

### Integration with MCP Clients

Add to your MCP client configuration (e.g., `config.json`):

```json
{
  "mcpServers": {
    "opcua-mcp": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/opcua-mcp-server",
        "run",
        "opcua-mcp-server.py"
      ],
      "env": {
        "OPCUA_SERVER_URL": "opc.tcp://localhost:4840"
      }
    }
  }
}
```

## API Reference

### Reading Data

**Read a single node:**
```python
read_opcua_node(node_id="ns=2;i=3")
# Returns: "Node ns=2;i=3 value: 26.57"
```

**Read multiple nodes:**
```python
read_multiple_opcua_nodes(node_ids=["ns=2;i=3", "ns=2;i=4", "ns=2;i=5"])
# Returns: Multiple node read results with all values
```

### Writing Data

**Write to a single node:**
```python
write_opcua_node(node_id="ns=2;i=10", value="1500")
# Returns: "Successfully wrote 1500 to node ns=2;i=10"
```

**Write to multiple nodes:**
```python
write_multiple_opcua_nodes(
    nodes_to_write=[
        {"node_id": "ns=2;i=10", "value": "1500"},
        {"node_id": "ns=2;i=12", "value": "true"}
    ]
)
```

### Browsing Nodes

**Explore node hierarchy:**
```python
browse_opcua_node_children(node_id="ns=0;i=85")  # Objects folder
browse_opcua_node_children(node_id="ns=2;i=2")   # Sensors folder
```

### Method Calls

**Execute OPC UA methods:**
```python
call_opcua_method(
    object_node_id="ns=2;i=27",
    method_node_id="ns=2;i=28",
    arguments=["param1", "param2"]
)
```

## Node ID Format

OPC UA node IDs follow the format: `ns=<namespace>;i=<identifier>`

- `ns`: Namespace index (0 for standard OPC UA, 2+ for custom)
- `i`: Numeric identifier within the namespace

**Examples:**
- `ns=0;i=85` - Objects folder (standard)
- `ns=2;i=3` - Temperature sensor (custom)
- `ns=2;i=27` - Methods folder (custom)

## Common Use Cases

### Industrial Monitoring
```python
# Read temperature from multiple sensors
read_multiple_opcua_nodes([
    "ns=2;i=3",  # Temperature
    "ns=2;i=4",  # Pressure
    "ns=2;i=6"   # Tank Level
])
```

### Process Control
```python
# Set motor speed and valve position
write_multiple_opcua_nodes([
    {"node_id": "ns=2;i=10", "value": "1200"},  # Motor speed
    {"node_id": "ns=2;i=13", "value": "50"}     # Valve position
])
```

### System Discovery
```python
# Explore available sensors
browse_opcua_node_children("ns=2;i=2")  # Sensors folder

# Explore available actuators  
browse_opcua_node_children("ns=2;i=11") # Actuators folder
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPCUA_SERVER_URL` | OPC UA server endpoint URL | `opc.tcp://localhost:4840` |

## Error Handling

The server provides detailed error messages for:
- Connection failures to OPC UA servers
- Invalid node IDs or missing nodes
- Type conversion errors during writes
- Method call failures
- Network timeouts and communication issues

## Dependencies

- **mcp[cli]** (≥1.9.1) - Model Context Protocol framework
- **opcua** (≥0.98.13) - OPC UA client library
- **cryptography** (≥45.0.2) - Security and encryption support
- **httpx** (≥0.28.1) - HTTP client for additional communication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please refer to the license file for details.

## Support

For issues and questions:
- Check the error messages for debugging information
- Verify OPC UA server connectivity
- Ensure proper node ID formatting
- Review the OPC UA server logs for additional context
