import os
import email
import smtplib
import requests
import hashlib


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
        
        
def send_result_to_telegram(chat_id, message, attachment_list):
    token = os.getenv("TELEGRAM_TOKEN")
    send_message_url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        response = requests.post(send_message_url, json={"chat_id": chat_id, "text": message, "parse_mode": "markdown"})
        print(response.text)
    except Exception as e:
        print(e)
    
    if attachment_list is not None:
        send_photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
        for file_path in attachment_list:
            try:
                response = requests.post(send_photo_url, json={"chat_id": chat_id}, files={"photo": open(file_path, "rb")})
                print(response.text)
            except Exception as e:
                print(e)

    
def send_result_to_edu(comment, task_score, max_score):
    env_file = os.getenv("GITHUB_ENV")
    answer = f"status={comment}\nmax_score={max_score}\ntask_score={task_score}\n"
    print(answer)
    
    with open(env_file, "a") as myfile:
        myfile.write(answer)
        
        
def get_variant(chat_id, salt, min_variant, max_variant):
    hash_string = str(chat_id) + salt
    hash_object = hashlib.md5(hash_string.encode("utf8"))
    hash_int = int.from_bytes(hash_object.digest(), "big")
    variant = (hash_int % (max_variant - min_variant + 1)) + min_variant
    return variant
