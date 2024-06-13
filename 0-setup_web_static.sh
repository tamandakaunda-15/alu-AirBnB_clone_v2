#!/usr/bin/env bash
# This script sets up my web servers for the deployment of web_static

# server names (actual IP addresses)
export SERVER_NAME_1="3.91.244.104"
export SERVER_NAME_2="204.236.213.151"

# Install Nginx if it's not already installed
if ! dpkg -s nginx >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create directories if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership of /data/ directory
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i "/^\tlocation \/hbnb_static/ {
    \n\t\talias /data/web_static/current;\n\t}
    /^\t\tlocation \/ {
    \n\t\t\treturn 301 https://3.91.244.104\n\t\t}
    /^\t\tlocation \/ {
    \n\t\t\treturn 301 https://204.236.213.151\n\t\t}
}
" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
