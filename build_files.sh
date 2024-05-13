
echo "BUILD START"
#!/bin/bash

# Define the output directory
OUTPUT_DIR="staticfiles_build"

# Check if the output directory exists
if [ ! -d "$OUTPUT_DIR" ]; then
    # If the output directory does not exist, create it
    mkdir -p "$OUTPUT_DIR"
fi

# Install Python dependencies
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --no-input

# Move static files to the output directory
if [ -d "staticfiles" ]; then
    mv staticfiles/* "$OUTPUT_DIR/"
fi


echo "BUILD END"
