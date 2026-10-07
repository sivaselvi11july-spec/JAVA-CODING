@echo off
title JavaCraft AI - Java and OOP Chatbot
echo ========================================================
echo         JavaCraft AI: Java & OOP Chatbot Server
echo ========================================================
echo.
echo Checking Java version...
javac -version
if %errorlevel% neq 0 (
    echo [WARNING] javac is not detected in PATH.
    echo Please make sure JDK is installed and configured in PATH.
)
echo.
echo Starting JavaCraft Assistant Server on http://localhost:8080 ...
start http://localhost:8080
python server.py
pause
