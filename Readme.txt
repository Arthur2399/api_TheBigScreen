djcines/setting cambiar la base de datos a una base local

pip3 install virtualenv

virtualenv env

source env/bin/activate

./manage migrate

./manage createsuperuser

./manage runserver 0.0.0.0:8086