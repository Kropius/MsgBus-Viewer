from flask_wtf import FlaskForm
from wtforms import FileField, validators, SubmitField


class UploadFile(FlaskForm):
    file = FileField(u'Log File', validators=[validators.DataRequired()])
    changeFile = SubmitField("Change File")

class SelectDeselect(FlaskForm):
    select = SubmitField('Select')
    deselect = SubmitField('Deselect')
