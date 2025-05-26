# Contributing to YouTube Gemini MCP Server

Thank you for your interest in contributing to the YouTube Gemini MCP Server! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

We welcome contributions in the form of:

- **Bug reports** and **feature requests** via GitHub Issues
- **Code contributions** via Pull Requests
- **Documentation improvements**
- **Testing** and **quality assurance**
- **Community support** and **discussions**

## 🛠️ Development Setup

### Prerequisites

- **Python 3.10+** (3.11+ recommended)
- **Poetry** for dependency management
- **Git** for version control
- **Google AI API Key** for testing (optional for non-integration tests)

### Setup Steps

1. **Fork the Repository**
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/your-username/youtube-gemini-mcp.git
cd youtube-gemini-mcp
```

2. **Set Up Development Environment**
```bash
# Install dependencies
poetry install

# Set up pre-commit hooks (recommended)
poetry run pre-commit install

# Copy environment template
cp .env.example .env
# Add your GOOGLE_API_KEY if testing integration features
```

3. **Verify Setup**
```bash
# Run tests
poetry run pytest

# Check code quality
poetry run mypy src/
poetry run black --check src/ tests/
poetry run isort --check src/ tests/
```

## 📝 Code Style and Standards

### Python Code Standards

**Type Hints**: Required for all public functions and methods
```python
def create_session(description: str, video_source: str) -> Dict[str, Any]:
    """Function with proper type hints."""
    pass
```

**Docstrings**: Google-style docstrings for all public functions
```python
def analyze_video(video_url: str, prompt: str) -> Dict[str, Any]:
    """Analyze video content using Gemini.
    
    Args:
        video_url: YouTube URL or local file path
        prompt: Analysis instruction for the AI
        
    Returns:
        Dictionary containing success status and analysis results
        
    Raises:
        ValueError: If video_url format is invalid
    """
```

**Error Handling**: Structured responses following established patterns
```python
@mcp.tool()
def example_tool(param: str) -> Dict[str, Any]:
    """Tool with proper error handling."""
    try:
        # Implementation
        return {"success": True, "result": data}
    except Exception as e:
        logger.error(f"Tool failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "specific_error_category"
        }
```

### Code Formatting

We use automated tools to maintain consistent code style:

```bash
# Format code
poetry run black src/ tests/

# Sort imports
poetry run isort src/ tests/

# Type checking
poetry run mypy src/
```

**Configuration**: All tools are configured in `pyproject.toml`
- **Black**: Line length 88, consistent with project standards
- **isort**: Black-compatible profile
- **MyPy**: Strict mode with external library ignores

### Testing Standards

**Test Coverage**: All new functionality must include tests
```python
def test_new_feature():
    """Test new feature with descriptive name."""
    # Arrange
    input_data = "test_input"
    
    # Act
    result = new_feature(input_data)
    
    # Assert
    assert result["success"] is True
    assert "expected_key" in result
```

**Mock External APIs**: Use mocks for Google APIs and external services
```python
@patch('youtube_gemini_mcp.gemini_client.genai.Client')
def test_gemini_integration(mock_client):
    """Test Gemini integration with mocked API."""
    mock_client.return_value.models.generate_content.return_value.text = "test response"
    # Test implementation
```

## 🔄 Development Workflow

### 1. Creating Issues

**Bug Reports**: Use the bug report template
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS)
- Relevant logs or error messages

**Feature Requests**: Use the feature request template
- Clear description of the proposed feature
- Use cases and benefits
- Potential implementation approach
- Consideration of breaking changes

### 2. Working on Issues

**Claiming Issues**: Comment on issues you'd like to work on
**Discussion**: Engage in issue discussions before starting work
**Scope**: Keep changes focused on the specific issue

### 3. Pull Request Process

#### Before Creating a PR

1. **Create Feature Branch**
```bash
git checkout -b feature/descriptive-name
# or
git checkout -b fix/issue-number-description
```

2. **Make Changes**
- Follow code style guidelines
- Add comprehensive tests
- Update documentation if needed
- Ensure all tests pass

3. **Quality Checks**
```bash
# Run full test suite
poetry run pytest

# Check code quality
poetry run mypy src/
poetry run black src/ tests/
poetry run isort src/ tests/

# Verify no regressions
poetry run pytest --cov
```

#### Creating the PR

**Title**: Use clear, descriptive titles
- ✅ "Add timestamp-range analysis for video segments"
- ✅ "Fix session cleanup race condition in SessionManager"
- ❌ "Update code"
- ❌ "Fix bug"

**Description**: Use the PR template
- Summary of changes
- Related issues (use "Fixes #123" or "Closes #123")
- Testing performed
- Breaking changes (if any)
- Screenshots/examples (if applicable)

**Checklist**: Complete the PR checklist
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Code style checks pass
- [ ] No breaking changes (or properly documented)
- [ ] Related issues linked

#### Review Process

1. **Automated Checks**: All CI checks must pass
2. **Code Review**: At least one maintainer review required
3. **Address Feedback**: Respond to review comments promptly
4. **Final Approval**: Maintainer approval before merge

### 4. Commit Message Guidelines

**Format**: Use conventional commit format
```
type(scope): description

Optional longer description of the change.

Fixes #123
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(session): add timestamp-range analysis support

Add support for analyzing specific timestamp ranges within videos.
Users can now specify "MM:SS-MM:SS" format for focused analysis.

Fixes #45

fix(gemini): handle API rate limiting gracefully

Add exponential backoff for rate-limited requests to prevent
failures during high-usage periods.

Fixes #67
```

## 📚 Documentation Guidelines

### Code Documentation

**Inline Comments**: Explain complex logic and business rules
```python
# Files are auto-deleted after 48 hours due to Google Files API limitation
# This is a hard constraint that cannot be extended
if upload_time + timedelta(hours=48) < datetime.now():
    logger.warning("File approaching deletion deadline")
```

**API Documentation**: Document all public interfaces
```python
class SessionManager:
    """Thread-safe manager for video analysis sessions.
    
    Manages the lifecycle of video analysis sessions including creation,
    persistence, and automatic cleanup. All operations are thread-safe
    using RLock to support concurrent access.
    
    Attributes:
        max_sessions: Maximum number of concurrent active sessions
        session_timeout_hours: Hours before inactive sessions are cleaned up
    """
```

### Project Documentation

**README.md**: User-focused documentation
- Clear installation instructions
- Usage examples
- Configuration options
- Troubleshooting

**LLM.md**: AI system usage guide
- Comprehensive tool documentation
- Usage patterns and examples
- Best practices
- Limitations and constraints

**DEVELOPMENT.md**: Developer-focused documentation
- Architecture overview
- Development setup
- Testing strategies
- Contribution guidelines

## 🧪 Testing Guidelines

### Test Categories

**Unit Tests**: Test individual components in isolation
```python
def test_session_creation():
    """Test SessionManager.create_session method."""
    manager = SessionManager(max_sessions=5)
    result = manager.create_session("test", "video_source")
    assert result["success"] is True
```

**Integration Tests**: Test component interactions
```python
def test_youtube_to_gemini_flow():
    """Test complete YouTube video analysis flow."""
    # Requires GOOGLE_API_KEY environment variable
    # Tests actual API integration
```

**Mock Tests**: Test external API interactions
```python
@patch('youtube_gemini_mcp.gemini_client.genai.Client')
def test_gemini_api_error_handling(mock_client):
    """Test handling of Gemini API errors."""
    mock_client.side_effect = APIError("Rate limit exceeded")
    # Test error handling
```

### Test Running

```bash
# All tests
poetry run pytest

# Unit tests only
poetry run pytest tests/unit/

# Integration tests (requires API key)
GOOGLE_API_KEY="your_key" poetry run pytest tests/integration/

# Coverage report
poetry run pytest --cov=youtube_gemini_mcp --cov-report=html
```

## 🚀 Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. **Update Version**
```toml
# pyproject.toml
version = "0.2.0"
```

2. **Update Changelog**
- Document new features
- List bug fixes
- Note breaking changes
- Include migration guides

3. **Quality Assurance**
```bash
poetry run pytest
poetry run mypy src/
poetry install  # Test fresh install
```

4. **Documentation Review**
- Update README.md if needed
- Review LLM.md for new features
- Check DEVELOPMENT.md for accuracy

5. **Create Release**
```bash
git tag v0.2.0
git push origin v0.2.0
```

## 🏆 Recognition

Contributors are recognized in several ways:

- **CONTRIBUTORS.md**: Listed in the contributors file
- **GitHub Releases**: Mentioned in release notes
- **Documentation**: Author attribution for significant contributions
- **Issues/PRs**: Thanks and recognition in issue/PR comments

## 🎯 Areas for Contribution

We particularly welcome contributions in these areas:

### High Priority
- **Performance Optimization**: Session management, memory usage
- **Error Handling**: More robust error recovery and reporting
- **Testing**: Integration tests, edge case coverage
- **Documentation**: Usage examples, troubleshooting guides

### Medium Priority
- **New Features**: Additional analysis tools, export formats
- **UI/UX**: Better error messages, user feedback
- **Monitoring**: Health checks, metrics collection
- **Security**: Input validation, rate limiting

### Good First Issues
- **Documentation**: Fix typos, improve clarity
- **Testing**: Add test cases for existing functionality
- **Code Quality**: Improve type hints, add docstrings
- **Examples**: Create usage examples and tutorials

## 📞 Getting Help

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Code Review**: In-line comments on PRs
- **Documentation**: Check existing docs first

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to the YouTube Gemini MCP Server! Your contributions help make video analysis more accessible and powerful for everyone.