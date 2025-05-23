# OPC UA MCP Server


## Overview

Python and NPX implementations provide the same core functionality for OPC UA operations through MCP tools, but differ in their implementation approach and deployment model.

## Implementation Languages

### Python Version (`opcua-mcp-server`)
- **Language**: Python 3.13+
- **Framework**: FastMCP
- **OPC UA Library**: `opcua` (FreeOpcUa)
- **Transport**: STDIO
- **Entry Point**: `opcua-mcp-server.py`

### NPX Version (`opcua-mcp-npx-server`)
- **Language**: TypeScript/Node.js
- **Framework**: @modelcontextprotocol/sdk
- **OPC UA Library**: `node-opcua`
- **Transport**: STDIO
- **Entry Point**: `src/index.ts` (compiled to `build/index.js`)

## Features Comparison

| Feature | Python Version | NPX Version | Notes |
|---------|----------------|-------------|-------|
| Read Single Node | ✅ | ✅ | Both support automatic type detection |
| Write Single Node | ✅ | ✅ | Both support automatic type conversion |
| Browse Node Children | ✅ | ✅ | Both return JSON formatted results |
| Call OPC UA Methods | ✅ | ✅ | Both support parameter conversion |
| Read Multiple Nodes | ✅ | ✅ | Batch read operations |
| Write Multiple Nodes | ✅ | ✅ | Batch write operations |
| Connection Management | ✅ | ✅ | Both handle lifecycle automatically |
| Error Handling | ✅ | ✅ | Comprehensive error reporting |
| Type Conversion | ✅ | ✅ | Automatic data type conversion |

## Tool Implementations

### Available Tools (Both Versions)

1. **`read_opcua_node`**
   - Read value from a single OPC UA node
   - Parameters: `node_id` (string)
   - Returns: Node value with ID prefix

2. **`write_opcua_node`**
   - Write value to a single OPC UA node
   - Parameters: `node_id` (string), `value` (string)
   - Returns: Success/failure message

3. **`browse_opcua_node_children`**
   - Browse children of an OPC UA node
   - Parameters: `node_id` (string)
   - Returns: Array of child nodes with IDs and browse names

4. **`read_multiple_opcua_nodes`**
   - Read values from multiple nodes in one request
   - Parameters: `node_ids` (array of strings)
   - Returns: Dictionary mapping node IDs to values

5. **`write_multiple_opcua_nodes`**
   - Write values to multiple nodes in one request
   - Parameters: `nodes_to_write` (array of {node_id, value} objects)
   - Returns: Status results for each write operation

6. **`call_opcua_method`**
   - Call a method on an OPC UA object
   - Parameters: `object_node_id`, `method_node_id`, `arguments` (optional)
   - Returns: Method execution result

## Deployment & Installation

### Python Version
```bash
# Installation
cd opcua-mcp-server
uv install  # or pip install

# Usage
uv run opcua-mcp-server.py
# or
python opcua-mcp-server.py
```

### NPX Version
```bash
# Direct usage (recommended)
npx opcua-mcp-npx-server

# Global installation
npm install -g opcua-mcp-npx-server
opcua-mcp-npx-server

# Development
npm install
npm run build
npm start
```

## Configuration

Both versions use the same environment variable:
- `OPCUA_SERVER_URL`: OPC UA server endpoint (default: `opc.tcp://localhost:4840`)

### Python Configuration Example
```json
{
  "mcpServers": {
    "opcua-python": {
      "command": "/Users/mx/.local/bin/uv",
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

### NPX Configuration Example
```json
{
  "mcpServers": {
    "opcua-npx": {
      "command": "npx",
      "args": ["opcua-mcp-npx-server"],
      "env": {
        "OPCUA_SERVER_URL": "opc.tcp://localhost:4840"
      }
    }
  }
}
```

## Dependencies

### Python Version
- `mcp[cli]>=1.9.1`: MCP framework
- `opcua>=0.98.13`: OPC UA client library
- `cryptography>=45.0.2`: Security support
- `httpx>=0.28.1`: HTTP client

### NPX Version
- `@modelcontextprotocol/sdk`: MCP SDK for Node.js
- `node-opcua`: Comprehensive OPC UA library
- `typescript`: TypeScript compiler
- `@types/node`: Node.js type definitions

## Performance Considerations

### Python Version
- **Pros**: 
  - Simpler dependency tree
  - Mature OPC UA library
  - Lower memory footprint
- **Cons**:
  - Synchronous OPC UA operations wrapped in async
  - Python startup overhead

### NPX Version  
- **Pros**:
  - Native async/await support
  - Comprehensive OPC UA library with advanced features
  - NPX enables zero-install usage
  - TypeScript provides better type safety
- **Cons**:
  - Larger dependency tree
  - Node.js runtime overhead

## Security

Both versions currently connect with:
- `SecurityPolicy.None`
- `MessageSecurityMode.None`

For production use, both should implement:
- Certificate-based authentication
- Encrypted communication
- User authentication
- Input validation

## Use Cases

### Choose Python Version When:
- You prefer Python ecosystem
- Your project already uses Python
- You need minimal dependencies
- You're familiar with FreeOpcUa library

### Choose NPX Version When:
- You want zero-install deployment via NPX
- You prefer TypeScript/Node.js ecosystem
- You need advanced OPC UA features
- You want better async operation handling
- You're distributing to users who prefer NPM packages

## Error Handling

Both versions provide:
- Connection error handling
- Node read/write error reporting
- Type conversion error messages
- Method call failure details
- Graceful disconnection on shutdown

## Testing

### Test with Python Version
```bash
cd opcua-mcp-server
uv run opcua-mcp-server.py
```

### Test with NPX Version
```bash
npx opcua-mcp-npx-server
```

Both can be tested with the same OPC UA server and will provide identical functionality to MCP clients.

