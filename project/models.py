from . import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class MenuItem(db.Model):
    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    course = db.Column(db.String(250))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.    relationship(Restaurant)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


class UserAccount(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=True)

    @property
    def is_admin(self):
        return self.role == 'admin'


class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Enter Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user = UserAccount.query.filter_by(
            username=username.data).first()
        if existing_user:
            raise ValidationError(
                'That username already exists.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Enter Password"})

    submit = SubmitField('Login')
