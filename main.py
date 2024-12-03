import requests
from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap5
from forms import Cafe_Form,Login_Form,Register_Form
from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column
from sqlalchemy import Integer,String
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,LoginManager,current_user,logout_user,UserMixin,login_required
import os


app=Flask(__name__)
Bootstrap5(app)
print(os.environ.get("FLASK_KEY21"))
print(os.environ.get("DB_URI21"))
app.config["SECRET_KEY"]=os.environ.get("FLASK_KEY21")

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Users,user_id)

class Base(DeclarativeBase):
    pass
# 21

app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DB_URI21","sqlite:///C:/Users/ganes/PycharmProjects/pythonProject21/instance/user2.db")
db=SQLAlchemy(model_class=Base)
db.init_app(app)

class Users(db.Model,UserMixin):
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

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        print("hii")
        new_user=Users(
            name=request.form.get("name"),
            email=request.form.get("email"),
            password=request.form.get("password")
        )
        print(request.form.get("name"),"name of register")
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        data=db.session.execute(db.select(Users).where(Users.email==email))
        data=data.scalar()
        print(data,"login_data")
        if data:
            print(data,"login area")
            login_user(data)
            return redirect(url_for("home"))
        else:
            return redirect(url_for("register"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/cafe/<int:post_id>",methods=["GET"])
@login_required
def post(post_id):
    data_all=requests.get("https://pythonproject20.onrender.com/all")
    data_all=data_all.json()["data"]
    print(data_all)
    object=0
    for i in data_all:
        if post_id==i["id"]:
            object=i
            break
    return render_template("post.html",post=object,current_user=current_user)

@app.route("/delete_post/<int:post_id>")
@login_required
def delete_cafe(post_id):
    data=requests.delete(f"https://pythonproject20.onrender.com/report-closed/{post_id}",params={"api-key":"TopSecretAPIKey"})
    if data.status_code==200:
        return redirect(url_for('home'))
    else:
        return "sorry there is nothing to delete"

@app.route("/new_cafe",methods=["GET","POST"])
@login_required
def add_cafe():
    if request.method=="POST":
        print("name",request.form.get("image"))
        data={
            "name":request.form.get("name"),
            "img_url":request.form.get("img_url"),
            "map_url":request.form.get("map_url")
        }
        post_request = requests.post("https://pythonproject20.onrender.com/add", data=data)
        print(post_request.status_code)
        return redirect(url_for("home"))
    # form=Cafe_Form()
    # if form.validate_on_submit():
    #     data = {
    #                 "name":request.form["name"],
    #                 "img_url":request.form["img_url"],
    #                 "map_url":request.form["map_url"]
    #             }
    #     post_request=requests.post("https://pythonproject20.onrender.com/add",data=data)
    #     print(post_request.status_code)
    #     return redirect(url_for("home"))
    return render_template("new_cafe.html")


if __name__=="__main__":
    app.run(debug=True)










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














