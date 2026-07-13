import fnmatch
import os
import re
from pathlib import Path
from .terminal_utils import Colors


def load_ignored_extensions(config_path: str = "config/ignored_extensions.txt") -> set[str]:
    """
    Load non-text file extensions from an external configuration file.
    Returns a set of lowercase extensions starting with a dot.
    """
    path = Path(config_path)
    if not path.is_file():
        return set()
    
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip() and not line.strip().startswith("#")}


def load_ignored_directories(config_path: str = "config/ignored_directories.txt") -> set[str]:
    """
    Load directory names to skip from an external configuration file.
    Returns a set of directory names.
    """
    path = Path(config_path)
    if not path.is_file():
        return set()
        
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip() and not line.strip().startswith("#")}


def is_text_file(path: str, loaded_ignores: set[str], runtime_ignores: list[str] | None = None) -> bool:
    """
    Check if a file is a text file based on both pre-defined and runtime ignored extensions.
    """
    file_extension = Path(path).suffix.lower()
    
    all_ignored = loaded_ignores.copy()
    if runtime_ignores:
        for ext in runtime_ignores:
            clean_ext = ext.strip().lower()
            if not clean_ext.startswith("."):
                clean_ext = f".{clean_ext}"
            all_ignored.add(clean_ext)
            
    return file_extension not in all_ignored


def get_list_files(dir_path: str = ".") -> list[str]:
    """
    Get a list of file paths in a directory while completely skipping
    directories specified in the external configuration file.
    """
    files = []
    
    current_dir = Path(__file__).parent
    skip_dirs = load_ignored_directories(current_dir / "config" / "ignored_directories.txt")

    for root, dirs, filenames in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(str(file_path).replace("\\", "/"))

    print(f"{Colors.BLUE}[~]{Colors.RESET} {len(files)} files were found in directory '{dir_path}/' (filtered by configuration)")
    return files


def get_list_ignores(output: str) -> list[str]:
    """
    Read '.dir2txtignore' file if it exists.
    """
    path = Path(".")
    dir2txtignore_path = list(path.rglob(".dir2txtignore"))
    
    if not dir2txtignore_path:
        return []
    else:
        dir2txtignore_str = str(dir2txtignore_path[0])

    ignore_files = [dir2txtignore_str, output]

    with open(dir2txtignore_str, "r", encoding="utf-8") as f:
        content = f.read()
        for line in content.split("\n"):
            if line.strip():
                ignore_files.append(line.strip())

        print(f"{Colors.BLUE}[~]{Colors.RESET} {len(ignore_files) - 2} entries were received from .dir2txtignore.")
        return ignore_files


def get_final_files(files: list[str], ignores: list[str]) -> list[str]:
    """
    Get a list of all files and remove ignore items from it,
    following gitignore-like patterns.
    """
    final_files = []
    negations = [p[1:] for p in ignores if p.startswith("!")]
    positive_ignores = [p for p in ignores if not p.startswith("!")]

    for file_path in files:
        normalized_file_path = os.path.normpath(file_path)
        ignore_match = False

        for pattern in positive_ignores:
            if pattern.endswith("/") or pattern.endswith(os.sep):
                normalized_pattern = os.path.normpath(pattern)
                if normalized_file_path.startswith(normalized_pattern) or fnmatch.fnmatch(normalized_file_path, normalized_pattern):
                    ignore_match = True
                    break
            elif pattern.startswith("/") and os.sep in normalized_file_path:
                if fnmatch.fnmatch(normalized_file_path, pattern[1:]):
                    ignore_match = True
                    break
            else:
                if fnmatch.fnmatch(normalized_file_path, pattern):
                    ignore_match = True
                    break

        if ignore_match:
            is_negated = False
            for negation_pattern in negations:
                if negation_pattern.endswith("/") or negation_pattern.endswith(os.sep):
                    normalized_negation = os.path.normpath(negation_pattern)
                    if normalized_file_path.startswith(normalized_negation) or fnmatch.fnmatch(normalized_file_path, normalized_negation):
                        is_negated = True
                        break
                elif negation_pattern.startswith("/") and os.sep in normalized_file_path:
                    if fnmatch.fnmatch(normalized_file_path, negation_pattern[1:]):
                        is_negated = True
                        break
                else:
                    if fnmatch.fnmatch(normalized_file_path, negation_pattern):
                        is_negated = True
                        break

            if is_negated:
                ignore_match = False

        if not ignore_match:
            final_files.append(file_path)

    print(f"{Colors.BLUE}[~]{Colors.RESET} {len(final_files)} files were selected for conversion to text:\n{Colors.BLUE}[~]{Colors.RESET} ", end="")
    for f in final_files:
        print(f, end=" ")
    print("")

    return final_files


def remove_comments_from_string(code_string: str) -> str:
    """
    Removes programming comments (like # and //) from a single line string,
    while intelligently handling cases where these symbols appear within strings or URLs.
    """
    pattern = r"(\'[^'\\]*(?:\\.[^'\\]*)*\')|(\"[^\"\\]*(?:\\.[^\"\\]*)*\")|(#.*$)|(//.*$)"
    processed_string = ""
    last_end = 0

    matches = re.finditer(pattern, code_string)
    for match in matches:
        if match.group(1) or match.group(2):
            processed_string += code_string[last_end : match.end()]
            last_end = match.end()
        elif match.group(3) or match.group(4):
            processed_string += code_string[last_end : match.start()]
            last_end = match.end()
            break

    processed_string += code_string[last_end:]
    return processed_string.rstrip()


def convert_files_to_text(files: list[str], description: str, output_file: str, runtime_extensions: list[str] | None = None) -> None:
    """
    Extracting and organizing file content and saving them.
    """
    spaces = ["", "\n", " ", "\t", "    "]
    current_dir = Path(__file__).parent
    ignored_extensions_set = load_ignored_extensions(current_dir / "config" / "ignored_extensions.txt")

    print(f"{Colors.BLUE}[~]{Colors.RESET} Start writing file '{output_file}' ...")

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(description)
        for path in files:
            if not is_text_file(path, ignored_extensions_set, runtime_extensions):
                continue

            try:
                with open(path, "r", encoding="utf-8", errors="replace") as infile:
                    file_content = infile.read()
                
                outfile.write(f"$----Start----|{path}|----\n")
                for line in file_content.split("\n"):
                    line = remove_comments_from_string(line)
                    if line.strip() not in spaces:
                        outfile.write(f"{line}\n")
                outfile.write(f"$-----End-----|{path}|----\n\n\n")

            except Exception as e:
                outfile.write(f"# Error processing file {path}: {e}\n")
                outfile.write(f"FILE END: {path}\n\n")

    print(f"{Colors.BLUE}[~]{Colors.RESET} The file was written {Colors.BRIGHT_GREEN}SUCCESSFULLY{Colors.RESET}.")
    
    
def generate_tree_view(dir_path: str, output_tree_file: str) -> None:
    """
    Generates a clean, text-based directory tree structure and saves it to a file,
    respecting the ignored directories configuration.
    """
    current_dir = Path(__file__).parent
    skip_dirs = load_ignored_directories(current_dir / "config" / "ignored_directories.txt")
    
    tree_lines = [f"{os.path.basename(os.path.abspath(dir_path))}/"]

    def _build_tree(current_path: str, prefix: str = ""):
        try:
            items = sorted(
                [item for item in os.listdir(current_path) if item not in skip_dirs],
                key=lambda x: (not os.path.isdir(os.path.join(current_path, x)), x.lower())
            )
        except Exception:
            return

        count = len(items)
        for index, item in enumerate(items):
            path = os.path.join(current_path, item)
            is_last = (index == count - 1)
            connector = "└── " if is_last else "├── "
            
            tree_lines.append(f"{prefix}{connector}{item}")
            
            if os.path.isdir(path):
                extension_prefix = "    " if is_last else "│   "
                _build_tree(path, prefix + extension_prefix)

    _build_tree(dir_path)
    
    with open(output_tree_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tree_lines) + "\n")
        
    print(f"{Colors.BLUE}[~]{Colors.RESET} Tree structure saved successfully to '{output_tree_file}'.")


def file_quality_check_for_LLM(path_file: str) -> None:
    """
    It checks the file for the number of tokens and gives the user the necessary suggestions.
    """
    def estimate_tokens(text: str) -> int:
        text = text.replace("‌", " ")
        text = re.sub(r'([,.!?؛:،\-\(\)\[\]{}"\'/])', r" \1 ", text)
        parts = text.split()
        return len(parts)

    with open(path_file, "r", encoding="utf-8") as f:
        content = f.read()
        tokens = estimate_tokens(content)

    if tokens > 4000:
        print(f"{Colors.YELLOW}\n[NOTE] File {path_file} has {tokens} tokens and contains more than 4000 tokens. Your LLM model may not be able to process it correctly.")
        print(f"{Colors.BLUE}[~]{Colors.RESET} LLMs Token Range:{Colors.RESET}")
        print(
            f"""
    LLM                 Token
    {Colors.GREEN if tokens < 16385   else Colors.RED}GPT-3.5 Turbo      16K       {Colors.RESET}
    {Colors.GREEN if tokens < 8000    else Colors.RED}GPT-4              8K        {Colors.RESET}
    {Colors.GREEN if tokens < 128000  else Colors.RED}GPT-4 Turbo        128K      {Colors.RESET}
    {Colors.GREEN if tokens < 128000  else Colors.RED}GPT-4o             128K      {Colors.RESET}
    {Colors.GREEN if tokens < 2000000 else Colors.RED}Gemini 1.5 Pro     2M        {Colors.RESET}
    {Colors.GREEN if tokens < 200000  else Colors.RED}Claude 3.5 Sonnet  200K      {Colors.RESET}
    {Colors.GREEN if tokens < 8000    else Colors.RED}GitHub Copilot     8k        {Colors.RESET}
    {Colors.GREEN if tokens < 1000000 else Colors.RED}DeepSeek-Chat      1M        {Colors.RESET}
    {Colors.GREEN if tokens < 4000    else Colors.RED}Llama 2            4K        {Colors.RESET}
    {Colors.GREEN if tokens < 8000    else Colors.RED}Llama 3            8K ~ 32K  {Colors.RESET}\n"""
        )
        print(f"{Colors.BLUE}[~]{Colors.RESET} LLMs marked in red may not process your file properly.\n")