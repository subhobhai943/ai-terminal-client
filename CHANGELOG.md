# Changelog

All notable changes to this project will be documented in this file.

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
