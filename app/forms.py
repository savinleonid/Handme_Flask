from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    title = StringField('Product Name', validators=[DataRequired()])
    description = StringField('About',validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    category = SelectField('Category', validate_choice=False)
    location = StringField('Location', validators=[DataRequired()])
    image = FileField('Image', default='media/product_images/default_product.png')

