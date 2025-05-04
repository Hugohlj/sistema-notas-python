import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",         
        user="root",       
        password="001144Hugo",     # substituir pela senha do MySQL, se houver. ex: "40028922"
        database="sistema_nota"      # ex: 'sistema_nota'
    )