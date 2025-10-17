#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests",
#   "typing",
# ]
# ///
# https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file


"""mcp-ms-learn2.py here.

at https://github.com/wilsonmar/azure-quickly/blob/main/mcp-ms-learn2.py
by Wilson Mar

Query a MCP Server containing Microsoft's LEARN documents.
Use MCP-standard JSON 2.0 async protocol in 
SSE (Server-Sent Event) format (text/event-stream).

USAGE:
    chmod +x mcp-ms-learn2.py
    uv run mcp-ms-learn2.py
"""

#### SECTION 01. Metadata about this program file:

__last_commit__ = "25-10-16 v001 + new :mcp-ms-learn2.py"
__status__      = "json being output but not markdown format on macOS Sequoia 15.3.1"

#### SECTION 02: Import internal libraries already built-in into Python:

import json
import requests
from typing import Dict, Any

output_filepath = "mcp-ms-learn2.md"

def list_mcp_tools(url: str) -> Dict[str, Any]:
    """List available tools from the MCP server.
    
    Args:
        url: The MCP server endpoint URL
    Returns:
        The JSON response from the server
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Handle Server-Sent Events (SSE) format
        if response.headers.get('content-type') == 'text/event-stream':
            lines = response.text.strip().split('\n')
            for line in lines:
                if line.startswith('data: '):
                    json_data = line[6:]
                    try:
                        return json.loads(json_data)
                    except json.JSONDecodeError as json_err:
                        return {"error": f"Invalid JSON in SSE data: {json_err}"}
            return {"error": "No data found in SSE response"}
        else:
            try:
                return response.json()
            except json.JSONDecodeError as json_err:
                return {"error": f"Invalid JSON response: {json_err}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def query_mcp_server(url: str, question: str) -> Dict[str, Any]:
    """Query an MCP server with a question.
    
    Args:
        url: The MCP server endpoint URL
        question: The question to ask
    Returns:
        The JSON response from the server
    """
    # MCP protocol typically uses JSON-RPC 2.0 format
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "microsoft_docs_search",
            "arguments": {
                "query": question
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Debug: Print response details
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response text (first 500 chars): {response.text[:500]}")
        
        # Check if response is empty
        if not response.text.strip():
            return {"error": "Empty response from server"}
        
        # Handle Server-Sent Events (SSE) format
        if response.headers.get('content-type') == 'text/event-stream':
            # Parse SSE format
            lines = response.text.strip().split('\n')
            for line in lines:
                if line.startswith('data: '):
                    json_data = line[6:]  # Remove 'data: ' prefix
                    try:
                        return json.loads(json_data)
                    except json.JSONDecodeError as json_err:
                        return {
                            "error": f"Invalid JSON in SSE data: {json_err}",
                            "sse_data": json_data
                        }
            return {"error": "No data found in SSE response"}
        else:
            # Try to parse regular JSON
            try:
                return response.json()
            except json.JSONDecodeError as json_err:
                return {
                    "error": f"Invalid JSON response: {json_err}",
                    "response_text": response.text,
                    "status_code": response.status_code
                }
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def pretty_format_response(response: Dict[str, Any]) -> str:
    """Format the MCP response in a readable way.
    
    Args:
        response: The response dictionary from the MCP server
    Returns:
        A nicely formatted string representation
    """
    # Check for errors
    if "error" in response:
        return f"❌ Error: {response['error']}"
    
    # Format the response
    formatted = "=" * 60 + "\n"
    formatted += "MCP SERVER RESPONSE\n"
    formatted += "=" * 60 + "\n\n"
    
    # Pretty print the JSON with indentation
    formatted += json.dumps(response, indent=2, ensure_ascii=False)
    
    formatted += "\n\n" + "=" * 60
    
    return formatted

def test_endpoint(url: str) -> bool:
    """Test if the endpoint exists and is reachable."""
    try:
        response = requests.get(url, timeout=10)
        print(f"GET {url} - Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")
        return False

def main():
    """Perform the program."""
    mcp_server_url = "https://learn.microsoft.com/api/mcp"
    question = "What is MCP?"
    
    print(f"Testing endpoint: {mcp_server_url}")
    if not test_endpoint(mcp_server_url):
        print("\n⚠️  The endpoint might not exist. Trying MCP request anyway...\n")
    
    print(f"Listing available tools from: {mcp_server_url}")
    tools_response = list_mcp_tools(mcp_server_url)
    print("Available tools:")
    print(json.dumps(tools_response, indent=2))
    print("\n" + "="*60 + "\n")
    
    print(f"Querying MCP server at: {mcp_server_url}")
    print(f"Question: {question}\n")
    
    # Query the server
    response = query_mcp_server(mcp_server_url, question)
    
    # Pretty format and display the response
    formatted_output = pretty_format_response(response)
    print(formatted_output)
    
    # Optionally save to file
    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Response saved to: {output_filepath}")

if __name__ == "__main__":
    main()