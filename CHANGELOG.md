# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-05-26

### Added
- Initial release of YouTube Gemini MCP Server
- Session-based conversational video analysis using Gemini 2.5 Pro
- Hybrid architecture supporting YouTube URLs (direct) and local files (Files API)
- Thread-safe session management with automatic cleanup
- 10 comprehensive MCP tools for video analysis workflows:
  - `create_video_session` - Create conversational analysis sessions
  - `analyze_video_in_session` - Multi-turn video discussions
  - `analyze_youtube_video` - Single-shot YouTube analysis
  - `analyze_local_video` - Local file analysis via Files API
  - `get_session_status` - Session information and history
  - `list_active_sessions` - Active session overview
  - `close_session` - Session cleanup and archival
  - `validate_youtube_url` - URL validation and compatibility
  - `get_usage_guide` - Comprehensive documentation
  - `get_server_stats` - Server health monitoring
- YouTube URL validation and metadata extraction using yt-dlp
- Google Files API integration with 48-hour limitation handling
- Comprehensive error handling following openai-image-mcp patterns
- FastMCP server implementation with structured logging
- Complete documentation suite:
  - README.md with installation and usage guide
  - LLM.md with AI systems usage patterns
  - DEVELOPMENT.md with architecture and setup
  - CONTRIBUTING.md with contribution guidelines
  - PRD.md with complete product requirements
- Professional test suite with import and functionality tests
- Code quality tools: black, isort, mypy configuration
- Claude Desktop MCP integration configurations
- MIT License for open source distribution

### Technical Features
- **Visual Video Analysis**: Frame-by-frame understanding, not just transcripts
- **Cross-Modal Analysis**: Visual + audio correlation and scene understanding
- **Timestamp-Specific Analysis**: Segment-focused video examination
- **Conversation Context**: Multi-turn discussions with persistent memory
- **Automatic File Management**: Structured metadata storage and cleanup
- **Performance Optimization**: O(1) session lookup, concurrent session support
- **Gemini 2.5 Pro Integration**: Latest model with video capabilities

### Architecture
- **Singleton Pattern**: Thread-safe global component management
- **Structured Storage**: Session metadata and conversation logs
- **Hybrid Processing**: Direct YouTube URL + Files API for local videos
- **Error Recovery**: Comprehensive error categorization and handling
- **Memory Management**: Token limit management and conversation trimming

### Documentation
- **User Guide**: Complete setup and usage instructions
- **AI Integration**: Comprehensive LLM usage patterns and examples
- **Developer Guide**: Architecture overview and contribution setup
- **API Reference**: Complete tool specifications and examples
- **Configuration**: Environment variables and deployment options

[0.1.0]: https://github.com/aigentive/youtube-gemini-mcp/releases/tag/v0.1.0