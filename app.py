from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash
import logging, os, datetime, secrets
from passlib.hash import sha256_crypt

# Bibliotheken für die Verbindung mit dem mysql-Server
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

## Flask App deklarieren
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16) ## Geheimer Schlüssel für Benutzersitzung erforderlich

## SQL-Serverdaten
SQL_USERNAME = "car_user"
SQL_PASSWORD = "PW2Tlky0987"
SQL_HOST = "mysql"
SQL_DATABASE = "car_inventory"
SQL_PARAM = ("mysql+pymysql://{user}:{password}@{host}/{database}").format(user=SQL_USERNAME,password = SQL_PASSWORD,host = SQL_HOST,database = SQL_DATABASE)

## Initialisieren der Datenbankverbindung
engine = create_engine(SQL_PARAM, pool_recycle=1800)
db = scoped_session(sessionmaker(bind=engine))

## Prüfen, ob String ein Float ist
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

## Route zum Hinzufügen eines neuen Benutzers
def addUser(username, password, firstName, lastName):
    db.execute("INSERT INTO users(username, password, firstName, lastName, accType) VALUES (:username, :password, :firstName, :lastName, :accType)", {
        "username" : username.upper(),
        "password" : sha256_crypt.hash(password),
        "firstName" : firstName.capitalize(), 
        "lastName" : lastName.capitalize(),
        "accType" : "STANDARD"
    })
    db.commit();

## Prüfen, ob der Benutzer existiert
def validateUser(username, password):
    allUsernames = db.execute("SELECT username FROM users").fetchall()
    if (username,) in allUsernames:
        passwordReq = db.execute("SELECT password FROM users where username=:username",{
            "username" : username
        }).fetchone()
        if sha256_crypt.verify(password, passwordReq[0]):
            return True
    return False

## Benutzerkontotyp abrufen
def getAccType(username):
    accType = db.execute("SELECT accType FROM users WHERE username=:username",{
        "username" : username
    }).fetchone()
    return accType[0]

## Prüfen, ob der Benutzername bereits existiert
def checkExistingUsername(username):
    allUsernames = db.execute("SELECT username FROM users").fetchall()
    if (username,) in allUsernames:
        return True
    else:
        return False

## Details zur Sitzung 
def setSessionDetails(username):
    details = db.execute("SELECT firstName, lastName, accType from users WHERE username =:username",{
        "username" : username
    }).fetchall()[0]
    session["USERNAME"] = username
    session["FIRSTNAME"] = details[0]
    session["LASTNAME"] = details[1]
    session["ACCTYPE"] = details[2]

## Transaktion hinzufügen
@app.route("/addTransaction/reg=<regPlate>&kmDistance=<kmDistance>&fuelAmount=<fuelAmount>&fuelCost=<fuelCost>")
def addTransaction(regPlate, kmDistance, fuelCost, fuelAmount, date):
    db.execute("INSERT INTO cars(regplate, kmDistance, fuelAmount, fuelCOST, date) VALUES (:reg, :distance, :amount, :cost, :date)",{
        "reg" : regPlate,
        "distance" : kmDistance,
        "amount" : fuelAmount,
        "cost" : fuelCost,
        "date" : date
    })
    db.commit()

def getAllTransactions():
    allData = db.execute("SELECT * FROM cars ORDER BY date").fetchall()
    return allData

def getUserJourneys(username):
    data = db.execute("SELECT * FROM cars WHERE regplate=:username ORDER BY date",{
        "username" : username
    }).fetchall()
    return data




## Landing Page (Anmeldung)
@app.route("/")
def home():
    if "ACCTYPE" not in session:
        return render_template("login.html")
    else: 
        if session["ACCTYPE"] == "ADMIN":
            return redirect(url_for('adminDash'))
        else:
            return redirect(url_for('userDash'))


## Admin Seite
@app.route("/adminDash")
def adminDash():
    if "ACCTYPE" not in session:
        return redirect(url_for('home'))
    else: 
        if session["ACCTYPE"] == "ADMIN":
            return render_template("adminDash.html", data=getAllTransactions())
        else:
            return redirect(url_for('userDash'))


## Benutzeranmeldung 
@app.route("/handleLogin", methods=["POST"])
def handleLogin():
    username = (request.form['username']).upper()
    password = (request.form['password'])

    if (validateUser(username, password) == False):
        flash("The Account details are incorrect.")
        return redirect(url_for('home'))
    else :
        ## Benutzersitzung festlegen und Benutzer umleiten
        setSessionDetails(username=username)
        if getAccType(username=username.upper()) == "ADMIN" :
            return redirect(url_for('adminDash'))
        else:
            return redirect(url_for('userDash'))

@app.route("/createAccount")
def createAccount():
    if "ACCTYPE" not in session:
        return render_template("createAcc.html")
    else: 
        if session["ACCTYPE"] == "ADMIN":
            return redirect(url_for('adminDash'))
        else:
            return redirect(url_for('userDash'))

## Konto erstellen
@app.route("/handleCreateAccount", methods=["POST"])
def handleCreateAccount():
    username = (request.form['username']).upper()
    password = (request.form['password'])
    firstName = (request.form['firstName'])
    lastName = (request.form['lastName'])

    if checkExistingUsername(username=username):
        flash ("Reg plate account already exists")
        return redirect(url_for('createAccount')) 
    else:
        addUser(
            username=username,
            password=password,
            firstName=firstName,
            lastName=lastName
        )
        return redirect(url_for("userDash"))


## Allgemeine Benutzerseite
@app.route("/userDash")
def userDash():
    if "ACCTYPE" not in session:
        return redirect(url_for("home"))
    else:
        return render_template("userDash.html", data=getUserJourneys(session["USERNAME"]))


## Übermittlung von Benutzer-Dashs bearbeiten
@app.route("/handleNewTransaction", methods=["POST"])
def handleNewTransaction():
    cost = request.form['cost']
    amount = request.form['amount']
    distance = request.form['distance']
    date = request.form['date']

    if (isfloat(cost) == False or isfloat(amount) == False or isfloat(distance) == False):
        flash("Input must be number","danger")
        print ("error")
        return redirect(url_for("userDash"))


    else:
        flash("Journey Added","success")
        addTransaction(
            regPlate=session["USERNAME"],
            kmDistance=float(distance),
            fuelCost=float(cost),
            fuelAmount=float(amount),
            date=date
        )
        print ("added")
        return redirect(url_for("userDash"))
        

# Meldet den Benutzer ab
@app.route('/sign-out')
def signOut():
    ## Alle Sitzungsvariablen löschen
    session.clear()
    ## Zurück zur Anmeldeseite
    return redirect('/')

if __name__ == "__main__" :
    app.run(
        debug=True, port=7080, host='localhost'
    )
