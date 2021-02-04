from flask_admin import Admin
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView
from src.model.models import Character, Collection, Tag, Game, Player, User, Image
from src.admin.model_view import AppModelView, CharacterModelView, TagModelView, UserModelView, AppAdminIndexView, GameModelView
from src.db import db

admin = Admin(template_mode="bootstrap3", index_view=AppAdminIndexView(), base_template="admin/admin_master.html")
login_manager = LoginManager()

def init_admin(app):
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    admin.init_app(app)
    admin.add_view(CharacterModelView(Character, db.session))
    admin.add_view(AppModelView(Collection, db.session))
    admin.add_view(TagModelView(Tag, db.session))
    admin.add_view(GameModelView(Game, db.session))
    admin.add_view(AppModelView(Player, db.session))
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(AppModelView(Image, db.session))