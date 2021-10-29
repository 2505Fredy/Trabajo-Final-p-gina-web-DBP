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
    def save(self, dataUsers):
        dataUsers.write('\n'+self.username+'\n'+self.password+'\n'+self.email)
#Aquí se cargará los usuarios guardados
Users=[]

@app.route("/")
def index():
    if 'userInSession' in session:
        session.clear()
    return render_template("index.html")


@app.route("/login")
def login():
    if 'userInSession' in session:
        session.clear()
    return render_template("login.html")

counter= 0
@app.route("/chooseTemplate", methods=['POST', 'GET'])
def chooseTemplate():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    Users.clear()
    if request.method == 'POST':
        if email == "" and not 'userInSession' in session:
            loadUsers()
            for index, value in enumerate(Users):
                if value.username == username and value.password == password:
                    session['userInSession'] = username
                    Users.clear()
                    return render_template('chooseTemplate.html')
            Users.clear()
            return redirect('login')
        if not User(username, password, email) in Users:
            loadUsers()
            Users.append(User(username, password, email))
            saveUsers()
        Users.clear()
        session['userInSession'] = username
        return render_template('chooseTemplate.html')
    return redirect(url_for('login'))

@app.route("/fieldsGen", methods=['POST', 'GET'])
def fieldsGen():
    if not 'userInSession' in session:
        session.clear()
        return redirect(url_for('index'))
    if len(request.form)==0:
        return "ERROR: ¡¡Se necesitan datos del formulario anterior!!"
    session['templateSelected'] = request.form.get('template')
    return render_template("fieldsGen.html", template=session['templateSelected'])

@app.route('/fillFields', methods=['POST', 'GET'])
def fillFields():
    if not 'userInSession' in session :
        session.clear()
        return redirect(url_for('index'))
    if len(request.form)==0:
        return "ERROR: ¡¡Se necesitan datos del formulario anterior!!"
    session["noDataProfile"] = int(request.form.get("noDataProfile"))
    session["noProgram"] = int(request.form.get("noProgram"))
    session["noLanguage"] = int(request.form.get("noLanguage"))
    session["noWorks"] = int(request.form.get("noWorks"))
    session["noEducation"] = int(request.form.get("noEducation"))
    return render_template('fillFields.html', noData= session["noDataProfile"], noProgram= session["noProgram"], noLanguage= session["noLanguage"], noWorks= session["noWorks"], noEducation= session["noEducation"])

@app.route("/generated", methods=['POST', 'GET'])
def generated():
    if not 'userInSession' in session :
        session.clear()
        return redirect(url_for('index'))
    if len(request.form)==0:
        return "<h1>ERROR: ¡¡Se necesitan datos del formulario anterior!!</h1>"
    templateUrl = f"/static/css/{session['templateSelected']}.css"
    name= request.form.get("completName")
    workOcuped= request.form.get("positionHeld")
    presentacion=request.form.get("presentation")
    noData=session.get("noDataProfile", None)
    noProgram=session.get("noProgram", None)
    noLanguage=session.get("noLanguage", None)
    noWorks=session.get("noWorks", None)
    noEducation=session.get("noEducation", None)
    listContact=[request.form.get('contactMail'), request.form.get('contactWhats'), request.form.get('contactFace'), request.form.get('contactLink'), request.form.get('contactSky'), request.form.get('contactTwit')] 
    listData=[]
    listProgram=[]
    listLanguage=[]
    listWork=[]
    listEducation=[]
    for i in range(noProgram):
        listProgram.append([request.form.get(f'programName{i}'), request.form.get(f'programLevel{i}')])
    for i in range(noLanguage):
        listLanguage.append([request.form.get(f'langName{i}'), request.form.get(f'langLevel{i}')])
    for i in range(noData):
        listData.append([request.form.get(f'dataName{i}'), request.form.get(f'dataValue{i}')])
    for i in range(noWorks):
        listWork.append([request.form.get(f'dirWork{i}'), request.form.get(f'nameCompany{i}'), request.form.get(f'workName{i}'), request.form.get(f'startWork{i}'), request.form.get(f'endWork{i}'), request.form.get(f'review{i}')])
    for i in range(noEducation):
        listEducation.append([request.form.get(f'dirStudy{i}'), request.form.get(f'startStudy{i}'), request.form.get(f'endStudy{i}'), request.form.get(f'academicDegree{i}'), request.form.get(f'nameInstitution{i}')])
    return render_template("generated.html", templateUrl= templateUrl, name= name, workOcuped= workOcuped, presentation= presentacion, listContact= listContact, listData= listData, listLanguage= listLanguage, listProgram= listProgram, listWork= listWork, listEducation= listEducation)

@app.route("/logout")
def logout():
    session.pop('userInSession', None)
    session.clear()
    return redirect(url_for("index"))

def printU(users):
    for i in users:
        print(i)


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
        i.save(dataUsers)
    dataUsers.close()


if __name__ == "__main__":
    app.run(debug=True)