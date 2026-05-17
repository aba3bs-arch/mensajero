@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo  Generando secrets para Streamlit Cloud...
echo.
python generar_secrets_cloud.py
echo.
echo  Siguiente paso: lee DESPLIEGUE.md y sube el proyecto a GitHub.
echo.
pause
