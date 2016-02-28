# Instalador Quote WebeServer
# 06/09/2013
# por: Leonardo Bravo Illanes
#

OS=$(lsb_release -a | grep ID | awk '{print $3}')

if [ "$OS" = "Ubuntu" ] || [ "$OS" = "Debian" ]; then
  sudo apt-get install -y python-flask python-psycopg2
elif [ "$OS" = "Fedora" ]; then
  sudo dnf install python-flask
fi
