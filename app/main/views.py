# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, current_app, request, jsonify
from flask_login import current_user, login_required
from string import split
import threading
from threading import Thread

from . import main
from .forms import ArticleForm
from .. import db
from ..models import User, Article, Favorite, Prefer, Note
from ..decorators import admin_required
from ..crawler import robot
from ..service import service

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@main.route('/', methods=['GET', 'POST'])
def index():
	if current_user.is_authenticated:
		page = request.args.get('page', 1, type=int)
		active = request.args.get('active', 1, type=int)
		data = []
		tag_id = 1
		for item in current_user.prefers.all():
			belong, tag = item.belong, item.tag
			if active == tag_id:
				pagination = Article.query.filter_by(tag=tag, belong=belong).order_by(Article.date.desc()).paginate(page, \
					per_page=current_app.config['ARTICLES_PER_PAGE'], error_out=False)
			else:
				pagination = Article.query.filter_by(tag=tag, belong=belong).order_by(Article.date.desc()).paginate(1, \
					per_page=current_app.config['ARTICLES_PER_PAGE'], error_out=False)
			articles = pagination.items
			data.append(dict(pagination=pagination, articles=articles, id=tag_id, tag=tag))
			tag_id += 1
		#note
		notes = current_user.notes.order_by(Note.id.asc()).all()
		todo = []
		for note in notes:
			todo.append(dict(text=note.text, id=note.id))

		service_running = False
		thr_list = threading.enumerate()
		for thr in thr_list:
			if thr.getName() == 'service':
				service_running = True
				break
		return render_template('index.html', data=data, todo=todo, active=active, service_running=service_running)
	else:
		page = request.args.get('page', 1, type=int)
		pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page,
			per_page=current_app.config['ARTICLES_PER_PAGE'], error_out=False)
		articles = pagination.items
		return render_template('index_without_login.html', articles=articles, pagination=pagination)

@main.route('/articles/<int:id>')
def read(id):
	article = Article.query.get_or_404(id)
	text = article.text.split('\n')
	return render_template('article.html', article=article, text=text)

@login_required
@main.route('/user')
def user():
	user = User.query.filter_by(id=current_user.id).first()
	if user is None:
		flash(u'非法用户')
		return redirect(url_for('.index'))
	page = request.args.get('page', 1, type=int)
	pagination = user.favorites.order_by(Favorite.timestamp.desc()).paginate(page, per_page=current_app.config['ARTICLES_PER_PAGE'], error_out=False)
	favorites = [{'article': item.article, 'timestamp': item.timestamp} for item in pagination.items]
	return render_template('user.html', user=user, endpoint='.user', pagination=pagination, favorites=favorites)

@login_required
@main.route('/favorite/<int:id>')
def favorite(id):
	article = Article.query.filter_by(id=id).first()
	if Article is None:
		flash(u'非法文章')
		return redirect(url_for('.index'))
	if current_user.is_favoriting(article):
		flash(u'你已收藏该文章')
		return redirect(url_for('.read', id=article.id))
	current_user.favorite(article)
	flash(u'你已成功收藏文章：%s.' % article.title)
	return redirect(url_for('.read', id=article.id))

@login_required
@main.route('/unfavorite/<int:id>')
def un_favorite(id):
	article = Article.query.filter_by(id=id).first()
	if Article is None:
		flash(u'非法文章')
		return redirect(url_for('.index'))
	if not current_user.is_favoriting(article):
		flash(u'你未收藏该文章')
		return redirect(url_for('.read', id=article.id))
	current_user.un_favorite(article)
	flash(u'你已取消收藏文章：%s.' % article.title)
	return redirect(url_for('.read', id=article.id))

@main.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
	form = ArticleForm()
	if form.validate_on_submit():
		article = Article(title=form.title.data, belong=form.belong.data, tag=form.tag.data, text=form.text.data, link=form.link.data, date=form.date.data)
		db.session.add(article)
		db.session.commit()
		flash(u'成功添加文章')
		return redirect(url_for('.read', id=article.id))
	return render_template('add.html', form=form)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_article(id):
	article = Article.query.get_or_404(id)
	form = ArticleForm()
	if form.validate_on_submit():
		article.title = form.title.data
		article.tag = form.tag.data
		article.date = form.date.data
		article.link = form.link.data
		article.text = form.text.data
		db.session.commit()
		flash(u'成功编辑文章')
		return redirect(url_for('.index'))
	form.title.data = article.title
	form.tag.data = article.tag
	form.text.data = article.text
	form.date.data = article.date
	form.link.data = article.link
	return render_template('edit_article.html', form=form)

@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_article(id):
	article = Article.query.get_or_404(id)
	db.session.delete(article)
	db.session.commit()
	flash(u'成功删除文章')
	return redirect(url_for('.index'))

@login_required
@main.route('/prefer')
def prefer():
	config_dict = current_app.config['CLASSIFICATION']
	classification = []
	for belong in config_dict.keys():
		classification.append(dict(belong=belong, tags=[]))
		for tag in config_dict[belong].keys():
			select = current_user.is_preferring(belong, tag)
			notice = False
			if select:
				notice = current_user.is_noticing(belong, tag)
			classification[-1]['tags'].append(dict(tag=tag, select=select, notice=notice))
	return render_template('prefer.html', classification=classification)

@login_required
@main.route('/edit_prefer')
def edit_prefer():
	belong = request.args.get('belong', type=unicode)
	tag = request.args.get('tag', type=unicode)
	state = request.args.get('state', 0, type=int)
	if state == 0:
		current_user.prefer(belong, tag)
	elif state == 1:
		current_user.notice(belong, tag)
	else:
		current_user.un_prefer(belong, tag)
	return jsonify(state=state)

@login_required
@main.route('/add_note')
def add_note():
	print '***********'
	text = request.args.get('text', type=unicode)
	n = Note(user_id=current_user.id, text=text)
	db.session.add(n)
	db.session.commit()
	return jsonify(id=n.id, text=n.text)

@login_required
@main.route('/del_note')
def del_note():
	note_id = request.args.get('id', type=int)
	current_user.del_note(note_id)
	return jsonify(complete=True)

@login_required
@admin_required
@main.route('/service')
def start_service():
	thr_list = threading.enumerate()
	for thr in thr_list:
		if thr.getName() == 'service':
			flash(u'后台服务已经在运行中')
			return redirect(url_for('.index'))
	app = current_app._get_current_object()
	thr = Thread(target=service, name='service', args=[app])
	thr.start()
	flash(u'后台服务正在运行中')
	return redirect(url_for('.index'))