<p align="center">
  <img src="./images/logo.png" alt="Description" width="800">
</p>

<h1 align="center">📂 dir2txt</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/stars/unikOne56/dir2txt?style=for-the-badge&color=yellow" alt="Stars">
  <img src="https://img.shields.io/github/forks/unikOne56/dir2txt?style=for-the-badge&color=orange" alt="Forks">
</p>

<p align="center">
  <strong>Dump your entire project into one text file. For LLMs, code reviews, or backups.</strong>
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Ignore Patterns](#-ignore-patterns)
- [Output Example](#-output-example)
- [Requirements](#-requirements)
- [License](#-license)

---

## 🎯 Overview

**dir2txt** is a lightweight, zero-dependency Python command-line tool that recursively scans your project directory, extracts the content of all text-based files, and aggregates them into a single, well-structured text file.

**This tool is designed for developers who need to:**

- Feed entire codebases to Large Language Models (LLMs) like ChatGPT or Claude
- Perform comprehensive code reviews across multiple files
- Create human-readable backups of project source code
- Generate documentation that includes both structure and content
- Archive project states in a portable text format

---

## ✨ Features

**🔍 Recursive Scanning**  
Automatically traverses all subdirectories from the target path

**🚫 Binary Detection**  
Intelligently skips binary files using content-based detection

**📝 Comment Stripping**  
Removes code comments to reduce token usage

**📊 Token Estimation**  
Calculates token count and warns about context limits

**🎯 Custom Ignore Rules**  
Supports `.dir2txtignore` with `.gitignore`-style patterns

**📦 Zero Dependencies**  
Pure Python implementation requiring no external packages

**⚡ Fast Processing**  
Optimized for large projects with efficient file handling

**🎨 Clean Output**  
Generates structured output with directory tree and file separators

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/unikOne56/dir2txt
cd dir2txt

# Install as a Python package
pip install -e .

# Scan your current directory
python -m dir2txt

# Find your output in `project.txt`
```

---

## 📦 Installation

**Method 1: Install as a Package (Recommended)**

```bash
git clone https://github.com/unikOne56/dir2txt
cd dir2txt
pip install -e .
```

After installation, you can run the tool from any directory:

```bash
python -m dir2txt
```

**Method 2: Using Git without Installation**

```bash
git clone https://github.com/unikOne56/dir2txt
cd dir2txt
python -m dir2txt
```

---

## 📖 Usage Guide

### Basic Commands

**Scan the current working directory**  
```bash
python -m dir2txt
```

**Scan a specific directory**  
```bash
python -m dir2txt -i ./src
```

**Write output to a custom file**  
```bash
python -m dir2txt -o output.txt
```

**Add a description header to the output**  
```bash
python -m dir2txt -d "Project Description"
```

### Advanced Options

| Option | Description | Example |
|--------|-------------|---------|
| -i, --input | Target directory to scan | -i ./project/src |
| -o, --output | Custom output file path | -o docs/summary.txt |
| -d, --description | Add a description header | -d "My Django Project v2" |
| -e, --extensions | Ignore specific file extensions | -e pt onnx dcm |
| -h, --help | Show help message and exit | -h |

### Real-World Examples

**1. Scan a Django Project**

```bash
python -m dir2txt -i ./my_django_app -d "Django E-Commerce API" -o api_summary.txt
```

**2. Exclude Model Checkpoints**

```bash
python -m dir2txt -e pt pth h5 onnx
```

**3. Scan with Detailed Output**

```bash
python -m dir2txt -i ./src -o full_analysis.txt -d "Comprehensive Source Code Analysis"
```

---

## 🚫 Ignore Patterns

Create a `.dir2txtignore` file in your project root to exclude specific files or patterns:

```.dir2txtignore
# .dir2txtignore example

# Python bytecode and cache
*.pyc
__pycache__/
*.pyo

# Environment files
.env
.venv/
venv/

# Node.js
node_modules/
npm-debug.log

# Binary files
*.exe
*.dll
*.so

# Data files
*.pt
*.pth
*.onnx
*.dcm

# IDE specific
.vscode/
.idea/
*.swp
```

> **Note:** The tool uses the same pattern matching syntax as `.gitignore`. Wildcards (*), directory exclusions (/), and negation (!) are fully supported.

---

## 📄 Output Example

**Directory Tree Section**

```txt
$----Start----|test/project.tree.txt|----
test/
├── my_test_project
│   ├── .dir2txtignore
│   ├── example.exe          [SKIPPED - Binary]
│   ├── example.txt
│   └── my_privet_file.sec   [SKIPPED - Unknown type]
├── project.tree.txt
├── project.txt
└── run.sh
$-----End-----|test/project.tree.txt|----
```

**File Content Section**

```txt
$----Start----|test/my_test_project/example.txt|----
This is a test text.
$-----End-----|test/my_test_project/example.txt|----

$----Start----|test/run.sh|----
#!/bin/bash
echo "Running project..."
$-----End-----|test/run.sh|----
```

---

## 📋 Requirements

**Python:** Version 3.8 or higher  
**Dependencies:** None (pure Python standard library)

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENCE](LICENCE) file for details.

---

## 💡 Use Cases

- **LLM Context Preparation** – Feed your entire codebase to ChatGPT, Claude, or Gemini for analysis
- **Code Review Automation** – Create a single file for comprehensive code reviews
- **Project Backup** – Generate a human-readable text backup of your source code
- **Documentation Generation** – Combine structure and content for auto-documentation
- **Archiving** – Preserve the complete state of a project in portable text format
- **Auditing** – Perform security or compliance audits across all files

---

## ⚡ Performance Tips

1. **Large Projects**: Use `.dir2txtignore` to exclude unnecessary folders like `node_modules` or `__pycache__`

2. **Binary Files**: The tool automatically skips binaries, but you can extend the ignore list for specific types

3. **Token Limits**: For very large projects, consider:
   - Using `-e` to ignore large binary extensions
   - Splitting the output into multiple files
   - Using the token estimation to stay within model limits

---
