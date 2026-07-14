# TODO.md - Roadmap to Transform dir2txt into a Professional Tool

This document outlines the development roadmap to turn `dir2txt` into a comprehensive, professional-grade tool for project output management. Priorities are based on **user impact** and **ease of implementation**.

## 🔥 High Priority (Quick Wins)
_These features deliver the most value with the least development effort and are recommended for the next release._

- [ ] **JSON Output:** Add `--format json` option for structured output. (This immediately enables integration with other tools).
- [ ] **Multiple Ignore Files Support:** Automatically combine patterns from `.dir2txtignore`, `.gitignore`, and allow a custom file via `--ignore-file`.
- [ ] **Parallel Processing:** Use `concurrent.futures` for concurrent file scanning and reading to boost performance on large projects.
- [ ] **Keep Comments Option:** Add `--keep-comments` flag to let users decide whether to remove comments.
- [ ] **Progress Bar:** Display scanning progress using libraries like `tqdm` to improve UX on large projects.

## ⚡ Medium Priority (Core Enhancements)
_These features are essential for making the tool more professional and are part of the mid-term plan._

- [ ] **Configuration File:** Allow saving settings in `dir2txt.config.json` (including ignores, output format, and processing settings) at the project root.
- [ ] **Split Output:** Add options like `--split-by-dir` to generate separate files per folder, along with an index file.
- [ ] **Comprehensive Statistics Report:** Generate a report including file count, lines of code, blank lines, and basic statistics (using built-in libraries).
- [ ] **Smart Content Filtering:** Allow defining `include`/`exclude` rules based on file content using regex (e.g., `--include-content "class|def"`).
- [ ] **Compressed Output:** Add `--compress` option to produce a `.zip` archive alongside the text file.

## 🚀 Lower Priority (Advanced & Integration)
_These features are designed for advanced use cases and integration into larger workflows._

- [ ] **Templated Output:** Allow custom templates for file display via a template file (e.g., `template.mustache`).
- [ ] **Dependency Analysis:** Identify and report imported libraries (`import`/`require`) separately.
- [ ] **Remote Execution:** Ability to fetch directly from a Git repository (`-u https://...`) or a URL.
- [ ] **Summary Outputs:** Generate a separate `summary.md` file that reports key project information in a readable format.
- [ ] **Auto-detection of Language and Structure:** Identify project type (e.g., Django, React) and apply optimal default settings.

## 🌟 Long-term Ideas (Future Vision)
_These ideas aim to make `dir2txt` a standard tool in the software development ecosystem._

- [ ] **IDE Plugins:** Develop simple plugins for VS Code, PyCharm, or IntelliJ.
- [ ] **PyPI Publication:** Easier distribution as an installable package (`pip install dir2txt`).
- [ ] **Project Website:** A simple page for introduction, full documentation, and sample outputs.
- [ ] **GitHub Actions Integration:** Provide a ready-to-use action for automatic output generation on each commit.
- [ ] **More Output Formats:** Add support for formats like **Markdown**, **HTML**, or **CSV**.
