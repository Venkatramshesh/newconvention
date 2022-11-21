from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

##WTForm
class SubmitForm(FlaskForm):
    email = StringField(label='Email',validators=[DataRequired(), Length(max=32)])
    name = StringField(label='Name', validators=[DataRequired(), Length(max=32)])
    submit = SubmitField(label='Submit Comment')