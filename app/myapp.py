import datetime

def application(environ, start_response):
	now = datetime.datetime.now()
	out = now.strftime("%d-%m-%Y %H:%M") + '\n'
	output = bytes(out, "utf-8")
	headers = [('Content-Type', 'text/plain')]
	start_response('200 OK', headers)
	return [output]
