@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo  ========================================
echo   3B OFFICIAL - acceso desde celular
echo  ========================================
echo.
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found
)
:found
set IP=%IP: =%
echo  En la MISMA WiFi, abre en el celular:
echo.
echo      http://%IP%:8501
echo.
echo  La PC debe estar encendida con esta ventana abierta.
echo  Si Windows pregunta por el firewall, permite acceso.
echo.
echo  ========================================
echo.
streamlit run app_chat_3b.py
pause
