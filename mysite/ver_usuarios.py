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
        cursor.execute("SELECT id, username, email, is_superuser, is_staff FROM auth_user;")
        print("Usuarios en la base de datos:")
        for user in cursor.fetchall():
            print(f"  ID: {user[0]} | Usuario: {user[1]} | Email: {user[2]} | Superuser: {user[3]} | Staff: {user[4]}")
except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()