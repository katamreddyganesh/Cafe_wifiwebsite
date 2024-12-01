import requests
from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap5
from forms import Cafe_Form,Login_Form,Register_Form
from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column
from sqlalchemy import Integer,String
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,LoginManager,current_user,logout_user,UserMixin



app=Flask(__name__)
Bootstrap5(app)
app.config["SECRET_KEY"]="ganeshreddy"

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Users,user_id)

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///C:/Users/ganes/PycharmProjects/pythonProject21/instance/user2.db"
db=SQLAlchemy(model_class=Base)
db.init_app(app)

class Users(db.Model):
    __tablename__ = "users"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String,nullable=False)
    email:Mapped[str]=mapped_column(String,unique=True)
    password:Mapped[str]=mapped_column(String,nullable=False)
with app.app_context():
    db.create_all()




data=Users(
        name="Ganesh katamreddy",
        email="ganeshreddyk8g@gmail.com",
        password="k.ganesh789"
    )
# with app.app_context():
#     db.session.add(data)
#     db.session.commit()






@app.route("/")
def home():
    data_all=requests.get("https://pythonproject20.onrender.com/all")
    print(data_all.status_code)
    data_all=data_all.json()["data"]
    print(data_all)
    return render_template("index.html",data=data_all)

@app.route("/cafe/<int:post_id>",methods=["GET"])
def post(post_id):
    data_all=requests.get("https://pythonproject20.onrender.com/all")
    data_all=data_all.json()["data"]
    object=0
    for i in data_all:
        if post_id==i["id"]:
            object=i
            break
    return render_template("post.html",post=object,current_user=current_user)


@app.route("/delete_post/<int:post_id>")
def delete_cafe(post_id):
    data=requests.delete(f"https://pythonproject20.onrender.com/report-closed/{post_id}",params={"api-key":"TopSecretAPIKey"})
    if data.status_code==200:
        return redirect(url_for('home'))
    else:
        return "sorry there is nothing to delete"

@app.route("/new_cafe",methods=["GET","POST"])

def add_cafe():
    form=Cafe_Form()
    if form.validate_on_submit():
        print("name",request.form["name"])
        data={
            "name":request.form["name"],
            "img_url":request.form["img_url"],
            "map_url":request.form["map_url"]
        }
        post_request=requests.post("https://pythonproject20.onrender.com/add",data=data)
        print(post_request.status_code)
        return redirect(url_for("home"))
    return render_template("new_cafe.html",form=form,current_user=current_user)

@app.route("/register",methods=["GET","POST"])
def register():
    form=Register_Form()
    if form.validate_on_submit():
        data=Users(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"]
        )
        db.session.add(data)
        db.session.commit()
        login_user(data)
        return redirect(url_for("home"))
    return render_template("register.html",form=form,current_user=current_user)

@app.route("/login",methods=["GET","POST"])
def login():
    form=Login_Form()
    if form.validate_on_submit():
        email=request.form["email"]
        data=db.session.execute(db.select(Users).where(Users.email==email))
        data=data.scalar()
        if data:
            print(data,"login area")
            login_user(data)
            return redirect(url_for("home"))

    return render_template("login.html",form=form,current_user=current_user)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__=="__main__":
    app.run(debug=True,port=5001)










# data={
#     "name":"kotavenu8y384",
#     "map_url":"https://www.google.com/maps/place/Old+Spike+Roastery/@51.4651552,-0.0666088,17z/data=!4m12!1m6!3m5!1s0x487603a3a7dd838d:0x4105b39b30a737cf!2sOld+Spike+Roastery!8m2!3d51.4651552!4d-0.0666088!3m4!1s0x487603a3a7dd838d:0x4105b39b30a737cf!8m2!3d51.4651552!4d-0.0666088"
# }
#
# data_post=requests.post(url="https://pythonproject20.onrender.com/add",data=data)
# print(data_post.status_code)
# print(data_post.text)
#
# # #
# # data=requests.get("https://pythonproject20.onrender.com/update-price/4",params={"new_price":9})
# # print(data.status_code)
#
# # delete=requests.get("https://pythonproject20.onrender.com/report-closed/2",params={"api-key":"TopSecretAPIKey"})
# # print(delete.status_code)
# # print(delete.text)
# data=requests.get("https://pythonproject20.onrender.com/all")
# print(data.json())

# from flask_bootstrap import Bootstrap5
# app=Flask(__name__)
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# Bootstrap5(app)
#
#














