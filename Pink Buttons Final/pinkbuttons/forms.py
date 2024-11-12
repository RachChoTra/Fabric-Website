from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email

class CheckoutForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Purchase')


