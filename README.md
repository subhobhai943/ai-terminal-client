# 🤖 AI Terminal Client

A powerful, universal command-line interface (CLI) for interacting with multiple AI providers from your terminal. Supports OpenAI, Anthropic Claude, Google Gemini, Perplexity, Grok (X.AI), Cohere, and more!

## ✨ Features

- **🔍 Automatic API Key Detection**: Automatically detects which AI service your API key belongs to
- **🌐 Multi-Provider Support**: Works with OpenAI, Anthropic, Google, Perplexity, Grok, Cohere
- **🎯 Interactive Chat Sessions**: Engaging terminal-based conversations
- **⚡ Quick Prompts**: Send single prompts for fast responses  
- **🔧 Easy Configuration**: Simple setup wizard for managing API keys
- **🎨 Beautiful Terminal UI**: Colorized output and intuitive interface
- **📱 Model Selection**: Choose from available models for each provider

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/username/ai-terminal-client.git
cd ai-terminal-client

# Install dependencies
pip install -r requirements.txt

# Make the script executable
chmod +x ai_cli_tool.py
```

### Install as Package

```bash
# Install the package
pip install -e .

# Now you can use 'ai-cli' command from anywhere
ai-cli --help
```

## 📋 Supported AI Providers

| Provider | API Key Format | Models Supported |
|----------|----------------|------------------|
| **OpenAI** | `sk-...` | GPT-4, GPT-4 Turbo, GPT-3.5 Turbo, GPT-4o |
| **Anthropic** | `sk-ant-...` | Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku |
| **Google** | `AIza...` | Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini Pro |
| **Perplexity** | `pplx-...` | Llama 3.1 Sonar models |
| **Grok/X.AI** | `xai-...` | Grok Beta, Grok Vision Beta |
| **Cohere** | `[40+ chars]` | Command R+, Command R, Command |

## 🛠️ Usage

### First Time Setup

Run the setup wizard to configure your API keys:

```bash
python ai_cli_tool.py --setup
```

The tool will automatically detect which AI provider your API key belongs to based on the key format.

### Interactive Chat Session

Start a chat session (default mode):

```bash
# Basic chat
python ai_cli_tool.py

# Or explicitly start chat
python ai_cli_tool.py --chat
```

### Quick Prompts

Send a single prompt and get a response:

```bash
# Let the tool choose the provider
python ai_cli_tool.py --prompt "Explain quantum computing in simple terms"

# Specify a provider
python ai_cli_tool.py --prompt "Write a Python function to sort a list" --provider OpenAI

# Specify both provider and model
python ai_cli_tool.py --prompt "Tell me a joke" --provider Anthropic --model claude-3-haiku-20240307
```

### List Configured Providers

See which providers you have configured:

```bash
python ai_cli_tool.py --list
```

## 📖 Command Reference

```bash
python ai_cli_tool.py [OPTIONS]

Options:
  --setup              Run the interactive setup wizard
  --chat               Start an interactive chat session (default)
  --prompt TEXT        Send a single prompt
  --provider TEXT      Specify which AI provider to use
  --model TEXT         Specify which model to use
  --list               List all configured providers
  --help               Show help message
```

## 🔧 Configuration

Configuration files are stored in `~/.ai-cli/config.json`. This includes:

- API keys for each provider
- Default preferences
- Provider-specific settings

### Manual Configuration

You can manually edit the config file:

```json
{
  "api_keys": {
    "OpenAI": "sk-your-openai-key-here",
    "Anthropic": "sk-ant-your-anthropic-key-here",
    "Google": "AIza-your-google-key-here"
  }
}
```

## 🔒 Security

- API keys are stored locally in `~/.ai-cli/config.json`
- No keys are transmitted except to their respective AI providers
- Config file has restricted permissions (600)
- Keys are never logged or displayed in plaintext

## 📋 Examples

### Example 1: Setup and Basic Usage

```bash
# First time setup
$ python ai_cli_tool.py --setup
🔧 Welcome to AI Terminal Setup!
Enter your API key: sk-1234567890...
✅ Detected provider: OpenAI
🔑 API key saved for OpenAI

# Start chatting
$ python ai_cli_tool.py
🚀 Starting chat session with OpenAI
📱 Model: gpt-4
Type 'exit' or 'quit' to end the session

You: Hello, how are you?
AI (OpenAI): Hello! I'm doing well, thank you for asking...
```

### Example 2: Quick Prompt with Multiple Providers

```bash
# Compare responses from different providers
$ python ai_cli_tool.py --prompt "What is machine learning?" --provider OpenAI
$ python ai_cli_tool.py --prompt "What is machine learning?" --provider Anthropic
$ python ai_cli_tool.py --prompt "What is machine learning?" --provider Google
```

### Example 3: Specific Model Usage

```bash
# Use a specific model
$ python ai_cli_tool.py --prompt "Write a haiku about coding" --provider Anthropic --model claude-3-haiku-20240307
```

## 🔍 API Key Detection Logic

The tool automatically detects your AI provider based on API key patterns:

- **OpenAI**: Keys starting with `sk-` (but not `sk-ant-`)
- **Anthropic**: Keys starting with `sk-ant-`
- **Google**: Keys starting with `AIza`
- **Perplexity**: Keys starting with `pplx-`
- **Grok/X.AI**: Keys starting with `xai-`
- **Cohere**: Long alphanumeric strings (40+ characters)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**Q: My API key isn't being detected correctly**
A: Make sure you're copying the entire API key. Check the patterns in the table above.

**Q: I get a "requests" module error**
A: Install dependencies with `pip install -r requirements.txt`

**Q: The tool can't find my config file**
A: Run `--setup` again to recreate the configuration.

**Q: I want to use a model not listed**
A: You can specify any model name with `--model`, but it must be supported by the provider.

### Getting Help

- Check the Issues page
- Open a new issue if you find a bug
- For feature requests, open a discussion

## 🎯 Roadmap

- [ ] Add support for more AI providers (Mistral, Replicate, etc.)
- [ ] Conversation history and persistence
- [ ] Custom system prompts
- [ ] File upload support for multimodal models
- [ ] Streaming responses
- [ ] Plugin system for extensions
- [ ] Web interface companion
- [ ] Batch processing mode

## 🙏 Acknowledgments

- Inspired by existing CLI tools like LLM by Simon Willison
- Built with love for the developer community
- Thanks to all AI providers for their amazing APIs

---

**Made with ❤️ for developers who live in the terminal**
