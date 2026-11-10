@echo off
echo Activando entorno virtual y levantando Streamlit...
call "%~dp0.venv\Scripts\activate.bat"
streamlit run "%~dp0app.py"
pause

