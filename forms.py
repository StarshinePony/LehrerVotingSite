from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TeacherForm(FlaskForm):
    name = StringField('Teacher Name', validators=[DataRequired(), Length(min=3, max=100)])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=3, max=100)])
    bio = TextAreaField('Biography', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Save Teacher')

class RatingForm(FlaskForm):
    score = SelectField('Rating', 
                        choices=[(1, '1 - Poor'), (2, '2 - Below Average'), 
                                 (3, '3 - Average'), (4, '4 - Good'), 
                                 (5, '5 - Excellent')], 
                        validators=[DataRequired()],
                        coerce=int)
    comment = TextAreaField('Comment (Optional)', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Submit Rating')
