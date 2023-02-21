import os
import requests


class NotificationService(object):
    def send_to_telegram(self, chat_id, message, attachment_list):
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
                    response = requests.post(send_photo_url, {"chat_id": chat_id}, files={"photo": open(file_path, "rb")})
                    print(response.text)
                except Exception as e:
                    print(e)
    def send_result_to_edu(self, comment, task_score, max_score):
        env_file = os.getenv("GITHUB_ENV")
        answer = f"status={comment}\nmax_score={max_score}\ntask_score={task_score}\n"
        print(answer)

        with open(env_file, "a") as myfile:
            myfile.write(answer)
