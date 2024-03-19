#!/usr/bin/python3
"""
markdown2html.py - Converts a Markdown file to an HTML file

This script takes two command-line arguments:

  1. source_file: The path to the Markdown file to be converted.
  2. target_file: The path to the output HTML file.

If the script is called with fewer than two arguments,
it will print an error message and exit with code 1.
If the source file doesn't exist, it will also print an error 
message and exit with code 1.
Otherwise, it will exit with code 0 indicating successful execution.
"""
import sys, os

if len(sys.argv) < 3:
    print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
    sys.exit(1)
elif not os.path.exists(sys.argv[1]):
    print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
    sys.exit(1)
else:
    sys.exit(0)

# I will use this function later
def to_html_heading(markdown_line):
    heading_dict = {
        'level_1': ['<h1>', '</h1>'],
        'level_2': ['<h2>', '</h2>'],
        'level_3': ['<h3>', '</h3>'],
        'level_4': ['<h4>', '</h4>'],
        'level_5': ['<h5>', '</h5>'],
        'level_6': ['<h6>', '</h6>'],
    }

    markdown_heading, heading_text = markdown_line.split(' ', 1)

    heading_level = markdown_heading.count('#')
    if not heading_level in range(1, 7):
        print('Heading level must be between 1 to 6', file=sys.stderr)
        sys.exit(1)

    correct_html_tags = heading_dict['level_{}'.format(heading_level)]

    html_heading = "{}{}{}".format(
        correct_html_tags[0],
        heading_text,
        correct_html_tags[1]
        )

    return html_heading
