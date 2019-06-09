#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#sys.path.append('/config')
import configparser



class sendemail(object):
	def __init__(self,):
		pass

	def __new__(self,alert):
		config = configparser.ConfigParser()
		config.read(config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config', 'dnspharming.ini')))	
		domain = config.get('monitor', 'domain')
		fromemailaddr = config.get('email', 'fromemailaddr')
		toemailaddr = config.get('email', 'toemailaddr')
		subject = config.get('email', 'subject')
		smtp = config.get('email', 'smtp')
		smtp_port = config.get('email', 'smtp_port')
		passwd = config.get('email','passwd')
		msg = MIMEMultipart()
		msg['From'] = fromemailaddr
		msg['To'] = toemailaddr
		msg['Subject'] = subject + " " + domain

		body = alert
		msg.attach(MIMEText(body, 'html'))
		try:
			response = False
			server = smtplib.SMTP(smtp, int(smtp_port))
			server.starttls()
			server.login(fromemailaddr, passwd)
			text = msg.as_string()
			server.sendmail(fromemailaddr, toemailaddr, text)
			server.quit()
			response = True
		except Exception as e:
			print(e)
		return response
