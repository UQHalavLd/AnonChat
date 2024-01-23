@echo off
echo Installing required modules...
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install colorama
echo Installation complete.
pause
