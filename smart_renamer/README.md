# Smart Renamer

A powerful and flexible command-line tool for intelligently renaming files in a directory with various options for customization.

## Features

- Add prefixes and suffixes to filenames
- Replace specific strings in filenames
- Sequentially number files
- Convert filenames to lowercase or uppercase
- Remove specific characters from filenames
- Apply regex patterns for advanced renaming

## Installation

1. Clone this repository or download the script
2. Ensure you have Python 3.6+ installed

No additional dependencies are required as the script only uses Python standard libraries.

## Usage

```
python smart_renamer.py <directory> [options]
```

### Arguments

- `directory`: The directory containing the files to rename (required)

### Options

- `-p, --prefix`: Prefix to add to filenames
- `-s, --suffix`: Suffix to add to filenames
- `-r, --replace`: Strings to replace in filenames (format: 'old1,new1;old2,new2')
- `-n, --number`: Sequentially number the files
- `-l, --lowercase`: Convert filenames to lowercase
- `-u, --uppercase`: Convert filenames to uppercase
- `-rm, --remove`: Characters to remove from filenames
- `-re, --regex`: Regex pattern to use for filename modification (use with -rr)
- `-rr, --regex_replace`: Replace pattern in regex mode

## Examples

### Add a prefix to all files

```
python smart_renamer.py ~/Documents/photos -p "vacation_"
```

This will rename files like "img001.jpg" to "vacation_img001.jpg".

### Sequentially number files

```
python smart_renamer.py ~/Documents/reports -n
```

This will rename files with sequential numbers like "0001_report.pdf", "0002_presentation.pptx", etc.

### Replace text in filenames

```
python smart_renamer.py ~/Music -r "old,new;spaces, "
```

This will replace "old" with "new" and spaces with underscores in all filenames.

### Convert to lowercase and add a suffix

```
python smart_renamer.py ~/Downloads -l -s "_archived"
```

This will convert all filenames to lowercase and add "_archived" to the end.

### Remove specific characters

```
python smart_renamer.py ~/Projects -rm "()[]"
```

This will remove parentheses and square brackets from all filenames.

### Use regex for advanced renaming

```
python smart_renamer.py ~/Data -re "\d{4}-\d{2}-\d{2}" -rr "date_"
```

This will replace dates in the format "YYYY-MM-DD" with "date_".

## Combining Options

You can combine multiple options to perform complex renaming operations:

```
python smart_renamer.py ~/Documents -p "doc_" -l -rm "#@" -r "report,summary;draft,final"
```

This will:
1. Add "doc_" as a prefix
2. Convert filenames to lowercase
3. Remove "#" and "@" characters
4. Replace "report" with "summary" and "draft" with "final"

## Notes

- The script will only rename files, not directories
- When using the numbering option, files are sorted alphabetically before numbering
- Be careful when renaming files in important directories; consider making a backup first


