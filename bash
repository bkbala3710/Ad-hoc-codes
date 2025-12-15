#!/bin/bash

# Directory to clean up
TARGET_DIR="/path/to/your/directory"

# Find and delete files older than 21 days
find "$TARGET_DIR" -type f -mtime +21 -exec rm -f {} \;

# Optional: print confirmation
echo "Deleted files older than 21 days from $TARGET_DIR"

find "$TARGET_DIR" -type f -mtime +21 -exec ls -l {} \;

chmod +x delete.sh
./delete.sh
/path/to/delete.sh
bash delete.sh
0 0 * * * /path/to/delete.sh

