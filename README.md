# <h2> <b> dnspharming detection utility </b></h2>

Very simple project to monitor passively your brand against malicious responses

-=-=-=-=-Brand Monitoring against DNS Pharming/Poisoning attacks -=-=-=-=-=
-=-=-=-=-       v.1.0 2019-06-09 	             -=-=-=-=-=

![alt text](https://raw.githubusercontent.com/byhardest/dnspharming/master/dnspharming_bash.png)

This code was made using python 3.6.7 <br>
Make sure you meet the following criterias before running;

sudo easy_install pip3<br>
sudo pip3 install -r requirements.txt

This script is suitable for monitoring, I recommend to schedule via cron hourly/daily.

<b>-=-=-=-=CONFIG FILE-=-=-=-=</b>

By default dnspharming.ini config comes at blank, which can be filled when running the dnspharming.py script for the 1st time. 

-FEEDS as: (Whitelist, and DNS Servers) MUST be at feeds/ If you use CDNs, Akamai and Cloudfront was uploaded by 2019-06-09. 
If you are not sure. Contact your provider for up-to-date information. 

-CONFIG as (domain name, filenames feeds ones) must be at /config.

<b>-=-=-=-=-=E-mail Notification-=-=-=-=</b>

![alt text](https://raw.githubusercontent.com/byhardest/dnspharming/master/dnspharming_emailnotification.png)

By default, e-mail notification comes with 0. (Disabled) Switch enabled_email to 1.

I have only tested with GMAIL using port 587. 
I recommend you to setup a specific account for this purpose.
You will also need to grant access as 'high risk considered applications.' in order to work. 
https://myaccount.google.com/security.

Following the procedures above or picking up an account is at your own risk.
<b>-=-=-=-=-=LOGS-=-=-=-=</b>

Logs are generated under /logs within files written per month.
They can be extracted and set to a SIEM. <p></p>

-=-=-=-=-=To be improved-=-=-=-=-=

-support for multiple domains.<p>
-compression and rotation for /logs folder.<p>
-encryption for smtp password under /config folder.<p>


How does the attack work?

![Source:Imperva](https://www.imperva.com/learn/wp-content/uploads/sites/13/2019/01/DNS-spoofing.jpg)
