# Claude Desktop MCP Example

Add Apeiron to your Claude Desktop MCP config after installing the `mcp` extra:

```json
{
  "mcpServers": {
    "apeiron": {
      "command": "python",
      "args": ["-m", "apeiron.api.mcp_server"],
      "cwd": "/path/to/apeiron"
    }
  }
}
```
