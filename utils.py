import email
import smtplib


def send_result(to_email, message_subject, message_body):
    from_email = os.getenv('EMAIL')
    print(from_email)
    from_email_password = os.getenv('PASSWORD')
    
    msg = email.message_from_string(message_body)
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = message_subject
    
    s = smtplib.SMTP("smtp-mail.outlook.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(from_email, from_email_password)
    
    s.sendmail(from_email, to_email, msg.as_string())
    s.quit()
