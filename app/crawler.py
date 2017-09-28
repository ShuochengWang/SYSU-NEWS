# -*- coding:utf-8 -*-  
import re
import sys
import requests
from bs4 import BeautifulSoup
from . import db
from .models import Article
from datetime import date
from flask import current_app

def robot(app):
	with app.app_context():
		config_dict = current_app.config['CLASSIFICATION']
		for belong in config_dict.keys():
			for tag in config_dict[belong].keys():
				ls = config_dict[belong][tag]
		
				url = ls[0]
				url = requests.get(url)
				
				for item in re.findall(ls[2], url.text):
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