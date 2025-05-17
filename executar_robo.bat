@echo off
cd /d "C:\Users\crist\Desktop\robomercado"

echo Executando o robô...
python main.py

echo Fazendo push do arquivo de alertas...
git add alertas_gerados.json
git commit -m "Atualização manual dos alertas"
git push

echo.
echo ✅ Processo concluído! Pressione qualquer tecla para sair.
pause >nul
