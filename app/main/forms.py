from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Doctor, Departments, Patient
import datetime


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddDoctorForm(Form):
    workcard = StringField('Workcard', validators=[DataRequired(), Length(4,4),
                                                   Regexp('[0-9]',0,'workcard must be numbers')])
    idcard = StringField('Idcard', validators=[DataRequired(), Length(18, 18),
                                               Regexp('[0-9]', 0, 'idcard must be numbers')])
    name = StringField('Name', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    depart_id = SelectField(u'department', coerce=int)
    submit = SubmitField('AddDoctor')

    def validate_workcard(self, field):
        if Doctor.query.filter_by(workcard=field.data).first():
            raise ValidationError('workcard already registered.')

    def validate_idcard(self, field):
        if Doctor.query.filter_by(idcard=field.data).first():
            raise ValidationError('idcard already in use.')

class AddDepartmentForm(Form):
    name = StringField('Name', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'departmentnames must have only letters, '
                                              'numbers, dots or underscores')])
    submit = SubmitField('AddDepartment')

    def validate_name(self, field):
        if Departments.query.filter_by(name=field.data).first():
            raise ValidationError('department already added.')

class AddPatientForm(Form):
    medcard = StringField('Medcard', validators=[DataRequired(), Length(8,8),
                                                   Regexp('[0-9]',0,'medcard must be numbers')])
    idcard = StringField('Idcard', validators=[DataRequired(), Length(18, 18),
                                               Regexp('[0-9]', 0, 'idcard must be numbers')])
    birthday = DateField('Birthday', validators=[DataRequired()],format='%Y-%m-%d')
    gender = SelectField(u'Gender', coerce=int)
    phone = StringField('Phone', validators=[DataRequired(), Length(11, 11),
                                                 Regexp('[0-9]', 0, 'phone must be numbers')])
    address = StringField('Address', validators=[DataRequired(),Length(1,128)])
    name = StringField('Name', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('AddPatient')

    def validate_medcard(self, field):
        if Patient.query.filter_by(medcard=field.data).first():
            raise ValidationError('medcard already registered.')

    def validate_idcard(self, field):
        if Patient.query.filter_by(idcard=field.data).first():
            raise ValidationError('idcard already in use.')

class BookingForm(Form):
    depart_id = SelectField(u'Department', coerce=int)
    bookingday = DateField('Bookingday', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Submit')

    def validate_bookingday(self, field):
        if field.data < datetime.datetime.now().date():
            raise ValidationError("You can't book a doctor from the past.")


class BookingDoctorForm(Form):
    doctor_id = SelectField(u'Doctor', coerce=int)
    submit = SubmitField('Submit')