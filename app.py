from flask import Flask, render_template, request
import json

app = Flask(__name__)

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

if __name__=="__main__":
    app.run(debug=True)