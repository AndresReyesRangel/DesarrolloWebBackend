from flask import Flask, redirect, render_template, request, session, url_for
import datetime
import pymongo


# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=1)
app.secret_key = "super secret key"
#############################################################

# MONGODB
#############################################################
mongodb_key = "mongodb+srv://desarrollowebuser:desarrollowebpassword@cluster0.dfh7g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(
    mongodb_key, tls=True, tlsAllowInvalidCertificates=True)
db = client.Escuela
cuentas = db.alumno
#############################################################

@app.route('/')
def home():
    email = None
    if "email" == session:
        email = session["email"]
        return render_template('index.html', data = email)
    else:
        return render_template('login.html', data = email)


@app.route('/signup')
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    return render_template('index.html', error=email)
    

@app.route('/login', methods=["GET","POST"])
def login():
    if "email" in session:
        return redirect(url_for("home"))
    else:
        if(request.method == "GET"):
            return render_template('login.html', error="email")
        else:
            email = request.form["email"]
            password = request.form["password"]
            return render_template('index.html', error=email)

@app.route('/estructuradedatos')
def prueba():
    nombres = []
    nombres.append({"nombre":"andrés",
        "Semestre01":[{
            "Matematicas":"10",
            "Español":"10"
            }],
        "Semestre02":[{
            "Fisica":"10",
            "Progra":"10"
            }]
    })
    return render_template("home.html", data=nombres)

@app.route('/usuarios')
def usuarios():
    cursor = cuentas.find({})
    users = []
    for doc in cursor:
        users.append(doc)
    return render_template("/usuarios.html", data = users)

@app.route('/insert', methods=["POST"])
def insertUsers():
    user = {
        "matricula":"A01746592",
        "nombre":"Andres Reyes",
        "correo":"A01746592@tec.mx",
        "contrasena":"1234567"
    }

    try:
        cuentas.insert_one(user)
        return redirect(url_for("usuarios"))
    except Exception as e:
        return "<p>El servicio no está disponible: %s %s<p>" % type(e), e
    
@app.route('/find_one/<matricula>')
def find_one(matricula):
    try:
        user = cuentas.find_one({"matricula":(matricula)})
        if user == None:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            return "<p>Encontramos: %s </p>" % (user)
    except Exception as e:
        return "%s" % e

@app.route('/delete/<matricula>')
def delete_one(matricula):
    try:
        user = cuentas.delete_one({"matricula":(matricula)})
        if user.deleted_count == None:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            return redirect(url_for("usuarios"))

    except Exception as e:
        return "%s" % e


@app.route('/update', methods=["POST"])
def update():
    try:
        filter = {"matricula": request.form["matricula"]}
        user = {"$set": {
            "nombre": request.form["nombre"],
            "constrasena": request.form["contrasena"]
            }}
        cuentas.update_one(filter, user)
        return redirect(url_for("usuarios"))

    except Exception as e:
        return "error %s" % (e)

@app.route('/create')
def create():
    
    return render_template("/CreateForm.html")

    