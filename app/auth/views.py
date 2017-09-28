# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .. import db
from .forms import LoginForm, RegistrationForm, ResetForm, ResetForm2
from ..emails import generate_confirmation_token, confirm_token, send_email
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from threading import Thread

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username_or_email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		user = User.query.filter_by(email=form.username_or_email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash(u'用户名、邮箱或密码错误')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash(u'你已经成功退出')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,  email=form.email.data\
			, password=form.password.data, confirmed=False)
		db.session.add(user)
		db.session.commit()
		confirm(user)
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)

# 日后单独确认邮箱
@auth.route('/confirm_email_later')
@login_required
def confirm_email_later():
	if current_user.can_email():
		user.set_email_time()
		confirm(current_user)
		return redirect(url_for('main.user'))
	flash(u'您发送邮件过于频繁，请稍后再试')
	return redirect(url_for('main.user'))

# 确认邮箱
def confirm(user):
	# 带密钥的confirm_url，点击之后在数据库中更新确认的状态
	token = generate_confirmation_token(user.email)
	confirm_url = url_for('auth.confirm_email', token=token, _external=True)
	# 邮件内容是html格式的，设置邮件的from，to，subject
	html = render_template('auth/email_activate.html', confirm_url=confirm_url)
	message = MIMEText(html, 'html', 'utf-8')
	message['From'] = Header("SweetOrange", 'utf-8')
	message['To'] = Header(user.email, 'utf-8')
	message['Subject'] = Header(u'请确认您的邮箱', 'utf-8')
	# 发送邮件的函数，设置目的邮件地址，和string类型的内容即可，可以用到推送上面
	app = current_app._get_current_object()
	thr = Thread(target=send_email, args=[app, user.email, message.as_string()])
	thr.start()
	flash(u'确认邮件已经发至邮箱，请尽快确认；如未收到，请检查邮件垃圾箱', 'success')

#确认邮箱 -- 口令检验
@auth.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash(u'该链接已失效', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash(u'邮箱已成功确认', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash(u'你已经成功确认邮箱，谢谢！', 'success')
    return redirect(url_for('auth.login'))

#重设密码-输入邮箱
@auth.route('/reset_password1', methods=['GET', 'POST'])
def reset_password1():
	form = ResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			flash(u'该邮箱未被注册')
			return render_template('auth/reset_password1.html', form=form)
		if not user.can_email():
			flash(u'该邮箱发送邮件过于频繁，请稍后再试')
			return render_template('auth/reset_password1.html', form=form)
		user.set_email_time()
		token = generate_confirmation_token(user.email)
		url = url_for('auth.reset_password2', token=token, _external=True)
		# 邮件内容是html格式的，设置邮件的from，to，subject
		html = render_template('auth/email_reset.html', url=url)
		message = MIMEText(html, 'html', 'utf-8')
		message['From'] = Header("SweetOrange", 'utf-8')
		message['To'] = Header(user.email, 'utf-8')
		message['Subject'] = Header(u'重设密码', 'utf-8')
		# 发送邮件的函数，设置目的邮件地址，和string类型的内容即可，可以用到推送上面
		app = current_app._get_current_object()
		thr = Thread(target=send_email, args=[app, user.email, message.as_string()])
		thr.start()
		flash(u'重设密码邮件已经发至邮箱，请尽快确认；如未收到，请检查邮件垃圾箱', 'success')
	return render_template('auth/reset_password1.html', form=form)

#输入新密码
@auth.route('/reset_password2/<token>', methods=['GET', 'POST'])
def reset_password2(token):
    try:
        email = confirm_token(token)
    except:
        flash(u'该链接已失效', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    form = ResetForm2()
    if form.validate_on_submit():
    	user.password = form.password.data
    	user.confirmed = True
    	db.session.add(user)
        db.session.commit()
        flash(u'密码已重设', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password2.html', form=form)