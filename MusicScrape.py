

#scraping imports
from bs4 import BeautifulSoup
import pandas as pd
import requests
#email imports
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import csv
import yagmail
#schedule imports
import schedule
import time

"""

def emailFunc(subject, body, filename):

	port = 465
	smtp_server = 'smtp.gmail.com'

	#subject = 'An email with attachment from Python'
	#body = 'This is an email with an attachment sent from Python'
	sender_email = 'kyleb.develop@gmail.com'
	receiver_email = 'kylebremont@gmail.com'
	password = getpass.getpass(prompt='Password: ', stream=None)

	# Create a multipart message and set headers
	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Subject"] = subject
	message["Bcc"] = receiver_email  # Recommended for mass emails

	# Add body to email
	message.attach(MIMEText(body, "plain"))

	#filename = "TreatedDraft.pdf"  # In same directory as script

	# Open PDF file in binary mode
	with open(filename, "rb") as attachment:
	    # Add file as application/octet-stream
	    # Email client can usually download this automatically as attachment
	    part = MIMEBase("application", "octet-stream")
	    part.set_payload(attachment.read())

	# Encode file in ASCII characters to send by email    
	encoders.encode_base64(part)

	# Add header as key/value pair to attachment part
	part.add_header(
	    "Content-Disposition",
	    f"attachment; filename= {filename}",
	)

	# Add attachment to message and convert message to string
	message.attach(part)
	text = message.as_string()

	# Log in to server using secure context and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
	    server.login(sender_email, password)

	    with open('contact_list.csv') as file:
	    	reader = csv.reader(file)
	    	next(reader)
	    	for name, email in reader:
	    		server.sendmail(sender_email, email, text.format(name=name))
"""


# email sent using yagmail, much simpler than above solution
def emailFunc2(subject, body, filename):

	sender = 'kyleb.develop@gmail.com'
	yag = yagmail.SMTP(sender)
	with open('contact_list.csv') as file:
		reader = csv.reader(file)
		next(reader)
		for name, email in reader:
			yag.send(
				to=email,
				subject=subject,
				contents=body.format(name=name),
				attachments=filename,
			)


def webScrape():

	titles = [] # title of the song
	titles2 = []
	artists = [] # name of the artist
	artists2 = []
	releaseDates = [] # song's release date
	releaseDates2 = []


	# This is to scrape complex
	for i in range(2):

		if i == 0:
			res = requests.get('https://hiphopdx.com/singles')
		else:
			res = requests.get('https://hiphopdx.com/singles/{}'.format(i+1))
		
		soup = BeautifulSoup(res.text)

		for title in soup.find_all('td', class_='title'):
			title = str(title)
			title = title[18:len(title)-5]
			titles.append(title)

		for artist in soup.find_all('td', class_='artist'):
			artist = str(artist)
			artist = artist[31:len(artist)-5]
			artists.append(artist)

		for date in soup.find_all('td', class_='date'):
			date = str(date)
			date = date[50:len(date)-5]
			releaseDates.append(date)


	# This is to scrape PopVortex
	res = requests.get('http://www.popvortex.com/music/charts/new-rap-songs.php')
	soup = BeautifulSoup(res.text)

	for em in soup.find_all('em', attrs={'class':'artist'}):
		artist = em.find('a').contents[0]
		artist = str(artist)
		#print(em.find('a').contents[0])
		artists.append(artist)
	

	for cite in soup.find_all('cite', attrs={'class':'title'}):
		title = cite.find('a').contents[0]
		title = str(title)
		#print(cite.find('a').contents[0])
		titles.append(title)

	
	for div in soup.find_all('div', attrs={'class':'chart-content col-xs-12 col-sm-8'}):
		n = 1
		for li in div.find_all('li'):
			if n % 2 == 0:
				date = str(li.contents[1])
				date = date[2:len(date)-6]
				releaseDates.append(date)
			n += 1


	# creating the csv file
	df = pd.DataFrame({'Title':titles, 'Artist':artists, 'Release Date':releaseDates})
	df = df.sort_values(by=['Release Date'])
	df.to_csv('New_Songs.csv', index=False, encoding='utf-8')
	
	filename = 'New_Songs.csv'
	subject = 'Your Weekly New Songs'
	body = 'Hi {name}, attached is your weekly music update.'
	emailFunc2(subject, body, filename)
	


def main():

	"""
	schedule.every(15).seconds.do(webScrape)

	while True:
		schedule.run_pending()
		time.sleep(1)
	"""
	webScrape()
	
	

	


if __name__ == '__main__':
	main()




#Autumn Murray,autumn.murray13@gmail.com

