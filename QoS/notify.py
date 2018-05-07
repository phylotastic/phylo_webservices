#module to send email notifications
from os.path import dirname, abspath 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
import smtplib
import ConfigParser
 
#---------------------------------------------
def get_smtp_params():
	config = ConfigParser.ConfigParser()
	current_dir = dirname(abspath(__file__))

	config_path = os.path.join(current_dir, "smtp.cfg")
	#print config_path
	if os.path.exists(config_path):
		config.read(config_path)
	else:
		print "SMTP Config file not found! Exiting!"
		sys.exit(1)

	email = config.get('gmail', 'email')
	password = config.get('gmail', 'password')
	recipients = config.get('gmail', 'recipients')

	return email, password, recipients


#----------------Multiple Emails-----------------------------
#https://stackoverflow.com/questions/8856117/how-to-send-email-to-multiple-recipients-using-python-smtplib
def send_notifications(subj, messg, recipients=None):
	"""
	Send an email to multiple recipients
	"""
	# create message object instance
	msg = MIMEMultipart()
	message = messg
 
	from_email, password, recipients_str = get_smtp_params()
	
	# setup the parameters of the message
	msg['From'] = from_email
	msg['To'] =  recipients_str #", ".join(recipients)
	msg['Subject'] = subj
 
	recipients_list = recipients_str.split(", ")
 
	# add in the message body
	msg.attach(MIMEText(message, 'plain'))
 
	#create server
	server = smtplib.SMTP('smtp.gmail.com: 587')
 
	server.starttls()
 
	# Login Credentials for sending the mail
	server.login(msg['From'], password)
 
	# send the message via the server.
	server.sendmail(msg['From'], recipients_list, msg.as_string())
 
	server.quit()
 
	for email in recipients_list:
		print "successfully sent email to %s" % (email)


#----------------------------------------------

if __name__ == '__main__':
	send_notifications("Service Status", "OToL_Tree service is down")	

