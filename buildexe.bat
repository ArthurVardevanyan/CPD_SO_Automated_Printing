pyinstaller -F Email.py
pyinstaller -F Print.py
pyinstaller -F EmailPrint.py
pyinstaller -F web/webPrint.py
RMDIR "build" /S /Q
RMDIR "__pycache__" /S /Q
del Email.spec
del Print.spec
del EmailPrint.spec
del webPrint.spec
pause