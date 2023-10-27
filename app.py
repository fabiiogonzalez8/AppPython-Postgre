from flask import Flask, flash, redirect, request, session, render_template, abort
import os
import psycopg2

app = Flask (__name__)

def get_db_connect():
    connect = None
    emp = None
    dept = None
    tabla = None

    try:
        connect = psycopg2.connect(host="192.168.122.133", dbname="prueba", user="fabio", password="usuario")
    except Exception as excepcion:
        print("No puedo conectar a la base de datos:",excepcion)

    return connect


def emp_dept():
    connect = get_db_connect()

    emp = connect.cursor()
    emp.execute("select * from emp;")
    empno = emp.fetchall()

    tabla_cursor = connect.cursor()
    tabla_cursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    tablas = tabla_cursor.fetchall()

    dept = connect.cursor()
    dept.execute("select * from dept;")
    deptno=dept.fetchall()

    return render_template("postgres.html", tablas=tablas, empno=empno, deptno=deptno)


@app.route('/',methods=["GET"])
def inicio():
    if not session.get("logged_in"):
        return render_template("index.html")
    else:
        return emp_dept()

@app.route('/login', methods=["POST"])
def login():
    if request.form['usuario'] == 'fabio' and request.form['clave'] == 'usuario':
        session['logged_in'] = True
    return redirect("/")

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run('0.0.0.0' ,debug=False)