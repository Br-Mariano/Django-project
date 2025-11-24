import pymysql

connection = pymysql.connect(
    host='shupapibase.c6x4ouicsyul.us-east-1.rds.amazonaws.com',
    user='shupapidatabase',
    password='020507Bruno',  # Pon tu contraseña real
    port=3306
)

try:
    with connection.cursor() as cursor:
        # Ver bases de datos actuales
        cursor.execute("SHOW DATABASES;")
        print("Bases de datos actuales:")
        for db in cursor.fetchall():
            print(f"  - {db[0]}")
        
        print("\nCreando base de datos 'shupapibase'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS shupapibase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        connection.commit()
        print("Base de datos 'shupapibase' creada exitosamente")
        
        # Ver bases de datos después
        cursor.execute("SHOW DATABASES;")
        print("\nBases de datos despues de crear:")
        for db in cursor.fetchall():
            print(f"  - {db[0]}")
            
except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()