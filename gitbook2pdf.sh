#!/bin/bash

# Convert a gitbook to pdf
# usage: gitbook2pdf.sh <directory>
# output: <directory>.pdf

# read arguments
search_dir=$1

# list all markdown files
list_files=$(find "$search_dir" -type f -name "*.md" | sort | tr '\n' ' ')
list_files=${list_files:0:-1}

# list all img folders
list_img_folders=$(find "$search_dir" -type d -name "img" | sort | sed 's/img//' | tr '\n' ':')
list_img_folders=${list_img_folders:0:-1}

# use pandoc to convert markdown to pdf
pandoc  $list_files --pdf-engine=xelatex -o "$search_dir.pdf" --verbose --from markdown-yaml_metadata_block --resource-path="$list_img_folders" 
