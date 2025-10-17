#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests",
#   "typing",
# ]
# ///
# https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file


"""mcp-ms-learn.py here.

at https://github.com/wilsonmar/azure-quickly/blob/main/mcp-ms-learn.py
by Wilson Mar

Query a MCP Server containing Microsoft's LEARN documents.
Use MCP-standard JSON 2.0 async protocol in 
SSE (Server-Sent Event) format (text/event-stream).

USAGE:
    chmod +x mcp-ms-learn.py
    uv run mcp-ms-learn.py
"""

#### SECTION 01. Metadata about this program file:

__last_commit__ = "25-10-16 v001 + new :mcp-ms-learn.py"
__status__      = "working on macOS Sequoia 15.3.1"

#### SECTION 02: Import internal libraries already built-in into Python:

import json
import requests
from pathlib import Path
from typing import Dict, Any

test_run_endpoint = False
show_tools = False
mcp_server_url = "https://learn.microsoft.com/api/mcp"
question = "What is the difference between MCP and A2A?"
output_json_filepath = "mcp-ms-learn.json"
output_md_filepath = "mcp-ms-learn.md"

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


def format_json_to_markdown(json_file_path: str, output_path: str) -> None:
    """Read a JSON file and convert it to Markdown formatted text."""
    path = Path(json_file_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")

    # Read JSON file:
    with open(json_file_path, 'r', encoding="utf-8") as f:
        data = json.load(f)

    # Write pretty-printed JSON to a new file:
    markdown_output = []
    if "result" in data and "content" in data["result"]:
        for item in data["result"]["content"]:
            if "text" in item:
                try:
                    # The 'text' field itself contains a JSON string
                    inner_content_list = json.loads(item["text"])
                    for inner_item in inner_content_list:
                        title = inner_item.get("title", "No Title")
                        content_text = inner_item.get("content", "No Content")
                        content_url = inner_item.get("contentUrl", "#")
                        markdown_output.append(f"## {title}\n\n{content_text}\n\n[Read more]({content_url})\n\n---\n")
                except json.JSONDecodeError:
                    markdown_output.append(f"## Raw Content\n\n{item['text']}\n\n---\n")

    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(markdown_output) if markdown_output else "No parsable content found.")
    
    #try:
    #    markdown_output = json.loads(content)
    #    print(f"DEBUGGING: markdown_output={markdown_output}")
    ##except json.JSONDecodeError:
    #    raise ValueError("Invalid JSON content found in file.")    
    #    markdown_output = "``````"
    
    #with open(output_path, "w", encoding="utf-8") as out:
    #    out.write(json.dumps(markdown_output, indent=2, ensure_ascii=False))
    
    #print(f"Markdown-formatted JSON written to: {output_path}")
    return


def main():
    """Just do the program."""
    if mcp_server_url:
        print(f"Querying MCP server at: {mcp_server_url}")
    else:
        print("FAIL: No mcp_server_url!")
        exit(9)
    
    if test_run_endpoint:
        print(f"Testing endpoint: {mcp_server_url}")
        if not test_endpoint(mcp_server_url):
            print("\n⚠️  The endpoint might not exist. Trying MCP request anyway...\n")
    
    if show_tools:
        print(f"Listing available tools from: {mcp_server_url}")
        tools_response = list_mcp_tools(mcp_server_url)
        print("Available tools:")
        print(json.dumps(tools_response, indent=2))
        print("\n" + "="*60 + "\n")
    
    if not question:
        print("FAIL: No question text to answer!")
        exit(9)
    # else:

    print(f"Question: {question}\n")
    # Query the server
    response = query_mcp_server(mcp_server_url, question)


    # Pretty format and display the response
    formatted_output = pretty_format_response(response)
    print(formatted_output)
    
    # Optionally save to file
    with open(output_json_filepath, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Response saved to: {output_json_filepath}")

    format_json_to_markdown(output_json_filepath, output_md_filepath)

if __name__ == "__main__":
    main()

"""
Response headers: {'Content-Type': 'text/event-stream', 'Content-Encoding': 'identity', 'Request-Context': 'appId=cid-v1:b4f06...guid', 'X-Powered-By': 'ASP.NET', 'x-azure-ref': '20251017T033714Z-r18f794d4f8n4xv9hC1CO1qg3400000000x0000000000fb4', 'nel': '{"report_to":"network-errors","max_age":604800,"success_fraction":0.01,"failure_fraction":1.0}', 'report-to': '{"group":"network-errors","max_age":604800,"endpoints":[{"url":"https://mdec.nelreports.net/api/report?cat=mdocs"}]}', 'X-Content-Type-Options': 'nosniff', 'Content-Length': '19753', 'Cache-Control': 'no-cache, no-store', 'Expires': 'Fri, 17 Oct 2025 03:37:14 GMT', 'Date': 'Fri, 17 Oct 2025 03:37:14 GMT', 'Connection': 'keep-alive', 'Set-Cookie': 'ASLBSA=...; Path=/; Secure; HttpOnly;, ASLBSACORS=...; SameSite=none; Path=/; Secure; HttpOnly;', 'Akamai-Cache-Status': 'Miss from child, Miss from parent', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload'}
Response text (first 500 chars): event: message

data: {"result":{"content":[{"type":"text","text":"[{\u0022title\u0022:\u0022MCP support\u0022,\u0022content\u0022:\u0022# MCP support\\nModel Context Protocol (MCP) is an open protocol that standardizes how applications provide context to large language models (LLMs). Starting in AI Shell 1.0.0-preview.6, AI Shell can act as an MCP Host and client to MCP servers. The key participants in the MCP architecture are:\\n1. MCP Host - AI Shell coordinates and manages one or multiple MCP

"""