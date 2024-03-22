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

import sys
import os

# Convert markdown to html


def markdown_to_html(markdown_lines):
    html_lines = []
    html_unordered_list = []
    i = 0
    num_lines = len(markdown_lines)
    while i < num_lines:
        if markdown_lines[i].startswith('-'):
            while i < num_lines and markdown_lines[i].startswith('-'):
                html_unordered_list.append(markdown_lines[i][2:])
                i += 1
            html_lines.extend(to_html_unordered_list(html_unordered_list))
            html_unordered_list = []
        if i < num_lines and markdown_lines[i].startswith('#'):
            html_lines.append(to_html_heading(markdown_lines[i]))
        elif i < num_lines:
            html_lines.append(markdown_lines[i])
        i += 1
    return html_lines

# Read file function


def read_file(file_path):
    with open(file_path, 'r') as file:
        markdown_lines = file.readlines()
    return markdown_lines

# Write file function


def write_file(file_path, html_lines):
    with open(file_path, 'w') as file:
        for line in html_lines:
            file.write(line)

# To HTML Heading


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
    if heading_level not in range(1, 7):
        print('Heading level must be between 1 to 6', file=sys.stderr)
        sys.exit(1)

    correct_html_tags = heading_dict['level_{}'.format(heading_level)]

    html_heading = "{}{}{}".format(
        correct_html_tags[0],
        heading_text.strip(),
        correct_html_tags[1]
    )

    return html_heading

# To HTML Unordered List


def to_html_unordered_list(markdown_lines):
    html_lines = ['<ul>\n']
    for line in markdown_lines:
        html_lines.append('\t<li>{}</li>\n'.format(line.strip()))

    html_lines.append('</ul>\n')
    return html_lines


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        sys.exit(1)
    elif not os.path.exists(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        sys.exit(1)
    else:
        markdown_lines = read_file(sys.argv[1])
        html_lines = markdown_to_html(markdown_lines)
        write_file(sys.argv[2], html_lines)
        sys.exit(0)
