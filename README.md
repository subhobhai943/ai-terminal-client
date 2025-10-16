# 🤖 AI Terminal Client

![AI Terminal Client Banner](https://user-gen-media-assets.s3.amazonaws.com/seedream_images/55cce51a-aa43-4a96-a01a-feccd957e82d.png)

A powerful, universal command-line interface (CLI) for interacting with multiple AI providers from your terminal. Supports OpenAI, Anthropic Claude, Google Gemini, Perplexity, Grok (X.AI), Cohere, and more!

## ✨ Features

- **🔍 Automatic API Key Detection**: Automatically detects which AI service your API key belongs to
- **🌐 Multi-Provider Support**: Works with OpenAI, Anthropic, Google, Perplexity, Grok, Cohere
- **🎯 Interactive Chat Sessions**: Engaging terminal-based conversations
- **⚡ Quick Prompts**: Send single prompts for fast responses  
- **🔧 Easy Configuration**: Simple setup wizard for managing API keys
- **🎨 Beautiful Terminal UI**: Colorized output and intuitive interface
- **📱 Model Selection**: Choose from available models for each provider

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/subhobhai943/ai-terminal-client.git
cd ai-terminal-client
pip install -r requirements.txt
python ai_cli_tool.py --setup
```

For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md).

### Setup Wizard
![Setup Wizard](https://user-gen-media-assets.s3.amazonaws.com/seedream_images/b414d930-9b94-4674-8bfc-9b5937cb4d45.png)

Run the setup wizard and paste your API key - the tool will automatically detect your provider:

```bash
python ai_cli_tool.py --setup
```

### Start Chatting
![Chat Interface](https://user-gen-media-assets.s3.amazonaws.com/seedream_images/58c9f109-28f6-42eb-8ac9-64dc43102999.png)

```bash
python ai_cli_tool.py --chat
```

## 📋 Supported AI Providers (Updated October 2025)

| Provider | API Key Format | Latest Models Supported |
|----------|----------------|------------------------|
| **OpenAI** | `sk-...` | GPT-5, GPT-5 Mini, GPT-5 Nano, GPT-4.1, O3, O3-Mini |
| **Anthropic** | `sk-ant-...` | Claude Sonnet 4.5, Claude Haiku 4.5, Claude Opus 4.1, Claude Sonnet 4 |
| **Google** | `AIza...` | Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.5 Flash-Lite, Gemini 2.0 Flash |
| **Perplexity** | `pplx-...` | Sonar Deep Research, Sonar Reasoning Pro, Sonar Pro, R1-1776 |
| **Grok/X.AI** | `xai-...` | Grok-4, Grok-3, Grok-3 Mini, Grok-2 Image |
| **Cohere** | `[40+ chars]` | Command A 03-2025, Command R7B, Command A Translate, Command A Vision |

> ⚠️ **Model Updates**: All deprecated models (Gemini 1.5 Pro/Flash, Llama-3.1-sonar models) have been replaced with the latest 2025 models. The tool automatically uses the most current available models for each provider.
