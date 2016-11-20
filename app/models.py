from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


class Permission:
    DOCTOR = 0x01
    REGISTRAR = 0x02
    PATIENT = 0x04
    ADMINISTER = 0x80

class Registration(db.Model):
    __tablename__ = 'registrations'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    registration_date = db.Column(db.Date)


class Patient(UserMixin, db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    medcard = db.Column(db.String(64), unique=True, index=True)
    idcard = db.Column(db.String(64), unique=True, index=True)
    birthday = db.Column(db.Date)
    gender = db.Column(db.Integer)
    phone = db.Column(db.String(64), index=True)
    address = db.Column(db.String(256))
    name = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    doctors = db.relationship('Registration',
                              foreign_keys=[Registration.patient_id],
                              backref = db.backref('patient', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.medcard.encode('utf-8')

    def can(self, permissions):
        return permissions == Permission.PATIENT

    def is_administrator(self):
        return False

class Doctor(UserMixin, db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    workcard = db.Column(db.String(64), unique=True, index=True)
    idcard = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    depart_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    patients = db.relationship('Registration',
                               foreign_keys=[Registration.doctor_id],
                               backref=db.backref('doctor', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.workcard.encode('utf-8')

    def can(self, permissions):
        return permissions == Permission.DOCTOR

    def is_administrator(self):
        return False

class Departments(UserMixin, db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    doctors = db.relationship('Doctor', backref='department')

class Registrar(UserMixin, db.Model):
    __tablename__ = 'registrar'
    id = db.Column(db.Integer, primary_key=True)
    workcard = db.Column(db.String(64), unique=True, index=True)
    idcard = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.workcard.encode('utf-8')

    def can(self, permissions):
        return permissions == Permission.REGISTRAR

    def is_administrator(self):
        return False

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.account.encode('utf-8')

    def can(self, permissions):
        return permissions == Permission.ADMINISTER

    def is_administrator(self):
        return True

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    user_id = user_id.decode('utf-8')
    if len(user_id) == 8:
        return Patient.query.filter_by(medcard=user_id).first()
    elif len(user_id) == 5:
        return Registrar.query.filter_by(workcard=user_id).first()
    elif len(user_id) == 4:
        return Doctor.query.filter_by(workcard=user_id).first()
    elif len(user_id) == 3:
        return Admin.query.filter_by(account=user_id).first()
