from flask import Flask,render_template,request,url_for,logging,redirect,flash  
import mysql.connector
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'user'
app.config["MYSQL_PASSWORD"] = 'user'
app.config["MYSQL_DB"] = "register"
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        pswd = request.form["paswd"]
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users where Username = %s",(username,))
        res = cur.fetchone()
        cur.close()

        if res:
            if pswd == res['password']:
                #flash("You are logged in","success")
                return render_template("profile.html") 
            else:
                flash("Incorrect Password","danger")
                return render_template("login.html")
        else:
            flash("Username does not exist","danger")
            return render_template("login.html")
    else: 
        return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form["name"]
        username = request.form["uname"]
        password = request.form["pwd"]
        confirm = request.form["conf_pass"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users where Username = %s",(username,))
        res = cur.fetchone()
        if res is None:
            if password == confirm:
                cur.execute("INSERT INTO users(Name,Username,Password) VALUES(%s,%s,%s)",(name,username,password))
                mysql.connection.commit()
                flash("You are registered and can Login", "success")
                return redirect(url_for('login'))
            else:
                flash("Password does not match", "danger")
                return render_template("register.html")
        else:
            flash("Username is taken, please use another", "danger")
            return render_template("register.html")

if __name__ == '__main__':
    app.secret_key="asdfg"
    app.run(debug=True)
