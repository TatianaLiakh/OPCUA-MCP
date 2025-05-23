from mcp.server.fastmcp import FastMCP, Context
from opcua import Client
from contextlib import asynccontextmanager
from typing import AsyncIterator
import asyncio
import os
from typing import List, Dict, Any
from opcua import ua # 

server_url = os.getenv("OPCUA_SERVER_URL", "opc.tcp://localhost:4840")

# Manage the lifecycle of the OPC UA client connection
@asynccontextmanager
async def opcua_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Handle OPC UA client connection lifecycle."""
    client = Client(server_url)  
    try:
        # Connect to OPC UA server synchronously, wrapped in a thread for async compatibility
        await asyncio.to_thread(client.connect)
        print("Connected to OPC UA server")
        yield {"opcua_client": client}
    finally:
        # Disconnect from OPC UA server on shutdown
        await asyncio.to_thread(client.disconnect)
        print("Disconnected from OPC UA server")

# Create an MCP server instance
mcp = FastMCP("OPCUA-Control", lifespan=opcua_lifespan)

# Tool: Read the value of an OPC UA node
@mcp.tool()
def read_opcua_node(node_id: str, ctx: Context) -> str:
    """
    Read the value of a specific OPC UA node.
    
    Parameters:
        node_id (str): The OPC UA node ID in the format 'ns=<namespace>;i=<identifier>'.
                       Example: 'ns=2;i=2'.
    
    Returns:
        str: The value of the node as a string, prefixed with the node ID.
    """
    client = ctx.request_context.lifespan_context["opcua_client"]
    node = client.get_node(node_id)
    value = node.get_value()  # Synchronous call to get node value
    return f"Node {node_id} value: {value}"

# Tool: Write a value to an OPC UA node
@mcp.tool()
def write_opcua_node(node_id: str, value: str, ctx: Context) -> str:
    """
    Write a value to a specific OPC UA node.
    
    Parameters:
        node_id (str): The OPC UA node ID in the format 'ns=<namespace>;i=<identifier>'.
                       Example: 'ns=2;i=3'.
        value (str): The value to write to the node. Will be converted based on node type.
    
    Returns:
        str: A message indicating success or failure of the write operation.
    """
    client = ctx.request_context.lifespan_context["opcua_client"]
    node = client.get_node(node_id)
    try:
        # Convert value based on the node's current type
        current_value = node.get_value()
        if isinstance(current_value, (int, float)):
            node.set_value(float(value))
        else:
            node.set_value(value)
        return f"Successfully wrote {value} to node {node_id}"
    except Exception as e:
        return f"Error writing to node {node_id}: {str(e)}"

# Tool: Browse the children of a specific OPC UA node
@mcp.tool()
def browse_opcua_node_children(node_id: str, ctx: Context) -> str:
    """
    Browse the children of a specific OPC UA node.

    Parameters:
        node_id (str): The OPC UA node ID to browse (e.g., 'ns=0;i=85' for Objects folder).

    Returns:
        str: A string representation of a list of child nodes, including their NodeId and BrowseName.
             Returns an error message on failure.
    """
    client = ctx.request_context.lifespan_context["opcua_client"]
    try:
        node = client.get_node(node_id)
        children = node.get_children()
        
        children_info = []
        for child in children:
            try:
                browse_name = child.get_browse_name()
                children_info.append({
                    "node_id": child.nodeid.to_string(),
                    "browse_name": f"{browse_name.NamespaceIndex}:{browse_name.Name}"
                })
            except Exception as e:
                 children_info.append({
                     "node_id": child.nodeid.to_string(),
                     "browse_name": f"Error getting name: {e}"
                 })

        # import json
        # return json.dumps(children_info, indent=2) 
        return f"Children of {node_id}: {children_info!r}" 
        
    except Exception as e:
        return f"Error Browse children of node {node_id}: {str(e)}"

# Tool: Call an OPC UA method
@mcp.tool()
def call_opcua_method(object_node_id: str, method_node_id: str, arguments: List[Any] = None, ctx: Context) -> str:
    """
    Call a method on a specific OPC UA object node.

    Parameters:
        object_node_id (str): The OPC UA node ID of the object that contains the method.
                             Example: 'ns=2;i=1' for the Methods folder.
        method_node_id (str): The OPC UA node ID of the method to call.
                             Example: 'ns=2;i=2' for StartProduction method.
        arguments (List[Any], optional): List of arguments to pass to the method.
                                       Arguments will be converted to appropriate OPC UA variants.

    Returns:
        str: The result of the method call or an error message if the call fails.
    """
    client = ctx.request_context.lifespan_context["opcua_client"]
    try:
        # Get the object and method nodes
        object_node = client.get_node(object_node_id)
        
        # Prepare arguments
        method_args = []
        if arguments:
            for arg in arguments:
                # Convert arguments to appropriate types
                if isinstance(arg, str):
                    # Try to convert string to appropriate type
                    try:
                        # Try float first
                        method_args.append(float(arg))
                    except ValueError:
                        try:
                            # Try int
                            method_args.append(int(arg))
                        except ValueError:
                            # Keep as string
                            method_args.append(arg)
                else:
                    method_args.append(arg)
        
        # Call the method
        result = client.call_method(object_node_id, method_node_id, *method_args)
        
        return f"Method call successful. Object: {object_node_id}, Method: {method_node_id}, Result: {result}"
        
    except Exception as e:
        return f"Error calling method {method_node_id} on object {object_node_id}: {str(e)}"

# Tool: Read multiple OPC UA nodes
@mcp.tool()
def read_multiple_opcua_nodes(node_ids: List[str], ctx: Context) -> str:
    """
    Read the values of multiple OPC UA nodes in a single request.

    Parameters:
        node_ids (List[str]): A list of OPC UA node IDs to read (e.g., ['ns=2;i=2', 'ns=2;i=3']).

    Returns:
        str: A string representation of a dictionary mapping node IDs to their values, or an error message.
    """
    client = ctx.request_context.lifespan_context["opcua_client"]
    try:
        results = {}
        for node_id in node_ids:
            try:
                node = client.get_node(node_id)
                value = node.get_value()
                results[node_id] = value
            except Exception as e:
                results[node_id] = f"Error: {str(e)}"
        
        return f"Multiple node read results: {results!r}"
        
    except Exception as e:
        return f"Error reading multiple nodes: {str(e)}"

# Tool: Write multiple OPC UA nodes
@mcp.tool()
def write_multiple_opcua_nodes(nodes_to_write: List[Dict[str, Any]], ctx: Context) -> str:
    """
    Write values to multiple OPC UA nodes in a single request.

    Parameters:
        nodes_to_write (List[Dict[str, Any]]): A list of dictionaries, where each dictionary 
                                               contains 'node_id' (str) and 'value' (Any).
                                               The value will be wrapped in an OPC UA Variant.
                                               Example: [{'node_id': 'ns=2;i=2', 'value': 10.5}, 
                                                         {'node_id': 'ns=2;i=3', 'value': 'active'}]

    Returns:
        str: A message indicating the success or failure of the write operation. 
             Returns status codes for each write attempt.
    """
    client = ctx.request_context.lifespan_context["opcua_client"]
    try:
        results = []
        for item in nodes_to_write:
            node_id = item['node_id']
            value = item['value']
            
            try:
                node = client.get_node(node_id)
                
                # Convert value based on the node's current type
                current_value = node.get_value()
                if isinstance(current_value, (int, float)):
                    converted_value = float(value)
                elif isinstance(current_value, bool):
                    converted_value = str(value).lower() in ['true', '1', 'yes', 'on']
                else:
                    converted_value = str(value)
                
                node.set_value(converted_value)
                results.append({"node_id": node_id, "status": "Success"})
                
            except Exception as e:
                results.append({"node_id": node_id, "status": f"Error: {str(e)}"})
        
        return f"Write operation results: {results!r}"
        
    except Exception as e:
        return f"Error writing multiple nodes: {str(e)}"

# Run the server
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio') 