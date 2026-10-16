from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,Length, ValidationError

class postform(FlaskForm):
  title = StringField('title',validators=[DataRequired()])
  content = TextAreaField('content', validators =[DataRequired()])
  submit = SubmitField('submit')