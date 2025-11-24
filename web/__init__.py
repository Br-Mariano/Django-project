# Este archivo permite que Django use pymysql como reemplazo de mysqlclient
# pymysql es más fácil de instalar en Windows porque no requiere compiladores C++
import pymysql
pymysql.install_as_MySQLdb()