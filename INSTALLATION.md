# 📦 Installation Guide - AI Terminal Client

A comprehensive guide to installing and setting up the AI Terminal Client on various platforms.

## 🖥️ System Requirements

### Minimum Requirements
- **Python**: 3.7 or higher
- **Operating System**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Memory**: 100MB RAM
- **Storage**: 50MB free space
- **Internet**: Required for API calls

### Recommended Requirements
- **Python**: 3.9 or higher
- **Terminal**: Modern terminal with color support
- **Memory**: 256MB RAM
- **Storage**: 200MB free space (for dependencies and logs)

## 🚀 Quick Installation

### Method 1: Direct Download (Recommended)

```bash
# Clone the repository
git clone https://github.com/subhobhai943/ai-terminal-client.git
cd ai-terminal-client

# Install dependencies
pip install -r requirements.txt

# Make executable (Unix/macOS)
chmod +x ai_cli_tool.py

# Run setup
python ai_cli_tool.py --setup
```

### Method 2: Install as Python Package

```bash
# Clone and install
git clone https://github.com/subhobhai943/ai-terminal-client.git
cd ai-terminal-client

# Install in development mode
pip install -e .

# Now you can use 'ai-cli' command globally
ai-cli --setup
```

### Method 3: Direct Script Download

```bash
# Download just the main script
curl -O https://raw.githubusercontent.com/subhobhai943/ai-terminal-client/main/ai_cli_tool.py

# Install requirements
pip install requests

# Run directly
python ai_cli_tool.py --setup
```

## 🐍 Python Installation

If you don't have Python installed:

### Windows
1. **Download Python** from python.org
2. **Run installer** and check "Add Python to PATH"
3. **Verify installation**:
   ```cmd
   python --version
   pip --version
   ```

### macOS
```bash
# Using Homebrew (recommended)
brew install python

# Or using pyenv
curl https://pyenv.run | bash
pyenv install 3.11.0
pyenv global 3.11.0
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
pip3 --version
```

### Linux (CentOS/RHEL/Fedora)
```bash
sudo yum install python3 python3-pip
# or
sudo dnf install python3 python3-pip
```

## 🔧 Detailed Installation Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/subhobhai943/ai-terminal-client.git
cd ai-terminal-client
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv ai-cli-env
source ai-cli-env/bin/activate  # Windows: ai-cli-env\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python ai_cli_tool.py --help
```

### Step 5: Initial Setup
```bash
python ai_cli_tool.py --setup
```

## 📱 Platform-Specific Instructions

### Windows
- Command Prompt or PowerShell: clone repo, pip install -r requirements.txt, run setup
- WSL users: install python3 and pip3, then follow Linux steps

### macOS
- Install Python via Homebrew, clone repo, install requirements, run setup
- Apple Silicon: ensure ARM Python via Homebrew

### Linux
- Ubuntu/Debian: apt install python3 python3-pip git
- Arch: pacman -S python python-pip git
- CentOS/RHEL/Fedora: dnf/yum install python3 python3-pip git

## 🐳 Docker (Optional)

Dockerfile example:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x ai_cli_tool.py
VOLUME ["/root/.ai-cli"]
ENTRYPOINT ["python", "ai_cli_tool.py"]
```

Build and run:
```bash
docker build -t ai-terminal-client .
docker run -it --rm -v ~/.ai-cli:/root/.ai-cli ai-terminal-client --setup
```

## 🔍 Troubleshooting
- Use python3/pip3 if python/pip are missing
- On Unix/macOS, run `chmod +x ai_cli_tool.py`
- SSL issues on macOS: run "Install Certificates.command" in Python folder
- PATH issues: export PATH="$HOME/.local/bin:$PATH"

## 🧪 Developer Installation
```bash
python -m venv dev-env
source dev-env/bin/activate  # Windows: dev-env\Scripts\activate
pip install -e .
pip install pytest black flake8 mypy
python test_basic.py
```

## 📋 Post-Installation Checklist
- [ ] `python ai_cli_tool.py --help` prints help
- [ ] `python ai_cli_tool.py --setup` runs wizard
- [ ] `~/.ai-cli/config.json` is created
- [ ] `python ai_cli_tool.py --chat` starts a session
