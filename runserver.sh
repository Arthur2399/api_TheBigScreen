# /bin/bash
path=$(pwd)
cd ..
source env/bin/activate
cd $path
echo $path
./manage.py runserver 0.0.0.0:8087