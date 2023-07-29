#!/bin/bash
# join all markdown files in a directory into one file
# usage: joinmarkdown.sh <directory>
# output: <directory>.md

search_dir=$1
output_file="$search_dir.md"
if [ $# -eq 0 ]
then
    echo "Usage: joinmarkdown.sh <directory>"
    exit 1
fi

if [ ! -d "$search_dir" ]
then
    echo "Error: $search_dir is not a directory"
    exit 1
fi

echo "Joining markdown files in $search_dir"

# check if output file exists
if [ -f "$output_file" ]
then
    echo "Warning: $output_file exists, overwriting"
    echo "" > "$output_file"
fi

# join every file including inner files into output file .
list_files=$(find "$search_dir" -type f -name "*.md" | sort)

for entry in $list_files
do
    if [ -f "$entry" ]
    then
        echo "Adding $entry"
        cat $entry >> "$output_file"
        echo "" >> "$output_file"
    fi
done

# copying images in a central folder
mkdir img/
find $search_dir -type f -name "*.png" -print0 | xargs -0 cp -t img/