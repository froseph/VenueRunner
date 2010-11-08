from flaskext.wtf import Form, TextField, DateField, IntegerField, validators, BooleanField, TextAreaField

class addevent(Form):
  name = TextField('Event Name', [validators.Length(min=1, max=63)])
  date = DateField('Date', [validators.Required('Need to provide a date')])
  price = IntegerField('Default Price', [validators.optional(), validators.NumberRange(min=None, max=None)])
  description = TextField('Description', [validators.Length(min=1, max=16384)])

class addcustomer(Form):
  firstname = TextField('First Name', [validators.Length(min=1, max=63)])
  lastname = TextField('Last Name', [validators.Length(min=1, max=63)])
  email = TextField('E-mail', [validators.Length(min=1, max=63), validators.Email()])
  lead = BooleanField('Lead', [])
  follow = BooleanField('Follow', [])
  signup = DateField('Signup Date', [validators.optional(),validators.Required('Need to provide a date')]) #TODO add good default
  note = TextAreaField('Note', [])
