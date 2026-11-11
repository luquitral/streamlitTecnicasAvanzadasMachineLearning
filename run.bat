@echo off
title Streamlit - Clasificador ImageNet
cls
echo =======================================================
echo   Iniciando Servidor Streamlit...
echo   Para apagarlo presiona: CTRL + C
echo =======================================================
echo.

set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
if exist "%PYTHON_EXE%" goto run

set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
if exist "%PYTHON_EXE%" goto run

echo No se encontro un entorno virtual.
echo.
echo Crea el entorno ejecutando estos comandos desde la carpeta del proyecto:
echo   py -3 -m venv .venv
echo   .venv\Scripts\python.exe -m pip install -r requirements.txt
echo.
pause
exit /b 1

:run
"%PYTHON_EXE%" -m streamlit run "%~dp0app.py" --server.port 8501
if errorlevel 1 (
    echo.
    echo Streamlit termino con un error. Revisa el mensaje anterior.
    pause
)
