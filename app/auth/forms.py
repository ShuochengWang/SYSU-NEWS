# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from ..models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, validators
from wtforms.validators import Required, Length, Regexp, EqualTo, Email
from wtforms.fields.html5 import EmailField

class LoginForm(FlaskForm):
	username_or_email = StringField(u'用户名或邮箱', validators=[Required(), Length(5,64)])
	password = PasswordField(u'密码', validators=[Required()])
	remember_me = BooleanField(u'保持登录状态')
	submit = SubmitField(u'登录')

class ResetForm(FlaskForm):
	email = StringField(u'邮箱', validators=[Required(), Email()])
	submit = SubmitField(u'发送邮件')
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError(u'该邮箱尚未被注册')

class ResetForm2(FlaskForm):
	password = PasswordField(u'密码', validators=[Required()])
	submit = SubmitField(u'重设密码')

class RegistrationForm(FlaskForm):
	username = StringField(u'用户名', validators=[Required(), Length(5, 32), 
		Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名仅能使用字母、数字、点及下划线')])
	email = EmailField(u'邮箱', [Required(), Email()])
	password = PasswordField(u'密码', validators=[Required()])
	submit = SubmitField(u'注册')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'该用户名已被使用')
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError(u'该邮箱已被使用')
