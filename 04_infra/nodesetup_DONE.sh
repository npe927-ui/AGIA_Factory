#!/bin/bash

# Logger Function
log() {
  local message="$1"
  local type="$2"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  local color
  local endcolor="\033[0m"

  case "$type" in
    "info") color="\033[38;5;79m" ;;
    "success") color="\033[1;32m" ;;
    "error") color="\033[1;31m" ;;
    *) color="\033[1;34m" ;;
  esac

  echo -e "${color}${timestamp} - ${message}${endcolor}"
}

# Error handler function  
handle_error() {
  local exit_code=$1
  local error_message="$2"
  log "Error: $error_message (Exit Code: $exit_code)" "error"
  exit $exit_code
}

# Function to check for command availability
command_exists() {
  command -v "$1" &> /dev/null
}

check_os() {
    if ! [ -f "/etc/debian_version" ]; then
        echo "Error: Este script solo es compatible con sistemas basados en Debian."
        exit 1
    fi
}

# Function to Install the script pre-requisites
install_pre_reqs() {
    log "Instalando pre-requisitos" "info"

    # Run 'apt update'
    if ! apt update -y; then
        handle_error "$?" "Error al ejecutar 'apt update'"
    fi

    # Run 'apt install'
    if ! apt install -y apt-transport-https ca-certificates curl gnupg; then
        handle_error "$?" "Error al instalar paquetes"
    fi

    if ! mkdir -p /usr/share/keyrings; then
      handle_error "$?" "Asegúrate de que la ruta /usr/share/keyrings existe o ejecuta 'mkdir -p /usr/share/keyrings' con sudo"
    fi

    rm -f /usr/share/keyrings/nodesource.gpg || true
    rm -f /etc/apt/sources.list.d/nodesource.list || true

    # Run 'curl' and 'gpg' to download and import the NodeSource signing key
    if ! curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /usr/share/keyrings/nodesource.gpg; then
      handle_error "$?" "Error al descargar e importar la clave de firma de NodeSource"
    fi

    # Explicitly set the permissions to ensure the file is readable by all
    if ! chmod 644 /usr/share/keyrings/nodesource.gpg; then
        handle_error "$?" "Error al establecer permisos correctos en /usr/share/keyrings/nodesource.gpg"
    fi
}

# Function to configure the Repo
configure_repo() {
    local node_version=$1

    arch=$(dpkg --print-architecture)
    if [ "$arch" != "amd64" ] && [ "$arch" != "arm64" ] && [ "$arch" != "armhf" ]; then
      handle_error "1" "Arquitectura no soportada: $arch. Solo se admiten amd64, arm64 y armhf."
    fi

    echo "deb [arch=$arch signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$node_version nodistro main" | tee /etc/apt/sources.list.d/nodesource.list > /dev/null

    # N|solid Config
    echo "Package: nsolid" | tee /etc/apt/preferences.d/nsolid > /dev/null
    echo "Pin: origin deb.nodesource.com" | tee -a /etc/apt/preferences.d/nsolid > /dev/null
    echo "Pin-Priority: 600" | tee -a /etc/apt/preferences.d/nsolid > /dev/null

    # Nodejs Config
    echo "Package: nodejs" | tee /etc/apt/preferences.d/nodejs > /dev/null
    echo "Pin: origin deb.nodesource.com" | tee -a /etc/apt/preferences.d/nodejs > /dev/null
    echo "Pin-Priority: 600" | tee -a /etc/apt/preferences.d/nodejs > /dev/null

    # Run 'apt update'
    if ! apt update -y; then
        handle_error "$?" "Failed to run 'apt update'"
    else
        log "Repositorio configurado con éxito."
        log "Para instalar Node.js, ejecuta: apt install nodejs -y" "info"
        log "Puedes usar N|solid Runtime como alternativa a node.js" "info"
        log "Para instalar N|solid Runtime, ejecuta: apt install nsolid -y \n" "success"
    fi
}

# Define Node.js version
NODE_VERSION="20.x"

# Check OS
check_os

# Main execution
install_pre_reqs || handle_error $? "Error al instalar pre-requisitos"
configure_repo "$NODE_VERSION" || handle_error $? "Error al configurar el repositorio"
docker version
