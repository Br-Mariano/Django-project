import pymysql

connection = pymysql.connect(
    host='shupapibase.c6x4ouicsyul.us-east-1.rds.amazonaws.com',
    user='shupapidatabase',
    password='020507Bruno',
    database='shupapibase',
    port=3306
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nombre, usuario, correo, creado_en FROM usuarios;")
        print("Usuarios registrados en AWS RDS:")
        print("-" * 80)
        for user in cursor.fetchall():
            print(f"ID: {user[0]}")
            print(f"Nombre: {user[1]}")
            print(f"Usuario: {user[2]}")
            print(f"Correo: {user[3]}")
            print(f"Creado: {user[4]}")
            print("-" * 80)
except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()