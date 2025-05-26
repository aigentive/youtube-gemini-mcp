# Development Guide

This guide covers the technical architecture, development setup, and implementation details for the YouTube Gemini MCP Server.

## 🏗️ Architecture Overview

### Core Components

The server follows a modular architecture with clear separation of concerns:

```
src/youtube_gemini_mcp/
├── server.py              # FastMCP server with 10 MCP tools
├── session_manager.py     # Thread-safe session lifecycle management
├── gemini_client.py       # Google Gemini API integration
├── youtube_validator.py   # YouTube URL validation and metadata
├── files_uploader.py      # Google Files API wrapper
└── __init__.py            # Package initialization
```

### Key Design Patterns

#### 1. Session Management
**Thread-Safe Operations**: Uses `RLock` for concurrent access to session data
```python
def create_session(self, ...):
    with self._lock:
        # All session operations are thread-safe
        session = VideoSession(...)
        self.sessions[session.session_id] = session
```

**Persistent Storage**: Sessions are saved to disk with structured metadata
```
session_data/
├── sessions/
│   └── [session_id]/
│       ├── session_metadata.json
│       ├── conversation_log.json
│       ├── youtube_metadata.json  (if YouTube video)
│       └── files_api_info.json    (if local video)
└── expired_sessions/  # Archived sessions
```

**Automatic Cleanup**: Expired sessions are automatically archived
```python
def _cleanup_expired_sessions(self):
    current_time = datetime.now()
    for session_id, session in self.sessions.items():
        if time_diff > timeout_threshold:
            self.close_session(session_id)
```

#### 2. Hybrid Video Processing

**YouTube URL Direct Processing** (Preferred):
```python
# No download required - direct URL to Gemini
prompt_parts.append(
    types.Part(file_data=types.FileData(file_uri=youtube_url))
)
```

**Local Video Files API Processing**:
```python
# Upload to Google Files API, then process
uploaded_file = self.client.files.upload(path=video_path)
video_file = self.client.files.get(file_id)
prompt_parts.append(video_file)
```

#### 3. Error Handling Pattern

**Structured Responses**: All MCP tools follow consistent error format
```python
@mcp.tool()
def example_tool(param: str) -> Dict[str, Any]:
    try:
        # Implementation
        return {"success": True, "result": data}
    except Exception as e:
        logger.error(f"Tool failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "categorized_error_type"
        }
```

#### 4. Singleton Pattern for Global State

**Thread-Safe Initialization**:
```python
def get_session_manager() -> SessionManager:
    global session_manager
    if session_manager is None:
        session_manager = SessionManager(...)
    return session_manager
```

## 🛠️ Development Setup

### Prerequisites

- **Python 3.10+** (3.11+ recommended)
- **Poetry** for dependency management
- **Google AI API Key** for Gemini access
- **Git** for version control

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/youtube-gemini-mcp
cd youtube-gemini-mcp

# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Environment Variables

**Required**:
```bash
GOOGLE_API_KEY="your_google_api_key_here"
```

**Optional Configuration**:
```bash
MCP_MAX_SESSIONS=50               # Maximum concurrent sessions
MCP_SESSION_TIMEOUT=7200          # Session timeout in seconds
GEMINI_MODEL_DEFAULT="gemini-2.5-pro-preview-05-06"  # Default model
MAX_VIDEO_DURATION=7200           # Max video length in seconds
AUTO_CLEANUP_FILES="true"         # Auto-cleanup uploaded files
LOG_LEVEL="DEBUG"                 # Logging level
```

### Development Commands

```bash
# Run the server
poetry run python -m youtube_gemini_mcp.server

# Run tests
poetry run pytest
poetry run pytest -v              # Verbose output
poetry run pytest --cov          # With coverage

# Code quality
poetry run black src/ tests/      # Format code
poetry run isort src/ tests/      # Sort imports
poetry run mypy src/              # Type checking

# Install pre-commit hooks (optional)
poetry run pre-commit install
```

## 🧪 Testing Strategy

### Test Structure

```
tests/
├── test_server.py           # Server import and basic functionality
├── test_session_manager.py  # Session management (future)
├── test_youtube_validator.py # URL validation (future)
└── test_integration.py      # End-to-end tests (future)
```

### Current Test Coverage

**Import Tests**: Verify all modules can be imported without errors
```python
def test_import_server():
    from youtube_gemini_mcp import server
    assert hasattr(server, 'create_video_session')
```

**Environment Validation**: Test API key requirement
```python
def test_environment_variable_check():
    with patch.dict(os.environ, {}, clear=True):
        # Should fail gracefully without API key
```

**Component Initialization**: Test core components can be created
```python
def test_session_manager_import():
    manager = SessionManager(max_sessions=5)
    assert manager.max_sessions == 5
```

### Running Tests

```bash
# All tests
poetry run pytest

# Specific test file
poetry run pytest tests/test_server.py

# With coverage
poetry run pytest --cov=youtube_gemini_mcp

# Integration tests (requires API key)
GOOGLE_API_KEY="your_key" poetry run pytest tests/test_integration.py
```

## 🔧 Configuration

### MCP Integration

**Development Configuration** (`mcp-config.poetry.json`):
```json
{
  "mcpServers": {
    "youtube-gemini-mcp-dev": {
      "command": "poetry",
      "args": ["run", "python", "-m", "youtube_gemini_mcp.server"],
      "cwd": "/path/to/youtube-gemini-mcp",
      "env": {
        "GOOGLE_API_KEY": "your_api_key_here",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

**Production Configuration**:
```json
{
  "mcpServers": {
    "youtube-gemini-mcp": {
      "command": "youtube-gemini-mcp",
      "env": {
        "GOOGLE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Logging Configuration

**Format**: Matches openai-image-mcp exactly
```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)],
    force=True
)
```

**Log Outputs**:
- Session operations: Creation, updates, cleanup
- API calls: Gemini requests, Files API operations
- Errors: Structured error logging with context
- Performance: Session counts, cleanup operations

## 📊 Data Models

### VideoSession

**Core session state for conversational analysis**:
```python
@dataclass
class VideoSession:
    session_id: str = field(default_factory=uuid4)
    model: str = "gemini-2.5-pro-preview-05-06"
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    session_name: Optional[str] = None
    description: str = ""
    youtube_url: str = ""                    # For YouTube videos
    youtube_metadata: Dict[str, Any] = {}    # Video metadata
    google_file_id: Optional[str] = None     # For local videos
    video_file_path: Optional[str] = None    # Original file path
    conversation_history: List[Dict] = []    # Full conversation
    analysis_calls: List[VideoAnalysisCall] = []  # Structured calls
    active: bool = True
```

### VideoAnalysisCall

**Individual analysis within a session**:
```python
@dataclass
class VideoAnalysisCall:
    id: str
    prompt: str
    analysis_response: str
    video_metadata: Dict[str, Any]
    analysis_params: Dict[str, Any]
    created_at: datetime
    referenced_timestamps: List[str] = []
    key_insights: List[str] = []
```

## 🔌 API Integration

### Google Gemini API

**Direct YouTube URL Processing**:
```python
# Preferred method for YouTube videos
response = self.client.models.generate_content(
    model='models/gemini-2.5-pro-preview-05-06',
    contents=types.Content(parts=[
        types.Part(file_data=types.FileData(file_uri=youtube_url)),
        types.Part(text=user_prompt)
    ])
)
```

**Files API Integration**:
```python
# For local video files
uploaded_file = self.client.files.upload(path=video_path)
video_file = self.client.files.get(file_id)
```

### YouTube Metadata Extraction

**Using yt-dlp for metadata only**:
```python
ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'extractflat': False,  # Don't download
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(youtube_url, download=False)
```

## 🚀 Performance Considerations

### Memory Management

**Session Storage**: O(1) lookup with dictionary-based storage
```python
self.sessions: Dict[str, VideoSession] = {}
```

**Conversation Context**: Limited to last 5 exchanges to manage token limits
```python
recent_history = session.conversation_history[-5:]
```

**Automatic Cleanup**: Expired sessions are archived and removed
```python
def _cleanup_expired_sessions(self):
    # Move expired sessions to archived directory
    # Remove from active sessions dictionary
```

### Concurrency

**Thread Safety**: All session operations use RLock
```python
with self._lock:
    # All session modifications are thread-safe
```

**Concurrent Limits**: Default maximum 50 active sessions
```python
if len(self.sessions) >= self.max_sessions:
    return session_limit_exceeded_error
```

### File Management

**YouTube Videos**: No local storage required
**Local Videos**: 
- Upload to Google Files API
- 48-hour automatic deletion
- 2GB per file, 20GB per project limits

## 🐛 Debugging

### Common Issues

**1. API Key Missing**
```bash
CRITICAL_MAIN: GOOGLE_API_KEY environment variable is required
```
**Solution**: Set environment variable or check .env file

**2. Session Not Found**
```python
{"success": False, "error_type": "session_not_found"}
```
**Solution**: Check session ID, verify session hasn't expired

**3. YouTube URL Invalid**
```python
{"success": False, "error_type": "invalid_youtube_url"}
```
**Solution**: Use `validate_youtube_url` tool to check format

**4. File Too Large**
```python
{"success": False, "error_type": "upload_error"}
```
**Solution**: Check file size (2GB limit) and format

### Debug Tools

**Server Stats**: Check component health
```python
get_server_stats()
# Returns: component status, active sessions, environment
```

**Session Status**: Detailed session information
```python
get_session_status(session_id)
# Returns: session info, conversation history, metadata
```

**Logs**: Check stderr for detailed error information
```bash
tail -f mcp_server_stderr.log
```

## 🔄 Development Workflow

### Feature Development

1. **Create Feature Branch**
```bash
git checkout -b feature/new-functionality
```

2. **Implement Changes**
- Add/modify components in `src/youtube_gemini_mcp/`
- Follow existing patterns and error handling
- Add type hints for all new functions

3. **Add Tests**
```python
# tests/test_new_feature.py
def test_new_functionality():
    # Test implementation
    pass
```

4. **Quality Checks**
```bash
poetry run pytest
poetry run mypy src/
poetry run black src/ tests/
poetry run isort src/ tests/
```

5. **Documentation**
- Update relevant `.md` files
- Add docstrings for new functions
- Update `LLM.md` if adding new tools

### Release Process

1. **Version Update**
```toml
# pyproject.toml
version = "0.2.0"
```

2. **Changelog**
- Document new features
- Note breaking changes
- List bug fixes

3. **Tag Release**
```bash
git tag v0.2.0
git push origin v0.2.0
```

## 🔧 Extending the Server

### Adding New MCP Tools

1. **Create Tool Function**
```python
@mcp.tool()
def new_analysis_tool(param: str) -> Dict[str, Any]:
    """Tool description for MCP."""
    try:
        # Implementation
        return {"success": True, "result": data}
    except Exception as e:
        logger.error(f"New tool failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "new_tool_error"
        }
```

2. **Update Documentation**
- Add to `LLM.md` usage guide
- Update `README.md` tool list
- Add examples and use cases

3. **Add Tests**
```python
def test_new_analysis_tool():
    # Test the new tool functionality
    pass
```

### Adding New Components

1. **Create Module**
```python
# src/youtube_gemini_mcp/new_component.py
class NewComponent:
    def __init__(self):
        logger.info("NewComponent initialized")
```

2. **Add to Server**
```python
# server.py
from .new_component import NewComponent

new_component: Optional[NewComponent] = None

def get_new_component() -> NewComponent:
    global new_component
    if new_component is None:
        new_component = NewComponent()
    return new_component
```

3. **Initialize in Main**
```python
def main():
    # Initialize components
    get_new_component()
```

This development guide provides the foundation for extending and maintaining the YouTube Gemini MCP Server. The modular architecture and clear patterns make it straightforward to add new functionality while maintaining code quality and reliability.