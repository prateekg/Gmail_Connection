import imaplib #To make a connection to a socket and return a connection
import email #Used to iterate over the email_message and walk through the body 
import pandas as pd #To create the dataframe
from textblob import TextBlob #It is similar to the NLTK Library but it is easy to use and some extra features are also there
import getpass #It is for getting the raw_input from user in password type

mail = imaplib.IMAP4_SSL('imap.gmail.com')
# imaplib module implements connection based on IMAPv4 protocol


username = raw_input("Enter the username: ")
password = getpass.getpass("Password: ") 
print "Trying to Login %s. . . \n" %username
mail.login(username, password)
print 'Connected ! \n'


mail.list() # Lists all labels in GMail
mail.select('INBOX') # Connected to inbox. #You can select for any other folder in the mail (You can see in the mail.list()
result, data = mail.uid('search', None, "ALL")


From = []; CC = []; To = []; Subject = []; Sentiment_Polarity = []; Body =[];
df = pd.DataFrame(columns=["From", "CC", "To", "Subject", "Sentiment_Polarity", "Body"])


i = len(data[0].split()) # data[0] is a space separate string
print "Accessing %d mails in INBOX \n\n" %i 


print "Getting the information....\n"
for x in range(i):
	latest_email_uid = data[0].split()[x] # unique ids wrt label selected
	result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')

 	raw_email = email_data[0][1]
	raw_email_string = raw_email.decode('utf-8')
	email_message = email.message_from_string(raw_email_string)
	
	email_subject = email_message['Subject']
	Subject.append(email_subject)
	
	email_from = email_message['From']
	From.append(email_from)
	
	email_to = email_message['To']
	To.append(email_to)

	email_cc = email_message['Cc']
	CC.append(email_cc)

	#print email_message
	print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

	for part in email_message.walk():
		print part.get_charsets()
		if part.get_content_type() == "text/plain" and {"utf-8", "UTF-8"}.intersection(part.get_charsets()):
			body = part.get_payload(decode=True) 
			#Creating a TextBlob object to perform various textblob methods on it
			blob = TextBlob(body.decode('utf-8'))
			print blob
			#print body + "\n\n"
			#save_string = str("email_" + str(x) + ".txt")
			# location on disk
			#myfile = open(save_string, 'a')
			#text = body.decode('utf-8')
			#myfile.write(text.encode('utf-8'))
			# body is again a byte literal
			#myfile.close()
		else:
			continue
	Body.append(blob)
	Sentiment_Polarity.append(blob.sentiment.polarity)


mail.logout()
print "Done\n\n"	
#columns=["From", "CC", "To", "Subject", "Sentiment_Polarity"]
#From = []; CC = []; To = []; Subject = []; Sentiment_Polarity = [];

print "Creating the dataframe..."
df["From"] = From
df["CC"] = CC
df["To"] = To
df["Subject"] = Subject
df["Sentiment_Polarity"] = Sentiment_Polarity
df["Body"] = Body

print "CSV created at /home/aviso/Desktop/Sentiment_score.csv"
df.to_csv("/home/aviso/Desktop/Sentiment_score.csv")

#print df
