#!/bin/bash

# Script para iniciar el servidor Flask y ngrok para marketingagent
# Uso: ./start_backend.sh

set -e

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
FLASK_PORT=15000
NGROK_PORT=4040
FLASK_DIR="frontend"
FLASK_APP="app.py"
LOG_DIR="/tmp/marketingagent"

# Crear directorio de logs si no existe
mkdir -p "$LOG_DIR"

echo -e "${BLUE}🚀 Iniciando Marketing Agent Backend${NC}"
echo ""

# Función para verificar si un puerto está en uso
check_port() {
    lsof -ti:$1 > /dev/null 2>&1
}

# Función para matar proceso en un puerto
kill_port() {
    local port=$1
    if check_port $port; then
        echo -e "${YELLOW}⚠️  Puerto $port está en uso, deteniendo proceso...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

# 1. Verificar y detener procesos existentes en los puertos
echo -e "${BLUE}📋 Verificando puertos...${NC}"
kill_port $FLASK_PORT
kill_port $NGROK_PORT

# 2. Iniciar servidor Flask
echo -e "${BLUE}🐍 Iniciando servidor Flask en puerto $FLASK_PORT...${NC}"
cd "$(dirname "$0")/$FLASK_DIR"

# Verificar que el archivo existe
if [ ! -f "$FLASK_APP" ]; then
    echo -e "${RED}❌ Error: No se encontró $FLASK_APP en $FLASK_DIR${NC}"
    exit 1
fi

# Iniciar Flask en background
nohup python3 "$FLASK_APP" > "$LOG_DIR/flask.log" 2>&1 &
FLASK_PID=$!

# Esperar a que Flask inicie
echo -e "${YELLOW}⏳ Esperando a que Flask inicie...${NC}"
sleep 5

# Verificar que Flask está corriendo
if check_port $FLASK_PORT; then
    echo -e "${GREEN}✅ Servidor Flask iniciado correctamente (PID: $FLASK_PID)${NC}"
else
    echo -e "${RED}❌ Error: Flask no se inició correctamente${NC}"
    echo -e "${YELLOW}📄 Revisa los logs en: $LOG_DIR/flask.log${NC}"
    tail -20 "$LOG_DIR/flask.log"
    exit 1
fi

# 3. Iniciar ngrok
cd "$(dirname "$0")"
echo -e "${BLUE}🌐 Iniciando ngrok en puerto $NGROK_PORT apuntando a $FLASK_PORT...${NC}"

# Verificar que ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo -e "${RED}❌ Error: ngrok no está instalado${NC}"
    echo -e "${YELLOW}💡 Instala ngrok con: brew install ngrok/ngrok/ngrok${NC}"
    exit 1
fi

# Iniciar ngrok en background
nohup ngrok http $FLASK_PORT --log=stdout > "$LOG_DIR/ngrok.log" 2>&1 &
NGROK_PID=$!

# Esperar a que ngrok inicie
echo -e "${YELLOW}⏳ Esperando a que ngrok inicie...${NC}"
sleep 5

# Obtener URL pública de ngrok
NGROK_URL=""
MAX_RETRIES=10
RETRY_COUNT=0

while [ -z "$NGROK_URL" ] && [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    sleep 2
    NGROK_URL=$(curl -s http://localhost:$NGROK_PORT/api/tunnels 2>/dev/null | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data.get('tunnels') else '')" 2>/dev/null || echo "")
    RETRY_COUNT=$((RETRY_COUNT + 1))
done

if [ -z "$NGROK_URL" ]; then
    echo -e "${YELLOW}⚠️  No se pudo obtener la URL de ngrok automáticamente${NC}"
    echo -e "${YELLOW}💡 Revisa la interfaz de ngrok en: http://localhost:$NGROK_PORT${NC}"
else
    echo -e "${GREEN}✅ Ngrok iniciado correctamente (PID: $NGROK_PID)${NC}"
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🎉 Backend iniciado correctamente!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}📍 URLs:${NC}"
    echo -e "   Local:  ${GREEN}http://localhost:$FLASK_PORT${NC}"
    echo -e "   Public: ${GREEN}$NGROK_URL${NC}"
    echo ""
    echo -e "${BLUE}📊 Monitoreo:${NC}"
    echo -e "   Ngrok UI: ${GREEN}http://localhost:$NGROK_PORT${NC}"
    echo -e "   Flask Logs: ${GREEN}$LOG_DIR/flask.log${NC}"
    echo -e "   Ngrok Logs: ${GREEN}$LOG_DIR/ngrok.log${NC}"
    echo ""
    echo -e "${YELLOW}💡 Para detener los servicios, ejecuta: ./stop_backend.sh${NC}"
    echo -e "${YELLOW}💡 O presiona Ctrl+C y ejecuta: kill $FLASK_PID $NGROK_PID${NC}"
    echo ""
fi

# Guardar PIDs en archivo para facilitar el stop
echo "$FLASK_PID $NGROK_PID" > "$LOG_DIR/pids.txt"

echo -e "${BLUE}✅ Script completado${NC}"

