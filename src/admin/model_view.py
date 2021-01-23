from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, helpers
import flask_login as login
from flask import request, url_for, redirect
from src.model.models import User
from src.db import get_db
from werkzeug.security import check_password_hash
from wtforms import form, fields, validators

class LoginForm(form.Form):
    username = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self):
        print("validate login data")
        user = self.get_user()

        if user is None:
            return False

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password_hash, self.password.data):
            return False

        return True

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()

class AppAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(AppAdminIndexView, self).index()

    @expose('/login', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form) and form.validate_login():
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))

        form.errors['login_error'] = "Username or password incorrect"
        self._template_args['form'] = form

        return super(AppAdminIndexView, self).index()

    @expose('/logout')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

class AppModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    create_modal = True
    edit_modal = True
    can_export = True
    column_display_pk = True

class UserModelView(AppModelView):
    can_delete = False
    column_exclude_list = ['password_hash', ]

class CharacterModelView(AppModelView):
    can_delete = True
    can_view_details = True
    column_searchable_list = ['name']
    column_filters = ['name', 'collection']

class TagModelView(AppModelView):
    column_list = ['name']

