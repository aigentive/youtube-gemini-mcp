# Claude Code Instructions for YouTube Gemini MCP

This document provides specific instructions for Claude Code when working with the YouTube Gemini MCP project.

## Project Overview

**Project**: YouTube Gemini MCP Server  
**Type**: Model Context Protocol (MCP) server for conversational video analysis  
**Architecture**: Session-based conversational video analysis using Gemini 2.5 Pro  
**Primary Purpose**: Enable multi-turn conversations about YouTube videos and local video files  

## Key Architecture Components

### Hybrid Video Processing
- **YouTube Videos**: Direct URL processing via Gemini API (no download required)
- **Local Videos**: Upload via Google Files API with 48-hour retention limit
- **Unified Interface**: Single MCP server handles both video sources seamlessly

### Core Components
```
src/youtube_gemini_mcp/
├── server.py              # FastMCP server with MCP tools
├── session_manager.py     # Thread-safe session management
├── gemini_client.py       # Google Gemini API integration
├── youtube_validator.py   # YouTube URL validation and metadata
├── files_uploader.py      # Google Files API wrapper
```

### Session Management
- **Thread-safe**: Uses RLock for concurrent access
- **Persistent**: Sessions stored to disk with conversation history
- **Timeout-based**: Automatic cleanup of expired sessions
- **Memory-efficient**: O(1) session lookup with dictionary storage

## Development Patterns

### Error Handling
All MCP tools must follow this exact pattern:
```python
@mcp.tool()
def example_tool(param: str) -> Dict[str, Any]:
    try:
        # Implementation
        return {"success": True, "result": "data"}
    except Exception as e:
        logger.error(f"Tool failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "tool_execution_error"
        }
```

### Logging Configuration
Must use exact format from openai-image-mcp:
```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)],
    force=True
)
```

### Singleton Pattern
Global instances with thread-safe initialization:
```python
def get_session_manager() -> SessionManager:
    global session_manager
    if session_manager is None:
        session_manager = SessionManager(...)
    return session_manager
```

## Testing Requirements

### Basic Import Tests
- Test server module imports without errors
- Test all core components can be imported
- Test environment variable validation
- Test tool availability

### Mock-Based Testing
- Mock external APIs (Google Gemini, Files API)
- Mock yt-dlp for metadata extraction
- Test error handling paths
- Test session management operations

## Important Limitations

### Google Files API
- **48-hour auto-deletion**: All uploaded files are automatically deleted after 48 hours
- **2GB file limit**: Maximum file size per upload
- **20GB project limit**: Total storage quota per Google project
- **No retention extension**: Cannot extend file lifespan beyond 48 hours

### YouTube Processing
- **2-hour video limit**: Recommended maximum length for Gemini processing
- **Public videos only**: Private/unlisted videos may not be accessible
- **Rate limiting**: Respect YouTube and Google API rate limits

## Environment Configuration

### Required Variables
```bash
GOOGLE_API_KEY="your_google_api_key_here"
```

### Optional Variables
```bash
MCP_MAX_SESSIONS=50                    # Maximum concurrent sessions
MCP_SESSION_TIMEOUT=7200               # Session timeout in seconds
GEMINI_MODEL_DEFAULT="gemini-2.5-pro"  # Default model
```

## Development Commands

### Setup
```bash
poetry install                    # Install dependencies
export GOOGLE_API_KEY="..."      # Set API key
```

### Testing
```bash
poetry run pytest                # Run tests
poetry run pytest --cov         # With coverage
poetry run mypy src/            # Type checking
```

### Running
```bash
poetry run python -m youtube_gemini_mcp.server
```

## Claude Desktop Integration

### Development Configuration
```json
{
  "mcpServers": {
    "youtube-gemini-mcp-dev": {
      "command": "poetry",
      "args": ["run", "python", "-m", "youtube_gemini_mcp.server"],
      "cwd": "/path/to/youtube-gemini-mcp",
      "env": {
        "GOOGLE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Code Style Requirements

### Type Hints
Required for all public functions and methods.

### Docstrings
Use Google-style docstrings for all public functions.

### Error Messages
- Include specific error context
- Use structured error types
- Log errors with appropriate level

### File Organization
- Follow session-based storage pattern
- Use consistent JSON formatting
- Handle datetime serialization properly

## Common Workflows

### Session-Based Analysis
1. `create_video_session()` - Initialize session with video source
2. `analyze_video_in_session()` - Perform analysis with context
3. Multiple follow-up calls build conversation history
4. `close_session()` - Clean up and archive

### Single-Shot Analysis
1. `analyze_youtube_video()` - Direct YouTube analysis
2. `analyze_local_video()` - Local file analysis with upload

### Session Management
1. `list_active_sessions()` - View all active sessions
2. `get_session_status()` - Get detailed session info
3. Automatic cleanup handles expired sessions

## Dependencies Management

### Core Dependencies
- `google-genai` - New Gemini API client (replaces deprecated library)
- `yt-dlp` - YouTube metadata extraction (no downloading)
- `mcp` - FastMCP framework
- `pydantic` - Data validation

### Development Dependencies
- `pytest` - Testing framework
- `black` - Code formatting
- `mypy` - Type checking
- `isort` - Import sorting

## Troubleshooting

### Common Issues
1. **API Key Missing**: Check GOOGLE_API_KEY environment variable
2. **Session Not Found**: Verify session ID and check for expiration
3. **File Upload Fails**: Check file size (2GB limit) and format
4. **YouTube URL Invalid**: Use validation tool to check URL format

### Debugging
- Check `mcp_server_stderr.log` for detailed error logs
- Use `get_server_stats()` tool to check component status
- Verify environment variables with `get_server_stats()`

## Implementation Notes

### Thread Safety
- All session operations use RLock
- Session manager handles concurrent access
- File operations are thread-safe

### Memory Management
- Sessions automatically cleaned up on timeout
- Conversation history has size limits
- Large responses are truncated for context building

### Error Recovery
- Graceful degradation on API failures
- Retry logic for transient errors
- Clear error messages for user guidance