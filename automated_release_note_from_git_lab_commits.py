import requests
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
MY_ADDRESS = 'sample@gmail.com'
PASSWORD = 'samplepassword'
EMAILS = ["tosomeone@gmail.com"]
PROJECT_ID = '1102'
def main():
    today = datetime.datetime.now() 
    last_day = today - datetime.timedelta(days=1)
    formated_lday = last_day.strftime("%Y-%m-%dT00:00:00Z")
    formated_tday = today.strftime("%Y-%m-%dT00:00:00Z")
    header = {"PRIVATE-TOKEN": "MY_GITLAB_API_PRIVATE_TOKEN"}
    response = requests.get('https://gitlaburl.com/api/v4/projects/%s/repository/commits?ref_name=master&since=%s&until=%s' % (PROJECT_ID, formated_lday, formated_tday), headers=header)
    data = response.json()
    message = ""
    for commit in data:
        if commit['title'].find('Merge branch'):
            message += "\n%s" % commit['title']
    if message == "":
	return True
    for email in EMAILS:
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(MY_ADDRESS, PASSWORD)
        msg = MIMEMultipart()
        msg.attach(MIMEText(message, 'plain'))
        msg['subject'] = 'My Project Release note - %s' % formated_tday
        s.sendmail(MY_ADDRESS, email, msg.as_string())
    s.quit()

if __name__ == "__main__":
    main()
