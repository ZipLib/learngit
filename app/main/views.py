from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Permission, Role, User
from ..decorators import admin_required, permission_required


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    return render_template('index.html', users=users, pagination=pagination)

    return render_template('index.html')

@main.route('/deleteuser/<int:id>')
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    return redirect(url_for('.index', page=request.args.get('page', 1, type=int)))