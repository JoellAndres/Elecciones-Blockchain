#!/usr/bin/env python3
"""
Script para crear la base de datos y tablas del sistema de votación blockchain
Uso: python setup_db.py
"""

import mysql.connector
from mysql.connector import Error
import sys
import os

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Cambiar si tiene contraseña
    'port': 3306
}

def read_sql_file(filepath):
    """Lee el archivo SQL y retorna el contenido"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"✗ Archivo no encontrado: {filepath}")
        return None

def execute_sql_script(sql_script):
    """Ejecuta un script SQL completo"""
    try:
        # Conectar sin especificar database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✓ Conexión a MySQL establecida\n")
        
        created_tables = 0
        inserted_rows = 0
        
        # Ejecutar el script SQL
        statements = sql_script.split(';')
        
        for statement in statements:
            statement = statement.strip()
            
            # Saltar comentarios y líneas vacías
            if not statement or statement.startswith('--'):
                continue
                
            try:
                cursor.execute(statement)
                conn.commit()
                
                # Contar lo que se creó/insertó
                if 'CREATE TABLE' in statement.upper():
                    table_name = statement.split('CREATE TABLE IF NOT EXISTS')[1].split('(')[0].strip()
                    print(f"✓ Tabla creada: {table_name}")
                    created_tables += 1
                elif 'INSERT INTO' in statement.upper():
                    rows = cursor.rowcount
                    if rows > 0:
                        inserted_rows += rows
                        table_name = statement.split('INSERT INTO')[1].split('(')[0].strip()
                        print(f"✓ {rows} registro(s) insertado(s) en {table_name}")
                elif 'CREATE INDEX' in statement.upper():
                    print(f"✓ Índice creado")
                    
            except Error as err:
                if err.errno == 1050:  # Table already exists
                    pass  # Ignorar silenciosamente
                elif err.errno == 1007:  # Database already exists
                    pass  # Ignorar silenciosamente
                elif err.errno == 1062:  # Duplicate entry
                    pass  # Ignorar silenciosamente
                else:
                    print(f"✗ Error SQL: {err}")
        
        cursor.close()
        conn.close()
        
        return True, created_tables, inserted_rows
        
    except Error as err:
        print(f"✗ Error de conexión: {err}")
        return False, 0, 0

def main():
    """Función principal"""
    # Obtener ruta del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(script_dir, 'setup_database.sql')
    
    print("=" * 70)
    print("CONFIGURADOR DE BASE DE DATOS - SISTEMA DE VOTACIÓN BLOCKCHAIN")
    print("=" * 70)
    print(f"\nArchivo SQL: {sql_file}")
    print(f"Host: {DB_CONFIG['host']}")
    print(f"Usuario: {DB_CONFIG['user']}")
    print("\nEjecutando script SQL...\n")
    
    # Leer el archivo SQL
    sql_content = read_sql_file(sql_file)
    if sql_content is None:
        return False
    
    # Ejecutar el script
    success, tables_created, rows_inserted = execute_sql_script(sql_content)
    
    if success:
        print("\n" + "=" * 70)
        print("✓ BASE DE DATOS CONFIGURADA EXITOSAMENTE")
        print("=" * 70)
        print(f"\nTablas creadas: {tables_created}")
        print(f"Registros insertados: {rows_inserted}")
        print("\n📊 Datos disponibles:")
        print("  • 3 partidos políticos: CAMBIO, VALOR, UNIDOS")
        print("  • 15 candidatos")
        print("  • 10 votantes de prueba:")
        print("    - DNI 11111111: Juan Perez")
        print("    - DNI 22222222: María González")
        print("    - DNI 33333333: Carlos López")
        print("    - DNI 44444444: Ana Martínez")
        print("    - DNI 55555555: Roberto Sánchez")
        print("    - DNI 66666666: Patricia García")
        print("    - DNI 77777777: Luis Rodríguez")
        print("    - DNI 88888888: Sandra Fernández")
        print("    - DNI 99999999: Miguel Díaz")
        print("    - DNI 10101010: Elena Torres")
        print("\n✅ La aplicación está lista para usar!")
        print("\nPróximos pasos:")
        print("  source venv/bin/activate")
        print("  cd back")
        print("  python app.py")
        return True
    else:
        print("\n" + "=" * 70)
        print("✗ ERROR AL CREAR LA BASE DE DATOS")
        print("=" * 70)
        print("\n🔧 Solución de problemas:")
        print("\n1. Verifica que MySQL/MariaDB está ejecutándose:")
        print("   Linux:   sudo systemctl start mariadb")
        print("   macOS:   brew services start mysql")
        print("   Windows: net start MySQL80")
        print("\n2. Verifica las credenciales en DB_CONFIG")
        print("   Si tiene contraseña, actualiza:")
        print("   DB_CONFIG['password'] = 'tu_contraseña'")
        print("\n3. Verifica que el usuario existe:")
        print("   mysql -u root -p")
        print("   mysql> SELECT user FROM mysql.user;")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
