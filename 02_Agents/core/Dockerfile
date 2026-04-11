# Usar la imagen oficial de Node.js 20 (slim para menor tamaño)
FROM node:20-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencia
COPY package*.json ./

# Instalar dependencias (omitir devDependencies para producción)
RUN npm install --production

# Copiar el resto del código
COPY . .

# Exponer un puerto por si añadimos un dashboard HTTP en el futuro
EXPOSE 3000

# Comando para ejecutar (por defecto corre el router)
CMD ["node", "index.js"]
