@echo off
pip install pyinstaller
pip install pipreqs
pipreqs
pip install -r requirements.txt
pyinstaller --onefile -n lovetools main.py