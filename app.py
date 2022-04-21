from flask import Flask, redirect, render_template, request, session, url_for
import datetime


# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=1)
app.secret_key = "super secret key"
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