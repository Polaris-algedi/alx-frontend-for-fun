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
import re

# Convert markdown to html


def markdown_to_html(markdown_lines):
    html_lines = []
    html_list = []
    i = 0
    num_lines = len(markdown_lines)
    while i < num_lines:
        # Check if the line starts with a dash (-) indicating an unordered list item
        if markdown_lines[i].startswith('-'):
            # Collect all consecutive lines starting with a dash (-) as list items
            while i < num_lines and markdown_lines[i].startswith('-'):
                html_list.append(markdown_lines[i][2:])
                i += 1
            # Convert the collected list items to HTML unordered list
            html_lines.extend(to_html_unordered_list(html_list))
            html_list = []
        # Check if the line starts with a double asterisk (**) indicating bold text
        elif check_line_starts_and_ends_with_asterisks(markdown_lines[i].strip()):
            html_lines.append('{}\n'.format(
                to_html_bold(markdown_lines[i].strip())))
        # Check if the line starts with a double underscore (__) indicating italic text
        elif check_line_starts_and_ends_with_double_underscores(markdown_lines[i].strip()):
            html_lines.append('{}\n'.format(
                to_html_italic(markdown_lines[i].strip())))
        # Check if the line starts with a asterisk (*) indicating an unordered list item
        elif markdown_lines[i].startswith('*'):
            # Collect all consecutive lines starting with a asterisk (*) as list items
            while i < num_lines and markdown_lines[i].startswith('*'):
                html_list.append(markdown_lines[i][2:])
                i += 1
            # Convert the collected list items to HTML ordered list
            html_lines.extend(to_html_ordered_list(html_list))
            html_list = []
        # Check if the line starts with a hash (#) indicating a heading
        elif i < num_lines and markdown_lines[i].startswith('#'):
            # Convert the heading to HTML format
            html_lines.append(to_html_heading(markdown_lines[i]))
        elif i < num_lines and not markdown_lines[i].startswith(('#', '-', '*', '\n')):
            # Collect all consecutive lines as a paragraph
            while i < num_lines and not markdown_lines[i].startswith(('#', '-', '*', '\n')):
                html_list.append(markdown_lines[i])
                i += 1
            # Append the line as it is if it's not a list item or heading
            html_lines.extend(to_html_paragraph(html_list))
            html_list = []
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
    # Define a dictionary to map heading levels to HTML tags
    heading_dict = {
        'level_1': ['<h1>', '</h1>'],
        'level_2': ['<h2>', '</h2>'],
        'level_3': ['<h3>', '</h3>'],
        'level_4': ['<h4>', '</h4>'],
        'level_5': ['<h5>', '</h5>'],
        'level_6': ['<h6>', '</h6>'],
    }

    # Split the markdown line into the heading level and heading text
    markdown_heading, heading_text = markdown_line.split(' ', 1)

    # Determine the heading level based on the number of '#' characters
    heading_level = markdown_heading.count('#')
    if heading_level not in range(1, 7):
        print('Heading level must be between 1 to 6', file=sys.stderr)
        sys.exit(1)

    # Get the correct HTML tags for the heading level
    correct_html_tags = heading_dict['level_{}'.format(heading_level)]

    # Create the HTML heading by combining the HTML tags and heading text
    html_heading = "{}{}{}\n".format(
        correct_html_tags[0],
        heading_text.strip(),
        correct_html_tags[1]
    )

    return html_heading


# To HTML UNORDERED LIST
def to_html_unordered_list(markdown_lines):
    html_lines = ['<ul>\n']
    for line in markdown_lines:
        line = to_html_bold(line.strip())
        line = to_html_italic(line)

        html_lines.append('\t<li>{}</li>\n'.format(line))

    html_lines.append('</ul>\n')
    return html_lines


# TO HTML ORDERED LIST
def to_html_ordered_list(markdown_lines):
    html_lines = ['<ol>\n']
    for line in markdown_lines:
        line = to_html_bold(line.strip())
        line = to_html_italic(line)
        html_lines.append('\t<li>{}</li>\n'.format(line))

    html_lines.append('</ol>\n')
    return html_lines


# To HTML Paragraph
def to_html_paragraph(markdown_lines):
    html_lines = ['<p>\n']
    if len(markdown_lines) == 1:
        line = to_html_bold(markdown_lines[0].strip())
        line = to_html_italic(line)
        html_lines.append('\t{}\n'.format(line))
    else:
        for i in range(len(markdown_lines)):
            line = to_html_bold(markdown_lines[i].strip())
            line = to_html_italic(line)
            html_lines.append('\t{}\n'.format(line))
            if i < len(markdown_lines) - 1:
                html_lines.append('\t{}\n'.format('<br />'))

    html_lines.append('</p>\n')
    return html_lines


# Extract text between asterisks
def extract_text_between_asterisks(text):
    pattern = r"\*\*(.*?)\*\*"
    matches = re.findall(pattern, text)
    return matches


# Extract text between double underscores
def extract_text_between_double_underscores(text):
    pattern = r"\_\_(.*?)\_\_"
    matches = re.findall(pattern, text)
    return matches


# To HTML Bold
def to_html_bold(text):
    matches = extract_text_between_asterisks(text)
    for match in matches:
        text = text.replace('**{}**'.format(match),
                            '<b>{}</b>'.format(match))
    return text


# To HTML Italic
def to_html_italic(text):
    matches = extract_text_between_double_underscores(text)
    for match in matches:
        text = text.replace('__{}__'.format(match),
                            '<em>{}</em>'.format(match))
    return text


# Check line starts and ends with asterisks
def check_line_starts_and_ends_with_asterisks(line):
    pattern = r"^\*\*.*\*\*$"
    return re.match(pattern, line) is not None


# Check line starts and ends with double underscores
def check_line_starts_and_ends_with_double_underscores(line):
    pattern = r"^__.*__$"
    return re.match(pattern, line) is not None


# Main function
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
