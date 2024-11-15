from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from vincemart.models import Users


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = Users.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
        
    def validate_email_address(self, email_address_to_check):
        email = Users.query.filter_by(email=email_address_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email address')
    
    username = StringField(label='username', validators= [Length(min=2, max=20), DataRequired()])
    email_address = StringField(label='email', validators= [Email(), DataRequired()])
    address = StringField(label='adrress', validators= [DataRequired()])
    phone = StringField(label='phone', validators= [DataRequired()])
    password1 = PasswordField(label='password1', validators= [Length(min=6), DataRequired()])
    password2 = PasswordField(label='password1', validators= [EqualTo('password1'), DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField(label='username', validators= [DataRequired(), Length(min=2, max=20)])
    password = PasswordField(label='password', validators= [DataRequired(), Length(min=6)])
    submit = SubmitField('Login')
