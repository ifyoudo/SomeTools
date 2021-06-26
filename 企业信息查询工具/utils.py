class Utils(object):
	"""docstring for Utils"""
	def __init__(self):
		super(Utils, self).__init__()
		
	def baseheader(self):
		base_headers={
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
		'X-Requested-With': 'XMLHttpRequest',
		'X-Forwarded-For': '8.8.8.8',
		}
		return base_headers