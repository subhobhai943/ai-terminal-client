#!/usr/bin/env python3
"""
Multi-AI Terminal Client Tool
A universal CLI for interacting with multiple AI providers
Supports OpenAI, Anthropic, Google Gemini, Perplexity, Grok, and more
Enhanced with file creation, modification, and project generation capabilities
"""

import os
import sys
import json
import re
import argparse
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import zipfile
import tempfile
from datetime import datetime

# Color codes for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

@dataclass
class AIProvider:
    name: str
    api_url: str
    key_pattern: str
    headers_template: Dict[str, str]
    request_template: Dict
    models: List[str]

class FileManager:
    """Handle file and folder operations"""
    
    @staticmethod
    def extract_code_blocks(response: str) -> List[Dict[str, str]]:
        """Extract code blocks from AI response"""
        # Pattern to match code blocks with filename and language
        pattern = r'```(?:(\w+)\s+)?(?:<!--\s*([^\s]+)\s*-->\s*)?\n?([\s\S]*?)```'
        
        # Also look for filename patterns
        filename_patterns = [
            r'(?:File|Filename|Save as|Create|Path):\s*([^\n]+)',
            r'([^\s]+\.(?:html|css|js|py|txt|md|json|xml|yml|yaml|toml|ini|cfg))\s*:',
            r'<!--\s*([^\s]+)\s*-->',
            r'//\s*([^\s]+\.(?:js|ts|jsx|tsx|css|html))\s*$',
            r'#\s*([^\s]+\.(?:py|sh|md))\s*$'
        ]
        
        code_blocks = []
        matches = re.finditer(pattern, response, re.MULTILINE)
        
        for match in matches:
            language = match.group(1) or ''
            filename = match.group(2) or ''
            content = match.group(3).strip()
            
            # If no filename in match, try to find it in the content or nearby text
            if not filename:
                # Look for filename patterns before the code block
                start_pos = max(0, match.start() - 200)
                context = response[start_pos:match.start()]
                
                for pattern in filename_patterns:
                    filename_match = re.search(pattern, context, re.IGNORECASE)
                    if filename_match:
                        filename = filename_match.group(1).strip()
                        break
                
                # If still no filename, try to infer from language
                if not filename and language:
                    extensions = {
                        'html': '.html',
                        'css': '.css',
                        'javascript': '.js',
                        'js': '.js',
                        'python': '.py',
                        'py': '.py',
                        'json': '.json',
                        'yaml': '.yml',
                        'yml': '.yml',
                        'xml': '.xml',
                        'md': '.md',
                        'markdown': '.md'
                    }
                    ext = extensions.get(language.lower())
                    if ext:
                        filename = f"file{ext}"
            
            if content:  # Only add if there's actual content
                code_blocks.append({
                    'filename': filename or f"file_{len(code_blocks) + 1}.txt",
                    'language': language,
                    'content': content
                })
        
        return code_blocks
    
    @staticmethod
    def create_project_structure(code_blocks: List[Dict[str, str]], project_name: str = None) -> str:
        """Create files and folders from code blocks"""
        if not code_blocks:
            return "No code blocks found in the response."
        
        # Determine project name
        if not project_name:
            project_name = f"ai_project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Clean project name
        project_name = re.sub(r'[^\w\-_]', '_', project_name)
        
        # Create project directory
        project_path = Path(project_name)
        if project_path.exists():
            # If exists, create with timestamp
            project_name = f"{project_name}_{datetime.now().strftime('%H%M%S')}"
            project_path = Path(project_name)
        
        project_path.mkdir(exist_ok=True)
        
        created_files = []
        
        for block in code_blocks:
            filename = block['filename']
            content = block['content']
            
            # Handle nested paths
            file_path = project_path / filename
            
            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                created_files.append(str(file_path))
            except Exception as e:
                print(f"{Colors.RED}Error creating {filename}: {e}{Colors.END}")
        
        return project_path, created_files
    
    @staticmethod
    def create_zip_archive(project_path: Path) -> str:
        """Create a zip archive of the project"""
        zip_path = f"{project_path}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in project_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(project_path)
                    zipf.write(file_path, arcname)
        
        return zip_path

class APIKeyDetector:
    """Detect AI service from API key patterns"""
    
    PATTERNS = {
        'OpenAI': {
            'regex': r'^sk-[a-zA-Z0-9]{48}$',
            'api_url': 'https://api.openai.com/v1/chat/completions',
            'models': ['gpt-5', 'gpt-5-mini', 'gpt-5-nano', 'gpt-4.1', 'gpt-4.1-mini', 'o3', 'o3-mini']
        },
        'Anthropic': {
            'regex': r'^sk-ant-[a-zA-Z0-9\-_]+$',
            'api_url': 'https://api.anthropic.com/v1/messages',
            'models': ['claude-sonnet-4-5-20250929', 'claude-haiku-4-5-20251001', 'claude-opus-4-1-20250805', 'claude-sonnet-4-20250514', 'claude-3-7-sonnet-20250219']
        },
        'Google': {
            'regex': r'^AIza[a-zA-Z0-9\-_]{35}$',
            'api_url': 'https://generativelanguage.googleapis.com/v1beta/models',
            'models': ['gemini-2.5-pro', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-2.0-flash', 'gemini-2.0-flash-lite']
        },
        'Perplexity': {
            'regex': r'^pplx-[a-zA-Z0-9]+$',
            'api_url': 'https://api.perplexity.ai/chat/completions',
            'models': ['sonar-deep-research', 'sonar-reasoning-pro', 'sonar-reasoning', 'sonar-pro', 'sonar', 'r1-1776']
        },
        'Grok': {
            'regex': r'^xai-[a-zA-Z0-9]+$',
            'api_url': 'https://api.x.ai/v1/chat/completions',
            'models': ['grok-4-0709', 'grok-3', 'grok-3-mini', 'grok-2-image-1212']
        },
        'Cohere': {
            'regex': r'^[a-zA-Z0-9]{40,}$',
            'api_url': 'https://api.cohere.ai/v1/chat',
            'models': ['command-a-03-2025', 'command-r7b-12-2024', 'command-a-translate-08-2025', 'command-a-reasoning-08-2025', 'command-a-vision-07-2025']
        }
    }
    
    @classmethod
    def detect_provider(cls, api_key: str) -> Optional[str]:
        """Detect AI provider from API key pattern"""
        api_key = api_key.strip()
        
        for provider, config in cls.PATTERNS.items():
            if re.match(config['regex'], api_key):
                return provider
        
        # Fallback: check for common prefixes
        if api_key.startswith('sk-') and 'ant' not in api_key:
            return 'OpenAI'
        elif api_key.startswith('sk-ant-'):
            return 'Anthropic'
        elif api_key.startswith('AIza'):
            return 'Google'
        elif api_key.startswith('pplx-'):
            return 'Perplexity'
        elif api_key.startswith('xai-'):
            return 'Grok'
        
        return 'Unknown'
    
    @classmethod
    def get_models(cls, provider: str) -> List[str]:
        """Get available models for a provider"""
        return cls.PATTERNS.get(provider, {}).get('models', [])
    
    @classmethod
    def get_api_url(cls, provider: str) -> str:
        """Get API URL for a provider"""
        return cls.PATTERNS.get(provider, {}).get('api_url', '')

class AIClient:
    """Universal AI client for multiple providers"""
    
    def __init__(self, api_key: str, provider: str = None):
        self.api_key = api_key
        self.provider = provider or APIKeyDetector.detect_provider(api_key)
        self.api_url = APIKeyDetector.get_api_url(self.provider)
        self.models = APIKeyDetector.get_models(self.provider)
        
    def send_message(self, message: str, model: str = None, create_files: bool = False) -> str:
        """Send message to AI provider with optional file creation"""
        if not model and self.models:
            model = self.models[0]  # Use first available model as default
        
        # Enhance prompt for file creation if requested
        if create_files:
            enhanced_message = f"""
{message}

Please provide complete, working code. For each file, use this format:
```language
<!-- filename.ext -->
[complete code here]
```

Make sure to:
1. Include ALL necessary files (HTML, CSS, JS, etc.)
2. Use proper file extensions
3. Provide complete, functional code
4. Include comments where helpful
5. Ensure files work together as a complete project

Example format:
```html
<!-- index.html -->
<!DOCTYPE html>
<html>...
```

```css
<!-- style.css -->
body {{ ... }}
```

```javascript
<!-- script.js -->
function example() {{ ... }}
```
"""
        else:
            enhanced_message = message
        
        try:
            if self.provider == 'OpenAI':
                return self._openai_request(enhanced_message, model)
            elif self.provider == 'Anthropic':
                return self._anthropic_request(enhanced_message, model)
            elif self.provider == 'Google':
                return self._google_request(enhanced_message, model)
            elif self.provider == 'Perplexity':
                return self._perplexity_request(enhanced_message, model)
            elif self.provider == 'Grok':
                return self._grok_request(enhanced_message, model)
            elif self.provider == 'Cohere':
                return self._cohere_request(enhanced_message, model)
            else:
                return f"Error: Unsupported provider '{self.provider}'"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _openai_request(self, message: str, model: str) -> str:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'messages': [{'role': 'user', 'content': message}],
            'max_tokens': 4000
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()['choices'][0]['message']['content']
    
    def _anthropic_request(self, message: str, model: str) -> str:
        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'max_tokens': 4000,
            'messages': [{'role': 'user', 'content': message}]
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()['content'][0]['text']
    
    def _google_request(self, message: str, model: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        data = {
            'contents': [
                {
                    'parts': [
                        {'text': message}
                    ]
                }
            ],
            'generationConfig': {
                'maxOutputTokens': 4000
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    
    def _perplexity_request(self, message: str, model: str) -> str:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'messages': [{'role': 'user', 'content': message}]
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()['choices'][0]['message']['content']
    
    def _grok_request(self, message: str, model: str) -> str:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'messages': [{'role': 'user', 'content': message}]
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()['choices'][0]['message']['content']
    
    def _cohere_request(self, message: str, model: str) -> str:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'message': message
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()['text']

class ConfigManager:
    """Manage configuration and API keys"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.ai-cli'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(exist_ok=True)
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def add_api_key(self, provider: str, api_key: str):
        if 'api_keys' not in self.config:
            self.config['api_keys'] = {}
        self.config['api_keys'][provider] = api_key
        self.save_config()
    
    def get_api_key(self, provider: str) -> Optional[str]:
        return self.config.get('api_keys', {}).get(provider)
    
    def list_providers(self) -> List[str]:
        return list(self.config.get('api_keys', {}).keys())

class AITerminal:
    """Main terminal interface"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.current_client = None
        
    def print_banner(self):
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                     🤖 AI Terminal Client v1.2 🤖                ║
║              Universal CLI for Multiple AI Providers             ║
║        Supports: OpenAI • Anthropic • Google • Perplexity      ║
║                   Grok • Cohere • File Generation!             ║
╚══════════════════════════════════════════════════════════════════╝{Colors.END}
"""
        print(banner)
    
    def setup_wizard(self):
        """Interactive setup for API keys"""
        print(f"{Colors.YELLOW}🔧 Welcome to AI Terminal Setup!{Colors.END}")
        print("Let's configure your AI providers.\n")
        
        while True:
            api_key = input(f"{Colors.GREEN}Enter your API key: {Colors.END}").strip()
            
            if not api_key:
                print(f"{Colors.RED}No API key provided. Exiting setup.{Colors.END}")
                break
            
            provider = APIKeyDetector.detect_provider(api_key)
            
            if provider == 'Unknown':
                print(f"{Colors.RED}❌ Could not detect provider from API key format{Colors.END}")
                continue
            
            print(f"{Colors.GREEN}✅ Detected provider: {Colors.BOLD}{provider}{Colors.END}")
            
            # Save the API key
            self.config.add_api_key(provider, api_key)
            print(f"{Colors.GREEN}🔑 API key saved for {provider}{Colors.END}\n")
            
            # Ask if user wants to add more keys
            add_more = input(f"{Colors.YELLOW}Add another API key? (y/N): {Colors.END}").strip().lower()
            if add_more != 'y':
                break
        
        print(f"{Colors.GREEN}✅ Setup complete!{Colors.END}")
    
    def select_provider_and_model(self) -> Tuple[Optional[str], Optional[str]]:
        """Interactive provider and model selection"""
        providers = self.config.list_providers()
        
        if not providers:
            print(f"{Colors.RED}❌ No API keys configured. Run setup first.{Colors.END}")
            return None, None
        
        if len(providers) == 1:
            provider = providers[0]
            print(f"{Colors.GREEN}Using provider: {Colors.BOLD}{provider}{Colors.END}")
        else:
            print(f"{Colors.CYAN}Available providers:{Colors.END}")
            for i, p in enumerate(providers, 1):
                print(f"  {i}. {p}")
            
            try:
                choice = int(input(f"{Colors.GREEN}Select provider (1-{len(providers)}): {Colors.END}")) - 1
                provider = providers[choice]
            except (ValueError, IndexError):
                print(f"{Colors.RED}Invalid selection{Colors.END}")
                return None, None
        
        # Get models for selected provider
        api_key = self.config.get_api_key(provider)
        models = APIKeyDetector.get_models(provider)
        
        if not models:
            print(f"{Colors.YELLOW}Using default model for {provider}{Colors.END}")
            return provider, None
        
        print(f"{Colors.CYAN}Available models for {provider}:{Colors.END}")
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model}")
        
        try:
            choice = int(input(f"{Colors.GREEN}Select model (1-{len(models)}): {Colors.END}")) - 1
            model = models[choice]
            return provider, model
        except (ValueError, IndexError):
            print(f"{Colors.YELLOW}Using default model: {models[0]}{Colors.END}")
            return provider, models[0]
    
    def chat_session(self):
        """Interactive chat session"""
        provider, model = self.select_provider_and_model()
        
        if not provider:
            return
        
        api_key = self.config.get_api_key(provider)
        client = AIClient(api_key, provider)
        
        print(f"\n{Colors.GREEN}🚀 Starting chat session with {Colors.BOLD}{provider}{Colors.END}")
        if model:
            print(f"{Colors.GREEN}📱 Model: {Colors.BOLD}{model}{Colors.END}")
        print(f"{Colors.YELLOW}Type 'exit' or 'quit' to end the session{Colors.END}")
        print(f"{Colors.YELLOW}💡 Tip: Ask to 'create files' or 'generate project' to enable file creation mode{Colors.END}\n")
        
        while True:
            try:
                user_input = input(f"{Colors.BLUE}You: {Colors.END}").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print(f"{Colors.GREEN}👋 Goodbye!{Colors.END}")
                    break
                
                if not user_input:
                    continue
                
                # Check if user wants file creation
                create_files = any(keyword in user_input.lower() for keyword in [
                    'create file', 'generate file', 'make file', 'create project',
                    'generate project', 'build app', 'create app', 'make app',
                    'web app', 'website', 'html', 'css', 'javascript'
                ])
                
                print(f"{Colors.PURPLE}AI ({provider}): {Colors.END}", end="", flush=True)
                response = client.send_message(user_input, model, create_files=create_files)
                print(response)
                
                # Process file creation if requested
                if create_files:
                    code_blocks = FileManager.extract_code_blocks(response)
                    if code_blocks:
                        print(f"\n{Colors.CYAN}📁 Found {len(code_blocks)} code blocks. Creating files...{Colors.END}")
                        
                        # Ask for project name
                        project_name = input(f"{Colors.GREEN}Project name (or press Enter for auto-generated): {Colors.END}").strip()
                        if not project_name:
                            project_name = None
                        
                        project_path, created_files = FileManager.create_project_structure(code_blocks, project_name)
                        
                        print(f"{Colors.GREEN}✅ Created project: {Colors.BOLD}{project_path}{Colors.END}")
                        for file_path in created_files:
                            print(f"  📄 {file_path}")
                        
                        # Ask if user wants to create zip
                        create_zip = input(f"{Colors.YELLOW}Create ZIP archive? (y/N): {Colors.END}").strip().lower()
                        if create_zip == 'y':
                            zip_path = FileManager.create_zip_archive(project_path)
                            print(f"{Colors.GREEN}📦 ZIP archive created: {Colors.BOLD}{zip_path}{Colors.END}")
                    else:
                        print(f"{Colors.YELLOW}⚠️  No code blocks found in response{Colors.END}")
                
                print()
                
            except KeyboardInterrupt:
                print(f"\n{Colors.GREEN}👋 Chat session ended{Colors.END}")
                break
            except Exception as e:
                print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
    
    def generate_project(self, prompt: str, provider: str = None, model: str = None, project_name: str = None):
        """Generate a project from a single prompt"""
        if not provider:
            provider, model = self.select_provider_and_model()
            if not provider:
                return
        
        api_key = self.config.get_api_key(provider)
        if not api_key:
            print(f"{Colors.RED}No API key found for {provider}{Colors.END}")
            return
        
        client = AIClient(api_key, provider)
        
        print(f"{Colors.GREEN}🚀 Generating project with {Colors.BOLD}{provider}{Colors.END}")
        if model:
            print(f"{Colors.GREEN}📱 Model: {Colors.BOLD}{model}{Colors.END}")
        print(f"{Colors.YELLOW}📝 Prompt: {prompt}{Colors.END}\n")
        
        print(f"{Colors.PURPLE}Generating... {Colors.END}", end="", flush=True)
        response = client.send_message(prompt, model, create_files=True)
        print("Done!\n")
        
        print(f"{Colors.CYAN}📋 AI Response:{Colors.END}")
        print(response)
        
        # Extract and create files
        code_blocks = FileManager.extract_code_blocks(response)
        if code_blocks:
            print(f"\n{Colors.CYAN}📁 Found {len(code_blocks)} code blocks. Creating files...{Colors.END}")
            
            project_path, created_files = FileManager.create_project_structure(code_blocks, project_name)
            
            print(f"{Colors.GREEN}✅ Project created: {Colors.BOLD}{project_path}{Colors.END}")
            for file_path in created_files:
                print(f"  📄 {file_path}")
            
            # Create ZIP automatically for generated projects
            zip_path = FileManager.create_zip_archive(project_path)
            print(f"{Colors.GREEN}📦 ZIP archive created: {Colors.BOLD}{zip_path}{Colors.END}")
            
            print(f"\n{Colors.YELLOW}💡 You can now open the project in VS Code, Replit, or any IDE!{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠️  No code blocks found in response{Colors.END}")
    
    def run(self):
        """Main application entry point"""
        self.print_banner()
        
        parser = argparse.ArgumentParser(description='Universal AI Terminal Client with File Generation')
        parser.add_argument('--setup', action='store_true', help='Run setup wizard')
        parser.add_argument('--list', action='store_true', help='List configured providers')
        parser.add_argument('--chat', action='store_true', help='Start chat session')
        parser.add_argument('--prompt', type=str, help='Send a single prompt')
        parser.add_argument('--generate', type=str, help='Generate project from prompt')
        parser.add_argument('--provider', type=str, help='Specify provider')
        parser.add_argument('--model', type=str, help='Specify model')
        parser.add_argument('--project-name', type=str, help='Project name for generated files')
        
        args = parser.parse_args()
        
        if args.setup:
            self.setup_wizard()
        elif args.list:
            providers = self.config.list_providers()
            if providers:
                print(f"{Colors.GREEN}Configured providers:{Colors.END}")
                for provider in providers:
                    models = APIKeyDetector.get_models(provider)
                    print(f"  • {Colors.BOLD}{provider}{Colors.END} - Models: {', '.join(models[:3])}...")
            else:
                print(f"{Colors.YELLOW}No providers configured. Run --setup first.{Colors.END}")
        elif args.generate:
            self.generate_project(args.generate, args.provider, args.model, args.project_name)
        elif args.prompt:
            if args.provider and args.provider in self.config.list_providers():
                provider = args.provider
                api_key = self.config.get_api_key(provider)
                client = AIClient(api_key, provider)
                response = client.send_message(args.prompt, args.model)
                print(f"{Colors.PURPLE}AI ({provider}): {Colors.END}{response}")
            else:
                provider, model = self.select_provider_and_model()
                if provider:
                    api_key = self.config.get_api_key(provider)
                    client = AIClient(api_key, provider)
                    response = client.send_message(args.prompt, args.model or model)
                    print(f"{Colors.PURPLE}AI ({provider}): {Colors.END}{response}")
        elif args.chat or len(sys.argv) == 1:
            # Default to chat mode if no arguments
            providers = self.config.list_providers()
            if not providers:
                print(f"{Colors.YELLOW}No API keys configured. Running setup wizard...{Colors.END}\n")
                self.setup_wizard()
                print()
            
            if self.config.list_providers():
                self.chat_session()

def main():
    try:
        terminal = AITerminal()
        terminal.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")

if __name__ == '__main__':
    main()
