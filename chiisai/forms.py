from wtforms import Form, BooleanField, TextField, PasswordField, validators


class URLShortenerForm(Form):
    url = TextField('URL', [validators.Required(), validators.URL()])
    alias = TextField('Alias', [validators.Optional(), validators.Length(min=2, max=50)])
