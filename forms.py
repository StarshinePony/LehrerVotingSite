from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Anmelden')

class TeacherForm(FlaskForm):
    name = StringField('Name des Lehrers', validators=[DataRequired(), Length(min=3, max=100)])
    subject = StringField('Fach', validators=[DataRequired(), Length(min=3, max=100)])
    bio = TextAreaField('Biografie', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Lehrer speichern')

class RatingForm(FlaskForm):
    score = SelectField('Bewertung', 
                        choices=[(1, '1 - Mangelhaft'), (2, '2 - Ausreichend'), 
                                 (3, '3 - Befriedigend'), (4, '4 - Gut'), 
                                 (5, '5 - Sehr gut')], 
                        validators=[DataRequired()],
                        coerce=int)
    comment = TextAreaField('Kommentar (Optional)', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Bewertung abschicken')
