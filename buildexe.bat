pyinstaller -D --noconfirm Email.py
pyinstaller -D --noconfirm Print.py
pyinstaller -D --noconfirm EmailPrint.py
RMDIR "build" /S /Q
RMDIR "__pycache__" /S /Q
del Email.spec
del Print.spec
del EmailPrint.spec
cd dist
"C:\Program Files\7-Zip\7z.exe" a -tzip Email.zip -r Email
"C:\Program Files\7-Zip\7z.exe" a -tzip Print.zip -r Print
"C:\Program Files\7-Zip\7z.exe" a -tzip EmailPrint.zip -r EmailPrint
RMDIR "Email" /S /Q
RMDIR "Print" /S /Q
RMDIR "EmailPrint" /S /Q
pause