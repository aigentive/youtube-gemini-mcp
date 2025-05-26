# YouTube to Gemini MCP Server - Product Requirements Document

## 📋 Executive Summary

**Project Name**: YouTube to Gemini MCP Server  
**Status**: Pre-Development  
**Architecture**: Session-based conversational video analysis using Gemini 2.5 Pro's direct YouTube URL support + Files API for local videos  
**Primary Integration**: Claude Desktop via Model Context Protocol (MCP)  
**Expected Delivery**: Q1 2025  

### Vision Statement

Create a sophisticated MCP server that enables conversational analysis of YouTube videos using Gemini 2.5 Pro's direct YouTube URL support (eliminating download/upload steps) while also supporting local video files via Files API, facilitating multi-turn conversations about video content with full context awareness and memory.

### 🎯 Key Differentiator

**CRITICAL**: This MCP provides actual video analysis (frame-by-frame visual understanding), NOT just transcript analysis. Unlike other YouTube MCPs that only extract and analyze text transcripts, this server leverages Gemini 2.5 Pro's built-in YouTube URL support for direct video processing, providing comprehensive visual, audio, and contextual analysis including:

- **Visual scene analysis** - Objects, people, settings, actions
- **Temporal understanding** - Changes over time, sequences, transitions  
- **Audio-visual correlation** - Speech with visual context, music with scenes
- **Timestamp-specific analysis** - "What happens at 5:30?" with visual context
- **Frame-level detail** - Text in videos, facial expressions, product details
- **Cross-modal analysis** - How visual and audio elements work together

**KEY ARCHITECTURAL ADVANTAGE**: Our hybrid approach (YouTube URL direct + Files API fallback) provides optimal user experience:
- **YouTube videos**: Instant analysis with no storage limitations
- **Local videos**: Full upload support with 48-hour session lifespan (Files API limitation)

## 🎯 Problem Statement

### Current Limitations

❌ **Fragmented video analysis workflows** - Multiple tools needed for YouTube → analysis pipeline  
❌ **No conversational context** - Each video analysis query starts from scratch  
❌ **Manual file management** - Complex upload/download processes  
❌ **Limited video memory** - Cannot reference previous discussions about videos  
❌ **Single-shot limitations** - "Tell me more about minute 5:30" requires re-uploading context  

### Our Solution

✅ **Direct YouTube processing** - YouTube URL → Gemini analysis (no download/upload needed)  
✅ **Dual video support** - YouTube URLs (direct) + local files (Files API)  
✅ **Session-based conversations** - Multi-turn discussions with video context retention  
✅ **Automatic file management** - Organized metadata storage and cleanup  
✅ **Persistent video memory** - Reference previous analysis naturally  
✅ **Conversational refinement** - "What about the second speaker?" works contextually  

## 🏗️ Technical Architecture

### Core Components (Following openai-image-mcp Patterns) - UPDATED

```
src/youtube_gemini_mcp/
├── server.py                 # FastMCP server with MCP tools
├── session_manager.py        # Video session lifecycle management  
├── gemini_client.py          # Google Gemini API client (YouTube URL + Files API)
├── youtube_validator.py      # YouTube URL validation and metadata extraction
├── files_uploader.py         # Google Files API integration for local videos
├── video_processor.py        # Local video validation and processing
├── conversation_builder.py   # Video context and conversation management
└── file_organizer.py         # Structured metadata and session storage
```

**HYBRID ARCHITECTURE**: 
- **YouTube videos**: Direct URL processing (no download/upload)
- **Local video files**: Files API upload and processing (still needed)
- **Unified interface**: Single MCP server handles both video sources seamlessly

### Data Classes (Adapting from openai-image-mcp)

```python
@dataclass
class VideoAnalysisCall:
    """Represents a single video analysis within conversation."""
    id: str                      # Unique analysis ID
    prompt: str                  # User's analysis request
    analysis_response: str       # Gemini's analysis response
    video_metadata: Dict[str, Any]  # Video info (title, duration, etc.)
    analysis_params: Dict[str, Any]  # Analysis parameters
    created_at: datetime
    referenced_timestamps: List[str] = field(default_factory=list)
    key_insights: List[str] = field(default_factory=list)

@dataclass  
class VideoSession:
    """Complete session state for conversational video analysis."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    model: str = "gemini-2.5-pro-preview-05-06"
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    session_name: Optional[str] = None
    description: str = ""
    youtube_url: str = ""
    youtube_metadata: Dict[str, Any] = field(default_factory=dict)
    google_file_id: Optional[str] = None
    video_file_path: Optional[str] = None
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    analysis_calls: List[VideoAnalysisCall] = field(default_factory=list)
    active: bool = True
```

### Key Design Patterns (Inherited from openai-image-mcp)

**Session Management**: Thread-safe video session lifecycle
- **O(1) session lookup** using dictionary-based storage
- **Automatic cleanup** with configurable timeouts
- **Thread-safe operations** using RLock for concurrent access

**Conversation Context**: Multi-turn video discussions with context
- **Video-aware conversations** with persistent memory
- **Context trimming** to manage token limits
- **Video reference preservation** for continuity

**Advanced API Integration**: Gemini 2.5 Pro with Google Files API
- **Structured video uploads** via Google Files API
- **Automatic retry** with exponential backoff  
- **Error categorization** for appropriate handling

**Comprehensive Error Handling**: Structured error responses
- **Error types** for programmatic handling
- **Recovery guidance** for common issues
- **Logging integration** for debugging

## 🛠️ Complete Implementation Specifications

### Logging Configuration (Exact from openai-image-mcp)

```python
import logging
import sys

# Configure logging (CRITICAL: Use exact same format as openai-image-mcp)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)],
    force=True
)

logger = logging.getLogger(__name__)
logger.info("YouTube Gemini MCP Server initializing...")
```

### FastMCP Server Initialization (Exact from openai-image-mcp)

```python
from mcp.server import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastMCP server (CRITICAL: Use exact same pattern)
mcp = FastMCP("youtube-gemini-mcp")

# Global instances (CRITICAL: Use exact same singleton pattern)
session_manager: Optional[SessionManager] = None
gemini_client: Optional[GeminiClient] = None
conversation_builder: Optional[ConversationBuilder] = None
video_processor: Optional[VideoProcessor] = None
file_organizer: Optional[FileOrganizer] = None
youtube_validator: Optional[YouTubeValidator] = None
files_uploader: Optional[FilesUploader] = None
```

### Error Handling Pattern (Exact from openai-image-mcp)

```python
# CRITICAL: Every MCP tool must use this exact error handling pattern
@mcp.tool()
def example_tool(param: str) -> Dict[str, Any]:
    """Tool description."""
    try:
        # Implementation here
        return {
            "success": True,
            "result": "success_data"
        }
    except Exception as e:
        logger.error(f"Failed to execute tool: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "tool_execution_error"
        }
```

### Thread-Safe Singleton Pattern (Exact from openai-image-mcp)

```python
def get_session_manager() -> SessionManager:
    """Get or create session manager instance."""
    global session_manager
    if session_manager is None:
        max_sessions = int(os.getenv("MCP_MAX_SESSIONS", "50"))
        session_timeout = int(os.getenv("MCP_SESSION_TIMEOUT", "7200")) // 3600
        session_manager = SessionManager(max_sessions=max_sessions, session_timeout_hours=session_timeout)
        logger.info("SessionManager initialized")
    return session_manager

def get_gemini_client() -> GeminiClient:
    """Get or create Gemini client instance."""
    global gemini_client
    if gemini_client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("CRITICAL: GOOGLE_API_KEY environment variable is required")
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        gemini_client = GeminiClient(api_key=api_key)
        logger.info("GeminiClient initialized")
    return gemini_client
```

### Main Entry Point (Exact from openai-image-mcp)

```python
def main():
    """Main entry point for the MCP server."""
    try:
        # Validate environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("CRITICAL_MAIN: GOOGLE_API_KEY environment variable is required. Server cannot start.")
            return
        
        logger.info("Starting YouTube Gemini MCP Server")
        
        # Initialize global instances
        get_session_manager()
        get_gemini_client()
        get_conversation_builder()
        get_file_organizer()
        get_video_processor()
        get_youtube_validator()
        get_files_uploader()
        
        logger.info("All components initialized successfully")
        
        # Run the MCP server
        mcp.run()
        
    except Exception as e:
        logger.error(f"CRITICAL_MAIN: Server startup failed: {e}")

if __name__ == "__main__":
    main()
```

## 🛠️ MCP Tools Specification

### Session Management Tools

#### `create_video_session(description, video_source, model="gemini-2.5-pro-preview-05-06", session_name=None, source_type="youtube_url")`
**Purpose**: Create new conversational video analysis session  
**Input**: 
- `description`: Session context/purpose
- `video_source`: YouTube URL or local video file path
- `model`: Gemini model to use
- `session_name`: Optional friendly name
- `source_type`: "youtube_url" (default) or "local_file"

**Output**:
```json
{
  "success": true,
  "session_id": "uuid-string",
  "video_info": {
    "title": "YouTube Video Title",
    "duration": "15:30",
    "channel": "Channel Name",
    "video_id": "dQw4w9WgXcQ"
  },
  "processing_method": "youtube_url_direct",
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "model": "gemini-2.5-pro-preview-05-06",
  "status": "ready_for_analysis"
}
```

**Alternative for Local Files**:
```json
{
  "success": true,
  "session_id": "uuid-string",
  "video_info": {
    "title": "Local Video File",
    "duration": "8:45",
    "file_size": "125MB"
  },
  "processing_method": "files_api",
  "google_file_id": "files/abc123",
  "model": "gemini-2.5-pro-preview-05-06",
  "status": "ready_for_analysis"
}
```

#### `analyze_video_in_session(session_id, prompt, timestamp_range=None)`
**Purpose**: Analyze video within session context  
**Input**:
- `session_id`: UUID of existing session
- `prompt`: Analysis question/instruction
- `timestamp_range`: Optional "MM:SS-MM:SS" for segment analysis

**Output**:
```json
{
  "success": true,
  "analysis": "Detailed video analysis response",
  "referenced_timestamps": ["1:30", "5:45"],
  "session_context": "Context summary",
  "video_insights": {
    "key_topics": ["topic1", "topic2"],
    "speakers": ["speaker1", "speaker2"],
    "segments_discussed": ["0:00-2:30", "5:00-7:15"]
  }
}
```

#### `get_session_status(session_id)`
**Purpose**: Get current session status and history
**Output**: Session metadata, conversation history, video info

#### `list_active_sessions()`
**Purpose**: List all active video analysis sessions
**Output**: Array of active sessions with summaries

#### `close_session(session_id)`
**Purpose**: Close session and cleanup resources
**Output**: Session closure confirmation with cleanup status

### Direct Video Analysis Tools

#### `analyze_youtube_video(youtube_url, prompt, model="gemini-2.5-pro-preview-05-06", session_id=None)`
**Purpose**: Single-shot or session-integrated YouTube video analysis using direct URL method  
**Input**:
- `youtube_url`: YouTube video URL or ID
- `prompt`: Analysis instruction
- `model`: Gemini model to use
- `session_id`: Optional session for context

**Workflow (UPDATED)**:
1. Validate and normalize YouTube URL
2. Extract metadata using yt-dlp (no download)
3. Send YouTube URL directly to Gemini API
4. Return structured response with video insights
5. No cleanup needed (no local files)

#### `analyze_local_video(video_path, prompt, model="gemini-2.5-pro-preview-05-06", session_id=None)`
**Purpose**: Single-shot or session-integrated local video analysis using Files API  
**Input**:
- `video_path`: Local video file path
- `prompt`: Analysis instruction
- `model`: Gemini model to use
- `session_id`: Optional session for context

**Workflow**:
1. Validate local video file
2. Upload to Google Files API
3. Send to Gemini for analysis
4. Return structured response
5. Optional cleanup of uploaded file

#### `continue_video_discussion(session_id, prompt)`
**Purpose**: Continue discussion about previously analyzed video
**Input**: 
- `session_id`: Existing session UUID
- `prompt`: Follow-up question or instruction

### Video Processing Tools

#### `download_youtube_video(youtube_url, quality="best", format_preference="mp4")`
**Purpose**: Download YouTube video for processing  
**Features**:
- Support for video URLs and IDs
- Quality selection (best, worst, specific resolution)
- Format preferences (mp4, webm, etc.)
- Metadata extraction (title, duration, channel, etc.)

#### `upload_video_to_google_files(video_path, display_name=None)`
**Purpose**: Upload video to Google Files API for Gemini processing
**Features**:
- Automatic format validation
- Progress tracking for large files
- Retry logic for failed uploads
- File metadata preservation

#### `validate_youtube_url(url)`
**Purpose**: Validate and normalize YouTube URLs/IDs
**Output**: Validation status, normalized URL, video metadata

### Workflow Tools

#### `promote_video_to_session(youtube_url, session_description, analysis_summary=None)`
**Purpose**: Convert single-shot analysis to conversational session
**Use Case**: Start with quick analysis, then expand to detailed session

#### `get_video_transcript(session_id, include_timestamps=True)`
**Purpose**: Extract video transcript with optional timestamps
**Features**:
- Auto-generated transcripts via Gemini
- Manual transcript support
- Timestamp alignment
- Speaker identification

### Utility Tools

#### `get_usage_guide()`
**Purpose**: Comprehensive tool documentation and examples
**Output**: Complete usage guide, best practices, examples

#### `get_server_stats()`
**Purpose**: Server statistics and health monitoring
**Output**: Active sessions, memory usage, API quotas

## 📁 File Organization Structure

### Video Content Organization
```
workspace/
├── session_data/
│   ├── sessions/
│   │   └── [session_id]/
│   │       ├── session_metadata.json      # Session info and video source
│   │       ├── conversation_log.json      # Full conversation history
│   │       ├── youtube_metadata.json      # YouTube video info (if applicable)
│   │       └── files_api_info.json        # Files API details (if local video)
│   └── expired_sessions/                  # Archived sessions with expired files
├── transcripts/                           # Generated transcripts
└── cache/                                 # URL validation and metadata cache
```

### Metadata Format Examples

**Video Metadata (`video_metadata.json`)**:
```json
{
  "youtube_id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up",
  "channel": "Rick Astley",
  "duration": "3:33",
  "upload_date": "2009-10-25",
  "view_count": 1400000000,
  "description": "Video description...",
  "downloaded_at": "2025-05-26T10:00:00Z",
  "file_size_bytes": 52428800,
  "format": "mp4",
  "resolution": "720p"
}
```

**Google Files Info (`google_file_info.json`)**:
```json
{
  "file_id": "files/abc123def456",
  "display_name": "Rick Astley - Never Gonna Give You Up",
  "mime_type": "video/mp4",
  "size_bytes": 52428800,
  "upload_timestamp": "2025-05-26T10:05:00Z",
  "expires_at": "2025-05-28T10:05:00Z",
  "gemini_processing_status": "active"
}
```

## 🔧 Technical Requirements

### Dependencies

**Core Libraries** (Updated for 2025):
- `google-genai` >= 0.1.0 (New Google Gemini API - replaces deprecated google-generativeai)
- `yt-dlp` >= 2024.12.0 (YouTube downloading - for local video fallback only)
- `mcp` >= 1.0.0 (MCP framework with CLI extras)
- `python-dotenv` >= 1.0.0 (Environment management)
- `pydantic` >= 2.0.0 (Data validation)
- `httpx` >= 0.27.0 (HTTP client)
- `requests` >= 2.32.0 (File operations)

**Development Dependencies** (Exact versions from openai-image-mcp):
- `pytest` >= 8.0.0
- `black` >= 25.0.0 
- `isort` >= 6.0.0
- `mypy` >= 1.0.0
- `pytest-asyncio` >= 0.26.0

### Exact pyproject.toml Template (Based on openai-image-mcp)

```toml
[tool.poetry]
name = "youtube-gemini-mcp"
version = "0.1.0"
description = "Session-based conversational YouTube video analysis MCP server using Gemini 2.5 Pro"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{include = "youtube_gemini_mcp", from = "src"}]
repository = "https://github.com/yourusername/youtube-gemini-mcp"
homepage = "https://github.com/yourusername/youtube-gemini-mcp"
keywords = ["youtube", "gemini", "mcp", "video-analysis", "ai", "claude", "conversational"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]

[tool.poetry.dependencies]
python = "^3.10"
google-genai = ">=0.1.0"
yt-dlp = ">=2024.12.0"
mcp = {extras = ["cli"], version = "^1.0.0"}
python-dotenv = "^1.0.0"
pydantic = "^2.0.0"
httpx = "^0.27.0"
requests = "^2.32.3"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
black = "^25.0.0"
isort = "^6.0.0"
mypy = "^1.0.0"
pytest-asyncio = "^0.26.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.scripts]
youtube-gemini-mcp = "youtube_gemini_mcp.server:main"

[tool.black]
line-length = 88

[tool.isort]
profile = "black"

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
asyncio_default_fixture_loop_scope = "function"
```

### Google Gemini API Integration Patterns (UPDATED)

**CRITICAL**: Gemini API has built-in YouTube URL support! No need for separate download/upload for YouTube videos.

```python
from google import genai
from google.genai import types

class GeminiClient:
    """Google Gemini API client for video analysis."""
    
    def __init__(self, api_key: str):
        """Initialize Gemini client."""
        self.client = genai.Client(api_key=api_key)
        logger.info("GeminiClient initialized")
    
    def analyze_youtube_video_direct(
        self, 
        youtube_url: str, 
        user_prompt: str,
        timestamp_range: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze YouTube video directly using URL (PREFERRED METHOD)."""
        try:
            # Build prompt parts for direct YouTube URL analysis
            prompt_parts = []
            
            # Add YouTube video directly via URL
            prompt_parts.append(
                types.Part(
                    file_data=types.FileData(file_uri=youtube_url)
                )
            )
            
            # Add timestamp context if provided
            if timestamp_range:
                prompt_parts.append(
                    types.Part(text=f"Focus on timestamp range: {timestamp_range}")
                )
            
            # Add user prompt
            prompt_parts.append(types.Part(text=user_prompt))
            
            # Generate response using Gemini 2.5 Pro
            response = self.client.models.generate_content(
                model='models/gemini-2.5-pro-preview-05-06',
                contents=types.Content(parts=prompt_parts)
            )
            
            return {
                "success": True,
                "analysis_response": response.text,
                "method": "youtube_url_direct",
                "video_url": youtube_url
            }
            
        except Exception as e:
            logger.error(f"Direct YouTube analysis failed for {youtube_url}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "youtube_direct_error"
            }
    
    def upload_local_video_file(self, video_path: str, display_name: str) -> str:
        """Upload local video to Google Files API (for non-YouTube videos)."""
        try:
            # Upload video file using Files API
            video_file = self.client.files.upload(video_path, mime_type="video/mp4")
            logger.info(f"Uploaded video {video_path} as {video_file.name}")
            
            # Wait for processing
            import time
            while video_file.state.name == "PROCESSING":
                time.sleep(10)
                video_file = self.client.files.get(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise ValueError(f"Video processing failed: {video_file.state}")
            
            return video_file.name
            
        except Exception as e:
            logger.error(f"Failed to upload video {video_path}: {e}")
            raise
    
    def analyze_uploaded_video(
        self, 
        file_id: str, 
        user_prompt: str,
        timestamp_range: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze uploaded video using Files API (for local videos)."""
        try:
            # Build prompt parts for uploaded video analysis
            prompt_parts = []
            
            # Add uploaded video file reference
            video_file = self.client.files.get(file_id)
            prompt_parts.append(video_file)
            
            # Add timestamp context if provided
            if timestamp_range:
                prompt_parts.append(
                    types.Part(text=f"Focus on timestamp range: {timestamp_range}")
                )
            
            # Add user prompt
            prompt_parts.append(types.Part(text=user_prompt))
            
            # Generate response
            response = self.client.models.generate_content(
                model='models/gemini-2.5-pro-preview-05-06',
                contents=types.Content(parts=prompt_parts)
            )
            
            return {
                "success": True,
                "analysis_response": response.text,
                "method": "files_api",
                "file_id": file_id
            }
            
        except Exception as e:
            logger.error(f"Uploaded video analysis failed for {file_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "files_api_error"
            }
    
    def analyze_video_with_conversation(
        self, 
        session: VideoSession, 
        user_prompt: str,
        timestamp_range: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze video using conversation context."""
        try:
            # Build conversation context
            conversation_context = self.build_conversation_context(session)
            
            # Build prompt parts
            prompt_parts = []
            
            # Add video reference (YouTube URL or Files API)
            if session.youtube_url:
                # Use direct YouTube URL method (PREFERRED)
                prompt_parts.append(
                    types.Part(
                        file_data=types.FileData(file_uri=session.youtube_url)
                    )
                )
            elif session.google_file_id:
                # Use Files API for uploaded local videos
                video_file = self.client.files.get(session.google_file_id)
                prompt_parts.append(video_file)
            else:
                raise ValueError("No video source available in session")
            
            # Add conversation context
            if conversation_context:
                prompt_parts.append(
                    types.Part(text=f"Previous conversation context:\n{conversation_context}")
                )
            
            # Add timestamp context if provided
            if timestamp_range:
                prompt_parts.append(
                    types.Part(text=f"Focus on timestamp range: {timestamp_range}")
                )
            
            # Add user prompt
            prompt_parts.append(types.Part(text=f"User request: {user_prompt}"))
            
            # Generate response
            response = self.client.models.generate_content(
                model='models/gemini-2.5-pro-preview-05-06',
                contents=types.Content(parts=prompt_parts)
            )
            
            return {
                "success": True,
                "analysis_response": response.text,
                "conversation_length": len(session.conversation_history),
                "method": "youtube_url_direct" if session.youtube_url else "files_api"
            }
            
        except Exception as e:
            logger.error(f"Conversational video analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "conversation_analysis_error"
            }
```

### YouTube URL Validation and Metadata (UPDATED)

**NOTE**: yt-dlp now only used for metadata extraction and optional local fallback, not for video downloading since Gemini API supports direct YouTube URLs.

```python
import yt_dlp
import os
from urllib.parse import urlparse, parse_qs

class YouTubeValidator:
    """YouTube URL validation and metadata extraction."""
    
    def __init__(self):
        """Initialize validator."""
        logger.info("YouTubeValidator initialized")
    
    def validate_and_normalize_url(self, url: str) -> Dict[str, Any]:
        """Validate and normalize YouTube URL."""
        try:
            # Extract video ID from various YouTube URL formats
            if "youtube.com/watch" in url:
                parsed = urlparse(url)
                video_id = parse_qs(parsed.query).get('v', [None])[0]
            elif "youtu.be/" in url:
                video_id = url.split("youtu.be/")[1].split("?")[0]
            elif len(url) == 11:  # Direct video ID
                video_id = url
                url = f"https://www.youtube.com/watch?v={video_id}"
            else:
                raise ValueError("Invalid YouTube URL format")
            
            if not video_id:
                raise ValueError("Could not extract video ID")
            
            normalized_url = f"https://www.youtube.com/watch?v={video_id}"
            
            return {
                "valid": True,
                "video_id": video_id,
                "normalized_url": normalized_url,
                "original_url": url
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "original_url": url
            }
    
    def extract_metadata(self, youtube_url: str) -> Dict[str, Any]:
        """Extract video metadata using yt-dlp (without downloading)."""
        try:
            validation = self.validate_and_normalize_url(youtube_url)
            if not validation["valid"]:
                raise ValueError(f"Invalid URL: {validation['error']}")
            
            # Extract metadata without downloading
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extractflat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(validation["normalized_url"], download=False)
                
                # Check video duration (max 2 hours for Gemini)
                duration = info.get('duration', 0)
                if duration > 7200:  # 2 hours
                    logger.warning(f"Video duration {duration}s exceeds recommended 2-hour limit")
                
                return {
                    "success": True,
                    "video_metadata": {
                        "video_id": validation["video_id"],
                        "title": info.get('title', ''),
                        "channel": info.get('uploader', ''),
                        "duration": duration,
                        "duration_formatted": self._format_duration(duration),
                        "upload_date": info.get('upload_date', ''),
                        "view_count": info.get('view_count', 0),
                        "description": info.get('description', '')[:500],  # Truncate
                        "normalized_url": validation["normalized_url"]
                    }
                }
                
        except Exception as e:
            logger.error(f"Metadata extraction failed for {youtube_url}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "metadata_extraction_error"
            }
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration in seconds to HH:MM:SS or MM:SS."""
        if seconds < 3600:  # Less than 1 hour
            minutes, seconds = divmod(seconds, 60)
            return f"{minutes:02d}:{seconds:02d}"
        else:  # 1 hour or more
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def check_gemini_compatibility(self, youtube_url: str) -> Dict[str, Any]:
        """Check if YouTube video is compatible with Gemini API requirements."""
        try:
            metadata_result = self.extract_metadata(youtube_url)
            if not metadata_result["success"]:
                return metadata_result
            
            metadata = metadata_result["video_metadata"]
            duration = metadata["duration"]
            
            # Gemini API limits
            compatibility_checks = {
                "duration_ok": duration <= 7200,  # 2 hours max
                "public_video": True,  # Assume public if metadata extracted successfully
                "supported_format": True,  # YouTube videos are supported
            }
            
            compatible = all(compatibility_checks.values())
            
            warnings = []
            if duration > 7200:
                warnings.append(f"Video duration ({metadata['duration_formatted']}) exceeds 2-hour Gemini limit")
            
            return {
                "success": True,
                "compatible": compatible,
                "checks": compatibility_checks,
                "warnings": warnings,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Compatibility check failed for {youtube_url}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "compatibility_check_error"
            }
```

### Files API Integration for Local Videos

```python
import os
import time
from typing import Dict, Any, Optional
from google import genai

class FilesUploader:
    """Google Files API integration for local video uploads."""
    
    def __init__(self, genai_client: genai.Client):
        """Initialize with Gemini client."""
        self.client = genai_client
        logger.info("FilesUploader initialized")
    
    def upload_video_file(self, video_path: str, display_name: Optional[str] = None) -> Dict[str, Any]:
        """Upload local video file to Google Files API (CORRECTED)."""
        try:
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            # Validate file size (CORRECTED: 2GB per file, 20GB per project)
            file_size = os.path.getsize(video_path)
            max_size = 2 * 1024 * 1024 * 1024  # 2GB limit per file
            
            if file_size > max_size:
                raise ValueError(f"File too large: {file_size} bytes (max: {max_size})")
            
            # IMPORTANT: Files are auto-deleted after 48 hours
            logger.info(f"Uploading {video_path} ({file_size} bytes) - will auto-delete in 48 hours")
            
            # Upload file using CORRECTED API syntax
            uploaded_file = self.client.files.upload(path=video_path)
            
            logger.info(f"Uploaded video as {uploaded_file.name}")
            
            # Return file information (CORRECTED: no processing wait needed)
            return {
                "success": True,
                "file_id": uploaded_file.name,
                "file_uri": uploaded_file.uri if hasattr(uploaded_file, 'uri') else None,
                "display_name": uploaded_file.display_name if hasattr(uploaded_file, 'display_name') else os.path.basename(video_path),
                "size_bytes": file_size,
                "upload_time": time.time(),
                "expires_in_hours": 48,
                "note": "File will be automatically deleted after 48 hours"
            }
            
        except Exception as e:
            logger.error(f"Failed to upload video {video_path}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "upload_error"
            }
    
    def delete_file(self, file_id: str) -> Dict[str, Any]:
        """Delete uploaded file from Google Files API (CORRECTED)."""
        try:
            # Use CORRECTED API syntax
            self.client.files.delete(file_id)
            logger.info(f"Deleted file: {file_id}")
            
            return {
                "success": True,
                "file_id": file_id,
                "status": "deleted"
            }
            
        except Exception as e:
            logger.error(f"Failed to delete file {file_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "deletion_error"
            }
    
    def get_file_info(self, file_id: str) -> Dict[str, Any]:
        """Get information about uploaded file (CORRECTED)."""
        try:
            # Use CORRECTED API syntax
            file_metadata = self.client.files.get(file_id)
            
            return {
                "success": True,
                "file_info": {
                    "file_id": file_metadata.name,
                    "display_name": getattr(file_metadata, 'display_name', 'Unknown'),
                    "mime_type": getattr(file_metadata, 'mime_type', 'Unknown'),
                    "size_bytes": getattr(file_metadata, 'size_bytes', 0),
                    "create_time": getattr(file_metadata, 'create_time', None),
                    "update_time": getattr(file_metadata, 'update_time', None),
                    "expires_in_hours": 48,
                    "note": "File auto-deletes after 48 hours"
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get file info for {file_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "file_info_error"
            }
    
    def list_files(self) -> Dict[str, Any]:
        """List all uploaded files (CORRECTED)."""
        try:
            files = self.client.files.list()
            
            file_list = []
            for file in files:
                file_list.append({
                    "file_id": file.name,
                    "display_name": getattr(file, 'display_name', 'Unknown'),
                    "mime_type": getattr(file, 'mime_type', 'Unknown'),
                    "size_bytes": getattr(file, 'size_bytes', 0),
                    "create_time": getattr(file, 'create_time', None)
                })
            
            return {
                "success": True,
                "files": file_list,
                "total_files": len(file_list),
                "storage_note": "All files auto-delete after 48 hours",
                "project_limit": "20GB total storage per project"
            }
            
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "list_files_error"
            }
```

### Environment Variables

**Required**:
- `GOOGLE_API_KEY` - Google AI API key for Gemini access

**Optional Configuration**:
- `MCP_MAX_SESSIONS` - Maximum concurrent sessions (default: 50)
- `MCP_SESSION_TIMEOUT` - Session timeout in seconds (default: 7200)
- `GEMINI_MODEL_DEFAULT` - Default Gemini model (default: "gemini-2.5-pro-preview-05-06")
- `MAX_VIDEO_DURATION` - Maximum video length in seconds (default: 7200)
- `AUTO_CLEANUP_FILES` - Auto-cleanup uploaded files after session (default: "true")

### Critical Files API Limitations (IMPORTANT)

**48-Hour Auto-Deletion**: 
- All uploaded files are automatically deleted after 48 hours
- No way to extend file retention period
- Sessions referencing deleted files will fail

**Storage Quotas**:
- Maximum 2GB per file
- Maximum 20GB total storage per project
- Files count against project quota immediately

**Implications for Our MCP**:
- Local video sessions have 48-hour maximum lifespan
- Need warning system for sessions approaching file expiration
- YouTube URL sessions unaffected (no file upload required)
- Consider session archival/recreation workflows

### System Requirements

**Python**: 3.10+ (3.11+ recommended)  
**Storage**: 5GB minimum for video cache  
**Network**: High-speed internet for video downloads  
**Memory**: 4GB RAM minimum for video processing  

### API Limitations and Quotas

**Google Gemini API**:
- Video upload limit: 2 hours per video
- File size limit: 2GB per video
- Processing time: ~1 minute per hour of video
- Rate limits: Apply per API key

**YouTube Download**:
- Respect YouTube's terms of service
- Rate limiting to prevent blocks
- Error handling for geo-restricted content

## 🎯 Use Cases and User Stories

### Primary Use Cases

**📚 Educational Content Analysis**
```
User: "Analyze this lecture video about machine learning"
System: Processes YouTube URL directly → Creates session
User: "What are the key concepts covered?"
System: Provides comprehensive analysis with timestamps
User: "Explain the part about neural networks in more detail"
System: References specific segments with context
```

**🎥 Content Research**
```
User: "I need to research this documentary about climate change"
System: Processes video, creates analysis session
User: "What are the main arguments presented?"
System: Identifies key arguments with supporting evidence
User: "Find contradictions or areas that need fact-checking"
System: Analyzes content critically with specific references
```

**🎤 Interview Analysis**
```
User: "Analyze this podcast interview with a tech CEO"
System: Processes YouTube URL directly, creates session
User: "What are the key business insights shared?"
System: Extracts business strategies and insights
User: "Compare this to their previous interview from last year"
System: References historical context if available in session
```

**📹 Tutorial Learning**
```
User: "Help me understand this coding tutorial"
System: Processes tutorial video
User: "Break down the code examples shown"
System: Identifies and explains code segments with timestamps
User: "What prerequisites do I need for this tutorial?"
System: Analyzes complexity and requirements
```

### Secondary Use Cases

**Content Creation Research**: Analyze competitor videos for insights  
**Academic Research**: Systematic analysis of video sources  
**Training Material Development**: Extract key points from educational videos  
**Quality Assurance**: Review and analyze produced video content  

## 🔐 Security and Privacy

### Data Handling

**Video Storage**: 
- Temporary local storage during processing
- Automatic cleanup after session closure
- No permanent video retention (user configurable)

**API Keys**:
- Environment variable storage only
- No logging of API keys
- Secure transmission to Google services

**User Content**:
- Conversation logs stored locally only
- Optional session data export
- Configurable data retention policies

### Compliance

**YouTube Terms of Service**: 
- Educational and research use focus
- No redistribution of downloaded content
- Respect for copyright restrictions

**Google API Compliance**:
- Follow Google Cloud terms of service
- Appropriate API key usage
- Quota management and monitoring

## 🧪 Testing Strategy

### Unit Testing
- **Session management**: Create, update, close sessions
- **Video downloading**: URL validation, format handling, error scenarios
- **Google API integration**: Upload, processing, error handling
- **Conversation building**: Context management, history preservation

### Integration Testing
- **End-to-end workflows**: YouTube URL → Analysis → Discussion
- **Error recovery**: Network failures, API limitations, invalid content
- **Session persistence**: Long-running conversations, context retention

### Performance Testing
- **Large video handling**: 2-hour video processing
- **Concurrent sessions**: Multiple simultaneous analyses
- **Memory management**: Long conversation histories

### Quality Assurance
- **Content accuracy**: Verify analysis quality against known videos
- **Timestamp accuracy**: Ensure references align with video content
- **Error messaging**: Clear, actionable error responses

## 📊 Success Metrics

### Technical Metrics
- **Session success rate**: >95% successful session creation
- **Download success rate**: >98% successful YouTube downloads
- **Analysis accuracy**: Verified against sample content
- **Response time**: <30 seconds for typical analysis requests

### User Experience Metrics
- **Tool adoption**: Integration in Claude Desktop workflows
- **Session engagement**: Average conversation length >5 turns
- **Error recovery**: <5% of sessions require user intervention
- **Content satisfaction**: Analysis relevance and accuracy

### Performance Benchmarks
- **Video processing**: <2 minutes for 1-hour video
- **Memory usage**: <2GB during processing
- **Storage efficiency**: <1.5x video size for complete session data
- **API quota efficiency**: Optimal usage of Google API limits

## 🛣️ Development Roadmap

### Phase 1: Core Infrastructure (Weeks 1-2)
- [ ] Project setup following openai-image-mcp patterns
- [ ] Basic session management implementation
- [ ] YouTube URL validation (yt-dlp for metadata only)
- [ ] Google Files API integration
- [ ] Basic Gemini client implementation with direct YouTube URL support

### Phase 2: MCP Tools Development (Weeks 3-4)
- [ ] Session management tools
- [ ] Video analysis tools
- [ ] File organization system
- [ ] Error handling and recovery

### Phase 3: Advanced Features (Weeks 5-6)
- [ ] Conversation context management
- [ ] Timestamp-based analysis
- [ ] Video promotion workflows
- [ ] Comprehensive testing suite

### Phase 4: Polish and Documentation (Week 7)
- [ ] Performance optimization
- [ ] Complete documentation
- [ ] Usage guides and examples
- [ ] Claude Desktop integration testing

### Phase 5: Release (Week 8)
- [ ] Final testing and validation
- [ ] Package publication
- [ ] Community feedback integration
- [ ] Initial user support

## 🧪 Complete Testing Implementation

### Test Structure (Exact from openai-image-mcp)

```python
# tests/test_server.py
"""Basic tests for the YouTube Gemini MCP Server."""

import pytest
import os
from unittest.mock import patch
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_import_server():
    """Test that the server module can be imported without errors."""
    try:
        from youtube_gemini_mcp import server
        assert server is not None
        
        # Test that key components are available
        assert hasattr(server, 'create_video_session') 
        assert hasattr(server, 'analyze_video_in_session')
        assert hasattr(server, 'get_usage_guide')
        assert hasattr(server, 'mcp')
        assert hasattr(server, 'main')
    except ImportError as e:
        pytest.fail(f"Failed to import server module: {e}")

def test_environment_variable_check():
    """Test environment variable validation."""
    with patch.dict(os.environ, {}, clear=True):
        with patch('youtube_gemini_mcp.server.logger') as mock_logger:
            with patch('youtube_gemini_mcp.server.mcp.run') as mock_run:
                from youtube_gemini_mcp.server import main
                main()
                
                # Should log error and not run server
                mock_logger.error.assert_called_with("CRITICAL_MAIN: GOOGLE_API_KEY environment variable is required. Server cannot start.")
                mock_run.assert_not_called()
```

### Claude Desktop MCP Configuration

```json
{
  "mcpServers": {
    "youtube-gemini-mcp": {
      "command": "sh",
      "args": [
        "-c", 
        "youtube-gemini-mcp 2> mcp_server_stderr.log"
      ],
      "env": {
        "GOOGLE_API_KEY": "your_google_api_key_here"
      }
    }
  }
}
```

### Development MCP Configuration

```json
{
  "mcpServers": {
    "youtube-gemini-mcp-dev": {
      "command": "sh", 
      "args": [
        "-c",
        "poetry run python -m youtube_gemini_mcp.server 2> mcp_server_stderr.log"
      ],
      "cwd": "/path/to/youtube-gemini-mcp",
      "env": {
        "GOOGLE_API_KEY": "your_google_api_key_here",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

## 📁 Complete Project Structure

```
youtube-gemini-mcp/
├── src/
│   └── youtube_gemini_mcp/
│       ├── __init__.py
│       ├── server.py                 # Main FastMCP server
│       ├── session_manager.py        # Video session management
│       ├── gemini_client.py          # Google Gemini API client
│       ├── youtube_validator.py      # yt-dlp integration for validation
│       ├── files_uploader.py         # Google Files API wrapper
│       ├── conversation_builder.py   # Context management
│       ├── video_processor.py        # Video validation/processing
│       └── file_organizer.py         # Structured storage
├── tests/
│   ├── __init__.py
│   ├── test_server.py               # Server import tests
│   ├── test_session_manager.py      # Session management tests
│   ├── test_youtube_validator.py    # URL validation functionality tests
│   └── test_usage_guide.py          # Documentation tests
├── session_data/                   # Session metadata and logs
│   ├── sessions/
│   │   └── [session_id]/
│   │       ├── session_metadata.json      # Session info and video source
│   │       ├── conversation_log.json      # Full conversation history
│   │       ├── youtube_metadata.json      # YouTube video info (if applicable)
│   │       └── files_api_info.json        # Files API details (if local video)
│   └── expired_sessions/                  # Archived sessions with expired files
├── docs/                           # Documentation
│   └── youtube-video-analysis.md
├── assets/                         # Project assets
│   └── hero-image.png
├── mcp-config.poetry.json          # Dev MCP config
├── mcp-config.private.json         # Production MCP config  
├── mcp_server_stderr.log           # Server logs
├── pyproject.toml                  # Poetry configuration
├── poetry.lock                     # Locked dependencies
├── README.md                       # Main documentation
├── LLM.md                          # LLM usage guide
├── DEVELOPMENT.md                  # Development guide
├── CONTRIBUTING.md                 # Contribution guidelines
├── LICENSE                         # MIT License
├── CLAUDE.md                       # Claude-specific instructions
└── .gitignore                      # Git ignore patterns
```

## 📚 Required Documentation Files

### README.md Structure (Based on openai-image-mcp)

```markdown
![YouTube Gemini MCP Hero](assets/hero-image.png)

# YouTube Gemini MCP Server

A Model Context Protocol (MCP) server that provides conversational YouTube video analysis capabilities using Gemini 2.5 Pro. Analyze videos through multi-turn conversations with advanced visual understanding.

## 🎯 What Problems Does This Solve?

### Traditional Video Analysis Pain Points
❌ **Transcript-only limitations** - Missing visual context and scene understanding  
❌ **No conversation memory** - Each analysis starts from scratch  
❌ **Manual workflows** - Complex download/upload processes  

### Our Solution  
✅ **Full video analysis** - Visual, audio, and contextual understanding  
✅ **Session memory** - Builds on previous analysis automatically  
✅ **Integrated workflows** - YouTube URL to analysis in one step  

## 🚀 Key Capabilities

### 🔄 Session-Based Video Conversations
[Content following openai-image-mcp patterns...]
```

### LLM.md Structure (Critical for Implementation)

```markdown
# LLM Usage Guide: YouTube Video Analysis MCP Tools

**Updated:** [Date]  
**Architecture:** Session-based Conversational Video Analysis using Gemini 2.5 Pro  
**For:** Large Language Models using the YouTube Gemini MCP Server

## 🚀 Key Features

### Visual Video Analysis
- **Frame-by-frame understanding** - Not just transcripts
- **Multi-turn video conversations** with persistent context
- **Timestamp-specific analysis** with visual context
- **Cross-modal understanding** - Visual + audio correlation

[Complete usage patterns following openai-image-mcp LLM.md structure...]
```

### DEVELOPMENT.md Structure

```markdown
# Development Guide

## 🏗️ Architecture

### Core Components
[Component descriptions...]

### Key Design Patterns
**Session Management**: Thread-safe video session lifecycle
**Conversation Context**: Multi-turn video discussions
**Gemini Integration**: Video upload and analysis workflows

## 🧪 Testing
[Testing instructions...]

## 🛠️ Development Installation
[Installation instructions...]
```

### CONTRIBUTING.md Structure

```markdown  
# Contributing to YouTube Gemini MCP

## 🛠️ Development Setup
[Setup instructions...]

## 📝 Code Style
- **Type Hints**: Required for all public functions
- **Docstrings**: Google-style docstrings
- **Error Handling**: Structured responses following openai-image-mcp patterns

[Rest following openai-image-mcp CONTRIBUTING.md...]
```

## 🔧 Implementation Priorities

### CRITICAL Must-Haves
1. **Exact FastMCP patterns** from openai-image-mcp
2. **Thread-safe session management** with RLock
3. **Structured error handling** with success/error responses
4. **Logging format** exactly matching openai-image-mcp
5. **Singleton pattern** for global instances
6. **File organization** following openai-image-mcp structure

### Video-Specific Requirements  
1. **yt-dlp integration** for reliable downloads
2. **Google Files API** for video uploads
3. **Gemini 2.5 Pro** for visual analysis (not just transcripts)
4. **Conversation context** preservation across video discussions
5. **Timestamp analysis** with frame-level understanding

### Testing Requirements
1. **Import tests** following openai-image-mcp patterns
2. **Environment validation** tests
3. **Mock integrations** for CI/CD
4. **Usage guide validation** tests

## 🤝 Team and Resources

### Required Expertise
- **Python development**: FastMCP, async programming, API integration
- **Google Cloud APIs**: Gemini, Files API, authentication
- **Video processing**: yt-dlp, format handling, metadata extraction
- **MCP framework**: Tool development, Claude Desktop integration

### External Dependencies
- **Google AI**: Gemini API access and quota
- **YouTube**: Video access and download compliance
- **MCP ecosystem**: Framework updates and compatibility

## 📈 Future Enhancements

### Advanced Video Features
- **Multi-video sessions**: Compare and analyze multiple videos
- **Video segment extraction**: Save and reference specific clips
- **Live stream analysis**: Real-time YouTube live stream processing
- **Batch processing**: Analyze video playlists or channels

### Enhanced AI Capabilities
- **Custom analysis templates**: Pre-built analysis frameworks
- **Visual recognition**: Identify objects, people, text in videos
- **Audio analysis**: Music recognition, speaker identification
- **Cross-reference**: Link to external knowledge bases

### Integration Expansions
- **Other video platforms**: Vimeo, Twitch, custom uploads
- **Export capabilities**: Generate reports, summaries, presentations
- **Collaboration features**: Shared sessions, multi-user analysis
- **API extensions**: RESTful API for external integrations

---

**Document Version**: 1.0  
**Last Updated**: 2025-05-26  
**Next Review**: 2025-06-02