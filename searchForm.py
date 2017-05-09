from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(Form):
    studentId = StringField("Student Id", validators=[DataRequired("Student ID is a required field")])
    subjectCode = StringField("Subject Code", validators=[DataRequired("Subject Code is required")])
    gradePoint = StringField("Minimum Grade Point") 
    submit = SubmitField("Search Now")