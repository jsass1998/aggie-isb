echo "~~~~~~~~~~ Provisioning vagrant machine... ~~~~~~~~~~"

# Update apt, install python2 dependencies
echo "Updating apt & installing dependencies..."
sudo apt-get update -y
sudo apt update -y
sudo apt-get install build-essential checkinstall -y
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libpq-dev -y
echo "Done!"

# Download python2
echo "Installing Python2..."
cd /usr/src/
echo "Downloading Python2 to:"
pwd
wget https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz
sudo tar xzf Python-2.7.18.tgz

# Install python2
cd Python-2.7.18
sudo ./configure --enable-optimizations
sudo make altinstall
cd /usr/bin/

# Create Python2 symbolic link
sudo ln -s /usr/src/Python-2.7.18/python python2
echo "Done!"

# Install nvm and nodejs
echo "Installing Node.js..."
cd /home/vagrant
# echo "Downloading nvm to:"
# pwd
# curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
# export NVM_DIR="$HOME/.nvm"
sudo apt install npm -y
npm install node
echo "Done!"

# Install django
echo "Installing pip, venv, and django..."
sudo apt install python3-pip -y
sudo apt-get install python3-venv -y
pip3 install django --user
echo "Done!"

echo "~~~~~~~~~~~~~~ Done with provisioning! ~~~~~~~~~~~~~~"
