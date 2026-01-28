# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Kongtze is a Node.js project (ES modules) using the BMad Method (Build More, Architect Dreams) for project architecture, scaffolding, and AI-agent-driven development workflows.

## Commands

### Development
```bash
# Install dependencies
npm install

# Development mode with hot reload
npm run dev

# Production mode
npm start

# Run tests (not yet configured)
npm test
```

### Environment Setup
```bash
# Copy environment template
cp .env.example .env
# Edit .env with actual values
```

### BMad Method Installation
```bash
# Install BMad Method (if not already installed)
npx bmad-method@alpha install
```

## Architecture

### Core Concepts

**BMad Method Integration**: This project uses the BMad Method framework, which provides:
- **Agent-driven workflows**: Structured AI agents with specific personas (Developer, Architect, PM, QA, etc.)
- **Workflow orchestration**: Predefined workflows for planning, architecture, implementation, and testing
- **Configuration-driven**: All agent behavior is controlled via YAML configs in `_bmad/` directory
- **Multi-module system**: Separate modules for different development contexts (BMM for standard apps, BMGD for games, etc.)

### Directory Structure

```
Kongtze/
├── _bmad/                    # BMad Method configuration & workflows (git-ignored)
│   ├── _config/              # Manifests for agents, workflows, tasks
│   ├── core/                 # Core BMad agents & workflows
│   ├── bmm/                  # BMad Method Module (standard software dev)
│   ├── bmgd/                 # BMad Game Development module
│   ├── bmb/                  # BMad Builder (create agents/workflows)
│   └── cis/                  # Creative Innovation Systems module
├── _bmad-output/             # Generated artifacts from BMad workflows (git-ignored)
│   ├── planning-artifacts/   # PRDs, epics, stories, architecture docs
│   └── implementation-artifacts/  # Generated during dev workflows
├── .cursor/, .claude/, etc.  # IDE-specific BMad agent command shortcuts
├── docs/                     # Project knowledge/documentation
├── index.js                  # Main application entry point
├── package.json              # Node.js configuration (ES modules)
└── .env                      # Environment variables (git-ignored)
```

### BMad Method Workflow System

**How BMad Agents Work**:
1. Each agent has a specific persona and menu-driven interface
2. Agents load configuration from `_bmad/{module}/config.yaml` on activation
3. Workflows are defined in YAML/MD files with structured steps
4. All artifacts are generated to `_bmad-output/`

**Key Configuration Values** (from `_bmad/bmm/config.yaml`):
- `project_name`: Kongtze
- `user_name`: Frankhu
- `communication_language`: English
- `user_skill_level`: intermediate

**Common Agents**:
- `bmad-master`: Master orchestrator, lists all available tasks/workflows
- `dev`: Developer agent for implementing stories with TDD
- `architect`: Creates technical architecture documents
- `pm`: Product manager for creating PRDs and epics
- `tea`: Test Automation Engineer

**Common Workflows**:
- `dev-story`: Execute user stories with TDD (red-green-refactor cycle)
- `code-review`: Adversarial code review that must find 3-10 issues
- `create-architecture`: Generate architecture documentation
- `sprint-planning`: Plan sprints from epics
- `generate-project-context`: Create AI-optimized project context

### Application Architecture

**Entry Point**: `index.js`
- ES module format (`"type": "module"` in package.json)
- Uses dotenv for environment variable management
- Handles SIGINT/SIGTERM for graceful shutdown
- Structured with async `main()` function for startup logic

**Environment Variables**:
- `NODE_ENV`: Environment mode (defaults to 'development')
- `PORT`: Application port (defaults to 3000)
- Database and API keys can be added as needed

**Node.js Requirements**:
- Node.js >= 18.0.0 (enforced in package.json)
- ES modules enabled

## BMad Method Development Patterns

### Story-Driven Development
When implementing features:
1. Stories are created in `_bmad-output/planning-artifacts/stories/`
2. Each story contains tasks/subtasks in strict execution order
3. Developer agent (`dev`) executes tasks using red-green-refactor TDD
4. Tests MUST be written before implementation
5. All tests MUST pass before marking task complete
6. Never skip tasks or reorder them

### Test-Driven Development (TDD)
**Red-Green-Refactor Cycle**:
1. Write failing test for the task
2. Implement minimum code to make test pass
3. Refactor while keeping tests green
4. Mark task [x] only when tests pass

**Important**: BMad agents are configured to NEVER lie about test coverage - tests must actually exist and pass.

### File Management
- Always update file lists after implementation
- Document changes in Dev Agent Record
- Save outputs after each workflow step (never batch)

### Agent Activation Pattern
All BMad agents follow this activation pattern:
1. Load persona from agent file
2. Load `_bmad/{module}/config.yaml` and store session variables
3. Display greeting using user's name
4. Show numbered menu of available commands
5. Wait for user input (number, command trigger, or fuzzy match)
6. Execute selected workflow or action

## Working with WARP in This Repository

### When Implementing Features
1. Check if a story file exists in `_bmad-output/planning-artifacts/stories/`
2. If story exists, follow tasks/subtasks in strict order
3. Load `project-context.md` (if exists) for implementation guidance
4. Write tests first (TDD approach)
5. Ensure all existing tests pass before considering work complete

### When Architecture is Needed
1. Look for architecture docs in `_bmad-output/planning-artifacts/`
2. Check `docs/` for project-specific knowledge
3. When conflicts exist, story requirements take precedence over other docs

### Understanding BMad Structure
- `_bmad/` contains the framework (auto-generated, shouldn't be manually edited)
- `_bmad-output/` contains project-specific artifacts (this is your work product)
- Agent commands in `.cursor/`, `.claude/`, etc. are shortcuts to activate agents
- Manifests in `_bmad/_config/` list all available agents, workflows, and tasks

### Project Context
If `project-context.md` exists (generated via workflow), it contains:
- Critical rules and patterns for code consistency
- Architectural decisions and constraints
- LLM-optimized guidance for implementation
- This takes precedence over general patterns, but stories override it

## References

- BMad Method Docs: http://docs.bmad-method.org/
- BMad GitHub: https://github.com/bmad-code-org/BMAD-METHOD/
- BMad YouTube: https://www.youtube.com/@BMadCode
