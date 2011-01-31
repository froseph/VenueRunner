from flaskext.wtf import Form, TextField, DateField, IntegerField, validators, BooleanField, TextAreaField

class addevent(Form):
  name = TextField('Event Name', [validators.Length(min=1, max=63)])
  date = DateField('Date', [validators.Required('Need to provide a date')])
  description = TextAreaField('Description', [validators.Length(min=1, max=16384)])

class addcustomer(Form):
  first_name = TextField('First Name', [validators.Length(min=1, max=63)])
  last_name = TextField('Last Name', [validators.Length(min=1, max=63)])
  email = TextField('E-mail', [validators.Length(min=1, max=63), validators.Email()])
  lead = BooleanField('Lead', [])
  follow = BooleanField('Follow', [])
  signup = DateField('Signup Date', [validators.optional(),validators.Required('Need to provide a date')]) #TODO add good default
  note = TextAreaField('Note', [])
