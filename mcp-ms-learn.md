## About MCP servers in Azure API Management

# About MCP servers in Azure API Management
## MCP concepts and architecture
AI agents are becoming widely adopted because of enhanced LLM capabilities. However, even the most advanced models face limitations because of their isolation from external data. Each new data source potentially requires custom implementations to extract, prepare, and make data accessible for the models.
The [model context protocol](https://www.anthropic.com/news/model-context-protocol) (MCP) helps solve this problem. MCP is an open standard for connecting AI models and agents with external data sources such as local data sources (databases or computer files) or remote services (systems available over the internet, such as remote databases or APIs).
MCP follows a client-server architecture where a host application can connect to multiple servers. Whenever your MCP host or client needs a tool, it connects to the MCP server. The MCP server then connects to, for example, a database or an API. MCP hosts and servers connect with each other through the MCP protocol.
The following diagram illustrates the MCP architecture:
![Diagram of model context protocol (MCP) architecture.](https://learn.microsoft.com/en-us/azure/api-management/media/mcp-server-overview/mcp-architecture.png)
The architecture consists of the following components:
| Component | Description| 
|  --- | ---  |
| **MCP hosts** | LLM applications such as chat apps or AI assistants in your IDEs (like GitHub Copilot in Visual Studio Code) that need to access external capabilities |
| **MCP clients** | Protocol clients, inside the host application, that maintain 1:1 connections with servers |
| **MCP servers** | Lightweight programs that each expose specific capabilities and provide context, tools, and prompts to clients |
| **MCP protocol** | Transport layer in the middle |

The MCP architecture is built on [JSON-RPC 2.0 for messaging](https://modelcontextprotocol.io/docs/concepts/architecture). Communication between clients and servers occurs over defined transport layers, and supports primarily two modes of operation:
1. **Remote MCP servers** - Run as independent processes accessible over the internet using HTTP-based transports (like Streamable HTTP), enabling MCP clients to connect to external services and APIs hosted anywhere.
2. **Local MCP servers** MCP clients use standard input/output as a local transport method to connect to MCP servers on the same machine.

[Read more](https://learn.microsoft.com/en-us/azure/api-management/mcp-server-overview#mcp-concepts-and-architecture)

---

## Connect AI agents to Business Central through MCP server

# Connect AI agents to Business Central through MCP server
## Feature details
MCP is an open API standard that enables intelligent clients to discover, describe, and invoke operations on remote services in a self-describing, plug-and-play way.
MCP standardizes how applications provide context to language models. This standardization helps applications integrate seamlessly with different data sources and tools. This open standard connects AI assistants and agents to various systems where data resides, such as content repositories, business tools, and development environments. An MCP-compliant agent uses rich contextual information to act efficiently. A non-MCP-compliant agent doesn't have the necessary context.
With the MCP server for Business Central, you can easily connect agents to existing knowledge sources and APIs. You can enable agents to interface directly with Business Central. Actions and knowledge synchronize automatically. This synchronization facilitates real-time updates and the evolution of functionality. This model simplifies agent development and minimizes ongoing maintenance efforts.
For more information, go to [The autonomous enterprise: How generative AI is reshaping business applications](https://www.microsoft.com/dynamics-365/blog/business-leader/2025/05/20/the-autonomous-enterprise-how-generative-ai-is-reshaping-business-applications/?msockid=0868d1b7a20260d00630c41da369618e).
## Geographic areas
Visit the [Explore Feature Geography](https://aka.ms/FeatureGeographicAvailabilityReport) report for Microsoft Azure areas where this feature is planned or available.
## Language availability
Visit the [Explore Feature Language](https://aka.ms/FeatureLanguageAvailabilityReport) report for information on this feature's availability.

[Read more](https://learn.microsoft.com/en-us/dynamics365/release-plan/2025wave2/smb/dynamics365-business-central/connect-ai-agents-business-central-through-mcp-server#feature-details)

---

## Get started with .NET AI and the Model Context Protocol

# Get started with .NET AI and the Model Context Protocol
The Model Context Protocol (MCP) is an open protocol designed to standardize integrations between AI apps and external tools and data sources. By using MCP, developers can enhance the capabilities of AI models, enabling them to produce more accurate, relevant, and context-aware responses.
For example, using MCP, you can connect your LLM to resources such as:
1. Document databases or storage services.
2. Web APIs that expose business data or logic.
3. Tools that manage files or performing local tasks on a user's device.
Many Microsoft products already support MCP, including:
1. [Copilot Studio](https://www.microsoft.com/microsoft-copilot/blog/copilot-studio/introducing-model-context-protocol-mcp-in-copilot-studio-simplified-integration-with-ai-apps-and-agents/)
2. [Visual Studio Code GitHub Copilot agent mode](https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode)
3. [Semantic Kernel](https://devblogs.microsoft.com/semantic-kernel/integrating-model-context-protocol-tools-with-semantic-kernel-a-step-by-step-guide/).
You can use the MCP C# SDK to quickly create your own MCP integrations and switch between different AI models without significant code changes.
### MCP client-server architecture
MCP uses a client-server architecture that enables an AI-powered app (the host) to connect to multiple MCP servers through MCP clients:
1. **MCP Hosts**: AI tools, code editors, or other software that enhance their AI models using contextual resources through MCP. For example, GitHub Copilot in Visual Studio Code can act as an MCP host and use MCP clients and servers to expand its capabilities.
2. **MCP Clients**: Clients used by the host application to connect to MCP servers to retrieve contextual data.
3. **MCP Servers**: Services that expose capabilities to clients through MCP. For example, an MCP server might provide an abstraction over a REST API or local data source to provide business data to the AI model.
The following diagram illustrates this architecture:
![A diagram showing the architecture pattern of MCP, including hosts, clients, and servers.](https://learn.microsoft.com/en-us/dotnet/ai/media/mcp/model-context-protocol-architecture-diagram.png)
MCP client and server can exchange a set of standard messages:

[Read more](https://learn.microsoft.com/en-us/dotnet/ai/get-started-mcp)

---

## Model Context Protocol (MCP) on Databricks

# Model Context Protocol (MCP) on Databricks
This page is an overview of the MCP options on Databricks. [MCP](https://modelcontextprotocol.io/introduction) is an open source standard that connects AI agents to tools, resources, prompts, and other contextual information.
The main benefit of MCP is standardization. You can create a tool once and use it with any agent—whether it's one you've built or a third-party agent. Similarly, you can use tools developed by others, either from your team or from outside your organization.
MCP is one of three tool approaches available in Databricks Agent Framework. For guidance on when to choose MCP over Unity Catalog function tools or agent code tools, see [Choose your tool approach](https://learn.microsoft.com/en-us/azure/databricks/generative-ai/agent-framework/agent-tool#tool-comparison).

[Read more](https://learn.microsoft.com/en-us/azure/databricks/generative-ai/mcp/)

---

## MCP support

# MCP support
Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to large language models (LLMs). Starting in AI Shell 1.0.0-preview.6, AI Shell can act as an MCP Host and client to MCP servers. The key participants in the MCP architecture are:
1. MCP Host - AI Shell coordinates and manages one or multiple MCP clients
2. MCP Client - The client component of AI Shell maintains a connection to an MCP server and obtains context from an MCP server for the MCP host to use
3. MCP Server - A program, running locally or hosted remotely, that provides context to MCP clients
For more information about MCP, see the [Architecture Overview](https://modelcontextprotocol.io/docs/learn/architecture) in the official Model Context Protocol documentation.
MCP tools enable AI agents to access external tools and services to enhance their capabilities and provide more accurate responses. MCPs can integrate with various APIs, databases, and other resources, allowing agents to retrieve real-time information and perform complex tasks.

[Read more](https://learn.microsoft.com/en-us/powershell/utility-modules/aishell/how-to/mcp-support?view=ps-modules)

---

## Use MCP servers

# Use MCP servers
Model Context Protocol (MCP) is an open standard that enables AI models to interact with external tools and services through a unified interface. In Visual Studio, MCP support enhances GitHub Copilot agent mode by allowing you to connect any MCP-compatible server to your agentic coding workflow.
This article guides you through setting up MCP servers and using tools with agent mode in Visual Studio.
## Prerequisites
1. [Visual Studio 2022 version 17.14](https://learn.microsoft.com/en-us/visualstudio/releases/2022/release-history) or later. We highly recommend the latest servicing release of 17.14 because each release adds MCP features.
## How MCP and Visual Studio extend the GitHub Copilot agent
MCP support in Visual Studio works as follows:
1. MCP clients, such as Visual Studio, connect to MCP servers and request actions on behalf of the AI model.
2. MCP servers provide one or more tools that expose specific functionalities through a well-defined interface.
3. The protocol defines the message format for communication between clients and servers, including tool discovery, invocation, and response handling.
For example, an MCP server for a file system might provide tools for reading, writing, or searching files and directories. [The official GitHub MCP server](https://github.com/github/github-mcp-server) offers tools to list repositories, create pull requests, or manage issues. MCP servers can run locally on your machine or be hosted remotely. Visual Studio supports both configurations.
By standardizing this interaction, MCP eliminates the need for custom integrations between each AI model and each tool. You can then extend your AI assistant's capabilities by simply adding new MCP servers to your workspace. [Learn more about the MCP specification](https://modelcontextprotocol.io/specification/draft).

[Read more](https://learn.microsoft.com/en-us/visualstudio/ide/mcp-servers?view=vs-2022)

---

## Register and discover remote MCP servers in your API inventory

# Register and discover remote MCP servers in your API inventory
This article describes how to use Azure API Center to maintain an inventory (or *registry*) of remote model context protocol (MCP) servers and help stakeholders discover them using the API Center portal. MCP servers expose backend APIs or data sources in a standard way to AI agents and models that consume them.
## About MCP servers
AI agents are becoming widely adopted because of enhanced large language model (LLM) capabilities. However, even the most advanced models face limitations because of their isolation from external data. Each new data source potentially requires custom implementations to extract, prepare, and make data accessible for the models.
The [model context protocol](https://www.anthropic.com/news/model-context-protocol) (MCP) helps solve this problem. MCP is an open standard for connecting AI models and agents with external data sources such as local data sources (databases or computer files) or remote services (systems available over the internet, such as remote databases or APIs).
### MCP architecture
MCP follows a client-server architecture where a host application can connect to multiple servers. Whenever your MCP host or client needs a tool, it connects to the MCP server. The MCP server then connects to, for example, a database or an API. MCP hosts and servers connect with each other through the MCP protocol.
The MCP architecture is built on [JSON-RPC 2.0 for messaging](https://modelcontextprotocol.io/docs/concepts/architecture). Communication between clients and servers occurs over defined transport layers, and supports primarily two modes of operation:
1. **Remote MCP servers** - MCP clients connect to MCP servers over the internet, establishing a connection using HTTP and server-sent events (SSE), and authorizing the MCP client access to resources on the user's account using OAuth.
2. **Local MCP servers** MCP clients connect to MCP servers on the same machine, using standard input/output as a local transport method.

[Read more](https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server)

---

## A2A Client (TypeScript)

# A2A Client (TypeScript)
## What is an A2A Client?
An A2A client is an agent or application that can proactively send tasks to A2A servers and interact with them using the A2A protocol.
## Using A2AClient Directly
For direct control over A2A interactions, you can use the `A2AClient` from the SDK:
## Using A2AClientPlugin with ChatPrompt
A2A is most effective when used with an LLM. The `A2AClientPlugin` can be added to your chat prompt to allow interaction with A2A agents. Once added, the plugin will automatically configure the system prompt and tool calls to determine if the a2a server is needed for a particular task, and if so, it will do the work of orchestrating the call to the A2A server.
To send a message:
```typescript
// Now we can send the message to the prompt and it will decide if
// the a2a agent should be used or not and also manages contacting the agent
const result = await prompt.send(message);
```
### Advanced A2AClientPlugin Configuration
You can customize how the client interacts with A2A agents by providing custom builders:
## Sequence Diagram
Here's how the A2A client works with `ChatPrompt` and `A2AClientPlugin`:
![alt-text for a2a-client-1.png](https://learn.microsoft.com/en-us/microsoftteams/platform/teams-ai-library/assets/diagrams/a2a-client-1.png)

[Read more](https://learn.microsoft.com/en-us/microsoftteams/platform/teams-ai-library/typescript/in-depth-guides/ai/a2a/a2a-client#what-is-an-a2a-client)

---

## A2A (Agent-to-Agent) Protocol (TypeScript)

# A2A (Agent-to-Agent) Protocol (TypeScript)
Note
This package wraps the official [A2A SDK](https://github.com/a2aproject/a2a-js) for both server and client.
[What is A2A?](https://a2a-protocol.org/latest/)
A2A (Agent-to-Agent) is a protocol designed to enable agents to communicate and collaborate programmatically. This package allows you to integrate the A2A protocol into your Teams app, making your agent accessible to other A2A clients and enabling your app to interact with other A2A servers.
Install the package:
```bash
npm install @microsoft/teams.a2a
```
## What does this package do?
1. **A2A Server**: Enables your Teams agent to act as an A2A server, exposing its capabilities to other agents through the `/a2a` endpoint and serving an agent card at `/a2a/.well-known/agent-card.json`.
2. **A2A Client**: Allows your Teams app to proactively reach out to other A2A servers as a client, either through direct `AgentManager` usage or integrated with `ChatPrompt` for LLM-driven interactions.
## High-level Architecture
### A2A Server
![alt-text for overview-1.png](https://learn.microsoft.com/en-us/microsoftteams/platform/teams-ai-library/assets/diagrams/overview-1.png)
### A2A Client
![alt-text for overview-2.png](https://learn.microsoft.com/en-us/microsoftteams/platform/teams-ai-library/assets/diagrams/overview-2.png)
## Protocol Details
For detailed information about the A2A protocol, including agent card structure, message formats, and protocol specifications, see the official [A2A Protocol Documentation](https://a2a-protocol.org/latest/specification/).

[Read more](https://learn.microsoft.com/en-us/microsoftteams/platform/teams-ai-library/typescript/in-depth-guides/ai/a2a/overview)

---

## A2A Server (TypeScript)

# A2A Server (TypeScript)
In this guide, you'll learn to implement an A2A server to expose your Teams TypeScript app capabilities to other agents using the A2A protocol.
## What is an A2A Server?
An A2A server is an agent that exposes its capabilities to other agents using the A2A protocol. With this package, you can make your Teams app accessible to A2A clients.
## Adding the A2APlugin
To enable A2A server functionality, add the `A2APlugin` to your Teams app and provide an `agentCard`:
## Agent Card Exposure
The plugin automatically exposes your agent card at the path `/a2a/.well-known/agent-card.json`.
## Handling A2A Requests
Handle incoming A2A requests by adding an event handler for the `a2a:message` event. You may use `accumulateArtifacts` to iteratively accumulate artifacts for the task, or simply `respond` with the final result.
Note
1. You must have only a single handler that calls `respond`.
2. You **must** call `respond` as the last step in your handler. This resolves the open request to the caller.
## Sequence Diagram
![alt-text for a2a-server-1.png](https://learn.microsoft.com/en-us/microsoftteams/platform/teams-ai-library/assets/diagrams/a2a-server-1.png)

[Read more](https://learn.microsoft.com/en-us/microsoftteams/platform/teams-ai-library/typescript/in-depth-guides/ai/a2a/a2a-server)

---
