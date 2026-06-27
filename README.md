# 📂 dir2txt

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![GitHub stars](https://img.shields.io/github/stars/unikOne56/dir2txt)](https://github.com/unikOne56/dir2txt/stargazers)

Dump your entire project into one text file. For LLMs, code reviews, or backups.

## 🚀 Quick start

```bash
# Clone and run
git clone https://github.com/unikOne56/dir2txt
cd dir2txt
python -m dir2txt

# That's it. You'll get dirContent.txt
```

## 📖 Usage

```bash
# Scan current directory
python -m dir2txt

# Scan specific folder
python -m dir2txt -i ./src

# Custom output file
python -m dir2txt -o project.txt

# Add description header
python -m dir2txt -d "My Django project"
```

## ⚡ What it does

· Scans all files recursively
· Skips binary files (images, PDFs, executables)
· Respects .dir2txtignore (gitignore-style patterns)
· Removes code comments automatically
· Estimates tokens and checks against model limits

## 📄 Example output

```
FILE START: ./main.py
def hello():
    print("world")
FILE END: ./main.py
```

## 🚫 Ignore files

Create .dir2txtignore:

```
*.pyc
pycache/
.env
node_modules/
```

## 🔧 Requirements

Python 3.7+ only. No external dependencies.

## 📜 License

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

✨ Feed it to your AI. Save time.
