from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		if not current_user.is_administrator():
			abort(403)
		return f(*args, **kwargs)
	return wrapper