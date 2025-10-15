#!/usr/bin/env python3
"""
Setup script for AI CLI Tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-terminal-client",
    version="1.0.0",
    author="AI Terminal Client",
    author_email="support@ai-terminal.com",
    description="Universal CLI for multiple AI providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/ai-terminal-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-cli=ai_cli_tool:main",
        ],
    },
)
