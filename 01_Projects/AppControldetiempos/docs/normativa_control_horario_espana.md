# Normativa Española de Control Horario

## 1. Marco Legal

### 1.1 Real Decreto-ley 8/2019
El **Real Decreto-ley 8/2019, de 8 de marzo**, modificó el artículo 34 del Estatuto de los Trabajadores para establecer la obligatoriedad del registro diario de la jornada laboral. Entró en vigor el **12 de mayo de 2019**.

### 1.2 Artículo 34.9 del Estatuto de los Trabajadores
> "La empresa garantizará el registro diario de jornada, que deberá incluir el horario concreto de inicio y finalización de la jornada de trabajo de cada persona trabajadora, sin perjuicio de la flexibilidad horaria que se establece en este artículo."

### 1.3 Ámbito de aplicación
- **Todas las empresas** en España, sin importar tamaño o sector
- **Todos los trabajadores** por cuenta ajena (tiempo completo, parcial, indefinidos, temporales, teletrabajo)
- **Excepciones**: autónomos sin empleados, personal alta dirección

## 2. Obligaciones del Empresario

### 2.1 Registro diario obligatorio
- Hora concreta de **inicio** de jornada
- Hora concreta de **finalización** de jornada
- Registro de **pausas** cuando afecten al cómputo de jornada

### 2.2 Conservación de registros
- Los registros deben conservarse durante **4 años mínimo**
- Deben estar a disposición de:
  - Los propios trabajadores
  - Representantes legales de los trabajadores
  - Inspección de Trabajo y Seguridad Social

### 2.3 Totalización mensual
- Entrega mensual al trabajador junto con la nómina
- Total de horas ordinarias y extraordinarias

## 3. Requisitos Técnicos

### 3.1 Criterio Técnico 101/2019 (Inspección de Trabajo)
El sistema de registro debe ser:
- **Objetivo**: no depender de la voluntad del empleador
- **Fiable**: garantizar la veracidad de los datos
- **Accesible**: disponible para consulta inmediata
- **No manipulable**: garantizar la integridad de los datos

### 3.2 Contenido mínimo del registro
| Campo | Descripción | Obligatorio |
|-------|-------------|:-----------:|
| Identificación trabajador | Nombre completo + DNI/NIE | ✅ |
| Fecha | Día del registro | ✅ |
| Hora inicio | Hora concreta de entrada | ✅ |
| Hora fin | Hora concreta de salida | ✅ |
| Total horas | Cómputo total de la jornada | ✅ |
| Pausas | Detalle de pausas realizadas | Recomendado |
| Horas netas | Total menos pausas | Recomendado |

### 3.3 Formato de Exportación

#### 3.3.1 Requisitos de exportación
- Formato legible y estructurado (CSV recomendado)
- Filtrable por rango de fechas y por trabajador
- Debe poder generarse ante requerimiento de la Inspección

#### 3.3.2 Columnas CSV para Inspección
```
Trabajador_Nombre,Trabajador_DNI,Fecha,Hora_Inicio,Hora_Fin,Total_Horas,Pausas_Minutos,Horas_Netas
```

Ejemplo:
```csv
Trabajador_Nombre,Trabajador_DNI,Fecha,Hora_Inicio,Hora_Fin,Total_Horas,Pausas_Minutos,Horas_Netas
"García López, María",12345678A,2024-01-15,09:00,18:00,9.00,60,8.00
"Martínez Ruiz, Juan",87654321B,2024-01-15,08:30,17:30,9.00,45,8.25
```

## 4. Sanciones por Incumplimiento

### 4.1 Infracción grave (Art. 7.5 LISOS)
- **Grado mínimo**: 751 € - 1.500 €
- **Grado medio**: 1.501 € - 3.750 €
- **Grado máximo**: 3.751 € - 7.500 €

### 4.2 Infracción muy grave (falsificación)
- Sanciones superiores a 7.500 €
- Posibles consecuencias penales

## 5. Jornada Laboral

### 5.1 Límites legales
- **Jornada máxima ordinaria**: 40 horas semanales de promedio en cómputo anual
- **Jornada diaria máxima**: 9 horas (salvo convenio colectivo)
- **Descanso mínimo entre jornadas**: 12 horas
- **Descanso semanal**: día y medio ininterrumpido

### 5.2 Horas extraordinarias
- Máximo 80 horas extraordinarias al año
- Compensación por tiempo de descanso o retribución
- Registro obligatorio día a día

## 6. Previsión Normativa 2026

### 6.1 Nuevos requisitos
- Uso **obligatorio de sistemas digitales** (prohibición registro manual/Excel)
- Registros **inalterables** con trazabilidad
- **Acceso remoto** para la Inspección de Trabajo
- Sanciones **más severas**

## 7. Implicaciones para el Diseño de la Aplicación

### 7.1 Funcionalidades obligatorias
1. ✅ Registro diario con hora inicio y fin
2. ✅ Registro de pausas
3. ✅ Identificación del trabajador (nombre + DNI)
4. ✅ Conservación mínima 4 años
5. ✅ Exportación para Inspección de Trabajo
6. ✅ Acceso del trabajador a sus propios registros
7. ✅ Sistema fiable y no manipulable

### 7.2 Recomendaciones de implementación
- Timestamps automáticos del servidor (no del cliente)
- Registros inmutables una vez cerrada la jornada
- Auditoría de cambios
- Formato CSV estandarizado para la Inspección
- Cálculo automático de totales
