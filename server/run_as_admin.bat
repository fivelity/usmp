@echo off
powershell -Command "Start-Process -Verb RunAs -FilePath 'python' -ArgumentList 'test_admin.py' -WorkingDirectory '%~dp0'"
pause
