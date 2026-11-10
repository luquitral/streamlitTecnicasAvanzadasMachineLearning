@echo off
title Streamlit - Clasificador ImageNet
cls
echo =======================================================
echo   Iniciando Servidor Streamlit...
echo   Para apagarlo presiona: CTRL + C
echo =======================================================
echo.
"%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0app.py" --server.port 8501
