# <h2> <b> dnspharming detection utility </b></h2>

Very simple project to monitor passively your brand against malicious responses

![Source:Imperva](https://www.imperva.com/learn/wp-content/uploads/sites/13/2019/01/DNS-spoofing.jpg)
(image-src: Imperva)<br>


-=-=-=-=-<b>Brand Monitoring against DNS Pharming/Poisoning attacks</b> -=-=-=-=-=<br>
<center>v.1.0 2019-06-09</center>

![alt text](https://raw.githubusercontent.com/byhardest/dnspharming/master/dnspharming_bash.png)

<b>-=-=-=-=HOW DOES THE PREVENTION WORKS-=-=-=-=</b>

The scripts comes with a pre-built list of 20k+ open resolvers. <br>
Declare your domain <br>
Insert your whitelist IPs. <br>
Cron the script. It will check if any given answer does not match your whitelist. <br>
Enable email notification or Send the logs to your SIEM <br>
Be notified when someone answer an IP address which is not authozied by you. <br>


This code was made using python 3.6.7 <br>
Make sure you meet the following criterias before running;<br>

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

I have only tested with GMAIL using port 587. <br>
I recommend you to setup a specific account for this purpose.<br>
You will also need to grant access as 'high risk considered applications.' in order to work. <br>
https://myaccount.google.com/security.

Following the procedures above or picking up an account is at your own risk.<br>
<b>-=-=-=-=-=LOGS-=-=-=-=</b><br>

Logs are generated under /logs within files written per month.<br>
They can be extracted and set to your SIEM. <p></p>

-=-=-=-=-=To be improved-=-=-=-=-=

-support for multiple domains.<p>
-compression and rotation for /logs folder.<p>
-encryption for smtp password under /config folder.<p>
