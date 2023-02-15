import os
import email
import smtplib
import requests


def send_result_to_email(to_email, message_subject, message_body):
    from_email = os.getenv("EMAIL")
    from_email_password = os.getenv("PASSWORD")
    
    msg = email.message_from_string(message_body)
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = message_subject
    
    s = smtplib.SMTP("smtp-mail.outlook.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(from_email, from_email_password)
    
    s.sendmail(from_email, to_email, msg.as_string().encode("utf-8"))
    s.quit()
        
        
def send_result_to_telegram(chat_id, message):
    token = os.getenv("TELEGRAM_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        response = requests.post(url, json={"chat_id": chat_id, "text": message})
        print(response.text)
    except Exception as e:
        print(e)

    
def send_result_to_edu(comment, task_score, max_score):
    env_file = os.getenv("GITHUB_ENV")
    answer = f"status={comment}\nmax_score={max_score}\ntask_score={task_score}\n"
    print(answer)
    
    with open(env_file, "a") as myfile:
        myfile.write(answer)
