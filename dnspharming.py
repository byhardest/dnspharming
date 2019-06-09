#!/usr/bin/python3

import csv  
import dns.resolver 
import ipaddress
from collections import defaultdict
from datetime import datetime
import os
import sys
import configparser
import send_email
from pprint import pprint
import whois 
from jinja2 import Template

###READING CONFIGURATION FILES UNDER /CONFIG###

config = configparser.ConfigParser()

config.read(config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config', 'dnspharming.ini')))

resolvers = config.get('monitor', 'resolvers')
legitips = config.get('monitor','legitips')
domain = config.get('monitor','domain')
enabled_email = config.get('email','send_email')
emailto = config.get('email', 'toemailaddr')
###CHECK IF INPUT SETTINGS HAS BEEN PROVIDED AT /CONFIG###

###The following conditional ifs will fill parameters needed in case they are missing on memory###
count_writefile = int

if resolvers == "":
	count_writefile = 1
	uinput = input('We are missing the filename which should contain the DNS Servers. If they are already in the main directory, please type it:')
	config.set('monitor','resolvers',uinput)
	resolvers = config.get('monitor', 'resolvers')
	print("You can change manually later on dnspharming.ini file")


if legitips == "":
	count_writefile = 1
	uinput = input('We are missing the filename which contains your whitelist ips. Please provide its name:')
	config.set('monitor','legitips',uinput)
	legitips = config.get('monitor', 'legitips')
	print("You can change manually later on dnspharming.ini file")

if domain == "":
	count_writefile = 1
	uinput = input('We are missing the domain you want to monitor. Please type it:')
	config.set('monitor','domain',uinput)
	domain = config.get('monitor', 'domain')
	print("You can change manually later on dnspharming.ini file")

###change the following
if count_writefile == 1:
	with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config', 'dnspharming.ini'), "w+") as modif:
		config.write(modif)



def read_legitimateips(): ###Transforms your whitelist to arrays to interate later.

	f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'feeds',legitips), 'rt')
	legitips_array = []
	csvreader = csv.reader(f)
	for row in csvreader:
		legitips_array.append(str(row[:1]))

	return legitips_array
	f.close()

print('[*] [Legitimate IPs Whitelist >$] Loaded successfully '+legitips)


def sum_dnsresolvers(): ##check how many values existis within csv files:
	with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'feeds',resolvers), 'rt') as csv_file:
		count_resolvers = -1
		readerb = csv.reader(csv_file, delimiter=',')
		next(readerb)
		for row in readerb:
			count_resolvers += 1
		return count_resolvers

sum_dnsresolvers = str(sum_dnsresolvers())

print("[*] [DNS Resolvers >$] Loaded successfully "+resolvers+" file containing a total of "+sum_dnsresolvers+" DNS Resolvers servers.")
print('[*] [My Domain >$] Picked '+domain+' as the domain to be resolved')

if enabled_email == str(1):
	print("[*] Email notification is enabled if any alert is found.")
else:
	print("[*] Email notification is disabled. To enable it, check dnspharming.ini setting send_email parameter to 1")

def read_dnsresolvers(): ###check for known dns resolvers in csv and transform into array
	with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'feeds',resolvers), 'rt') as csv_file:
		result = []
		readerb = csv.reader(csv_file, delimiter=',')
		next(readerb)
		for row in readerb:
			result.append(str(row[:1]))
		return result



def run_dnsqueries_and_compare_with_legitimate_list():

	###DNS LIB SETTINGS###

	resolver = dns.resolver.Resolver()
	resolver.timeout = 1.0
	resolver.lifetime = 1.0

	###END OF DNS LIB SETTINGS###

	ips_resolved = []
	resolvedby = defaultdict(list)
	resolvedby.default_factory
	success=0

	for i in read_dnsresolvers(): ##gets resolvers csv as input to perform dns queries
		i = i.replace("[","").replace("]","").replace("'","")
		resolver.nameservers=[str(i)]

		try: 
			b = resolver.query(domain,'A')
			for j in b:
				success+=1
				ips_resolved.append(j.to_text()) ##collect ip resolveds by dns servers and stores as array ips_resolved
				resolvedby[j.to_text()].append(i)
				a = ("Resolved {0} with success {1} {2}/{3}").format(str(domain),str(i), str(success),sum_dnsresolvers)
				print(a)
		except Exception as e:
			print(i, e, "Try increasing resolver DNS timeout&lifetime settings")

    ##wl stands for whitelist

	valid_checked_ips=[]
	for resolved_ip in ips_resolved:
		for wl in read_legitimateips():
			wl = wl.replace("[","").replace("]","").replace("'","")
			if (ipaddress.ip_address(resolved_ip) in ipaddress.ip_network(wl)) == True:
				valid_checked_ips.append(resolved_ip)
				break

	comparison = [x for x in ips_resolved if x not in valid_checked_ips]

	'''the above comparison it is very critical to continue to run. 
	It will check if any resolved IP is not recognized by you. 
	If so, will start to make whois queries and generate alerts.'''

	'''General logging below'''

	with open(os.getcwd()+"/logs/DNS_Pharming_Detection."+datetime.now().strftime("%Y-%m")+".log", "a") as log:
		log.write("[*]|"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|message=Started dnspharming.py\n")
		log.write("[*]|"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|message=Loaded successfully "+resolvers+" file containing a total of "+ sum_dnsresolvers +" DNS Resolvers servers.\n")
		log.write("[*]|"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|message=Picked "+domain+" as the domain to be resolved\n")

	if not comparison:

		with open(os.getcwd()+"/logs/DNS_Pharming_Detection."+datetime.now().strftime("%Y-%m")+".log", "a") 	as log:
			log.write("[*]|"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|message=[*] =========SUCCESSFULLY COMPLETED=====. DNS Queries Ratio of (success/total): ("+str(success)+"/"+sum_dnsresolvers+")\n")
			log.write("[*]|"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|message=No divergence was found. It seems the queried DNS Servers are safe.\n")

		return("[*] No divergence was found. It seems the queried DNS Servers are safe.")
	else:
		try:
    	# Create logs Directory
			os.mkdir("logs")
		except FileExistsError:
			pass
    	
		final_detection_dict = defaultdict(list)
		final_detection_dict.default_factory 
		whois_query = defaultdict(list)
		whois_query.default_factory
		for i in set(comparison): ##set is used because one ip can be resolved by by multiple dns resolvers, so every ip will count only once.
			final_detection_message = ("[!]|"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+
			"|message=It seems that your monitored domain {0} is resolving the IP: {1} (which is not in your whitelist)"+
			" when querying the following {2} DNS server(s): {3} "+
			"raising a potencial indicator of a DNS Pharming Attack."+
			"|domain={0}|resolvedip={1}|totaldnsserver={2}|resolvedby={3}\n").format(str(domain), str(i), str(len(resolvedby[i])), ', '.join(resolvedby[i]))
			final_detection_dict[i].append(', '.join(resolvedby[i]))
			for j in resolvedby[i]:
				try:
					whoisa = whois.whois(j)
					whois_query[j].append(whoisa['nets'][0]['description'])
					whois_query[j].append(whoisa['nets'][0]['country'])
					whois_query[j].append(whoisa['nets'][0]['emails'])
					whois_query[j].append(whoisa['nets'][0]['created'])
				except Exception as e:
					print(j, e)

			with open(os.getcwd()+"/logs/DNS_Pharming_Detection."+datetime.now().strftime("%Y-%m")+".log", "a") as log:
				log.write(final_detection_message)
		with open(os.getcwd()+"/logs/DNS_Pharming_Detection."+datetime.now().strftime("%Y-%m")+".log", "a") as log:
			log.write("[*]|"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|message=Resolvers Whois DATA|"+str(dict(whois_query))+'\n')
			log.write("[*]|"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|message=[*] =========SUCCESSFULLY COMPLETED=====. DNS Queries Ratio of (success/total): ("+str(success)+"/"+sum_dnsresolvers+")\n")
		print("[*] =========SUCCESSFULLY COMPLETED===== DNS Queries Ratio (success/total) of ("+str(success)+"/"+sum_dnsresolvers+")")

		if enabled_email == str(1): ##Check if SMTP notifications are turned on.

		###E-mail template using jinja2

			t = Template("""
				<h3 style=\"color: #5e9ca0;\">New detection for {{ domain }} </h3>

	<table border="1">
	<table bgcolor="#F2F2F2">
	<table class="blueTable">
	<thead>
	<tr>
	<th>Resolved IP</th>
	<th>DNS Servers IPs</th>
	</tr>
	</thead>
	<tfoot></tfoot>
	<tbody>
				{% for n, g in final_detection_dict %} <tr><td>{{n}}</td><td>{{g}}
				{% endfor %}


	</tbody>
	</table>
	</table>
	</table>
	<p>
  
  <h4 style=\"color: #5e9ca0;\">Whois Data
  
</p>
	<table border="1">
	<table bgcolor="#F2F2F2">
	<table class="blueTable">
	<thead>
	<tr>
	<th><th align="center">DNS Server IP</th>
	<th><th align="center">Organization</th>
	<th><th align="center">Country</th>
    <th><th align="center">E-mail</th>
    <th><th align="center">Creation Date</th>
    	<tfoot></tfoot>
	<tbody>
				{%for key, value in whois_query.items()%}
				<tr>
				<td><td align="center">{{key}}</td>
				<td><td align="center">{{value[0]}}</td>
				<td><td align="center">{{value[1]}}</td>
				<td><td align="center">{{value[2]}}</td>
				<td><td align="center">{{value[3]}}</td>
				{% endfor %}
    </table>
    </table>
    </table>
    </table>
	<h4 style=\"color: #5e9ca0;\">Check /logs directory for more details. </h4>

	""")


			email_message = t.render(domain=domain,final_detection_dict=final_detection_dict.items(),whois_query=whois_query)
			
			try:
				send_email.sendemail(email_message)
				print("[!] An email alert has been sent to: " +str(emailto))
				with open(os.getcwd()+"/logs/DNS_Pharming_Detection."+datetime.now().strftime("%Y-%m")+".log", "a") as log:
					log.write("[!]|"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|message=An email alert has been sent to: emailto=%s\n" % str(emailto))
			except Exception as e:
				print("Error when sending email ", e)

	return final_detection_dict

pprint(dict(run_dnsqueries_and_compare_with_legitimate_list()))
