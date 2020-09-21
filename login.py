import os
from flask_login import LoginManager

import uuid
from flask_login import UserMixin  # 引入用户基类
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_login import login_user

from flask_login import current_user, login_required

from flask import redirect, url_for
from flask_login import logout_user

from userlist import USERS

import base64
import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


app = Flask(__name__)  # 创建 Flask 应用

app.secret_key = 'abc'  # 设置表单交互密钥

login_manager = LoginManager()  # 实例化登录管理对象
login_manager.init_app(app)  # 初始化应用
login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint


def create_user(user_name, password):
    """创建一个用户"""
    user = {
        "name": user_name,
        "password": generate_password_hash(password),
        "id": uuid.uuid4()
    }
    USERS.append(user)

def get_user(user_name):
    """根据用户名获得用户记录"""
    for user in USERS:
        if user.get("name") == user_name:
            return user
    return None

@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return User.get(user_id)





class User(UserMixin):
    """用户类"""
    def __init__(self, user):
        self.username = user.get("name")
        self.password_hash = user.get("password")
        self.id = user.get("id")

    def verify_password(self, password):
        """密码验证"""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """获取用户ID"""
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        for user in USERS:
            if user.get('id') == user_id:
                return User(user)
        return None

class LoginForm(FlaskForm):
    """登录表单类"""
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])


# 后端处理登录
@app.route('/login/', methods=('GET', 'POST'))  # 登录
def login():
    form = LoginForm()
    emsg = None
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_info = get_user(user_name)  # 从用户数据中查找用户记录
        if user_info is None:
            emsg = "用户名或密码密码有误"
        else:
            user = User(user_info)  # 创建用户实体
            if user.verify_password(password):  # 校验密码
                login_user(user, remember=True)  # 创建用户 Session
                return redirect(request.args.get('next') or url_for('index'))
            else:
                emsg = "用户名或密码密码有误"
    return render_template('login.html', form=form, emsg=emsg)



@app.route('/')  # 首页
@login_required  # 需要登录才能访问
def index():
    return render_template('index.html', user_name=current_user.username, user_id=current_user.id)

@app.route('/logout')  # 登出
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    print(dname)
    app.run(host='0.0.0.0', port='7777', debug=True)