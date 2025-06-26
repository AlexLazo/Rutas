@echo off
echo Instalando dependencias para el proxy...
pip install -r proxy_requirements.txt
echo.
echo Dependencias instaladas correctamente.
echo Para ejecutar el proxy simple: python simple_proxy.py
echo Para ejecutar el proxy avanzado: python local_proxy.py
echo.
pause
