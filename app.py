from flask import Flask, render_template, request, abort, make_response, session, redirect
import microservices.check as check
from dotenv import load_dotenv
from datetime import timedelta
import json
import os

load_dotenv()
app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")
app.secret_key = secret_key
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] =  "Lax"
app.config["SESSION_COOKIE_DOMAIN"] = "127.0.0.1:5000"
app.permanent_session_lifetime = timedelta(weeks=2)
app.url_map.strict_slashes = False

app.register_blueprint(check.check)

@app.route("/", methods=["GET"])
def main():
    readed = None
    with open("products.json", "r") as f:
        readed = json.load(f)
        
    return render_template("index.html", lista=readed)

@app.route("/post/product", methods=["POST"])
def post_method():
    name = request.form.get("producto")
    precio = request.form.get("precio")
    cant = request.form.get("cantidad")
    
    readed = None
    with open("products.json", "r") as f:
        readed = json.load(f)
        
    readed.append( {"id":10, "name":name, "price":precio, "cant":cant} )
    with open("products.json", "w") as f2:
        json.dump(readed, f2, indent=4)
        
    return "<h1>Hecho!</h1>"

@app.route("/login/form", methods=["GET"])
def form():
    return render_template("login.html")

@app.route("/login/verify", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if None in [username, password]:
        abort(400)
        
    if len(username) < 3 or len(username) > 20:
        response = make_response("Su nombre de usuario debe tener entre 3 y 20 caracteres")
        response.status_code = 400
        return response
    
    if len(password) < 8 or len(password) > 30:
        response = make_response("Su contraseña debe tener entre 8 y 30 caracteres")
        response.status_code = 400
        return response
    
    with open("users.json", "r") as file:
        f = json.load(file)
        for value in f:
            if value.get("username") == username and value.get("password") == password:
                response = redirect("/")
                response.status_code = 200
                session["username"] = username
                return response
    
    abort(401)

if __name__=="__main__":
    app.run(debug=True)