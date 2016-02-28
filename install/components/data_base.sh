
OS=$(lsb_release -a | grep ID | awk '{print $3}')

if [ "$OS"= "Ubuntu" ] || [ "$OS"= "Debian" ]; then
  sudo apt-get install -y  postgresql
elif [ "$OS"= "Fedora" ]; then
  sudo dnf -y install postgresql
fi
