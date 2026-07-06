from .file_utils import (
    get_list_files,
    get_list_ignores,
    get_final_files,
    convert_files_to_text,
    file_quality_check_for_LLM,
)
from .terminal_utils import Colors
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", help="Input directory path.")
    parser.add_argument("--output", "-o", help="Output file.")
    parser.add_argument("--description", "-d", help="Add a description to the beginning of the file.")
    args = parser.parse_args()

    input_ = args.input if args.input else "."
    output = args.output if args.output else "dirContent.txt"
    description = f"{args.description}\n" if args.description else ""

    files = get_list_files(dir_path=input_)
    ignores = get_list_ignores(output=output)
    final_files = get_final_files(files=files, ignores=ignores)

    convert_files_to_text(final_files, description, output)
    file_quality_check_for_LLM(output)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Colors.RED}[*]{Colors.RESET} It was {Colors.RED}UNSUCCESSFUL{Colors.RESET}. Error: {e}")
