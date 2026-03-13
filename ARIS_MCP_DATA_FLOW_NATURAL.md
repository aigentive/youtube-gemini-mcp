# ARIS MCP Data Flow: Natural Agentic Approach

**Insight:** Claude CLI is already a full agentic system with filesystem tools - let's use its natural capabilities instead of building complex orchestration  
**Approach:** Simple file-based workflow using Claude's existing Read/Write tools, enhanced system prompts, and standardized workspace management  

## The Natural Way (Much Simpler!)

### **Key Realization:**
Claude CLI already has:
- ✅ **File reading/writing tools** (Read, Write, Glob, etc.)
- ✅ **Complex reasoning capabilities** 
- ✅ **Ability to follow multi-step instructions**
- ✅ **Natural workflow understanding**

**What we actually need:** Just tell each profile where to find previous work and where to save results, plus a standardized workspace convention!

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
│                                                             │
│  🤖 "I'll coordinate a content creation workflow"           │
│  📁 Creates: workspaces/ai-automation-content/              │
│  📋 Calls each phase with workspace instructions            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                PHASE 1: RESEARCH                            │
│                                                             │
│  Master ARIS calls:                                         │
│  execute_workflow_phase(                                    │
│    profile="content_research_analyst",                      │
│    workspace="workspaces/ai-automation-content",            │
│    instruction="Research AI automation trends"              │
│  )                                                          │
│                                                             │
│  🔍 Research Agent:                                         │
│  📂 Reads: workspaces/ai-automation-content/instructions.md │
│  📂 Uses YouTube MCP to analyze videos                      │
│  📂 Writes: workspaces/ai-automation-content/research_results.md │
│  📂 Writes: workspaces/ai-automation-content/research_data.json │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                PHASE 2: STRATEGY                            │
│                                                             │
│  Master ARIS calls:                                         │
│  execute_workflow_phase(                                    │
│    profile="content_strategist",                            │
│    workspace="workspaces/ai-automation-content",            │
│    instruction="Create content strategy"                    │
│  )                                                          │
│                                                             │
│  📊 Strategy Agent:                                         │
│  📂 Reads: workspaces/ai-automation-content/research_results.md │
│  📂 Reads: workspaces/ai-automation-content/research_data.json │
│  📂 Creates content strategy                                │
│  📂 Writes: workspaces/ai-automation-content/content_strategy.md │
│  📂 Writes: workspaces/ai-automation-content/strategy_data.json │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                PHASE 3: WRITING                             │
│                                                             │
│  Master ARIS calls:                                         │
│  execute_workflow_phase(                                    │
│    profile="linkedin_content_writer",                       │
│    workspace="workspaces/ai-automation-content",            │
│    instruction="Write LinkedIn post"                        │
│  )                                                          │
│                                                             │
│  ✍️ Writing Agent:                                          │
│  📂 Reads: workspaces/ai-automation-content/research_results.md │
│  📂 Reads: workspaces/ai-automation-content/content_strategy.md │
│  📂 Writes LinkedIn post                                    │
│  📂 Writes: workspaces/ai-automation-content/linkedin_post.md │
│  📂 Writes: workspaces/ai-automation-content/post_data.json │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                PHASE 4: VISUALS                             │
│                                                             │
│  Master ARIS calls:                                         │
│  execute_workflow_phase(                                    │
│    profile="visual_content_creator",                        │
│    workspace="workspaces/ai-automation-content",            │
│    instruction="Create supporting visuals"                  │
│  )                                                          │
│                                                             │
│  🎨 Visual Agent:                                           │
│  📂 Reads: workspaces/ai-automation-content/linkedin_post.md │
│  📂 Uses OpenAI Image MCP to create visuals                 │
│  📂 Writes: workspaces/ai-automation-content/images/image1.png │
│  📂 Writes: workspaces/ai-automation-content/visual_summary.md │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              MASTER ARIS FINAL STEP                         │
│                                                             │
│  📂 Reads: workspaces/ai-automation-content/linkedin_post.md │
│  📂 Reads: workspaces/ai-automation-content/visual_summary.md │
│  📂 Reads: workspaces/ai-automation-content/images/         │
│                                                             │
│  🎯 "Here's your complete content package:"                 │
│  📝 LinkedIn post: [content]                                │
│  🖼️ Supporting images: [files]                              │
│  📊 Research insights: [summary]                            │
│  ✅ Ready for review/publishing                             │
└─────────────────────────────────────────────────────────────┘
```

## Workspace Structure & Management

### **Default Workspace Convention**
```
workspaces/                     # Default parent directory
├── ai-automation-content/      # Auto-generated from topic
│   ├── instructions.md         # Master instructions
│   ├── research_results.md     # Human-readable research summary
│   ├── research_data.json      # Structured research data
│   ├── content_strategy.md     # Strategy document
│   ├── strategy_data.json      # Structured strategy data
│   ├── linkedin_post.md        # Final LinkedIn post (deliverable!)
│   ├── post_data.json         # Post metadata
│   ├── visual_summary.md       # Visual creation summary
│   └── images/                 # Deliverable assets!
│       ├── linkedin_image.png
│       └── carousel_slide.png
├── marketing-strategy-content/ # Another workflow
└── product-launch-content/     # Another workflow
```

### **Workspace CLI Flags**
```bash
# Default: Auto-generate workspace in workspaces/ directory
$ aris --profile orchestrator_master
# Creates: workspaces/{topic-sanitized}/

# Custom workspace directory name
$ aris --profile orchestrator_master --workspace my-campaign
# Creates: workspaces/my-campaign/

# Custom full workspace path
$ aris --profile orchestrator_master --workspace-path ./custom/location/my-project
# Creates: ./custom/location/my-project/

# Custom parent directory for auto-generated workspaces
$ aris --profile orchestrator_master --workspace-parent ./my-projects
# Creates: ./my-projects/{topic-sanitized}/
```

### **Workspace Benefits:**
- 📁 **Organized storage** - All workflows in `workspaces/` directory
- 🔄 **Version control ready** - Can be committed to git
- 👀 **Easy review** - Human can inspect and edit results
- 🔗 **Reusable assets** - Images and content can be referenced later
- 📝 **Documentation** - Full workflow history preserved
- 🏗️ **Scalable** - Multiple workflows can coexist

## Enhanced Profile System Prompts (The Secret Sauce)

### **Research Analyst Profile** 
```yaml
# content_research_analyst.yaml
system_prompt: |
  You are an expert content research strategist with access to file system tools.
  
  WORKFLOW INSTRUCTIONS:
  1. Check for workspace/instructions.md to understand the overall project
  2. Research the topic using YouTube analysis tools
  3. Save your findings in TWO formats:
     - workspace/research_results.md (human-readable summary for next agents)
     - workspace/research_data.json (structured data for reference)
  
  When you save results, include:
  - Executive summary of research findings
  - Key insights and trends discovered
  - Video sources and metrics
  - Recommendations for content angles
  
  Your research will be used by the strategy and writing teams, so make it comprehensive and actionable.
```

### **Content Strategist Profile**
```yaml
# content_strategist.yaml
system_prompt: |
  You are a strategic content expert with access to file system tools.
  
  WORKFLOW INSTRUCTIONS:
  1. Read workspace/instructions.md for project context
  2. Read workspace/research_results.md for research insights
  3. Read workspace/research_data.json for detailed data
  4. Create content strategy and save in TWO formats:
     - workspace/content_strategy.md (strategy document for writers)
     - workspace/strategy_data.json (structured strategy data)
  
  Your strategy should include:
  - Content angle and unique perspective
  - Target audience definition
  - Key messages and hooks
  - Format recommendations
  - Success metrics
  
  The writing team will use your strategy to create the actual content.
```

### **LinkedIn Writer Profile**
```yaml
# linkedin_content_writer.yaml
system_prompt: |
  You are an expert LinkedIn content writer with access to file system tools.
  
  WORKFLOW INSTRUCTIONS:
  1. Read workspace/instructions.md for project context
  2. Read workspace/research_results.md for background research
  3. Read workspace/content_strategy.md for strategic direction
  4. Write LinkedIn post and save in TWO formats:
     - workspace/linkedin_post.md (final post content)
     - workspace/post_data.json (metadata: word count, key messages, etc.)
  
  Post should be:
  - ~400 words, professional yet engaging
  - Include compelling hook from strategy
  - Based on research insights
  - Optimized for LinkedIn engagement
  
  The visual team will use your post to create supporting imagery.
```

### **Visual Creator Profile**
```yaml
# visual_content_creator.yaml  
system_prompt: |
  You are a visual content specialist with access to file system and image generation tools.
  
  WORKFLOW INSTRUCTIONS:
  1. Read workspace/instructions.md for project context
  2. Read workspace/linkedin_post.md to understand content themes
  3. Create supporting visuals using image generation tools
  4. Save images to workspace/images/ directory
  5. Create workspace/visual_summary.md describing the visuals
  
  Create 1-2 professional images that:
  - Support the LinkedIn post content
  - Are optimized for social media
  - Match professional brand standards
  - Enhance the key messages
```

## MCP Tool Implementation with Workspace Management

### **Workspace Management Tools**

```python
import os
import re
from datetime import datetime
from typing import Dict, List, Any

def sanitize_workspace_name(topic: str) -> str:
    """Convert topic to filesystem-safe workspace name."""
    # Convert to lowercase, replace spaces and special chars with hyphens
    sanitized = re.sub(r'[^a-zA-Z0-9\s-]', '', topic.lower())
    sanitized = re.sub(r'\s+', '-', sanitized.strip())
    # Remove multiple consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)
    return sanitized.strip('-')

def resolve_workspace_path(
    topic: str = None,
    workspace_name: str = None, 
    workspace_path: str = None,
    workspace_parent: str = "workspaces"
) -> str:
    """
    Resolve workspace path based on CLI flags and topic.
    
    Priority:
    1. workspace_path (full path override)
    2. workspace_name (custom name in default parent)
    3. Auto-generate from topic in workspace_parent
    """
    if workspace_path:
        # Full path override
        return os.path.abspath(workspace_path)
    
    if workspace_name:
        # Custom name in workspace parent
        return os.path.join(workspace_parent, workspace_name)
    
    if topic:
        # Auto-generate from topic
        sanitized_topic = sanitize_workspace_name(topic)
        return os.path.join(workspace_parent, f"{sanitized_topic}-content")
    
    # Fallback: timestamp-based
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(workspace_parent, f"workflow_{timestamp}")

@mcp.tool()
def create_content_workflow(
    topic: str,
    workspace_name: str = None,
    workspace_path: str = None,
    workspace_parent: str = "workspaces"
) -> Dict[str, Any]:
    """
    Create a complete content workflow with proper workspace management.
    
    Args:
        topic: Content topic (e.g., "AI automation for marketing")
        workspace_name: Custom workspace directory name (optional)
        workspace_path: Full custom workspace path (optional)
        workspace_parent: Parent directory for workspaces (default: "workspaces")
    """
    try:
        # Resolve workspace path
        workspace = resolve_workspace_path(
            topic=topic,
            workspace_name=workspace_name,
            workspace_path=workspace_path,
            workspace_parent=workspace_parent
        )
        
        print(f"🎯 Creating content workflow for: {topic}")
        print(f"📁 Workspace: {workspace}")
        
        # Execute workflow phases
        phases = [
            ("content_research_analyst", f"Research {topic} trends and insights"),
            ("content_strategist", "Create content strategy based on research"),
            ("linkedin_content_writer", "Write LinkedIn post using strategy"),
            ("visual_content_creator", "Create supporting visuals for the post")
        ]
        
        results = []
        for profile, instruction in phases:
            result = execute_workflow_phase(profile, workspace, instruction)
            results.append(result)
            if result["success"]:
                print(f"✅ {profile.replace('_', ' ').title()}: {result['response'][:100]}...")
            else:
                print(f"❌ {profile.replace('_', ' ').title()}: {result['error']}")
                break
        
        # Read final deliverables
        try:
            final_post_path = os.path.join(workspace, "linkedin_post.md")
            images_dir = os.path.join(workspace, "images")
            
            deliverables = {
                "workspace": workspace,
                "linkedin_post": final_post_path if os.path.exists(final_post_path) else None,
                "images": list_files_in_directory(images_dir) if os.path.exists(images_dir) else [],
                "research": os.path.join(workspace, "research_results.md"),
                "strategy": os.path.join(workspace, "content_strategy.md")
            }
            
            return {
                "success": True,
                "topic": topic,
                "workspace": workspace,
                "deliverables": deliverables,
                "phase_results": results,
                "message": f"Content creation complete! All files available in {workspace}/"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error reading deliverables: {e}",
                "workspace": workspace,
                "phase_results": results
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "topic": topic
        }

@mcp.tool()
def execute_workflow_phase(
    profile: str,
    workspace: str, 
    instruction: str,
    timeout: int = 300
) -> Dict[str, Any]:
    """
    Execute a workflow phase using natural file-based coordination.
    
    Args:
        profile: ARIS profile to use
        workspace: Workspace directory path
        instruction: What this phase should accomplish
        timeout: Execution timeout
    """
    try:
        # Ensure workspace exists
        os.makedirs(workspace, exist_ok=True)
        
        # Create/update instructions file
        instructions_file = os.path.join(workspace, "instructions.md")
        with open(instructions_file, "w") as f:
            f.write(f"""# Workflow Instructions

## Current Phase: {profile}

## Task: {instruction}

## Workspace: {workspace}

## Previous Work:
Check this workspace for files from previous phases. Read any relevant files to understand the project context.

## Your Role:
Complete your phase of the workflow and save results appropriately for the next phase.
""")
        
        # Build ARIS command (simplified - no JSON output needed!)
        cmd = [
            "aris",
            "--profile", profile,
            "--non-interactive"
        ]
        
        # Create natural language prompt
        natural_prompt = f"""I need you to work on: {instruction}

Your workspace is: {workspace}

Please:
1. Read the instructions.md file in your workspace to understand the project
2. Check for any previous work files in the workspace
3. Complete your part of the workflow
4. Save your results appropriately for the next team member

Use your file system tools to read previous work and write your outputs."""
        
        # Execute ARIS
        process = subprocess.run(
            cmd,
            input=natural_prompt,
            text=True,
            capture_output=True,
            timeout=timeout
        )
        
        if process.returncode == 0:
            # No JSON parsing needed - natural conversation response is fine!
            return {
                "success": True,
                "profile": profile,
                "workspace": workspace,
                "response": process.stdout.strip(),  # Natural conversational response
                "files_created": list_workspace_files(workspace)
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

def list_workspace_files(workspace: str) -> List[str]:
    """List all files in workspace for result tracking."""
    files = []
    for root, dirs, filenames in os.walk(workspace):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(root, filename), workspace)
            files.append(rel_path)
    return files

def list_files_in_directory(directory: str) -> List[str]:
    """List files in a specific directory."""
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except (OSError, FileNotFoundError):
        return []
```

## Orchestrator Master Profile

```yaml
# orchestrator_master.yaml
profile_name: orchestrator_master
description: Natural workflow orchestrator using file-based coordination with workspace management
system_prompt: |
  You are a workflow orchestrator that coordinates content creation using a natural file-based approach with organized workspace management.
  
  When users request content creation, use the create_content_workflow tool which handles:
  1. Workspace creation in workspaces/ directory (organized and persistent)
  2. Sequential phase execution with proper file coordination
  3. Deliverable tracking and final results presentation
  
  Workspace Management:
  - Default: workspaces/{topic-sanitized}-content/
  - User can specify custom workspace names or paths
  - All files persist after workflow completion
  - Version control ready structure
  
  Workflow phases automatically include:
  - Research (content_research_analyst) - YouTube analysis and insights
  - Strategy (content_strategist) - Content planning and messaging
  - Writing (linkedin_content_writer) - LinkedIn post creation
  - Visuals (visual_content_creator) - Supporting image generation
  
  Each phase naturally builds on previous work by reading workspace files.

tools:
  - "mcp__aris-workflow-mcp__create_content_workflow"
  - "mcp__aris-workflow-mcp__execute_workflow_phase"
  - "Read"
  - "Write" 
  - "Glob"
  - "LS"

mcp_config_files:
  - "configs/aris-workflow.mcp-servers.json"
  - "configs/youtube-gemini.mcp-servers.json" 
  - "configs/openai-image.mcp-servers.json"

welcome_message: |
  🎯 Natural Workflow Orchestrator ready!
  
  I coordinate content creation using an organized workspace approach where:
  • Each workflow gets its own persistent directory in workspaces/
  • All phases naturally coordinate through shared files  
  • Deliverables are ready for immediate use and version control
  • Full workflow history is preserved for future reference
  
  Just tell me what content you need and I'll manage the entire workflow with proper workspace organization!
```

## Example Usage Flow

### **User Request:**
```bash
$ aris --profile orchestrator_master

User: "Create LinkedIn content about AI automation for marketing"
```

### **Master Orchestrator Response:**
```
I'll create a complete LinkedIn content package for you about AI automation for marketing. Let me coordinate this workflow with proper workspace management.

🎯 Creating content workflow for: AI automation for marketing
📁 Workspace: workspaces/ai-automation-for-marketing-content

Phase 1: Research - Analyzing trending AI automation content...
Phase 2: Strategy - Creating content strategy based on research...
Phase 3: Writing - Writing LinkedIn post using strategy...
Phase 4: Visuals - Creating supporting visuals for the post...

🎯 Content creation complete! All files available in workspaces/ai-automation-for-marketing-content/
```

### **Behind the Scenes:**
```python
# Master calls:
create_content_workflow(
    topic="AI automation for marketing"
    # workspace automatically becomes: workspaces/ai-automation-for-marketing-content/
)

# Which internally executes:
# 1. Research phase in organized workspace
# 2. Strategy phase with file coordination  
# 3. Writing phase with accumulated context
# 4. Visual phase with complete content context

# All phases naturally coordinate through the workspace files
```

## What This Eliminates

### **❌ No Longer Needed:**
- Complex session management
- JSON output mode from ARIS
- JSON extraction/parsing logic
- Context file passing mechanisms  
- Structured output requirements
- Session finalization processes
- Multiple fallback methods

### **✅ Natural Benefits:**
- **File-based coordination** - Each agent reads/writes naturally
- **Self-documenting workflow** - All work products are human-readable
- **Conversational responses** - Natural status updates, no parsing needed
- **Flexible file formats** - Agents choose best format for their output
- **Natural error recovery** - Agents can read and understand previous work
- **Debugging friendly** - Workspace shows exact state at each step

## ARIS Implementation Requirements

### **Minimal Changes Needed:**

#### **1. Non-Interactive Mode** (Essential)
```python
parser.add_argument("--non-interactive", action="store_true")
parser.add_argument("--input", type=str)
```

#### **2. Workspace Management CLI Flags** (Optional but Recommended)
```python
parser.add_argument("--workspace", type=str, help="Custom workspace directory name")
parser.add_argument("--workspace-path", type=str, help="Full custom workspace path") 
parser.add_argument("--workspace-parent", type=str, default="workspaces", help="Parent directory for workspaces")
```

#### **3. Enhanced Profile System Prompts** (Already Supported)
Just update profile YAML files with file-aware instructions.

### **That's It!** 
No JSON output mode, complex context files, session management, or extraction logic needed!

## Why This Is Brilliant

### **1. Leverages Existing Capabilities** 🎯
- Claude CLI already has Read/Write tools
- ARIS already supports rich system prompts
- Natural workflow understanding built-in

### **2. Simple and Robust** 💪
- File system is the session state
- Human-readable at every step
- Self-documenting workflow
- Easy debugging and recovery

### **3. Naturally Extensible** 🚀
- Add new phases by adding profiles
- Agents can create their own file structures  
- Works with any file format
- Easy to parallelize phases

### **4. Zero Complex Infrastructure** ⚡
- No session managers
- No context extraction
- No JSON parsing
- Just files and natural language

## Even Simpler Master Orchestrator Example

### **Natural Workflow Execution:**
```python
# Simple usage - auto-generated workspace
result = create_content_workflow("AI automation for marketing")
# Creates: workspaces/ai-automation-for-marketing-content/

# Custom workspace name
result = create_content_workflow(
    topic="AI automation for marketing",
    workspace_name="my-ai-campaign"
)
# Creates: workspaces/my-ai-campaign/

# Custom workspace path
result = create_content_workflow(
    topic="AI automation for marketing", 
    workspace_path="./projects/q4-content/ai-automation"
)
# Creates: ./projects/q4-content/ai-automation/

# Custom parent directory
result = create_content_workflow(
    topic="AI automation for marketing",
    workspace_parent="./my-content-projects"
)
# Creates: ./my-content-projects/ai-automation-for-marketing-content/
```

### **Real-World Usage Example:**

```bash
# User runs ARIS in their content project directory
cd ~/projects/my-content-repo

$ aris --profile orchestrator_master

User: "Create LinkedIn content about AI automation for marketing"

# Master orchestrator creates:
# workspaces/ai-automation-for-marketing-content/
# ├── linkedin_post.md           ← Ready to copy/paste!
# ├── images/linkedin_hero.png   ← Ready to upload!
# ├── research_results.md        ← Background research
# ├── content_strategy.md        ← Strategy notes
# └── instructions.md            ← Workflow documentation

# User can then:
git add workspaces/
git commit -m "Add AI automation LinkedIn content package"

# Or move specific deliverables:
cp workspaces/ai-automation-for-marketing-content/linkedin_post.md ./posts/
cp workspaces/ai-automation-for-marketing-content/images/* ./assets/
```

### **What Each Agent Actually Does:**

#### **Research Agent Natural Behavior:**
```
Agent reads: workspaces/ai-automation-for-marketing-content/instructions.md
Agent thinks: "I need to research AI automation trends for marketing"
Agent uses: YouTube MCP tools to analyze videos
Agent writes: workspaces/ai-automation-for-marketing-content/research_results.md with findings
Agent responds: "I've analyzed 5 trending videos about AI marketing automation. Key insights saved to research_results.md including time-saving benefits and practical applications."
```

#### **Strategy Agent Natural Behavior:**
```
Agent reads: workspaces/ai-automation-for-marketing-content/instructions.md
Agent reads: workspaces/ai-automation-for-marketing-content/research_results.md  
Agent thinks: "Based on this research, I'll create a content strategy"
Agent writes: workspaces/ai-automation-for-marketing-content/content_strategy.md
Agent responds: "Created content strategy focusing on '15 hours saved per week' angle. Strategy document includes target audience, key messages, and hooks."
```

**The conversational responses are just progress updates - the real deliverables are the persistent files!**

## Summary

**The Natural Approach:**
- Master orchestrator calls `execute_workflow_phase` for each step
- Each profile gets workspace path and natural language instruction
- Agents use existing Read/Write tools to coordinate via files
- File system becomes the shared memory
- Natural conversational responses (no JSON parsing needed!)
- Human-readable results at every step

**Required ARIS Changes:**
1. Add `--non-interactive` mode ✅
2. Update profile system prompts to be file-aware ✅

**Not Required:**
- ❌ JSON output mode
- ❌ Context file parsing  
- ❌ Session management
- ❌ Structured output extraction

**Result:** Elegant workflow orchestration using Claude's natural agentic capabilities with absolutely minimal infrastructure!