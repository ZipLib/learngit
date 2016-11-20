from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
#from ..models import User
from ..models import Patient, Doctor, Registrar, Admin
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm


def generateCard(length=8):
    import random
    card=''
    chars='1234567890'
    for i in range(length):
        card += random.choice(chars)
    return card

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cardlength = len(form.card.data)
        url = "main.index"
        user = None
        if cardlength == 8:
            user = Patient.query.filter_by(medcard=form.card.data).first()
            url = "main.patient"
        elif cardlength == 5:
            user = Registrar.query.filter_by(workcard=form.card.data).first()
            url = "main.registrar"
        elif cardlength == 4:
            user = Doctor.query.filter_by(workcard=form.card.data).first()
            url = "main.doctor"
        elif cardlength == 3:
            user = Admin.query.filter_by(account=form.card.data).first()
            url = "main.admin"

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for(url))
        flash('Invalid username or password.')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        medcard = generateCard()
        while(Patient.query.filter_by(medcard=medcard).first()):
            medcard = generateCard()
        user = Patient(medcard=medcard,
                    idcard=form.idcard.data,
                    address=form.address.data,
                    name=form.name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)




@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)





