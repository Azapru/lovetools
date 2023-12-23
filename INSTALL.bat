@echo off
echo Building lovetools...

call BUILD.bat

echo Installing lovetools...

mkdir %APPDATA%\lovetools
copy dist\lovetools.exe %APPDATA%\lovetools\lovetools.exe
setx PATH "%PATH%;%APPDATA%\lovetools"

echo Finished!
pause