from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Doctor,Patient,Registrar,Admin,Departments, Registration
from ..decorators import admin_required, patient_required,doctor_required,registrar_required
from flask import jsonify
from .forms import AddDoctorForm, AddDepartmentForm, AddPatientForm, BookingForm, BookingDoctorForm
import datetime

'''
@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    return render_template('index.html', users=users, pagination=pagination)


@main.route('/deleteuser', methods = ['POST'])
@login_required
@admin_required
def delete_user():
    id = request.form.get('uid', 0, type=int)
    user = User.query.get_or_404(id)
    db.session.delete(user)
    return jsonify({'ok': True})

'''
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/patient', methods= ['GET', 'POST'])
@login_required
@patient_required
def patient():
    return render_template('patient.html')

@main.route('/doctor', methods=['GET', 'POST'])
@login_required
def doctor():
    return

@main.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar():
    return

@main.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():
    return render_template('admin.html')

@main.route('/admin/adddoctor', methods=['GET', 'POST'])
@login_required
@admin_required
def add_doctor():
    form = AddDoctorForm()
    form.depart_id.choices = [(d.id, d.name) for d in Departments.query.order_by('id')]
    if form.validate_on_submit():
        user = Doctor(workcard=form.workcard.data,
                      idcard=form.idcard.data,
                      name=form.name.data,
                      password=form.password.data,
                      depart_id=form.depart_id.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.add_doctor'))
    return render_template('add_doctor.html', form=form)

@main.route('/admin/doctorlist', methods=['GET', 'POST'])
@login_required
@admin_required
def doctor_list():
    page = request.args.get('page', 1, type=int)
    pagination = Doctor.query.order_by(Doctor.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    return render_template('doctorlist.html', doctors=users, pagination=pagination)

@main.route('/admin/adddepartment', methods=['GET', 'POST'])
@login_required
@admin_required
def add_department():
    form = AddDepartmentForm()
    if form.validate_on_submit():
        dpart = Departments(name=form.name.data)
        db.session.add(dpart)
        db.session.commit()
        return redirect(url_for('.add_department'))
    return render_template('add_department.html', form=form)

@main.route('/admin/departmentlist', methods=['GET', 'POST'])
@login_required
@admin_required
def department_list():
    page = request.args.get('page', 1, type=int)
    pagination = Departments.query.order_by(Departments.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    dparts = pagination.items
    return render_template('departmentlist.html', departments=dparts, pagination=pagination)

@main.route('/admin/addpatient', methods=['GET', 'POST'])
@login_required
@admin_required
def add_patient():
    form = AddPatientForm()
    form.gender.choices = [(1, 'male'), (2, 'female')]
    if form.validate_on_submit():
        user = Patient(medcard=form.medcard.data,
                       idcard=form.idcard.data,
                       birthday=form.birthday.data,
                       gender=form.gender.data,
                       phone=form.phone.data,
                       address=form.address.data,
                       name=form.name.data,
                       password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.add_patient'))
    return render_template('add_patient.html', form=form)

@main.route('/admin/patientlist', methods=['GET', 'POST'])
@login_required
@admin_required
def patient_list():
    page = request.args.get('page', 1, type=int)
    pagination = Patient.query.order_by(Patient.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    return render_template('patientlist.html', patients=users, pagination=pagination)

@main.route('/patient/booking', methods=['GET', 'POST'])
@login_required
@patient_required
def booking():
    form = BookingForm()
    form.depart_id.choices = [(d.id, d.name) for d in Departments.query.order_by('id')]
    if form.validate_on_submit():
        return redirect(url_for('.booking_doctor', depart_id=form.depart_id.data, date=form.bookingday.data))
    return render_template('booking.html', form=form)

@main.route('/patient/booking_doctor/<depart_id>/<date>', methods=['GET', 'POST'])
@login_required
@patient_required
def booking_doctor(depart_id, date):
    form = BookingDoctorForm()
    form.doctor_id.choices = [(d.id, d.name) for d in Doctor.query.filter_by(depart_id=depart_id).all()]
    if form.validate_on_submit():
        tdate = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        regi = Registration(doctor_id=form.doctor_id.data,
                             patient_id=current_user.id,
                             registration_date=tdate)
        db.session.add(regi)
        db.session.commit()
        return redirect(url_for('.booking'))
    return render_template('booking_doctor.html', form=form)

@main.route('/patient/booking_list', methods=['GET', 'POST'])
@login_required
@patient_required
def booking_list():
    page = request.args.get('page', 1, type=int)
    pagination = Registration.query.filter_by(patient_id=current_user.id).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    registrations = pagination.items
    return render_template('bookinglist.html', registrations=registrations, pagination=pagination)