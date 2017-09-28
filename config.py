# -*- coding: UTF-8 -*- 
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ARTICLES_PER_PAGE = 10
    SUPER_USERNAME = 'SUPER_USERNAME'
    SECURITY_PASSWORD_SALT = 'SECURITY_PASSWORD_SALT'
    SECRET_KEY = 'SECRET_KEY'

    EMAIL_CONFIRM_USERNAME = 'example@outlook.com'
    EMAIL_CONFIRM_PASSWORD = 'password'
    EMAIL_CONFIRM_SMTP = 'smtp-mail.outlook.com'
    EMAIL_CONFIRM_SMTP_PORT = 587

    EMAIL_NOTICE_USERNAME = 'example@outlook.com'
    EMAIL_NOTICE_PASSWORD = 'password'
    EMAIL_NOTICE_SMTP = 'smtp-mail.outlook.com'
    EMAIL_NOTICE_SMTP_PORT = 587

    CLASSIFICATION = { \
    u'中山大学教务部': {u'交流合作': ['http://jwc.sysu.edu.cn/noticeannouncement/exchange?field_tzgg_tid=All&page=0', \
                        'http://jwc.sysu.edu.cn/content/', 'a href="/content/(\d+)"', \
                        'div', {'class': 'field-items'}, \
                        '(\d{4})/(\d{1,2})/(\d{1,2})', \
                        'li', {'class': 'active'}], \
              u'计划与质量管理': ['http://jwc.sysu.edu.cn/noticeannouncement/development?field_tzgg_tid=All&page=0', \
                        'http://jwc.sysu.edu.cn/content/', 'a href="/content/(\d+)"', \
                        'div', {'class': 'field-items'}, \
                        '(\d{4})/(\d{1,2})/(\d{1,2})', \
                        'li', {'class': 'active'}], \
              u'教务管理': ['http://jwc.sysu.edu.cn/noticeannouncement/educational?field_tzgg_tid=All&page=0', \
                        'http://jwc.sysu.edu.cn/content/', 'a href="/content/(\d+)"', \
                        'div', {'class': 'field-items'}, \
                        '(\d{4})/(\d{1,2})/(\d{1,2})', \
                        'li', {'class': 'active'}], \
              u'临床教学': ['http://jwc.sysu.edu.cn/noticeannouncement/clinic_teach?field_tzgg_tid=All&page=0', \
                        'http://jwc.sysu.edu.cn/content/', 'a href="/content/(\d+)"', \
                        'div', {'class': 'field-items'}, \
                        '(\d{4})/(\d{1,2})/(\d{1,2})', \
                        'li', {'class': 'active'}], \
              u'综合管理': ['http://jwc.sysu.edu.cn/noticeannouncement/mangage?field_tzgg_tid=All&page=0', \
                        'http://jwc.sysu.edu.cn/content/', 'a href="/content/(\d+)"', \
                        'div', {'class': 'field-items'}, \
                        '(\d{4})/(\d{1,2})/(\d{1,2})', \
                        'li', {'class': 'active'}], \
              u'教学条件保障': ['http://jwc.sysu.edu.cn/noticeannouncement/resource?field_tzgg_tid=All&page=0', \
                        'http://jwc.sysu.edu.cn/content/', 'a href="/content/(\d+)"', \
                        'div', {'class': 'field-items'}, \
                        '(\d{4})/(\d{1,2})/(\d{1,2})', \
                        'li', {'class': 'active'}], \
              }, \
    u'数据科学与计算机学院': {u'本科生教务': ['http://sdcs.sysu.edu.cn/?cat=25&paged=1', \
                        'http://sdcs.sysu.edu.cn/?p=', 'href="http://sdcs.sysu.edu.cn/\?p=(\d+)"', \
                        'div', {'class': 'article_content'}, \
                        '(\d{4})-(\d{1,2})-(\d{1,2})', \
                        'div', {'class': 'art_title clearfix'}], \
                    u'研究生教务': ['http://sdcs.sysu.edu.cn/?cat=35&paged=1', \
                        'http://sdcs.sysu.edu.cn/?p=', 'href="http://sdcs.sysu.edu.cn/\?p=(\d+)"', \
                        'div', {'class': 'article_content'}, \
                        '(\d{4})-(\d{1,2})-(\d{1,2})', \
                        'div', {'class': 'art_title clearfix'}], \
                    u'学院动态': ['http://sdcs.sysu.edu.cn/?cat=76&paged=1', \
                        'http://sdcs.sysu.edu.cn/?p=', 'href="http://sdcs.sysu.edu.cn/\?p=(\d+)"', \
                        'div', {'class': 'article_content'}, \
                        '(\d{4})-(\d{1,2})-(\d{1,2})', \
                        'div', {'class': 'art_title clearfix'}], \
                    u'学生事务' :['http://sdcs.sysu.edu.cn/?cat=58&paged=1', \
                        'http://sdcs.sysu.edu.cn/?p=', 'href="http://sdcs.sysu.edu.cn/\?p=(\d+)"', \
                        'div', {'class': 'article_content'}, \
                        '(\d{4})-(\d{1,2})-(\d{1,2})', \
                        'div', {'class': 'art_title clearfix'}]},\
    u'中山大学学生处': {u'勤工助学':['http://xsc.sysu.edu.cn/zh-hans/qgzx?page=0', \
                          'http://xsc.sysu.edu.cn/zh-hans/node/', '   <a href="/zh-hans/node/(\d+)">',
                          'div',{'class': 'content clearfix'}, \
                          '(\d{4})-(\d{1,2})-(\d{1,2})', \
                          'h1', {'class': 'title', 'id': 'page-title'}],
                    u'资助管理': ['http://xsc.sysu.edu.cn/zh-hans/zzgl?page=0', \
                          'http://xsc.sysu.edu.cn/zh-hans/node/', '   <a href="/zh-hans/node/(\d+)">', \
                          'div',{'class': 'content clearfix'}, \
                          '(\d{4})-(\d{1,2})-(\d{1,2})', \
                          'h1', {'class': 'title', 'id': 'page-title'}]
                 },
    u'法学院': {u'学术科研': ['http://law.sysu.edu.cn/research/research1?page=0', \
                       'http://law.sysu.edu.cn/node/', '<a href="/node/(\d+)"', \
                       'div', {'class': 'content clearfix'}, \
                       '(\d{4})-(\d{1,2})-(\d{1,2})', \
                       'h1', {'class': 'title', 'id': 'page-title'}], \
                u'教学教务': ['http://law.sysu.edu.cn/undergraduate/undergraduate1?page=0', \
                       'http://law.sysu.edu.cn/node/', '<a href="/node/(\d+)"', \
                       'div', {'class': 'content clearfix'}, \
                       '(\d{4})-(\d{1,2})-(\d{1,2})', \
                       'h1', {'class': 'title', 'id': 'page-title'}], \
                u'学生工作': ['http://law.sysu.edu.cn/student/student1?page=0', \
                       'http://law.sysu.edu.cn/node/', '<a href="/node/(\d+)"', \
                       'div', {'class': 'content clearfix'}, \
                       '(\d{4})-(\d{1,2})-(\d{1,2})', \
                       'h1', {'class': 'title', 'id': 'page-title'}], \
                u'学院新闻': ['http://law.sysu.edu.cn/news?page=0', \
                       'http://law.sysu.edu.cn/node/', '<a href="/node/(\d+)"', \
                       'div', {'class': 'content clearfix'}, \
                       '(\d{4})-(\d{1,2})-(\d{1,2})', \
                       'h1', {'class': 'title', 'id': 'page-title'}]}, \
    u'工学院': {u'通知公告':['http://egs.sysu.edu.cn/zh-hans/notice', \
                          'http://egs.sysu.edu.cn/zh-hans/content/', '   <a href="/zh-hans/content/(\d+)">',
                          'div',{'class': 'field-item even', 'property': 'content:encoded'}, \
                          '(\d{4})/(\d{1,2})/(\d{1,2})',\
                        'div', {'class': 'l-content'}], \
             u'学院新闻':['http://egs.sysu.edu.cn/zh-hans/news', \
                          'http://egs.sysu.edu.cn/zh-hans/content/', '   <a href="/zh-hans/content/(\d+)">',
                          'div',{'class': 'field-item even', 'property': 'content:encoded'}, \
                          '(\d{4})/(\d{1,2})/(\d{1,2})',\
                        'div', {'class': 'l-content'}], \
             u'科学研究':['http://egs.sysu.edu.cn/zh-hans/research', \
                          'http://egs.sysu.edu.cn/zh-hans/content/', '   <a href="/zh-hans/content/(\d+)">',
                          'div',{'class': 'field-item even', 'property': 'content:encoded'}, \
                          '(\d{4})/(\d{1,2})/(\d{1,2})',\
                        'div', {'class': 'l-content'}]}, \
    u'管理学院': {u'教务信息':['http://bus.sysu.edu.cn/announcement.aspx?typeid=d3e0b81d-4e19-4cbc-a9ae-54efe72648e1', \
                          'http://bus.sysu.edu.cn/NewsContent.aspx?typeid=', 'href=\'NewsContent.aspx\?typeid=(.+?)\'',
                          'div',{'class': 'cons_detail'}, \
                          '(\d{4}).(\d{1,2}).(\d{1,2}).</em', \
                       'div', {'class': 'cons'}], \
              u'科研信息':['http://bus.sysu.edu.cn/news.aspx?typeid=68204441-e52d-479d-9b04-6b40c7691578', \
                          'http://bus.sysu.edu.cn/NewsContent.aspx?typeid=', 'href=\'NewsContent.aspx\?typeid=(.+?)\'',
                          'div',{'class': 'cons_detail'}, \
                          '(\d{4}).(\d{1,2}).(\d{1,2}).</em', \
                       'div', {'class': 'cons'}], \
              u'行政工会':['http://bus.sysu.edu.cn/news.aspx?typeid=d8048e05-853a-48cc-aed9-cbdc841d13ee', \
                          'http://bus.sysu.edu.cn/NewsContent.aspx?typeid=', 'href=\'NewsContent.aspx\?typeid=(.+?)\'',
                          'div',{'class': 'cons_detail'}, \
                          '(\d{4}).(\d{1,2}).(\d{1,2}).</em', \
                       'div', {'class': 'cons'}]
                 }, \
    u'材料科学与工程学院': {u'教务通知':['http://mse.sysu.edu.cn/benke/tz', \
                          'http://mse.sysu.edu.cn/node/', '<a href="/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})-(\d{1,2})-(\d{1,2})', \
                          'li', {'class': 'active'}],
                    u'学生项目': ['http://mse.sysu.edu.cn/benke/xm', \
                          'http://mse.sysu.edu.cn/node/', '<a href="/node/(\d+)">', \
                           'div',{'class': 'content'}, \
                          '(\d{4})-(\d{1,2})-(\d{1,2})', \
                          'li', {'class': 'active'}]
                 }, \
    u'外国语学院': {u'本科实践':['http://fls.sysu.edu.cn/jx/bk/2', \
                          'http://fls.sysu.edu.cn/node/', '<a href="/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})/(\d{1,2})/(\d{1,2})', \
                          'li', {'class': 'active last'}], \
               u'本科学籍':['http://fls.sysu.edu.cn/jx/bk/1', \
                          'http://fls.sysu.edu.cn/node/', '<a href="/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})/(\d{1,2})/(\d{1,2})', \
                          'li', {'class': 'active last'}], \
               u'本科科研':['http://fls.sysu.edu.cn/jx/bk/3', \
                          'http://fls.sysu.edu.cn/node/', '<a href="/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})/(\d{1,2})/(\d{1,2})', \
                          'li', {'class': 'active last'}], \
               u'合作交流':['http://fls.sysu.edu.cn/jx/bk/4', \
                          'http://fls.sysu.edu.cn/node/', '<a href="/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})/(\d{1,2})/(\d{1,2})', \
                          'li', {'class': 'active last'}]
                 }, \
    u'国际翻译学院': {u'学院新闻':['http://sti.sysu.edu.cn/zh-hans/news', \
                          'http://sti.sysu.edu.cn/zh-hans/node/', '<a href="/zh-hans/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})/(\d{1,2})/(\d{1,2})', \
                          'li', {'class': 'active last'}], \
                u'公告栏':['http://sti.sysu.edu.cn/zh-hans/gonggao', \
                          'http://sti.sysu.edu.cn/zh-hans/node/', '<a href="/zh-hans/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})/(\d{1,2})/(\d{1,2})', \
                          'li', {'class': 'active last'}], \
                u'学术科研':['http://sti.sysu.edu.cn/zh-hans/xsky', \
                          'http://sti.sysu.edu.cn/zh-hans/node/', '<a href="/zh-hans/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})/(\d{1,2})/(\d{1,2})', \
                          'li', {'class': 'active last'}]
               }, \
    u'政治与公共事务管理学院': {u'教务信息':['http://sog.sysu.edu.cn/zh-hans/jw', \
                          'http://sog.sysu.edu.cn/zh-hans/node/', '<a href="/zh-hans/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})-(\d{1,2})-(\d{1,2})', \
                          'li', {'class': 'active'}], \
                     u'科研信息':['http://sog.sysu.edu.cn/zh-hans/zh/research/kyxx', \
                          'http://sog.sysu.edu.cn/zh-hans/node/', '<a href="/zh-hans/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})-(\d{1,2})-(\d{1,2})', \
                          'li', {'class': 'active'}], \
                     u'学工信息':['http://sog.sysu.edu.cn/zh-hans/zh/develop/xgxx', \
                          'http://sog.sysu.edu.cn/zh-hans/node/', '<a href="/zh-hans/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})-(\d{1,2})-(\d{1,2})', \
                          'li', {'class': 'active'}], \
                     u'访问交流':['http://sog.sysu.edu.cn/zh-hans/zh/international_cop/fwjl', \
                          'http://sog.sysu.edu.cn/zh-hans/node/', '<a href="/zh-hans/node/(\d+)">',
                          'div',{'class': 'content'}, \
                          '(\d{4})-(\d{1,2})-(\d{1,2})', \
                          'li', {'class': 'active'}]
                     }
             }

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRO_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
config = {
	'development' : DevelopmentConfig,
	'testing' : TestingConfig,
	'production': ProductionConfig,

	'default' : ProductionConfig
}