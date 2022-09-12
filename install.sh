# /bin/bash
sudo apt-get install python3-pip 
sudo apt install libpq-dev python3-dev postgresql-server-dev-all
sudo pip3 install virtualenv
path=$(pwd)
cd ..
virtualenv env
source env/bin/activate
cd $path
pip3 install -r requirement.txt

./manage.py migrate
./manage.py createsuperuser
./manage.py runserver 0.0.0.0:8086