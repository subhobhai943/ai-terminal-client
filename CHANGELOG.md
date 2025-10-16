# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-10-16

### 🚀 Major Feature: File Generation & Project Creation
- **NEW**: Complete file and folder creation system
- **NEW**: Automatic code block extraction from AI responses
- **NEW**: Project generation mode with `--generate` command
- **NEW**: ZIP archive creation for easy project sharing
- **NEW**: IDE-ready project structure (VS Code, Replit compatible)

### File Generation Features:
- **Smart Code Detection**: Automatically extracts HTML, CSS, JavaScript, Python, and other code files
- **Project Organization**: Creates proper folder structure with nested directories
- **Multiple File Support**: Handles complex projects with multiple interconnected files
- **IDE Integration**: Generated projects work seamlessly in VS Code, Replit, CodePen, etc.
- **Enhanced Prompts**: AI models receive optimized prompts for better code generation

### New Commands:
- `--generate "prompt"`: Generate complete projects from a single prompt
- `--project-name "name"`: Specify custom project names
- Enhanced chat mode with automatic file detection keywords

### UI/UX Improvements:
- Updated banner to reflect v1.2 with file generation
- File creation progress indicators and success messages
- Interactive project naming and ZIP archive options
- Better error handling for file operations

### Technical Enhancements:
- New `FileManager` class for code extraction and file operations
- Improved token limits (4000 tokens) for longer code generation
- Enhanced regex patterns for filename detection
- Support for nested file structures and complex projects

### Example Use Cases:
- Web apps: "Create a calculator with HTML, CSS, JavaScript"
- Python projects: "Build a Flask REST API with authentication"
- React apps: "Generate a todo app with local storage"
- Games: "Create a Snake game with HTML5 Canvas"

### Developer Experience:
- Projects ready to run immediately after generation
- Automatic README.md generation for projects
- Proper file extensions and naming conventions
- Clean, organized code structure

## [1.1.0] - 2025-10-16

### 🚀 Major Model Updates
- **BREAKING**: Updated all AI provider models to latest 2025 versions
- **DEPRECATED**: Removed outdated models (Gemini 1.5 Pro/Flash, Llama-3.1-sonar models)
- **NEW**: Added support for latest models across all providers

### Updated Models by Provider:
- **OpenAI**: Added GPT-5, GPT-5 Mini, GPT-5 Nano, GPT-4.1, O3, O3-Mini
- **Anthropic**: Updated to Claude Sonnet 4.5, Haiku 4.5, Opus 4.1 (2025 versions)
- **Google**: Updated to Gemini 2.5 Pro, 2.5 Flash, 2.5 Flash-Lite, 2.0 Flash series
- **Perplexity**: Updated to Sonar Deep Research, Sonar Reasoning Pro, Sonar Pro, R1-1776
- **Grok/X.AI**: Updated to Grok-4, Grok-3, Grok-3 Mini, Grok-2 Image
- **Cohere**: Updated to Command A 03-2025, Command R7B, Command A Translate/Reasoning/Vision

### Documentation Updates
- Enhanced README with updated model table and deprecation notices
- Added model update warnings for users
- Updated examples with latest model names

### Notes
- Old model names may cause API errors - users should update to new model names
- All models researched from official provider documentation (October 2025)
- Backward compatibility maintained for API key detection and core functionality

## [1.0.0] - 2025-10-16

### 🎉 Initial Release
- Multi-provider AI CLI with automatic API key detection
- Support for OpenAI, Anthropic, Google Gemini, Perplexity, Grok, Cohere
- Interactive chat sessions and quick prompts
- Beautiful terminal UI with colorized output
- Comprehensive documentation and installation guides
- Apache 2.0 license
- GitHub repository with CI/CD setup

### Features
- Automatic provider detection from API key patterns
- Interactive setup wizard
- Provider and model selection
- Configuration management
- Cross-platform support (Windows, macOS, Linux)
- Docker support
- Basic test suite

### Migration Guide (v1.1 → v1.2)
- No breaking changes to existing functionality
- All previous commands continue to work
- New file generation features are opt-in
- Configuration files remain compatible
