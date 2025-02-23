
#!/bin/bash

# Update package lists and install Python pip if not already installed
sudo apt update
sudo apt install -y python3-pip

# Install the required Python packages
pip3 install -r requirements.txt

# Run the Flask application
python3 app.py
