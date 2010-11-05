from flaskext.wtf import Form, TextField, DateField, IntegerField, validators

class addevent(Form):
  name = TextField('Event Name', [validators.Length(min=1, max=63)])
  date = DateField('Date', [validators.Required('Need to provide a date')])
  price = IntegerField('Default Price', [validators.optional(), validators.NumberRange(min=None, max=None)])
  description = TextField('Description', [validators.Length(min=1, max=16384)])
