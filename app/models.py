from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import datetime

class Favorite(db.Model):
	__tablename__ = 'favorites'
	article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Prefer(db.Model):
	__tablename__ = 'prefer'
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	belong = db.Column(db.String(32), primary_key=True)
	tag = db.Column(db.String(32), primary_key=True)
	notice = db.Column(db.Boolean, default=False)

class Note(db.Model):
	__tablename__ = 'note'
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	text = db.Column(db.Text)

class Article(db.Model):
	__tablename__ = 'articles'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	text = db.Column(db.Text)
	link = db.Column(db.String(256))
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	date = db.Column(db.Date)

	favorites = db.relationship('Favorite', foreign_keys=[Favorite.article_id],
								backref=db.backref('article', lazy='joined'), lazy='dynamic',
								cascade='all, delete-orphan')

	belong = db.Column(db.String(32), index=True)
	tag = db.Column(db.String(32), index=True)
	noticed = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return '<Article %r>' % self.title

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True, nullable=False)
	password_hash = db.Column(db.String(128))
	email = db.Column(db.String(64), unique=True, nullable=False)
	is_admin = db.Column(db.Boolean, default=False)
	confirmed = db.Column(db.Boolean, nullable=False, default=False)
	confirmed_on = db.Column(db.DateTime, nullable=True)

	lasttime_email = db.Column(db.DateTime, default=datetime.utcnow)

	favorites = db.relationship('Favorite', foreign_keys=[Favorite.user_id],
								backref=db.backref('user', lazy='joined'), lazy='dynamic',
								cascade='all, delete-orphan')

	prefers = db.relationship('Prefer', foreign_keys=[Prefer.user_id],
								backref=db.backref('user', lazy='joined'), lazy='dynamic',
								cascade='all, delete-orphan')

	notes = db.relationship('Note', foreign_keys=[Note.user_id],
								backref=db.backref('user', lazy='joined'), lazy='dynamic',
								cascade='all, delete-orphan')

	def __init__(self, username, email, password, confirmed, confirmed_on=None):
		self.username = username
		self.email = email
		self.password_hash = generate_password_hash(password)
		self.registered_on = datetime.now()
		self.confirmed = confirmed
		self.confirmed_on = confirmed_on

		if self.username == current_app.config['SUPER_USERNAME']:
			self.is_admin = True
		else:
			self.is_admin = False

	def can_email(self):
		return (datetime.utcnow() - self.lasttime_email).seconds > 1200

	def set_email_time(self):
		self.lasttime_email = datetime.utcnow()
		db.session.add(self)
		db.session.commit()

	def is_administrator(self):
		return self.is_admin

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def is_favoriting(self, article):
		return self.favorites.filter_by(article_id=article.id).first() is not None

	def favorite(self, article):
		if not self.is_favoriting(article):
			f = Favorite(user_id=self.id, article_id=article.id)
			db.session.add(f)
			db.session.commit()

	def un_favorite(self, article):
		f = self.favorites.filter_by(article_id=article.id).first()
		if f:
			db.session.delete(f)
			db.session.commit()

	def is_preferring(self, belong, tag):
		return self.prefers.filter_by(belong=belong, tag=tag).first() is not None

	def is_noticing(self, belong, tag):
		return self.prefers.filter_by(belong=belong, tag=tag, notice=True).first() is not None

	def notice(self, belong, tag):
		p = self.prefers.filter_by(belong=belong, tag=tag).first()
		if p:
			p.notice = True
			db.session.add(p)
			db.session.commit()
		else:
			p = Prefer(user_id=self.id, belong=belong, tag=tag, notice=True)
			db.session.add(p)
			db.session.commit()

	def prefer(self, belong, tag):
		if not self.is_preferring(belong, tag):
			p = Prefer(user_id=self.id, belong=belong, tag=tag, notice=False)
			db.session.add(p)
			db.session.commit()
		else:
			p = self.prefers.filter_by(belong=belong, tag=tag).first()
			p.notice = False
			db.session.add(p)
			db.session.commit()

	def un_prefer(self, belong, tag):
		p = self.prefers.filter_by(belong=belong, tag=tag).first()
		if p:
			db.session.delete(p)
			db.session.commit()

	def del_note(self, id):
		n = self.notes.filter_by(id=id).first()
		if n:
			db.session.delete(n)
			db.session.commit()

	def __repr__(self):
		return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class AnonymousUser(AnonymousUserMixin):
	def is_administrator(self):
		return False
	def is_preferring(self, belong, tag):
		return False
	def is_favoriting(self, article):
		return False
	def is_noticing(self, belong, tag):
		return False

login_manager.anonymous_user = AnonymousUser





