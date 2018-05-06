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

	return email, password


#----------------Multiple Emails-----------------------------
#https://stackoverflow.com/questions/8856117/how-to-send-email-to-multiple-recipients-using-python-smtplib
def send_notifications(subj, messg, recipients):
	"""
	Send an email to multiple recipients
	"""
	# create message object instance
	msg = MIMEMultipart()
	message = messg
 
	from_email, password = get_smtp_params()
	
	# setup the parameters of the message
	msg['From'] = from_email
	msg['To'] = ", ".join(recipients)
	msg['Subject'] = subj
 
	# add in the message body
	msg.attach(MIMEText(message, 'plain'))
 
	#create server
	server = smtplib.SMTP('smtp.gmail.com: 587')
 
	server.starttls()
 
	# Login Credentials for sending the mail
	server.login(msg['From'], password)
 
	# send the message via the server.
	server.sendmail(msg['From'], recipients, msg.as_string())
 
	server.quit()
 
	for email in recipients:
		print "successfully sent email to %s" % (email)


#----------------------------------------------

if __name__ == '__main__':
	send_notifications("Service Status", "OToL_Tree service is down", ["abusalehmdtayeen@gmail.com", "mdtayeen@yahoo.com"])	

