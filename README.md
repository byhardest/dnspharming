# dnspharming
Very simple project to monitor passively your brand against malicious responses

-=-=-=-=-Brand Monitoring against DNS Pharming -=-=-=-=-=
-=-=-=-=-       v.1.0 2019-06-09 	             -=-=-=-=-=

This project was made using python 3.6.7 
Make sure you meet the following criterias before running;

sudo easy_install pip3
sudo pip3 install -r requirements.txt

This script is suitable for monitoring, I recommend to schedule via cron hourly/daily.

-=-=-=-=CONFIG FILE-=-=-=-=

By default dnspharming.ini config comes blank, which can be filled when running the dnspharming.py script for the 1st time. 

-FEEDS as: (Whitelist, and DNS Servers) MUST be at feeds/ If you use CDNs, Akamai and Cloudfront was uploaded by 2019-06-09. 
If you are not sure. Contact your provider for up-to-date information. 

-CONFIG as (domain name, filenames feeds ones) must be at /config.

-=-=-=-=-=E-mail Notification-=-=-=-=

By default, e-mail notification comes with 0. (Disabled) Switch enabled_email to 1.

I have only tested with GMAIL using port 587. 
I recommend you to setup a specific account for this purpose.
You will also need to grant access as 'high risk considered applications.' in order to work. 
https://myaccount.google.com/security.

Following the procedures above or picking up an account is at your own risk.

-=-=-=-=-=To be improved-=-=-=-=-=

-support for multiple domains.<p>
-compression and rotation for /logs folder.<p>
-encryption for smtp password under /config folder.<p>
