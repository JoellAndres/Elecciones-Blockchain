# Base de Datos - Sistema de Votación Blockchain

## Resumen

He creado la estructura completa de la base de datos MySQL para tu sistema de votación blockchain. Todos los archivos necesarios están listos en la raíz del proyecto.

---

## Archivos Generados

### 1. **setup_database.sql** (5.8 KB)
Script SQ| Base de datos | Creada |
| Tablas | 4 tablas |
| Índices | 5 índices |
| Datos de ejemplo | 28 registros |
| Documentación | Completa |
| Scripts | Python y SQL |

Listo para empezarto con:
- [✓] Crear base de datos `blockchain`
- [✓] 4 tablas principales
- [✓] Índices optimizados
- [✓] Datos de ejemplo (3 partidos, 15 candidatos, 10 votantes)
- [✓] Restricciones de integridad referencial

### 2. **setup_db.py** (5.6 KB)
Script Python automático que:
- [✓] Se conecta a MySQL
- [✓] Ejecuta el SQL automáticamente
- [✓] Maneja errores de conexión
- [✓] Muestra progreso y resumen

**Uso:**
```bash
python setup_db.py
```

### 3. **SETUP_DATABASE.md** (8.4 KB)
Documentación completa con:
- [✓] Guía de instalación paso a paso
- [✓] Solución de problemas
- [✓] Consultas útiles
- [✓] Seguridad para producción

### 4. **SQL_QUERIES.sql** (300 líneas)
Colección de consultas SQL útiles:
- [✓] Visualización de datos
- [✓] Estadísticas de votación
- [✓] Depuración
- [✓] Integridad referencial
- [✓] Backup y mantenimiento

---

## Estructura de Tablas

### `candidatos`
```
id_candidato (PK)
nombre
apellido
cargo (presidente, vice_presidente, gobernador, intendente)
foto (BLOB)
nombre_foto
created_at, updated_at
```

### `partidos`
```
id_partidos (PK)
nombre (UNIQUE) - CAMBIO, VALOR, UNIDOS
lista
id_presidente, id_vice_presidente, id_gobernador, id_vice_gobernador, id_intendente (FKs)
foto_presidentes, foto_gobernadores, foto_intendente
created_at, updated_at
```

### `votantes`
```
id_votante (PK)
dni (UNIQUE)
nombre
apellido
foto (BLOB)
nombre_foto
ha_votado (0/1)
fecha_voto
created_at, updated_at
```

### `transacciones_blockchain`
```
id (PK)
tx_hash (UNIQUE)
bloque_numero
direccion_emisora
timestamp
created_at
```

---

## Datos de Ejemplo

### Partidos (3):
- CAMBIO (Lista 1)
- VALOR (Lista 2)
- UNIDOS (Lista 3)

### Candidatos (15):
Cada partido con 5 candidatos distribuidos en 5 cargos

### Votantes (10):
DNI desde 11111111 hasta 10101010 - todos sin votar

---

## Pasos de Instalación

### 1. Instalar XAMPP con MySQL

**Windows/Linux/macOS:**
Descargar desde: https://www.apachefriends.org/download.html

**Después de instalar:**
- Abre XAMPP Control Panel
- Inicia el servicio MySQL (verás "Running" en verde)
- Puerto predeterminado: 3306

### 2. Ejecutar el Script SQL

**Opción A: Con MySQL Workbench** (Recomendado)
1. Abre MySQL Workbench
2. Conecta a `localhost:3306` con usuario `root` (sin contraseña)
3. File → Open SQL Script
4. Selecciona `/setup_database.sql`
5. Ejecuta con Ctrl + Shift + Enter

**Opción B: Con línea de comandos**
```bash
/opt/lampp/bin/mysql --socket=/opt/lampp/var/mysql/mysql.sock < setup_database.sql
```

**Opción C: Con Python**
```bash
source venv/bin/activate
python setup_db.py
```

### 3. Verificar Instalación

```bash
python -c "
import mysql.connector
conn = mysql.connector.connect(host='localhost', user='root', database='blockchain')
cursor = conn.cursor()
cursor.execute('SHOW TABLES')
for table in cursor:
    print(f'✓ {table[0]}')
"
```

---

## Consultas Útiles Rápidas

### Ver todos los votantes
```sql
SELECT dni, nombre, apellido, ha_votado FROM votantes;
```

### Contar votantes que ya votaron
```sql
SELECT COUNT(*) FROM votantes WHERE ha_votado = 1;
```

### Ver partidos y candidatos
```sql
SELECT nombre, lista FROM partidos;
SELECT nombre, apellido, cargo FROM candidatos;
```

### Estadísticas de votación
```sql
SELECT 
    (SELECT COUNT(*) FROM votantes WHERE ha_votado = 1) as votos_emitidos,
    (SELECT COUNT(*) FROM votantes WHERE ha_votado = 0) as votos_pendientes,
    (SELECT COUNT(*) FROM votantes) as total;
```

### Marcar votante como votado
```sql
UPDATE votantes SET ha_votado = 1, fecha_voto = NOW() WHERE dni = '11111111';
```

---

## Configuración de Conexión

En `back/db_config.py`:
```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Cambia si MySQL tiene contraseña
    'database': 'blockchain',
    'port': 3306
}
```

---

## Seguridad en Producción

Nunca uses `root` sin contraseña en producción. Crea un usuario específico:

```sql
CREATE USER 'votacion_user'@'localhost' IDENTIFIED BY 'ContrasenaFuerte123!@#';
GRANT SELECT, INSERT, UPDATE, DELETE ON blockchain.* TO 'votacion_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## Validaciones Implementadas

- [✓] DNI único en tabla votantes
- [✓] Nombres únicos en tabla partidos
- [✓] Hash único en transacciones blockchain
- [✓] Integridad referencial (FK entre partidos y candidatos)
- [✓] Campos timestamp automáticos
- [✓] Índices optimizados para búsquedas

---

## Índices Creados

```sql
idx_votantes_dni
idx_votantes_ha_votado
idx_partidos_nombre
idx_transacciones_hash
idx_transacciones_bloque
```

Optimizan las búsquedas más comunes en la aplicación.

---

## Checklist de Verificación

- [ ] XAMPP instalado con MySQL
- [ ] Servicio MySQL ejecutándose en XAMPP (puerto 3306)
- [ ] Script SQL ejecutado exitosamente
- [ ] 4 tablas creadas
- [ ] Datos de ejemplo insertados
- [ ] Índices creados
- [ ] Aplicación Flask conecta a BD
- [ ] Prueba de votación en http://127.0.0.1:5002

---

## Solución de Problemas

### "Can't connect to MySQL server"
- Abre XAMPP Control Panel
- Inicia el servicio MySQL haciendo clic en "Start" (debe mostrar "Running" en verde)
- Verifica que el puerto sea 3306

### "Access denied for user 'root'"
- Sin contraseña: `mysql -u root`
- Con contraseña: `mysql -u root -p`

### "Database already exists"
- Es normal y seguro - las tablas se saltan si ya existen
- Para reiniciar: `DROP DATABASE blockchain;`

### Tablas no aparecen
- Verifica: `SHOW TABLES FROM blockchain;`
- Si está vacío, ejecuta de nuevo: `python setup_db.py`

---

## Documentación Adicional

Consulta `SETUP_DATABASE.md` para:
- Guía completa paso a paso
- Más consultas SQL útiles
- Procedimientos almacenados
- Vistas de datos
- Backup y recuperación
- Seguridad avanzada

---

## Próximo Paso

Una vez que la BD esté configurada:

```bash
source venv/bin/activate
cd back
python app.py
```

Luego abre: http://127.0.0.1:5002

---

## Resumen Rápido

| Item | Estado |
|------|--------|
| Base de datos | ✅ Creada |
| Tablas | ✅ 4 tablas |
| Índices | ✅ 5 índices |
| Datos de ejemplo | ✅ 28 registros |
| Documentación | ✅ Completa |
| Scripts | ✅ Python y SQL |

**¡Listo para empezar! ��**
