from flask import Flask, redirect, url_for, request, render_template, session
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
mongodb_key = "mongodb+srv://userdesarrolloweb:password_desarrolloweb@cluster0.6vflw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(
    mongodb_key, tls=True, tlsAllowInvalidCertificates=True)
db = client.Escuela
cuentas = db.Alumno
#############################################################

@app.route('/')
def home():
    email = None
    if 'email' in session:
        email = session['email']
    return render_template('index.html', error=email)


@app.route('/login', methods=['GET'])
def login():
    email = None
    if 'email' in session:
        email = session['email']
        return render_template('index.html', error=email)

    return render_template('login.html', error=email)


@app.route('/login', methods=['POST'])
def login2Index():
    email = ""
    if 'email' in session:
        return render_template('index.html', error=email)
    email = request.form['email']
    password = request.form['password']
    email_exist = cuentas.find_one({"correo":(email)})
    pass_exist = cuentas.find_one({"contrasena":(password)})
    if pass_exist != None and email_exist != None:
        session['email'] = email
        session['password'] = password
        return render_template('index.html', error=email)
    else:
        return "<p>Usuario o Contraseña incorrecta, regresa al login e intentelo de nuevo</p>" 


@app.route('/signup', methods=['POST'])
def signup():
    email = ""
    if 'email' in session:
        return render_template('index.html', error=email)
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        session['email'] = email
        session['password'] = password
        session['name'] = name
    return render_template('Create.html')


@app.route('/logout')
def logout():
    if 'email' in session:
        email = session['email']
    session.clear()
    return redirect(url_for('home'))


@app.route("/usuarios")
def usuarios():
    cursor = cuentas.find({})
    users = []
    for doc in cursor:
        users.append(doc)
    return render_template("/Usuarios.html", data=users)


@app.route("/insert", methods=["POST"])
def insertUsers():
    user = {
        "nombre": request.form["nombre"],
        "correo": request.form["correo"],
        "contrasena": request.form["contrasena"],
    }
    try:
        cuentas.insert_one(user)
        return redirect(url_for("usuarios"))
    except Exception as e:
        return "<p>El servicio no esta disponible =>: %s %s" % type(e), e


@app.route("/find_one/<matricula>")
def find_one(matricula):
    try:
        user = cuentas.find_one({"matricula": (matricula)})
        if user == None:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            return "<p>Encontramos: %s </p>" % (user)
    except Exception as e:
        return "%s" % e


@app.route("/delete/<nombre>")
def delete_one(matricula):
    try:
        user = cuentas.delete_one({"matricula": (matricula)})
        if user.deleted_count == None:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            return redirect(url_for("usuarios"))
    except Exception as e:
        return "%s" % e


@app.route("/update", methods=["POST"])
def update():
    try:
        filter = {"matricula": request.form["matricula"]}
        user = {"$set": {
            "nombre": request.form["nombre"],
        }}
        cuentas.update_one(filter, user)
        return redirect(url_for("usuarios"))

    except Exception as e:
        return "error %s" % (e)


@app.route('/create')
def create():
    return render_template('Create.html')
    

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