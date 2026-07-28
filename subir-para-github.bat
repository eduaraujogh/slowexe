@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ================================================
echo   Enviando o site Slowexe para o GitHub
echo   https://github.com/eduaraujogh/slowexe
echo ================================================
echo.
echo Se abrir uma janela pedindo login do GitHub, faca o login por ela.
echo.
git push -u origin main
echo.
if %errorlevel%==0 (
  echo ================================================
  echo   PRONTO! Codigo enviado com sucesso.
  echo ================================================
) else (
  echo ================================================
  echo   Algo deu errado. Copie a mensagem acima e me mande.
  echo ================================================
)
echo.
pause
