import fnmatch
import os
import re
from .terminal_utils import Colors
from pathlib import Path


def get_list_files(dir_path=".") -> list[str]:
    """
    Get a list of the paths of all files in a directory

    Example output:
        ```
        ['./main.py', './test/mytest.py', './data/save.json']
        ```
    """
    base = Path(dir_path)
    files = []

    for p in base.rglob("*"):
        if p.is_file():
            files.append(str(p).replace("\\", "/"))

    print(f"{Colors.BLUE}[~]{Colors.RESET} {len(files)} files were found in directory '{dir_path}/'")

    return files


def get_list_ignores(output: str) -> list[str] | list[None]:
    """
    Read '.dir2txtignore' file

    What is '.dir2txtignore'?
        - This is a file that, if it exists, can contain the names of files that should be ignored for conversion to text.

    Example for file content:
        ```.dir2txtignore
        data.json
        .gitignore
        /.venv/
        *.pyc
        ```

    Example output:
        ```
        ['data.json', '.gitignore', '*.pyc', '/.venv/']
        ```
    """
    
    path = Path(".")
    dir2txtignore_path = list(path.rglob(".dir2txtignore"))
    
    if not dir2txtignore_path:
        return []
    else:
        dir2txtignore_path = str(dir2txtignore_path[0])

    ignore_files = [dir2txtignore_path, output]

    with open(dir2txtignore_path, "r") as f:
        content = f.read()
        for line in content.split("\n"):
            ignore_files.append(line)

        print(f"{Colors.BLUE}[~]{Colors.RESET} {len(ignore_files) - 2} entries were received from .dir2txtignore.")

        return ignore_files


def get_final_files(files: list[str], ignores: list[str]) -> list[str]:
    """
    Get a list of all files and remove ignore items from it,
    following gitignore-like patterns.

    Args:
        files (list): A list of file paths.
        ignores (list): A list of ignore patterns. Patterns can include:
                        - Exact file names (e.g., 'note.txt')
                        - Wildcards (e.g., '*.log', 'temp?.*')
                        - Directory patterns (e.g., 'build/', '.venv/')
                        - Root-only patterns (e.g., '/config.yaml')
                        - Recursive directory patterns (e.g., '**/tmp/')
                        - Negation patterns (e.g., '!important.log')

    Returns:
        list: A list of file paths that do not match any ignore patterns.

    Example:
        >>> get_final_files(
        ...     files=['./.venv/python.exe', 'main.py', 'data.json', 'note.txt', 'logs/app.log', 'src/config.yaml', 'temp.dat']
        ...     , ignores=['/.venv/', '*.json', 'note.txt', 'logs/', '!logs/app.log', '*.dat']
        ...     )
        ['main.py', 'logs/app.log']
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
                if normalized_file_path.startswith(
                    normalized_pattern
                ) or fnmatch.fnmatch(normalized_file_path, normalized_pattern):
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
                    if normalized_file_path.startswith(
                        normalized_negation
                    ) or fnmatch.fnmatch(normalized_file_path, normalized_negation):
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

    print(
        f"{Colors.BLUE}[~]{Colors.RESET} {len(final_files)} files were selected for conversion to text:\n{Colors.BLUE}[~]{Colors.RESET} ",
        end="",
    )

    for f in final_files:
        print(f, end=" ")

    print("")

    return final_files


def is_text_file(path: str) -> bool:
    
    non_text_formats = ['.pdf', '.docx', '.xlsx', '.pptx', '.jpg', '.png', '.gif', '.bmp', '.tiff', '.svg'
                        , '.mp3', '.wav', '.aac', '.flac', '.ogg', '.mp4', '.avi', '.mkv', '.mov', '.wmv'
                        , '.flv', '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.iso', '.exe', '.dll', '.apk'
                        , '.jar', '.pyc', '.swf', '.psd', '.ai', '.eps', '.indd', '.dwg', '.dxf', '.stl', '.obj'
                        , '.fbx', '.blend', '.mpp', '.vsd', '.ost', '.pst', '.edb', '.mdb', '.accdb', '.dbf', '.rdb'
                        , '.cr2', '.nef', '.arw', '.dng', '.raw', '.heic', '.heif', '.webp', '.avif', '.dds', '.ktx'
                        , '.pkm', '.wad', '.pk3', '.pak', '.vpk', '.bsg', '.ldf', '.mdf', '.sldx', '.pptm', '.docm'
                        , '.xlsm', '.odt', '.ods', '.odp', '.fb2', '.epub', '.mobi', '.azw', '.chm', '.djvu', '.lrc'
                        , '.srt', '.vtt', '.ass', '.ssa', '.idx', '.sub', '.bin', '.dat', '.mem', '.nvram', '.cfg'
                        , '.ini', '.reg', '.inf', '.lic', '.key', '.crt', '.cer', '.pem', '.der', '.p12', '.pfx'
                        , '.jks', '.ks', '.p10', '.csr', '.ocsp', '.crl', '.pkcs7', '.pkcs12', '.webm', '.ogm'
                        , '.asf', '.rm', '.rmvb', '.vob', '.m2ts', '.mts', '.ts', '.wma', '.amr', '.midi', '.s3m'
                        , '.it', '.xm', '.mod', '.rmi', '.voc', '.aif', '.aifc', '.au', '.snd', '.aiff', '.ac3'
                        , '.dts', '.eac3', '.mp2', '.mpa', '.mpc', '.swa', '.wv', '.ape', '.tta', '.spx', '.3gp'
                        , '.3g2', '.amv', '.avchd', '.bdmv', '.dcp', '.dff', '.dv', '.dvd', '.evob', '.f4v', '.h264'
                        , '.h265', '.hevc', '.m1v', '.m2p', '.m2ts', '.m2v', '.m4v', '.mk3d', '.mkv', '.mov', '.mp4'
                        , '.mpeg', '.mpg', '.mpg2', '.mpv', '.mts', '.mxf', '.ogm', '.ogv', '.qt', '.rm', '.rmvb'
                        , '.sdp', '.svi', '.swf', '.tod', '.tp', '.tpo', '.ts', '.vcd', '.vdr', '.vob', '.vp8'
                        , '.vp9', '.vvc', '.vvo', '.vwr', '.wave', '.webm', '.wm', '.wma', '.wmv', '.wmp', '.wmvhd'
                        , '.wms', '.wmt', '.wmva', '.wvx', '.xac', '.xmv', '.xvid', '.xwm', '.yuv', '.3gp2', '.3gpp'
                        , '.asf', '.avi', '.dat', '.divx', '.dv', '.evob', '.flv', '.h264', '.h265', '.hevc', '.m1v'
                        , '.m2p', '.m2ts', '.m2v', '.m4v', '.mk3d', '.mkv', '.mov', '.mp4', '.mpeg', '.mpg', '.mpg2'
                        , '.mpv', '.mts', '.mxf', '.ogm', '.ogv', '.qt', '.rm', '.rmvb', '.sdp', '.svi', '.swf', '.tod'
                        , '.tp', '.tpo', '.ts', '.vcd', '.vdr', '.vob', '.vp8', '.vp9', '.vvc', '.vvo', '.vwr', '.wave'
                        , '.webm', '.wm', '.wma', '.wmv', '.wmp', '.wmvhd', '.wms', '.wmt', '.wmva', '.wvx', '.xac'
                        , '.xmv', '.xvid', '.xwm', '.yuv', '.3gp2', '.3gpp', '.amv', '.asf', '.avchd', '.bdmv', '.bin'
                        , '.dat', '.dcp', '.dff', '.dv', '.dvd', '.evob', '.f4v', '.flv', '.hdmov', '.hevc', '.ifo'
                        , '.iso', '.m1v', '.m2p', '.m2ts', '.m2v', '.m4v', '.mk3d', '.mkv', '.mov', '.mp4', '.mpeg'
                        , '.mpg', '.mpg2', '.mpv', '.mts', '.mxf', '.ogm', '.ogv', '.qt', '.rm', '.rmvb', '.sdp'
                        , '.svi', '.swf', '.tod', '.tp', '.tpo', '.ts', '.vcd', '.vdr', '.vob', '.vp8', '.vp9'
                        , '.vvc', '.vvo', '.vwr', '.wave', '.webm', '.wm', '.wma', '.wmv', '.wmp', '.wmvhd'
                        , '.wms', '.wmt', '.wmva', '.wvx', '.xac', '.xmv', '.xvid', '.xwm', '.yuv']
    
    file_extension = os.path.splitext(path)[1].lower()
    return file_extension not in non_text_formats


def remove_comments_from_string(code_string):
    """
    Removes programming comments (like # and //) from a single line string,
    while intelligently handling cases where these symbols appear within strings or URLs.

    Args:
        code_string: The input string (a single line of code).

    Returns:
        The string with comments removed.
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


def convert_files_to_text(files: list[str], description: str, output_file: str) -> str:
    """
    Extracting and organizing file content and saving them

    Args:
        files (list): A list of file paths.
        output (str): The name of the output file.
    """
    spaces = ["", "\n", " ", "\t", "    "]

    print(f"{Colors.BLUE}[~]{Colors.RESET} Start writing file '{output_file}' ...")

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(description)
        for path in files:
            if not is_text_file(path):
                outfile.write(f"FILE START: {path}\n# This is not a text file.\nFILE END: {path}\n\n")
                continue

            try:
                with open(path, "r", encoding="utf-8", errors="replace") as infile:
                    content = infile.read()
                outfile.write(f"FILE START: {path} \n")
                for line in content.split("\n"):
                    line = remove_comments_from_string(line)
                    if line.strip() not in spaces:
                        outfile.write(f"{line}\n")
                outfile.write(f"FILE END: {path} \n\n")

            except Exception as e:
                outfile.write(f"# Error processing file {path}: {e}\n")
                outfile.write(f"FILE END: {path}\n\n")

    print(f"{Colors.BLUE}[~]{Colors.RESET} The file was written {Colors.BRIGHT_GREEN}SUCCESSFULLY{Colors.RESET}.")


def file_quality_check_for_LLM(path_file: str) -> None:
    """It checks the file for the number of tokens and gives the user the necessary suggestions."""

    tokens = 0

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
    LLM                Token
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
        print(
            f"{Colors.BLUE}[~]{Colors.RESET} LLMs marked in red may not process your file properly.\n"
        )
