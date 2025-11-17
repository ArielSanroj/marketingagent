#!/bin/bash

# Script para detener el servidor Flask y ngrok
# Uso: ./stop_backend.sh

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
LOG_DIR="/tmp/marketingagent"

echo -e "${BLUE}🛑 Deteniendo Marketing Agent Backend${NC}"
echo ""

# Función para matar proceso en un puerto
kill_port() {
    local port=$1
    local name=$2
    if lsof -ti:$port > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Deteniendo $name en puerto $port...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 1
        echo -e "${GREEN}✅ $name detenido${NC}"
    else
        echo -e "${BLUE}ℹ️  $name no está corriendo en puerto $port${NC}"
    fi
}

# Leer PIDs del archivo si existe
if [ -f "$LOG_DIR/pids.txt" ]; then
    PIDS=$(cat "$LOG_DIR/pids.txt")
    FLASK_PID=$(echo $PIDS | cut -d' ' -f1)
    NGROK_PID=$(echo $PIDS | cut -d' ' -f2)
    
    if [ ! -z "$FLASK_PID" ] && ps -p $FLASK_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Deteniendo Flask (PID: $FLASK_PID)...${NC}"
        kill -9 $FLASK_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Flask detenido${NC}"
    fi
    
    if [ ! -z "$NGROK_PID" ] && ps -p $NGROK_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Deteniendo ngrok (PID: $NGROK_PID)...${NC}"
        kill -9 $NGROK_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Ngrok detenido${NC}"
    fi
    
    rm -f "$LOG_DIR/pids.txt"
fi

# Detener por puertos como respaldo
kill_port $FLASK_PORT "Flask"
kill_port $NGROK_PORT "ngrok"

# Detener cualquier proceso de Flask o ngrok relacionado
echo -e "${BLUE}🧹 Limpiando procesos relacionados...${NC}"
pkill -f "python.*app.py" 2>/dev/null || true
pkill -f "ngrok http" 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ Todos los servicios han sido detenidos${NC}"

