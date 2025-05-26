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
Create persistent sessions for multi-turn video analysis:
```bash
# Create session
create_video_session(
    description="Analyze machine learning lecture",
    video_source="https://youtube.com/watch?v=abc123",
    source_type="youtube_url"
)

# Continue conversation
analyze_video_in_session(session_id="uuid", prompt="What are the key concepts?")
analyze_video_in_session(session_id="uuid", prompt="Explain the neural networks part")
```

### 📹 Direct YouTube Processing
No downloads required - process YouTube videos directly:
```bash
analyze_youtube_video(
    youtube_url="https://youtube.com/watch?v=abc123",
    prompt="Summarize this video's main points"
)
```

### 💾 Local Video Support
Upload and analyze local video files (48-hour retention):
```bash
analyze_local_video(
    video_path="/path/to/video.mp4",
    prompt="What happens in this video?"
)
```

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- Google AI API key
- Poetry (recommended) or pip

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/youtube-gemini-mcp
cd youtube-gemini-mcp

# Install with Poetry
poetry install

# Or with pip
pip install -e .

# Set environment variable
export GOOGLE_API_KEY="your_google_api_key_here"
```

## 🔧 Claude Desktop Integration

Add to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "youtube-gemini-mcp": {
      "command": "youtube-gemini-mcp",
      "env": {
        "GOOGLE_API_KEY": "your_google_api_key_here"
      }
    }
  }
}
```

For development:
```json
{
  "mcpServers": {
    "youtube-gemini-mcp-dev": {
      "command": "poetry",
      "args": ["run", "python", "-m", "youtube_gemini_mcp.server"],
      "cwd": "/path/to/youtube-gemini-mcp",
      "env": {
        "GOOGLE_API_KEY": "your_google_api_key_here"
      }
    }
  }
}
```

## 📚 Available Tools

| Tool | Description |
|------|-------------|
| `create_video_session` | Create new conversational analysis session |
| `analyze_video_in_session` | Analyze video within session context |
| `analyze_youtube_video` | Single-shot YouTube video analysis |
| `analyze_local_video` | Single-shot local video analysis |
| `get_session_status` | Get session information and history |
| `list_active_sessions` | List all active sessions |
| `close_session` | Close session and cleanup resources |
| `validate_youtube_url` | Validate and normalize YouTube URLs |
| `get_usage_guide` | Comprehensive documentation |
| `get_server_stats` | Server health and statistics |

## 🎯 Use Cases

### Educational Content Analysis
Analyze lectures, tutorials, and educational videos with follow-up questions.

### Content Research
Research documentaries, interviews, and informational content systematically.

### Video Summarization
Extract key insights and create summaries from long-form content.

### Training Material Development
Analyze existing training videos to extract learning objectives and key points.

## ⚡ Quick Examples

### Analyze a YouTube Video
```python
# Direct analysis
result = analyze_youtube_video(
    youtube_url="https://youtube.com/watch?v=dQw4w9WgXcQ",
    prompt="What is this video about?"
)
```

### Session-Based Analysis
```python
# Create session
session = create_video_session(
    description="Learning about AI",
    video_source="https://youtube.com/watch?v=abc123"
)

# Multi-turn conversation
analyze_video_in_session(session["session_id"], "What are the main topics?")
analyze_video_in_session(session["session_id"], "Explain deep learning concepts")
analyze_video_in_session(session["session_id"], "What examples are given?")
```

## 🔐 Configuration

### Environment Variables
- `GOOGLE_API_KEY` (required) - Google AI API key
- `MCP_MAX_SESSIONS` (optional) - Maximum concurrent sessions (default: 50)
- `MCP_SESSION_TIMEOUT` (optional) - Session timeout in seconds (default: 7200)

### Limitations
- **YouTube videos**: No duration limit for sessions
- **Local videos**: 48-hour session limit (Files API restriction)
- **File size**: Maximum 2GB per video file
- **Video length**: Recommended maximum 2 hours

## 🧪 Testing

```bash
# Run tests
poetry run pytest

# With coverage
poetry run pytest --cov=youtube_gemini_mcp

# Type checking
poetry run mypy src/
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [MCP Specification](https://github.com/modelcontextprotocol/specification)
- [Claude Desktop](https://claude.ai/desktop)
- [Google Gemini API](https://ai.google.dev/)

## 📞 Support

- 📧 Email: [your.email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/youtube-gemini-mcp/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/youtube-gemini-mcp/discussions)