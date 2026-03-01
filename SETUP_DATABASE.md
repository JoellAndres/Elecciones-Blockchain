# Guía de Configuración de Base de Datos

Este documento contiene las consultas SQL y instrucciones para crear la base de datos del sistema de votación blockchain.

## Requisitos

- MySQL 5.7+ (XAMPP incluye MariaDB 12.2.2)
- Python 3.8+ (si usas el script automático)
- Acceso como usuario `root` en MySQL

---

## Opción 1: Script Python Automático (Recomendado)

### Paso 1: Iniciar MySQL/XAMPP

**XAMPP (Windows/Linux/macOS):**
```bash
# Abre XAMPP Control Panel
# Inicia el servicio MySQL (debe mostrar "Running" en verde)
# Puerto: 3306
```

**macOS (Alternativa sin XAMPP):**
```bash
brew install mysql
brew services start mysql
```
- Descarga MySQL desde https://dev.mysql.com/downloads/mysql/
- Instala y sigue el asistente
- O usa XAMPP/WAMP que incluyen MySQL

### Paso 2: Ejecutar el script

```bash
# Desde la raíz del proyecto
source venv/bin/activate
python setup_db.py
```

Deberías ver:
```
✓ BASE DE DATOS CONFIGURADA EXITOSAMENTE
Tablas creadas: 4
Registros insertados: 28
```

---

## Opción 2: Ejecución Manual del SQL

### Linux/macOS:
```bash
mysql -u root -p blockchain < setup_database.sql
```

### Windows (CMD):
```cmd
mysql -u root -p blockchain < setup_database.sql
```

### Mediante MySQL Workbench:
1. Abre MySQL Workbench
2. Conecta a tu servidor local
3. Abre el archivo `setup_database.sql`
4. Ejecuta (Ctrl + Enter o Cmd + Enter)

---

## 📊 Estructura de la Base de Datos

### Tabla: `candidatos`
Almacena información de candidatos

```sql
SELECT * FROM candidatos;
```

**Campos:**
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_candidato | INT | Identificador único |
| nombre | VARCHAR(100) | Nombre del candidato |
| apellido | VARCHAR(100) | Apellido del candidato |
| cargo | VARCHAR(50) | presidente, vice_presidente, gobernador, etc. |
| foto | LONGBLOB | Foto en formato binario |
| nombre_foto | VARCHAR(255) | Nombre del archivo de foto |

---

### Tabla: `partidos`
Información de partidos políticos

```sql
SELECT nombre, lista FROM partidos;
```

**Campos:**
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_partidos | INT | Identificador único |
| nombre | VARCHAR(150) | Nombre del partido (CAMBIO, VALOR, UNIDOS) |
| lista | VARCHAR(50) | Número de lista electoral |
| id_presidente | INT | FK a candidatos |
| id_vice_presidente | INT | FK a candidatos |
| id_gobernador | INT | FK a candidatos |
| id_intendente | INT | FK a candidatos |
| foto_presidentes | VARCHAR(255) | Ruta a foto |

---

### Tabla: `votantes`
Padrón electoral

```sql
SELECT * FROM votantes WHERE ha_votado = 0;
```

**Campos:**
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_votante | INT | Identificador único |
| dni | VARCHAR(20) | Documento Nacional de Identidad (UNIQUE) |
| nombre | VARCHAR(100) | Nombre del votante |
| apellido | VARCHAR(100) | Apellido del votante |
| ha_votado | TINYINT(1) | 0 = No votó, 1 = Ya votó |
| fecha_voto | DATETIME | Fecha/hora del voto |
| foto | LONGBLOB | Foto biométrica del votante |

---

### Tabla: `transacciones_blockchain`
Registro de transacciones en la blockchain

```sql
SELECT * FROM transacciones_blockchain;
```

**Campos:**
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT | Identificador único |
| tx_hash | VARCHAR(255) | Hash de la transacción en blockchain |
| bloque_numero | INT | Número de bloque |
| direccion_emisora | VARCHAR(255) | Dirección Ethereum de quien emite |
| timestamp | DATETIME | Fecha/hora de la transacción |

---

## 📝 Datos de Ejemplo Incluidos

### Partidos (3):
- **CAMBIO** (Lista 1)
- **VALOR** (Lista 2)
- **UNIDOS** (Lista 3)

### Candidatos (15):
Cada partido tiene:
- 1 Presidente
- 1 Vice Presidente
- 1 Gobernador
- 1 Vice Gobernador
- 1 Intendente

### Votantes (10):
Para probar el sistema, usa estos DNI:

| DNI | Nombre | Apellido |
|-----|--------|----------|
| 11111111 | Juan | Perez |
| 22222222 | María | González |
| 33333333 | Carlos | López |
| 44444444 | Ana | Martínez |
| 55555555 | Roberto | Sánchez |
| 66666666 | Patricia | García |
| 77777777 | Luis | Rodríguez |
| 88888888 | Sandra | Fernández |
| 99999999 | Miguel | Díaz |
| 10101010 | Elena | Torres |

---

## Verificación de Instalación

### Opción 1: Desde Python
```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='blockchain'
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES;")

print("Tablas en la BD:")
for table in cursor:
    print(f"  • {table[0]}")

cursor.execute("SELECT COUNT(*) FROM votantes;")
print(f"\nTotal de votantes: {cursor.fetchone()[0]}")

cursor.close()
conn.close()
```

### Opción 2: Desde MySQL CLI
```bash
mysql -u root -p blockchain

mysql> SHOW TABLES;
mysql> SELECT COUNT(*) FROM votantes;
mysql> SELECT nombre, lista FROM partidos;
mysql> SELECT ha_votado, COUNT(*) FROM votantes GROUP BY ha_votado;
```

---

## Solución de Problemas

### Error: "Can't connect to MySQL server"

**Causa:** MySQL no está ejecutándose

**Solución:**
```bash
# XAMPP - Abre XAMPP Control Panel y inicia MySQL

# macOS (si usas Homebrew)
brew services restart mysql

# Windows (ejecutar como Administrador)
net start MySQL80
```

### Error: "Access denied for user 'root'"

**Causa:** Contraseña incorrecta

**Solución 1:** Si root no tiene contraseña (por defecto):
```bash
mysql -u root
```

**Solución 2:** Si tiene contraseña:
```bash
mysql -u root -p
# Luego ingresa la contraseña
```

**Solución 3:** Resetear contraseña (MySQL):
```bash
# Detener MySQL
sudo systemctl stop mysql

# Iniciar sin contraseña
sudo mysqld_safe --skip-grant-tables &

# Conectar
mysql -u root

# Resetear
mysql> FLUSH PRIVILEGES;
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'nueva_contraseña';
```

### Error: "Database 'blockchain' already exists"

Es seguro - significa que ya la creaste. Puedes:

1. **Eliminar y recrear:**
```bash
mysql -u root -p blockchain
mysql> DROP DATABASE blockchain;
```

2. **O simplemente ignorar el error** - el script manejará tablas existentes

### Error: "Table 'votantes' already exists"

Normal si ejecutas el script dos veces. Las tablas no se recrean si ya existen.

---

## 🔐 Configuración de Seguridad (Producción)

Para un entorno de producción, **NO uses** `root` sin contraseña.

### Crear usuario específico:

```sql
-- Conectar como root
mysql -u root -p

-- Crear usuario
mysql> CREATE USER 'votacion_user'@'localhost' IDENTIFIED BY 'ContrasenaSegura123!@#';

-- Otorgar permisos
mysql> GRANT SELECT, INSERT, UPDATE, DELETE ON blockchain.* TO 'votacion_user'@'localhost';

-- Aplicar cambios
mysql> FLUSH PRIVILEGES;

-- Verificar
mysql> SELECT user, host FROM mysql.user;
```

### Actualizar configuración en la aplicación:

En `back/db_config.py`:
```python
db_config = {
    'host': 'localhost',
    'user': 'votacion_user',
    'password': 'ContrasenaSegura123!@#',
    'database': 'blockchain',
    'port': 3306
}
```

O usando variables de entorno (crear `.env`):
```
DB_HOST=localhost
DB_USER=votacion_user
DB_PASSWORD=ContrasenaSegura123!@#
DB_NAME=blockchain
DB_PORT=3306
```

---

## Consultas SQL Útiles

### Ver todos los votantes
```sql
SELECT dni, nombre, apellido, ha_votado FROM votantes;
```

### Contar votantes que ya votaron
```sql
SELECT COUNT(*) FROM votantes WHERE ha_votado = 1;
```

### Ver información de un partido
```sql
SELECT p.nombre, c1.nombre as presidente, c2.nombre as gobernador
FROM partidos p
LEFT JOIN candidatos c1 ON p.id_presidente = c1.id_candidato
LEFT JOIN candidatos c2 ON p.id_gobernador = c2.id_candidato
WHERE p.nombre = 'CAMBIO';
```

### Marcar como votado
```sql
UPDATE votantes SET ha_votado = 1, fecha_voto = NOW() WHERE dni = '11111111';
```

### Resetear votación (para pruebas)
```sql
UPDATE votantes SET ha_votado = 0, fecha_voto = NULL;
DELETE FROM transacciones_blockchain;
```

---

## 📞 Soporte

Si tienes problemas:

1. Verifica que MySQL está ejecutándose
2. Revisa que las credenciales son correctas
3. Lee los logs de error en la consola
4. Consulta la documentación oficial de MySQL

---

## ✨ Próximos Pasos

Después de crear la BD exitosamente:

```bash
# 1. Activar el virtual environment
source venv/bin/activate

# 2. Navegar al directorio backend
cd back

# 3. Ejecutar la aplicación
python app.py

# 4. Abrir en el navegador
# http://127.0.0.1:5000
```

¡La aplicación de votación blockchain está lista para usar! 
