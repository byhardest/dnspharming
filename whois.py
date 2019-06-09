from ipwhois import IPWhois
from pprint import pprint

class whois(object):
	def __init__(self):
		pass

	def __new__(self,ip):
		try:
			obj = IPWhois(ip)
			results = obj.lookup_whois()
			
			return results

		except Exception as e:
			print("Whois error: ", e)
