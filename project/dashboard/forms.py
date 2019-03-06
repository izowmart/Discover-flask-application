from wtforms import Form, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=70)])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=20)])
