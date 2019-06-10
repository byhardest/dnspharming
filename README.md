# <h2> <b> dnspharming detection utility </b></h2>

Very simple project to monitor passively your brand against DNS malicious responses

![Source:Imperva](https://www.imperva.com/learn/wp-content/uploads/sites/13/2019/01/DNS-spoofing.jpg)
(image-src: Imperva)<br>


-=-=-=-=-<b>Brand/Domain monitoring against DNS Pharming/Poisoning attacks</b> -=-=-=-=-=<br>
<center>v.1.0 2019-06-09</center>

![alt text](https://raw.githubusercontent.com/byhardest/dnspharming/master/dnspharming_bash.png)

<b>-=-=-=-=How does the prevention work?-=-=-=-=</b>

1) The scripts comes with a pre-built list of 20k+ worldwide open resolvers but you can increment or pick your own. (Shodan API is a good option if you have enough credits.) <br>
2) Declare your domain. <br>
3) Insert your whitelist IPs. <br>
4) Cron the script. It will check if any given answer does not match your whitelist. <br>
Enable email notification or Send the logs to your SIEM. <br>
5) Be notified when someone answer an IP address which is not authozied by you. <br>


This code was made using python 3.6.7. <br>
Make sure you meet the following criterias before running;<br>

sudo easy_install pip3<br>
sudo pip3 install -r requirements.txt
USAGE: $> python3 dnspharming.py 

This script is suitable for monitoring, I recommend to schedule via cron hourly/daily.

<b>-=-=-=-=Config File-=-=-=-=</b>

By default config/dnspharming.ini config comes at blank arguments, which can be filled when running the dnspharming.py script for the 1st time or manually.

-FEEDS as: (Whitelist, and DNS Servers) MUST be at feeds/ <br>
If you use CDNs, Akamai and Cloudfront list was uploaded by 2019-06-09.<br>
If you are not sure about this information. Contact your DNS Administrator for up-to-date information. 
<br>
-CONFIG as (domain name, filenames feeds ones) must be at /config.

<b>-=-=-=-=-=E-mail Notification-=-=-=-=</b>

![alt text](https://raw.githubusercontent.com/byhardest/dnspharming/master/dnspharming_emailnotification.png)

By default, e-mail notification comes with 0. (Disabled) <br>Switch enabled_email to 1 for enabling it.

I have only tested with GMAIL using port 587. <br>
I recommend you to setup a specific account for this purpose.<br>
When using GMAIL, you will also need to grant access as 'high risk considered applications.' in order to work. <br>
https://myaccount.google.com/security.

Following the procedures above or picking up an account is at your own risk.<br>

<b>-=-=-=-=-=LOGS-=-=-=-=</b><br>

-Logs are generated under /logs within files written per month.<br>
-They can be extracted and set to your SIEM. <p></p>

-=-=-=-=-=To be improved-=-=-=-=-=

-support for multiple domains.<p>
-compression and rotation for /logs folder.<p>
-encryption for smtp credential stored under /config folder.<p>
