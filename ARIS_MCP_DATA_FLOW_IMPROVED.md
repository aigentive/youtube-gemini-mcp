# ARIS MCP Data Flow: Improved with Native Workspace Support

**Key Improvement:** Move workspace functionality into ARIS core, simplify MCP orchestration, and use automatic workspace variable injection  
**Result:** Cleaner profiles, simpler MCP tools, and more intuitive default behavior  

## The Improved Architecture

### **Native ARIS Workspace Integration**

#### **1. ARIS CLI Workspace Support**
```bash
# Default: Use current working directory (no workspace isolation)
$ aris --profile some_profile
# Working directory: wherever user is (./research_results.md, ./output.json)

# Named workspace: Create/use subdirectory in CWD
$ aris --profile some_profile --workspace my-project
# Working directory: ./my-project/ (auto-created if needed)

# Full path workspace: Use specific path
$ aris --profile some_profile --workspace /full/path/to/workspace
# Working directory: /full/path/to/workspace/

# Relative path workspace: Use relative path from CWD
$ aris --profile some_profile --workspace ../other-project
# Working directory: ../other-project/
```

#### **2. Automatic Workspace Variable Injection**
```python
# In ARIS profile execution:
def execute_profile_with_workspace(profile, workspace_path=None):
    # Resolve workspace path
    if workspace_path:
        if os.path.isabs(workspace_path):
            resolved_workspace = workspace_path
        else:
            resolved_workspace = os.path.join(os.getcwd(), workspace_path)
    else:
        resolved_workspace = os.getcwd()
    
    # Ensure workspace exists
    os.makedirs(resolved_workspace, exist_ok=True)
    
    # Change to workspace directory
    original_cwd = os.getcwd()
    os.chdir(resolved_workspace)
    
    # Inject workspace variable into profile
    profile_variables = {
        'workspace': resolved_workspace,
        'workspace_name': os.path.basename(resolved_workspace),
        **existing_profile_variables
    }
    
    try:
        # Execute profile with workspace context
        execute_profile(profile, profile_variables)
    finally:
        # Restore original directory
        os.chdir(original_cwd)
```

#### **3. Automatic System Prompt Enhancement**
```python
def enhance_system_prompt_with_workspace(system_prompt, workspace_path):
    """Automatically inject workspace context into system prompt."""
    
    workspace_context = f"""
## Workspace Information
Your workspace directory is: {workspace_path}
Use this workspace for reading previous work and saving your outputs.
When referencing files, you can use relative paths from your workspace.
"""
    
    # Inject workspace context into system prompt
    enhanced_prompt = system_prompt + "\n" + workspace_context
    return enhanced_prompt
```

## Simplified Visual Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│  USER: "Create LinkedIn content about AI automation"        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              ARIS Master Instance                           │
│           (orchestrator_master profile)                     │
│           Running in: ~/projects/my-content/                │
│                                                             │
│  🤖 "I'll coordinate a content creation workflow"           │
│  📁 Will create: ./ai-automation-content/                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                PHASE 1: RESEARCH                            │
│                                                             │
│  Master calls MCP tool:                                     │
│  execute_workflow_phase(                                    │
│    profile="content_research_analyst",                      │
│    workspace="ai-automation-content",                       │
│    instruction="Research AI automation trends..."           │
│  )                                                          │
│                                                             │
│  MCP executes:                                              │
│  echo "Research AI automation..." | \                       │
│    aris --profile content_research_analyst \                │
│         --workspace ai-automation-content                   │
│                                                             │
│  🔍 Research Agent runs in: ./ai-automation-content/        │
│  📂 Workspace variable: "./ai-automation-content"           │
│  📂 Saves: research_results.md (relative to workspace)      │
│  📂 Saves: research_data.json                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                PHASE 2: STRATEGY                            │
│                                                             │
│  Master calls MCP tool:                                     │
│  execute_workflow_phase(                                    │
│    profile="content_strategist",                            │
│    workspace="ai-automation-content",                       │
│    instruction="Create content strategy from research..."   │
│  )                                                          │
│                                                             │
│  MCP executes:                                              │
│  echo "Create content strategy..." | \                      │
│    aris --profile content_strategist \                      │
│         --workspace ai-automation-content                   │
│                                                             │
│  📊 Strategy Agent runs in: ./ai-automation-content/        │
│  📂 Reads: research_results.md (in workspace)               │
│  📂 Saves: content_strategy.md                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                PHASE 3: WRITING                             │
│                                                             │
│  Master calls MCP tool:                                     │
│  execute_workflow_phase(                                    │
│    profile="linkedin_content_writer",                       │
│    workspace="ai-automation-content",                       │
│    instruction="Write LinkedIn post using research..."      │
│  )                                                          │
│                                                             │
│  MCP executes:                                              │
│  echo "Write LinkedIn post..." | \                          │
│    aris --profile linkedin_content_writer \                 │
│         --workspace ai-automation-content                   │
│                                                             │
│  ✍️ Writing Agent runs in: ./ai-automation-content/         │
│  📂 Reads: research_results.md, content_strategy.md         │
│  📂 Saves: linkedin_post.md                                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                PHASE 4: VISUALS                             │
│                                                             │
│  Master calls MCP tool:                                     │
│  execute_workflow_phase(                                    │
│    profile="visual_content_creator",                        │
│    workspace="ai-automation-content",                       │
│    instruction="Create supporting visuals for post..."      │
│  )                                                          │
│                                                             │
│  MCP executes:                                              │
│  echo "Create supporting visuals..." | \                    │
│    aris --profile visual_content_creator \                  │
│         --workspace ai-automation-content                   │
│                                                             │
│  🎨 Visual Agent runs in: ./ai-automation-content/          │
│  📂 Reads: linkedin_post.md                                 │
│  📂 Saves: images/linkedin_hero.png                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              MASTER ARIS READS RESULTS                      │
│                                                             │
│  📂 Reads: ./ai-automation-content/linkedin_post.md         │
│  📂 Reads: ./ai-automation-content/images/                  │
│                                                             │
│  🎯 "Here's your complete content package in               │
│      ./ai-automation-content/"                              │
└─────────────────────────────────────────────────────────────┘
```

## Dramatically Simplified Profiles

### **Research Analyst Profile (Simplified)**
```yaml
# content_research_analyst.yaml
profile_name: content_research_analyst
description: Content research specialist using YouTube analysis
system_prompt: |
  You are an expert content research strategist.
  
  Your task:
  1. Research the requested topic using YouTube analysis tools
  2. Save your findings in research_results.md
  3. Save structured data in research_data.json
  
  Include in your research:
  - Key insights and trends
  - Video sources and metrics  
  - Content angle recommendations
  
  Your research will be used by strategy and writing teams.
  
  # Workspace: {workspace}
  Save all outputs to your workspace using relative paths.

tools:
  - "mcp__youtube-gemini-mcp-dev__create_video_session"
  - "mcp__youtube-gemini-mcp-dev__analyze_video_in_session"
  - "Write"
  - "Read"
  - "Glob"
```

### **Content Strategist Profile (Simplified)**
```yaml
# content_strategist.yaml
profile_name: content_strategist  
description: Strategic content planning expert
system_prompt: |
  You are a strategic content expert.
  
  Your task:
  1. Read research_results.md to understand the research findings
  2. Create content strategy and save as content_strategy.md
  3. Include strategy data in strategy_data.json
  
  Your strategy should include:
  - Content angle and unique perspective
  - Target audience and key messages
  - Format recommendations and success metrics
  
  The writing team will use your strategy to create content.
  
  # Workspace: {workspace}
  Read research files and save strategy files in your workspace.

tools:
  - "Read"
  - "Write"
  - "Glob"
```

### **LinkedIn Writer Profile (Simplified)**
```yaml
# linkedin_content_writer.yaml
profile_name: linkedin_content_writer
description: Expert LinkedIn content writer
system_prompt: |
  You are an expert LinkedIn content writer.
  
  Your task:
  1. Read research_results.md and content_strategy.md for context
  2. Write a compelling LinkedIn post and save as linkedin_post.md
  3. Save metadata in post_data.json
  
  Post requirements:
  - ~400 words, professional yet engaging
  - Include compelling hook from strategy
  - Optimized for LinkedIn engagement
  
  # Workspace: {workspace}
  Read previous work and save your post in the workspace.

tools:
  - "Read"
  - "Write"
  - "Glob"
```

### **Visual Creator Profile (Simplified)**
```yaml
# visual_content_creator.yaml
profile_name: visual_content_creator
description: Visual content specialist with image generation
system_prompt: |
  You are a visual content specialist.
  
  Your task:
  1. Read linkedin_post.md to understand content themes
  2. Create supporting visuals using image generation tools
  3. Save images to images/ subdirectory
  4. Create visual_summary.md describing the visuals
  
  Create 1-2 professional images that:
  - Support the LinkedIn post content
  - Are optimized for social media
  - Match professional brand standards
  
  # Workspace: {workspace}
  Read the post content and save visuals in workspace/images/

tools:
  - "mcp__openai-image-mcp__create_image_session"
  - "mcp__openai-image-mcp__generate_image_in_session"
  - "Read"
  - "Write"
  - "Glob"
```

## Dramatically Simplified MCP Implementation

### **Single Simple MCP Tool**
```python
import subprocess
import os
from typing import Dict, Any

@mcp.tool()
def execute_workflow_phase(
    profile: str,
    workspace: str,
    instruction: str,
    timeout: int = 300
) -> Dict[str, Any]:
    """
    Execute ARIS profile with workspace support.
    
    Args:
        profile: ARIS profile name
        workspace: Workspace directory name/path
        instruction: Task instruction
        timeout: Execution timeout
    """
    try:
        # Build simple ARIS command - let ARIS handle workspace management
        cmd = [
            "aris",
            "--profile", profile,
            "--workspace", workspace
        ]
        
        # Execute with natural language instruction via stdin
        process = subprocess.run(
            cmd,
            input=instruction,
            text=True,
            capture_output=True,
            timeout=timeout
        )
        
        if process.returncode == 0:
            return {
                "success": True,
                "profile": profile,
                "workspace": workspace,
                "response": process.stdout.strip()
            }
        else:
            return {
                "success": False,
                "error": process.stderr,
                "profile": profile
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "profile": profile
        }
```

## Master Orchestrator Profile (Simplified)

```yaml
# orchestrator_master.yaml
profile_name: orchestrator_master
description: Content workflow orchestrator using native ARIS workspace support
system_prompt: |
  You are a content workflow orchestrator that coordinates multi-phase content creation.
  
  When users request content creation, you will:
  1. Generate a workspace name based on the topic (e.g., "ai-automation-content")
  2. Execute each workflow phase in sequence using execute_workflow_phase
  3. Coordinate between phases using shared workspace files
  4. Present final deliverables to the user
  
  **Workflow Phases:**
  1. **Research**: Use "content_research_analyst" profile to research topic and save findings
  2. **Strategy**: Use "content_strategist" profile to create strategy from research
  3. **Writing**: Use "linkedin_content_writer" profile to write content using research+strategy
  4. **Visuals**: Use "visual_content_creator" profile to create supporting images
  
  **For each phase:**
  - Use execute_workflow_phase tool with appropriate profile, workspace, and instruction
  - Check if the phase completed successfully before moving to next phase
  - Read the outputs between phases to provide continuity
  
  **Workspace Management:**
  - Generate clean workspace names from topics (e.g., "AI automation trends" → "ai-automation-trends-content")
  - Use the same workspace for all phases so they can share files
  - Present final workspace location to user with all deliverables
  
  Be conversational and explain what you're doing at each step.

tools:
  - "mcp__aris-workflow-mcp__execute_workflow_phase"
  - "Read"
  - "Write"
  - "Glob"
  - "LS"

welcome_message: |
  🎯 Content Workflow Orchestrator ready!
  
  I coordinate multi-phase content creation with automatic workspace management:
  • Research phase analyzes trending content
  • Strategy phase creates content framework  
  • Writing phase produces LinkedIn posts
  • Visual phase generates supporting images
  
  All deliverables are organized in persistent workspace directories.
  What content would you like to create?
```

## Required ARIS Core Changes

### **1. CLI Arguments**
```python
# In cli_args.py
parser.add_argument(
    "--workspace",
    type=str,
    help="Workspace directory (relative to CWD or absolute path)"
)

parser.add_argument(
    "--input",
    type=str,
    help="Input prompt (automatically switches to non-interactive mode)"
)
```

### **2. Automatic Non-Interactive Mode**
```python
# In main ARIS execution
def main():
    args = parse_args()
    
    # Setup workspace
    workspace_path = setup_workspace(args.workspace)
    
    # Load profile with workspace variables
    profile = load_profile_with_workspace(args.profile, workspace_path)
    
    if args.input:
        # Non-interactive mode: --input provided
        user_input = args.input
        
        # Execute single conversation turn
        response = execute_single_turn(profile, user_input)
        print(response)
        sys.exit(0)
    else:
        # Check if stdin has input (for MCP usage)
        if not sys.stdin.isatty():
            # Non-interactive mode: input from stdin
            user_input = sys.stdin.read().strip()
            
            if user_input:
                response = execute_single_turn(profile, user_input)
                print(response)
                sys.exit(0)
        
        # Interactive mode: start chat loop
        start_chat_session(profile)

def execute_single_turn(profile, user_input):
    """Execute single request/response turn for non-interactive mode."""
    # Initialize conversation with profile
    conversation = initialize_conversation(profile)
    
    # Process user input and get response
    response = process_user_input(conversation, user_input)
    
    return response
```

### **3. Workspace Resolution in ARIS Core**
```python
# In main ARIS execution
def setup_workspace(workspace_arg):
    """Setup workspace and return resolved path."""
    if workspace_arg:
        if os.path.isabs(workspace_arg):
            workspace_path = workspace_arg
        else:
            workspace_path = os.path.join(os.getcwd(), workspace_arg)
        
        # Create workspace if it doesn't exist
        os.makedirs(workspace_path, exist_ok=True)
        
        # Change to workspace directory
        os.chdir(workspace_path)
        
        return workspace_path
    else:
        # Use current working directory
        return os.getcwd()
```

### **4. Automatic Variable Injection**
```python
# In profile loading/execution
def load_profile_with_workspace(profile_path, workspace_path):
    """Load profile and inject workspace variables."""
    profile = load_profile(profile_path)
    
    # Inject workspace variables
    workspace_variables = {
        'workspace': workspace_path,
        'workspace_name': os.path.basename(workspace_path)
    }
    
    # Add to profile variables
    profile['variables'] = {**profile.get('variables', {}), **workspace_variables}
    
    # Enhance system prompt with workspace context
    workspace_context = f"\n\n## Workspace\nYour workspace is: {workspace_path}\nSave outputs and read inputs relative to this workspace."
    profile['system_prompt'] = profile.get('system_prompt', '') + workspace_context
    
    return profile
```

## Usage Examples

### **Simple Default Usage (Interactive)**
```bash
cd ~/projects/my-content
$ aris --profile orchestrator_master

User: "Create LinkedIn content about AI automation"
# Creates: ./ai-automation-content/
# All work happens in organized subdirectory
```

### **Non-Interactive Mode with --input Flag**
```bash
cd ~/projects/my-content
$ aris --profile content_research_analyst \
       --workspace ai-automation-content \
       --input "Research AI automation trends using YouTube analysis"

# --input automatically switches to non-interactive mode
# Executes single turn and exits
# Saves: ./ai-automation-content/research_results.md
```

### **Non-Interactive Mode with stdin (MCP Usage)**
```bash
cd ~/projects/my-content
echo "Research AI automation trends using YouTube analysis" | \
  aris --profile content_research_analyst \
       --workspace ai-automation-content

# stdin input automatically switches to non-interactive mode
# This is how the MCP execute_workflow_phase tool works
```

### **Master Orchestrator with --input**
```bash
cd ~/projects/my-content
$ aris --profile orchestrator_master \
       --input "Create LinkedIn content about AI automation trends"

# Master automatically generates workspace name and coordinates phases
# Creates: ./ai-automation-trends-content/
# Executes all 4 phases in sequence and exits
```

### **Custom Workspace with --input**
```bash
cd ~/projects/my-content
$ aris --profile orchestrator_master \
       --workspace q4-ai-campaign \
       --input "Create content about AI automation for Q4 campaign"

# Uses specified workspace instead of auto-generated name
# Creates: ./q4-ai-campaign/
# Executes all 4 phases in sequence and exits
```

### **Direct Phase Usage (Interactive)**
```bash
cd ~/projects/my-content
$ aris --profile content_research_analyst --workspace my-research

User: "Research AI automation trends for marketing"
# Agent works in: ./my-research/
# Saves: ./my-research/research_results.md
# Uses {workspace} variable: "./my-research"
```

### **Direct Phase Usage with --input**
```bash
cd ~/projects/my-content
$ aris --profile content_research_analyst \
       --workspace my-research \
       --input "Research AI automation trends for marketing"

# Non-interactive single phase execution
# Agent works in: ./my-research/
# Saves: ./my-research/research_results.md
# Exits after completion
```

## Key Benefits of This Approach

### **1. Native Integration** 🎯
- Workspace is core ARIS functionality
- Consistent across all profiles and use cases
- No external dependencies for workspace management

### **2. Simplified Everything** ⚡
- **Profiles**: Just use `{workspace}` variable, no complex instructions
- **MCP Tools**: Simple orchestration, no file management
- **User Experience**: Intuitive default behavior (CWD)

### **3. Flexible Defaults** 📁
- No workspace flag = use current directory
- Workspace flag = create/use subdirectory
- Full paths supported for advanced use cases

### **4. Clean Separation** 🏗️
- **ARIS Core**: Handles workspace, variables, file operations
- **MCP Tools**: Handle orchestration and coordination
- **Profiles**: Focus on their specific expertise

### **5. Backwards Compatible** ↗️
- Existing profiles work without changes
- New `{workspace}` variable is optional
- Graceful fallback to CWD behavior

## Summary

**This approach moves workspace management where it belongs - into ARIS core - and simplifies everything else:**

1. **ARIS gets native `--workspace` support** with automatic variable injection
2. **Profiles become much simpler** with automatic workspace context
3. **MCP tools focus on orchestration** rather than file management  
4. **Default behavior is intuitive** (CWD unless specified)
5. **User experience is streamlined** with organized, persistent outputs

**Result:** A much cleaner, more maintainable, and more intuitive system! 🚀