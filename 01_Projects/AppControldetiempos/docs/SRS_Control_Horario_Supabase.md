# SRS - Control Horario App (Supabase)

## 1. Resumen Ejecutivo
Aplicación web gratuita de registro de jornada laboral para PYMES españolas (10-50 empleados). Cumple con el Real Decreto-ley 8/2019 y el Art. 34.9 del Estatuto de los Trabajadores.

## 2. Stack Tecnológico
- **Frontend**: React 18+ (Vite)
- **Styling**: Tailwind CSS + shadcn/ui
- **Backend**: Supabase (PostgreSQL + Auth + RLS)
- **Auth**: Supabase Auth (email/password)

## 3. Modelo de Datos

### 3.1 Tablas
| Tabla | Descripción |
|-------|-------------|
| `companies` | Empresas registradas (nombre, CIF, sector) |
| `workers` | Trabajadores de cada empresa (nombre, DNI, email, rol, departamento) |
| `work_sessions` | Sesiones de jornada (clock_in, clock_out, totales) |
| `pauses` | Pausas dentro de cada sesión |

### 3.2 Relaciones
- `companies` 1:N `workers`
- `workers` 1:N `work_sessions`
- `work_sessions` 1:N `pauses`

## 4. Roles y Permisos

### 4.1 Employee
- Ver/crear sus propios registros
- Clock in/out y pausas
- Historial propio (30 días)
- Exportar solo sus datos

### 4.2 Admin
- Todo lo de employee
- CRUD de trabajadores (máx 10 en plan gratuito)
- Ver todos los registros de la empresa
- Exportar todos los datos de la empresa

## 5. Flujos Principales

### 5.1 Registro + Onboarding
1. Registro con email + contraseña (Supabase Auth)
2. Wizard: nombre empresa, CIF, sector
3. Crear empresa → auto-crear worker admin
4. Redirigir a Dashboard

### 5.2 Clock In / Clock Out
1. Validar: no hay sesión activa hoy
2. Crear `work_session` con `clock_in = NOW()`
3. Estado: "Trabajando"
4. Para Clock Out: `clock_out = NOW()`, calcular totales
5. Estado: "Fuera"

### 5.3 Pausas
1. Validar: hay sesión activa y no hay pausa abierta
2. Crear `pause` con `pause_start = NOW()`
3. Estado: "En Pausa"
4. Para reanudar: `pause_end = NOW()`, calcular duración
5. Estado: "Trabajando"

### 5.4 Exportación CSV
1. Seleccionar filtros (fecha, trabajador)
2. Consultar datos con RLS
3. Generar CSV con columnas normativa
4. Descargar archivo

## 6. Validaciones
- 1 sesión activa máximo por trabajador
- `clock_out > clock_in`
- Advertencia si jornada > 9h (no bloquea)
- Pausas solo dentro de sesión activa
- Máximo 10 trabajadores por empresa (plan gratuito)

## 7. Seguridad (RLS)
- Políticas a nivel de fila en Supabase
- Workers solo ven datos de su company donde user_id = auth.uid()
- Admins ven todos los datos de su company
- Verificación de company_id en todas las consultas
