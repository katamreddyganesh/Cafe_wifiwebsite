from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Email,URL





class Cafe_Form(FlaskForm):
    name=StringField("Name",validators=[DataRequired()])
    img_url=StringField("Image_Url",validators=[DataRequired()])
    map_url=StringField("Location_Url",validators=[URL()])
    submit=SubmitField()


class Login_Form(FlaskForm):
    email=StringField("Email",validators=[DataRequired()])
    password=StringField("Password",validators=[DataRequired()])
    login=SubmitField()

class Register_Form(FlaskForm):
    name=StringField("Name",validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired()])
    password=StringField("Password",validators=[DataRequired()])
    register=SubmitField()


