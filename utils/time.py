import requests
from datetime import datetime

def str_parse_time(string):
	"""Parses given string into time"""
	r = requests.get("https://dateparser.piyush.codes/fromstr", params={"message": string})
	data = r.json()
	return data["message"]
	
def format_time(time):
	"""Formats the time"""
	format = time.strftime("%a, %b %d, %Y %X")
	days = round((datetime.utcnow() - time).total_seconds() / 86400)
	format += f"\n*{days} {'days' if days != 1 else 'day'} ago*"
	return format