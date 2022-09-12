set path=%cd%
set python=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe
cd ..
%python% -m pip install virtualenv
%python% -m virtualenv env
cd env/Scripts/
activate.bat