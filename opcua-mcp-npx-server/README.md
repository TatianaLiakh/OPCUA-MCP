# OPC UA MCP NPX Server

An NPX-based Model Context Protocol (MCP) server for OPC UA operations. This server provides a set of tools to interact with OPC UA servers, including reading/writing variables, browsing nodes, calling methods, and performing batch operations.

## Features

- **Read OPC UA Nodes**: Read values from individual or multiple OPC UA nodes
- **Write OPC UA Nodes**: Write values to individual or multiple OPC UA nodes  
- **Browse Node Children**: Explore the OPC UA address space by browsing node children
- **Call OPC UA Methods**: Execute methods on OPC UA objects with parameters
- **Batch Operations**: Perform multiple read/write operations in single requests
- **Automatic Type Conversion**: Intelligent conversion of values based on node data types
- **Connection Management**: Automatic connection handling with graceful disconnection

## Installation & Usage

### Using NPX (Recommended)

You can run the server directly using NPX without installing it globally:

```bash
npx opcua-mcp-npx-server
```

### Global Installation

```bash
npm install -g opcua-mcp-npx-server
opcua-mcp-npx-server
```

### Local Development

```bash
git clone <repository>
cd opcua-mcp-npx-server
npm install
npm run build
npm start
```

## Configuration

The server connects to an OPC UA server using the following environment variable:

- `OPCUA_SERVER_URL`: The OPC UA server endpoint (default: `opc.tcp://localhost:4840`)

Example:
```bash
OPCUA_SERVER_URL=opc.tcp://192.168.1.100:4840 npx opcua-mcp-npx-server
```

## MCP Tools

### 1. read_opcua_node

Read the value of a specific OPC UA node.

**Parameters:**
- `node_id` (string): The OPC UA node ID in the format 'ns=<namespace>;i=<identifier>'

**Example:**
```json
{
  "node_id": "ns=2;i=2"
}
```

### 2. write_opcua_node

Write a value to a specific OPC UA node.

**Parameters:**
- `node_id` (string): The OPC UA node ID
- `value` (string): The value to write (automatically converted to the correct type)

**Example:**
```json
{
  "node_id": "ns=2;i=3",
  "value": "42.5"
}
```

### 3. browse_opcua_node_children

Browse the children of a specific OPC UA node.

**Parameters:**
- `node_id` (string): The OPC UA node ID to browse

**Example:**
```json
{
  "node_id": "ns=0;i=85"
}
```

### 4. read_multiple_opcua_nodes

Read values from multiple OPC UA nodes in a single request.

**Parameters:**
- `node_ids` (array): List of OPC UA node IDs to read

**Example:**
```json
{
  "node_ids": ["ns=2;i=2", "ns=2;i=3", "ns=2;i=4"]
}
```

### 5. write_multiple_opcua_nodes

Write values to multiple OPC UA nodes in a single request.

**Parameters:**
- `nodes_to_write` (array): List of objects containing 'node_id' and 'value'

**Example:**
```json
{
  "nodes_to_write": [
    {"node_id": "ns=2;i=2", "value": "10.5"},
    {"node_id": "ns=2;i=3", "value": "active"}
  ]
}
```

### 6. call_opcua_method

Call a method on a specific OPC UA object node.

**Parameters:**
- `object_node_id` (string): The OPC UA node ID of the object containing the method
- `method_node_id` (string): The OPC UA node ID of the method to call
- `arguments` (array, optional): List of arguments to pass to the method

**Example:**
```json
{
  "object_node_id": "ns=2;i=1",
  "method_node_id": "ns=2;i=2",
  "arguments": ["25.0", "start"]
}
```

## Integration with Cursor/Claude

This server can be integrated with Cursor IDE or Claude Desktop for OPC UA operations. Add the following to your MCP configuration:

### Cursor Configuration

Add to your Cursor settings:

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

### Claude Desktop Configuration

Add to your Claude Desktop configuration file:

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

## Example Usage in Conversation

Once configured, you can ask Claude to perform OPC UA operations:

- "Read the temperature sensor value from node ns=2;i=100"
- "Set the pump speed to 75% on node ns=2;i=150"
- "Browse all children of the sensors folder at ns=2;i=200"
- "Start production with rate 25 units/hour using method call"
- "Read all sensor values from nodes ns=2;i=100 through ns=2;i=110"

## Security Considerations

- This server currently connects without security (SecurityPolicy.None)
- For production use, implement appropriate security policies and authentication
- Ensure proper network security when connecting to industrial OPC UA servers
- Validate and sanitize all input parameters

## Error Handling

The server provides detailed error messages for:
- Connection failures
- Invalid node IDs
- Type conversion errors
- Method call failures
- Read/write operation errors

## Dependencies

- `@modelcontextprotocol/sdk`: MCP SDK for Node.js
- `node-opcua`: OPC UA client library for Node.js
- `typescript`: TypeScript compiler

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the OPC UA server connectivity
- Verify node IDs are correct
- Ensure proper permissions for OPC UA operations
- Review server logs for detailed error information 