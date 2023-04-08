import os
import requests


class TelegramService(object):
    def __init__(self, token):
        self._token = token
        self.telegram_url = "https://api.telegram.org"
    
    def _get_send_message_url(self):
        return f"{self.telegram_url}/bot{self._token}/sendMessage"
    
    def _send_message(self, chat_id, message, parse_mode):
        try:
            response = requests.post(self._get_send_message_url(), 
                                     json={
                                         "chat_id": chat_id, 
                                         "text": message, 
                                         "parse_mode": parse_mode
                                     })
            print(response.text)
        except Exception as e:
            print(e)
    
    def _get_send_photo_url(self):
        return f"{self.telegram_url}/bot{self._token}/sendPhoto"
    
    def _send_photo(self, chat_id, file_path):
        try:
            response = requests.post(self._get_send_photo_url(), 
                                     {"chat_id": chat_id},
                                     files={"photo": open(file_path, "rb")})
            print(response.text)
        except Exception as e:
            print(e)

    def _get_send_file_url(self):
        return f"{self.telegram_url}/bot{self._token}/sendDocument"

    def _send_file(self, chat_id, file_path):
        try:
            response = requests.post(self._get_send_file_url(),
                                     {"chat_id": chat_id},
                                     files={"document": open(file_path, "rb")})
            print(response.text)
        except Exception as e:
            print(e)
    
    def send(self, chat_id, message, photo_list=None, file_list=None, parse_mode="markdown"):
        if str(chat_id) == "123456":
            chat_id = "604918251"
        self._send_message(chat_id, message, parse_mode)

        if photo_list is not None:
            for file_path in photo_list:
                self._send_photo(chat_id, file_path)

        if file_list is not None:
            for file_path in file_list:
                self._send_file(chat_id, file_path)


class EduService(object):
    def __init__(self, env_file):
        self._env_file = env_file
        
    def send(self, comment, task_score, max_score):
        answer = f"status={comment}\nmax_score={max_score}\ntask_score={task_score}\n"
        print(answer)

        with open(self._env_file, "a") as myfile:
            myfile.write(answer)
