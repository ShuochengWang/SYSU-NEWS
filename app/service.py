# -*- coding:utf-8 -*- 
import schedule
import time
import re
from bs4 import BeautifulSoup
from datetime import date
from flask import render_template, flash, current_app
import smtplib
import requests
from . import db
from .models import User, Article
from email.mime.text import MIMEText
from email.header import Header

def service(app):
	with app.app_context():
		schedule.every().day.at("12:00").do(job)
		schedule.every().day.at("8:00").do(job)
		schedule.every().day.at("20:00").do(job)
		while True:
			schedule.run_pending()
			time.sleep(1)

def job():
	try:
		crawler()
		notice()
	except:
		print 'error in job'

def crawler():
	print 'start cron job --- crawler'
	file = open('crawlerlog.txt', 'a')
	config_dict = current_app.config['CLASSIFICATION']
	for belong in config_dict.keys():
		for tag in config_dict[belong].keys():
			ls = config_dict[belong][tag]
	
			url = ls[0]
			url = requests.get(url)
			
			for item in re.findall(ls[2], url.text):
				try:
					link = ls[1] + item
					uurl = requests.get(link)
					bs = BeautifulSoup(uurl.text, 'html.parser')
					content = bs.find_all(ls[3], ls[4])[0].get_text()
					d = re.findall(ls[5], uurl.text)[0]
					title = bs.find_all(ls[6], ls[7])[0].get_text().split()[0]
					article = Article(title=title, belong=belong, tag=tag, text=content, 
						link=link, date=date(int(d[0]), int(d[1]), int(d[2])))
					art = Article.query.filter_by(title=article.title, date=date(int(d[0]), int(d[1]), int(d[2])), belong=belong, tag=tag).first()
					if art is None:
						db.session.add(article)
						db.session.commit()
				except:
					file.write(belong+tag)
					break
	file.close()
	print 'end cron job --- crawler'

def notice():
	print 'start cron job --- notice by email'
	server = smtplib.SMTP(current_app.config['EMAIL_NOTICE_SMTP'], current_app.config['EMAIL_NOTICE_SMTP_PORT'])
	server.starttls()
	server.login(current_app.config['EMAIL_NOTICE_USERNAME'], current_app.config['EMAIL_NOTICE_PASSWORD'])

	users = User.query.filter_by(confirmed=True).all()
	for user in users:
		notices = user.prefers.filter_by(notice=True).all()
		if not notices:
			continue
		res = []
		for notice in notices:
			articles = Article.query.filter_by(belong=notice.belong, tag=notice.tag, noticed=False).all()
			for article in articles:
				res.append(article)
		if not res:
			continue
		# prepare email
		html = render_template('email_notice.html', articles=res)
		message = MIMEText(html, 'html', 'utf-8')
		message['From'] = Header("SweetOrange", 'utf-8')
		message['To'] = Header(user.email, 'utf-8')
		message['Subject'] = Header(u'信息更新通知', 'utf-8')
		# send email
		try:
			server.sendmail(current_app.config['EMAIL_NOTICE_USERNAME'], user.email, message.as_string())
		except:
			server.quit()
			server.close()
			server = smtplib.SMTP(current_app.config['EMAIL_NOTICE_SMTP'], current_app.config['EMAIL_NOTICE_SMTP_PORT'])
			server.starttls()
			server.login(current_app.config['EMAIL_NOTICE_USERNAME'], current_app.config['EMAIL_NOTICE_PASSWORD'])
			server.sendmail(current_app.config['EMAIL_NOTICE_USERNAME'], user.email, message.as_string())

	server.quit()
	server.close()
	# make noticed = true
	articles = Article.query.filter_by(noticed=False).all()
	for art in articles:
		art.noticed = True
		db.session.add(art)
		db.session.commit()
	print 'end cron job --- notice by email'