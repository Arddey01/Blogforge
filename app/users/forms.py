from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed 
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,Length, ValidationError
from app.model import User

class Registerform(FlaskForm):
  username =StringField('username', validators=[DataRequired(),Length(min=2,max=20)])
  email = StringField('email', validators=[DataRequired(),Email()])
  password = PasswordField('password', validators=[DataRequired(),Length(min=2,max=20)])
  confirm_password = PasswordField('confirm_password', validators=[DataRequired(),EqualTo('password')])
  submit = SubmitField('sign up')


  def validate_username(self,username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('he username is taken. please choose a different username')

    
  def validate_email(self,email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('he email is taken. please choose a different username')

class loginform(FlaskForm):
  email=StringField("email",validators=[DataRequired(),Email()])
  password=PasswordField("password",validators=[DataRequired(),Length(min=2,max=20)])
  remember=  BooleanField("remember me")
  submit = SubmitField("sign in")


class Updateaccountform(FlaskForm):
  username =StringField('username', validators=[DataRequired(),Length(min=2,max=20)])
  email = StringField('email', validators=[DataRequired(),Email()])
  picture = FileField('update profile picture', validators =[FileAllowed(['jpg','jpeg', 'png'])])
  submit = SubmitField('update')


  def validate_username(self,username):
    if username.data != current_user.username:
      user = User.query.filter_by(username=username.data).first()
      if user:
       raise ValidationError('he username is taken. please choose a different username')

    
  def validate_email(self,email):
     if email.data != current_user.email:
         user = User.query.filter_by(email=email.data).first()
         if user:
          raise ValidationError('he email is taken. please choose a different username')


class requestresetform(FlaskForm):
  email = StringField('email', validators=[DataRequired(),Email()])
  submit = SubmitField('Request Password Reset')

def validate_email(self,email):
    user = User.query.filter_by(email=email.data).first()
    if user is None:
      raise ValidationError('There is no account with that email.You can Register')

class ResetPasswordForm(FlaskForm):
  password = PasswordField('password', validators=[DataRequired(),Length(min=2,max=20)])
  confirm_password = PasswordField('confirm_password', validators=[DataRequired(),EqualTo('password')])
  submit = SubmitField('Password Reset')