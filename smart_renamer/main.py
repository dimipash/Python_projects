import os
import re
import argparse
from typing import List


def rename_file(
    filepath: str,
    prefix: str = "",
    suffix: str = "",
    replace: List[str] = [],
    number: bool = False,
    lowercase: bool = False,
    uppercase: bool = False,
    remove_chars: str = "",
    regex_pattern: str = "",
    regex_replace: str = "",
) -> None:
    """
    Renames a single file based on the provided options.

    Args:
        filepath: The path to the file to rename.
        prefix: A prefix to add to the filename.
        suffix: A suffix to add to the filename.
        replace: A list of strings to replace in the filename (each element is a pair: [old, new]).
        number: Whether to sequentially number the files.
        lowercase: Whether to convert the filename to lowercase.
        uppercase: Whether to convert the filename to uppercase.
        remove_chars: A string of characters to remove from the filename.
        regex_pattern: A regex pattern to apply to the filename.
        regex_replace: The string to replace the regex matches with.
    """
    directory, filename = os.path.split(filepath)
    name, ext = os.path.splitext(filename)

    # Apply replacements
    for old, new in replace:
        name = name.replace(old, new)

    # Remove characters
    for char in remove_chars:
        name = name.replace(char, "")

    # Apply Regex
    if regex_pattern and regex_replace:
        name = re.sub(regex_pattern, regex_replace, name)

    # Apply case conversion
    if lowercase:
        name = name.lower()
    if uppercase:
        name = name.upper()

    new_filename = prefix + name + suffix + ext
    new_filepath = os.path.join(directory, new_filename)

    os.rename(filepath, new_filepath)
    print(f"Renamed: '{filename}' -> '{new_filename}'")


def main():
    parser = argparse.ArgumentParser(
        description="Smart Renamer: Intelligently rename files in a directory."
    )
    parser.add_argument(
        "directory", help="The directory containing the files to rename."
    )
    parser.add_argument(
        "-p", "--prefix", help="Prefix to add to filenames.", default=""
    )
    parser.add_argument(
        "-s", "--suffix", help="Suffix to add to filenames.", default=""
    )
    parser.add_argument(
        "-r",
        "--replace",
        help="Strings to replace in filenames (format: 'old1,new1;old2,new2').",
        default="",
    )
    parser.add_argument(
        "-n", "--number", help="Sequentially number the files.", action="store_true"
    )
    parser.add_argument(
        "-l", "--lowercase", help="Convert filenames to lowercase.", action="store_true"
    )
    parser.add_argument(
        "-u", "--uppercase", help="Convert filenames to uppercase.", action="store_true"
    )
    parser.add_argument(
        "-rm", "--remove", help="Characters to remove from filenames.", default=""
    )
    parser.add_argument(
        "-re",
        "--regex",
        help="Regex pattern to use for filename modification. Use with -rr.",
        default="",
    )
    parser.add_argument(
        "-rr", "--regex_replace", help="Replace pattern in regex mode.", default=""
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory.")
        return

    replace_list = []
    if args.replace:
        replacements = args.replace.split(";")
        for rep in replacements:
            try:
                old, new = rep.split(",")
                replace_list.append([old, new])
            except ValueError:
                print(f"Error: Invalid replace format: '{rep}'. Use 'old,new'.")
                return

    files = [
        f
        for f in os.listdir(args.directory)
        if os.path.isfile(os.path.join(args.directory, f))
    ]
    if args.number:
        files.sort()

    for i, filename in enumerate(files):
        filepath = os.path.join(args.directory, filename)

        prefix_to_use = f"{i+1:04d}_" if args.number else args.prefix
        rename_file(
            filepath,
            prefix=prefix_to_use,
            suffix=args.suffix,
            replace=replace_list,
            lowercase=args.lowercase,
            uppercase=args.uppercase,
            remove_chars=args.remove,
            regex_pattern=args.regex,
            regex_replace=args.regex_replace,
        )


if __name__ == "__main__":
    main()
