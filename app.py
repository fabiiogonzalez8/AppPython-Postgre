from flask import Flask,render_template,abort,json,request
import os

app = Flask(__name__)

f = open('msx.json',)

datos = json.load(f)

@app.route('/',methods=["GET","POST"])
def inicio():
	return render_template("index.html")

@app.route('/juegos',methods=["GET"])
def juegos():
    return render_template("juegos.html")

@app.route('/listajuegos',methods=["POST"])
def listajuegos():
  listajuegos=[]
  formulario=request.form.get("informacion")
  for a in datos:
  	if str(formulario) == "" or str(a["nombre"]).startswith(formulario) :
	   listajuegos.append(a)
  return render_template("listajuegos.html",listajuegos=listajuegos)

@app.route('/juego/<identificador>')
def juego(identificador):
  lista=[]
  ind=False
  for b in datos:
    if int(b.get("id")) == int(identificador):
      ind=True
      lista.append(b)
  if ind:
    return render_template("juego.html",lista=lista)
  else:
    abort(404)

app.run("0.0.0.0",5000,debug=True)
