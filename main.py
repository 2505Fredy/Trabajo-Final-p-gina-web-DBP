import enum
from flask import Flask, request, render_template, redirect, session, url_for
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'sa3243dsads3w24'

Session(app)

#Definimos la clase Usuario
class User:
    def __init__(self, username, password, email):
        self.username= username
        self.password= password
        self.email= email
    def __str__(self):
        return f"{self.username} {self.password} {self.email}"
    def save(self):
        dataUsers= open("data/users.txt", "a")
        dataUsers.write('\n'+self.username+'\n'+self.password+'\n'+self.email)
        dataUsers.close()
#Aquí se cargará los usuarios guardados
Users=[]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/chooseTemplate", methods=['POST', 'GET'])
def chooseTemplate():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    print(Users) #####
    if request.method == 'POST':
        if email == "" and not 'userInSession' in session:
            for index, value in enumerate(Users):
                if value.username == username and value.password == password:
                    session.pop('userInSession', username)
                    return render_template('chooseTemplate.html')
            return redirect('login')
        Users.append(User(username, password, email))
        session.pop('userInSession', username)
        print(Users[0])
        return render_template('chooseTemplate.html')
    session.clear()
    return render_template('login.html')

@app.route("/logout")
def logout():
    return render_template("logout.html")

def loadUsers():
    value=0
    username=""
    password=""
    email="" 
    dataUsers= open("data/users.txt", "r")
    value= dataUsers.readline()
    for i in range(int(value)):
        username= dataUsers.readline()
        password= dataUsers.readline()
        email= dataUsers.readline()
        username= username.replace('\n','')
        password= password.replace('\n','')
        email= email.replace('\n','')
        Users.append(User(username, password, email))
    dataUsers.close()
def saveUsers():
    dataUsers= open("data/users.txt", "w")
    dataUsers.write(str(len(Users)))
    dataUsers.close()
    dataUsers= open("data/users.txt", "a")
    for i in Users:
        i.save()
    dataUsers.close()


if __name__ == "__main__":
    app.run(debug=True)