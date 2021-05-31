:: setup venv, install all dependencies
py -m venv .\venv
venv\Scripts\activate.bat
pip3 install -r requirements.txt
pip3 install pyinstaller
venv\Scripts\deactivate.bat