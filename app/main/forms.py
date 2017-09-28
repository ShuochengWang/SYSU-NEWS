# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import Required, Length

class ArticleForm(FlaskForm):
	title = StringField(u'标题', validators=[Required(), Length(1,128)])
	belong = StringField(u'所属', validators=[Required()])
	tag = StringField(u'分类', validators=[Required()])
	link = StringField(u'原始链接', validators=[Required(), Length(1,256)])
	date = DateField(u'日期，格式：XXXX-XX-XX', validators=[Required()])
	text = TextAreaField(u'内容', validators=[Required()])
	submit = SubmitField(u'提交')
