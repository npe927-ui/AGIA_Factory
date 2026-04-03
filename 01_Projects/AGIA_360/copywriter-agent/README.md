# Manual de Arquitectura: Copywriter Agent

Esta estructura está diseñada para alimentar el cerebro de la IA de forma modular, evitando que el contexto se mezcle o se degrade.

## Estructura de Carpetas

### `00_INSTRUCCIONES_MAESTRAS`
Contiene el "ADN" del agente: quién es, cómo habla y qué reglas sigue siempre.

### `01_SISTEMA_Y_PROCESO`
Define los pasos obligatorios antes, durante y después de escribir. Incluye los frameworks (AIDCA, PAS, etc.).

### `02_DATASET_TRONCAL`
La base de conocimiento teórica: psicología, persuasión, ventas y neurociencia. Alimenta a todos los canales.

### `03_CANALES`
Especialización por formato. Cada subcarpeta contiene reglas y contextos específicos para ese canal (ej: Cold Email).

### `04_EJEMPLOS_REALES`
La "galería de trofeos" (buenos ejemplos) y el "cementerio" (malos ejemplos) para entrenamiento visual.

### `05_PLANTILLAS_Y_SALIDAS`
Moldes listos para usar y formatos de entrega final.

### `06_CLIENTES_Y_PROYECTOS`
Contextos específicos de cada encargo real.
