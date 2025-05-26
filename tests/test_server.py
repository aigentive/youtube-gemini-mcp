"""Basic tests for the YouTube Gemini MCP Server."""

import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_import_server():
    """Test that the server module can be imported without errors."""
    try:
        from youtube_gemini_mcp import server

        assert server is not None

        # Test that key components are available
        assert hasattr(server, "create_video_session")
        assert hasattr(server, "analyze_video_in_session")
        assert hasattr(server, "get_usage_guide")
        assert hasattr(server, "mcp")
        assert hasattr(server, "main")
    except ImportError as e:
        pytest.fail(f"Failed to import server module: {e}")


def test_environment_variable_check():
    """Test environment variable validation."""
    with patch.dict(os.environ, {}, clear=True):
        with patch("youtube_gemini_mcp.server.logger") as mock_logger:
            with patch("youtube_gemini_mcp.server.mcp.run") as mock_run:
                from youtube_gemini_mcp.server import main

                main()

                # Should log error and not run server
                mock_logger.error.assert_called_with(
                    "CRITICAL_MAIN: GOOGLE_API_KEY environment variable is required. Server cannot start."
                )
                mock_run.assert_not_called()


def test_get_usage_guide():
    """Test usage guide tool functionality."""
    try:
        from youtube_gemini_mcp.server import get_usage_guide

        # Mock the global instances to avoid initialization
        with patch("youtube_gemini_mcp.server.session_manager", None):
            result = get_usage_guide()

            assert result["success"] is True
            assert "server_info" in result
            assert "key_features" in result
            assert "workflow_examples" in result
            assert result["server_info"]["name"] == "YouTube Gemini MCP Server"

    except Exception as e:
        pytest.fail(f"get_usage_guide failed: {e}")


def test_session_manager_import():
    """Test that SessionManager can be imported and initialized."""
    try:
        from youtube_gemini_mcp.session_manager import SessionManager, VideoSession

        # Test basic initialization
        manager = SessionManager(max_sessions=5, session_timeout_hours=1.0)
        assert manager.max_sessions == 5
        assert manager.session_timeout_hours == 1.0
        assert isinstance(manager.sessions, dict)

    except Exception as e:
        pytest.fail(f"SessionManager import/init failed: {e}")


def test_youtube_validator_import():
    """Test that YouTubeValidator can be imported."""
    try:
        from youtube_gemini_mcp.youtube_validator import YouTubeValidator

        validator = YouTubeValidator()
        assert validator is not None

    except Exception as e:
        pytest.fail(f"YouTubeValidator import failed: {e}")


def test_gemini_client_import():
    """Test that GeminiClient can be imported (without API key)."""
    try:
        from youtube_gemini_mcp.gemini_client import GeminiClient

        # Should be importable even without API key
        assert GeminiClient is not None

    except Exception as e:
        pytest.fail(f"GeminiClient import failed: {e}")


def test_files_uploader_import():
    """Test that FilesUploader can be imported."""
    try:
        from youtube_gemini_mcp.files_uploader import FilesUploader

        assert FilesUploader is not None

    except Exception as e:
        pytest.fail(f"FilesUploader import failed: {e}")
