# LLM Usage Guide: YouTube Video Analysis MCP Tools

**Updated:** January 2025  
**Architecture:** Session-based Conversational Video Analysis using Gemini 2.5 Pro  
**For:** Large Language Models using the YouTube Gemini MCP Server

## 🚀 Key Features

### Visual Video Analysis
- **Frame-by-frame understanding** - Not just transcripts, but actual visual content analysis
- **Multi-turn video conversations** with persistent context and memory
- **Timestamp-specific analysis** with visual context ("What happens at 5:30?")
- **Cross-modal understanding** - Visual + audio correlation and analysis
- **Scene understanding** - Objects, people, settings, actions, and transitions

### Architecture Advantages
- **Hybrid processing**: YouTube URLs (direct) + local files (Files API)
- **No download required** for YouTube videos - instant analysis
- **Session persistence** - Build complex conversations about videos
- **Thread-safe operations** - Handle multiple concurrent analyses

## 🛠️ Available Tools

### Session Management Tools

#### `create_video_session`
**Purpose**: Create new conversational video analysis session  
**Best for**: Multi-turn video discussions, educational content analysis

```python
# YouTube video session
create_video_session(
    description="Analyze machine learning lecture for key concepts",
    video_source="https://youtube.com/watch?v=abc123",
    source_type="youtube_url",  # default
    session_name="ML Lecture Analysis"
)

# Local video session (48-hour limit)
create_video_session(
    description="Corporate training video analysis",
    video_source="/path/to/training.mp4",
    source_type="local_file",
    session_name="Training Analysis"
)
```

**Returns**: Session ID, video metadata, processing method, status

#### `analyze_video_in_session`
**Purpose**: Conversational video analysis with context  
**Best for**: Follow-up questions, detailed exploration, building insights

```python
# First analysis
analyze_video_in_session(
    session_id="uuid-string",
    prompt="What are the main topics covered in this video?"
)

# Follow-up with context
analyze_video_in_session(
    session_id="uuid-string", 
    prompt="Focus on the neural networks section - what examples are given?"
)

# Timestamp-specific analysis
analyze_video_in_session(
    session_id="uuid-string",
    prompt="Analyze the demonstration at 5:30-7:15",
    timestamp_range="5:30-7:15"
)
```

### Direct Analysis Tools

#### `analyze_youtube_video`
**Purpose**: Single-shot YouTube video analysis  
**Best for**: Quick insights, one-off analysis, rapid content review

```python
# Simple analysis
analyze_youtube_video(
    youtube_url="https://youtube.com/watch?v=dQw4w9WgXcQ",
    prompt="Summarize the main points of this video"
)

# Add to existing session
analyze_youtube_video(
    youtube_url="https://youtube.com/watch?v=xyz789",
    prompt="Compare this approach to the previous video",
    session_id="existing-session-uuid"
)
```

#### `analyze_local_video`
**Purpose**: Local video file analysis via Files API  
**Best for**: Private content, internal videos, custom recordings

```python
analyze_local_video(
    video_path="/Users/username/Downloads/presentation.mp4",
    prompt="Extract key business insights from this presentation"
)
```

**⚠️ Important**: Local files auto-delete after 48 hours due to Google Files API limitations.

### Session Utility Tools

#### `get_session_status`
**Purpose**: Detailed session information and conversation history

```python
get_session_status("session-uuid")
# Returns: session info, video metadata, recent conversation history
```

#### `list_active_sessions`
**Purpose**: Overview of all active video analysis sessions

```python
list_active_sessions()
# Returns: all sessions with summaries, conversation lengths, video sources
```

#### `close_session`
**Purpose**: Clean up and archive session data

```python
close_session("session-uuid")
# Archives conversation, cleans up resources, moves to expired directory
```

### Validation and Utility Tools

#### `validate_youtube_url`
**Purpose**: Check URL validity and Gemini compatibility

```python
validate_youtube_url("https://youtube.com/watch?v=abc123")
# Returns: validation status, normalized URL, compatibility checks, warnings
```

#### `get_usage_guide`
**Purpose**: Access comprehensive documentation and examples

#### `get_server_stats`
**Purpose**: Monitor server health and active sessions

## 🎯 Optimal Usage Patterns

### Educational Content Analysis
```python
# Step 1: Create focused session
session = create_video_session(
    description="Deep analysis of CS50 Lecture 1 on algorithms",
    video_source="https://youtube.com/watch?v=cs50-lecture1",
    session_name="CS50 Lecture 1 Analysis"
)

# Step 2: Get overview
analyze_video_in_session(
    session["session_id"],
    "Provide a comprehensive overview of topics covered, key concepts, and learning objectives"
)

# Step 3: Deep dive into specifics
analyze_video_in_session(
    session["session_id"],
    "Focus on the binary search explanation - how is it demonstrated and what examples are used?"
)

# Step 4: Extract practical elements
analyze_video_in_session(
    session["session_id"],
    "What coding examples are shown? Provide the algorithms discussed with explanations"
)

# Step 5: Assessment preparation
analyze_video_in_session(
    session["session_id"],
    "Based on this lecture, what would be good exam questions to test understanding?"
)
```

### Content Research Workflow
```python
# Multiple video comparison
session1 = create_video_session(
    description="Climate change documentary analysis",
    video_source="https://youtube.com/watch?v=climate-doc1",
    session_name="Climate Doc 1"
)

session2 = create_video_session(
    description="Alternative perspective on climate change",
    video_source="https://youtube.com/watch?v=climate-doc2", 
    session_name="Climate Doc 2"
)

# Analyze each for different aspects
analyze_video_in_session(session1["session_id"], "What evidence is presented? Focus on data and statistics")
analyze_video_in_session(session2["session_id"], "What evidence is presented? Focus on data and statistics")

# Compare insights (you'll need to synthesize responses manually)
```

### Corporate Training Analysis
```python
# Internal video analysis
result = analyze_local_video(
    video_path="/company/training/safety-procedures.mp4",
    prompt="Extract all safety procedures, requirements, and compliance points mentioned"
)

# Create detailed session for follow-up
session = create_video_session(
    description="Comprehensive safety training analysis for compliance review",
    video_source="/company/training/safety-procedures.mp4",
    source_type="local_file"
)

analyze_video_in_session(
    session["session_id"],
    "Identify any gaps or missing information compared to OSHA requirements"
)
```

## 💡 Advanced Techniques

### Timestamp-Focused Analysis
```python
# Segment-by-segment breakdown
analyze_video_in_session(
    session_id,
    "Analyze the introduction section (0:00-2:30) - what hooks and context are provided?",
    timestamp_range="0:00-2:30"
)

analyze_video_in_session(
    session_id,
    "Focus on the main demonstration (5:00-12:00) - what is being shown step by step?",
    timestamp_range="5:00-12:00"
)
```

### Cross-Modal Analysis
```python
# Visual + audio correlation
analyze_video_in_session(
    session_id,
    "How do the visual elements (slides, diagrams, demonstrations) support the spoken content? Are there any disconnects?"
)

# Scene understanding
analyze_video_in_session(
    session_id, 
    "Describe the setting, visual aids used, and how the physical environment contributes to the message"
)
```

### Conversation Threading
```python
# Build complex understanding
analyze_video_in_session(session_id, "What is the main thesis or argument?")
# -> Response: "The main thesis is X..."

analyze_video_in_session(session_id, "How is this thesis supported? What evidence is provided?")
# -> Uses previous context about thesis X

analyze_video_in_session(session_id, "Are there any logical gaps or counterarguments not addressed?")
# -> Builds on previous understanding of thesis and evidence

analyze_video_in_session(session_id, "How could this argument be strengthened?")
# -> Synthesizes entire conversation context
```

## ⚠️ Important Limitations

### Google Files API Constraints
- **48-hour auto-deletion**: Local video files automatically deleted after 48 hours
- **2GB file limit**: Maximum file size per upload
- **20GB project limit**: Total storage quota per Google project
- **No retention extension**: Cannot extend file lifespan

### YouTube Processing Limits
- **2-hour video limit**: Recommended maximum length for optimal processing
- **Public videos only**: Private/unlisted videos may not be accessible
- **Rate limiting**: Respect YouTube and Google API rate limits

### Session Management
- **Memory limits**: Very long conversations may hit token limits
- **Concurrent sessions**: Default maximum 50 active sessions
- **Timeout**: Sessions auto-expire after 2 hours of inactivity (configurable)

## 🔧 Best Practices

### Session Design
1. **Clear descriptions**: Use descriptive session names and descriptions
2. **Focused scope**: One video per session for best context management
3. **Logical progression**: Build questions that naturally flow from previous answers
4. **Regular cleanup**: Close sessions when analysis is complete

### Prompt Engineering
1. **Specific questions**: "What coding examples are shown at 5:30?" vs "Tell me about the video"
2. **Context building**: Reference previous parts of the conversation
3. **Multi-modal requests**: Ask about both visual and audio elements
4. **Structured output**: Request specific formats when needed

### Error Handling
1. **Validate URLs first**: Use `validate_youtube_url` before creating sessions
2. **Check file sizes**: Ensure local videos are under 2GB
3. **Monitor sessions**: Use `get_server_stats` to check system health
4. **Handle timeouts**: Be aware of session expiration times

## 🎓 Example Workflows by Use Case

### Academic Research
```python
# Literature review of video sources
sessions = []
video_urls = ["url1", "url2", "url3"]

for i, url in enumerate(video_urls):
    session = create_video_session(
        description=f"Research video {i+1} analysis for literature review",
        video_source=url,
        session_name=f"Research Video {i+1}"
    )
    sessions.append(session)
    
    # Standard analysis for each
    analyze_video_in_session(
        session["session_id"],
        "What is the main research question or hypothesis? What methodology is used?"
    )
```

### Content Creation
```python
# Competitive analysis
session = create_video_session(
    description="Analyze competitor content for insights and gaps",
    video_source="competitor_video_url",
    session_name="Competitor Analysis"
)

analyze_video_in_session(session["session_id"], "What content structure and format is used?")
analyze_video_in_session(session["session_id"], "What engagement techniques are employed?")
analyze_video_in_session(session["session_id"], "What topics or angles are missing that we could cover?")
```

### Training Development
```python
# Evaluate existing training effectiveness
session = create_video_session(
    description="Training video effectiveness evaluation",
    video_source="/training/current_module.mp4",
    source_type="local_file"
)

analyze_video_in_session(session["session_id"], "How clearly are learning objectives communicated?")
analyze_video_in_session(session["session_id"], "What interactive or engagement elements are used?")
analyze_video_in_session(session["session_id"], "How could this training be improved for better retention?")
```

## 🤖 Integration with AI Workflows

This MCP server is designed to integrate seamlessly with AI assistants and automation workflows:

1. **Claude Desktop Integration**: Add to MCP configuration for direct access
2. **API Integration**: Use tools programmatically in larger AI systems  
3. **Workflow Automation**: Chain video analysis with other AI tasks
4. **Knowledge Building**: Use session persistence to build comprehensive understanding

The session-based approach enables sophisticated AI workflows that can maintain context across multiple video analysis tasks, making it ideal for research, education, and content analysis applications.