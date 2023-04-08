from requests import get
from datetime import datetime
from .metaclass import Singleton


class ActionRunStorage(object, metaclass=Singleton):
    def __init__(self):
        self.run_dict = {}

    def append(self, id, status, conclusion, workflow_name, username, create_dttm, html_url):
        if username not in self.run_dict.keys():
            self.run_dict[username] = {}

        if (id not in self.run_dict[username]) or (self.run_dict[username][id]["status"] != "completed"):
            self.run_dict[username][id] = {
                "status": status,
                "conclusion": conclusion,
                "workflow_name": workflow_name,
                "project": f"https://github.com/{workflow_name}",
                "create_dttm": create_dttm,
                "run": html_url
            }
            return True
        else:
            return False

    def get_by_username(self, username):
        return self.run_dict.get(username, None)


class ActionRun(object, metaclass=Singleton):
    def __init__(self, github_token, cache_sec=300):
        self.github_token = github_token
        self.cache_sec = cache_sec
        self.actuality_dttm = None
        self.action_run_storage = ActionRunStorage()
        self.max_run_per_page = 50
        self.max_page_retry_cnt = 3

    def _load_page(self, page_num):
        loaded_run_cnt = 0
        has_intersection = False
        try:
            url = "https://api.github.com/repos/Xapulc/tf-data-analysis-lesson" \
                  + f"/actions/runs?per_page={self.max_run_per_page}&page={page_num}"
            res = get(url, headers={"Authorization": f"Bearer {self.github_token}"})

            if not res.ok:
                print(res.status_code)
                print(res.content)

            assert res.ok, "Неуспешный результат"

            workflow_run_list = res.json()["workflow_runs"]
            loaded_run_cnt = len(workflow_run_list)

            for workflow_run in workflow_run_list:
                id = workflow_run["id"]
                create_dttm = datetime.strptime(workflow_run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                status = workflow_run["status"]
                html_url = workflow_run["html_url"]
                conclusion = workflow_run.get("conclusion", None)
                workflow_name = workflow_run["display_title"]
                username = workflow_name.split("/")[0].strip(" ")

                if username[0] == "{":
                    username = username[1:]

                if username[-1] == "}":
                    username = username[:-1]

                append_res = self.action_run_storage.append(id=id, status=status, conclusion=conclusion,
                                                            workflow_name=workflow_name, username=username,
                                                            create_dttm=create_dttm, html_url=html_url)

                if not append_res:
                    has_intersection = True
        except Exception as e:
            print(e)
            return False, has_intersection, loaded_run_cnt, e

        return True, has_intersection, loaded_run_cnt

    def _update_run_dict(self):
        if self.actuality_dttm is None:
            loaded_run_cnt = self.max_run_per_page
            page_num = 1
            current_page_retry_cnt = 0

            while loaded_run_cnt == self.max_run_per_page:
                load_res = self._load_page(page_num)
                status = load_res[0]

                if status:
                    loaded_run_cnt = load_res[2]
                    page_num += 1
                    current_page_retry_cnt = 0
                elif (not status) and (current_page_retry_cnt < self.max_page_retry_cnt):
                    current_page_retry_cnt += 1
                else:
                    break

        elif (datetime.now() - self.actuality_dttm).seconds > self.cache_sec:
            page_num = 1
            current_page_retry_cnt = 0
            loaded_run_cnt = self.max_run_per_page
            has_intersection = False

            while (not has_intersection) and (loaded_run_cnt == self.max_run_per_page):
                load_res = self._load_page(page_num)
                status = load_res[0]

                if status:
                    has_intersection = load_res[1]
                    loaded_run_cnt = load_res[2]
                    page_num += 1
                    current_page_retry_cnt = 0
                elif (not status) and (current_page_retry_cnt < self.max_page_retry_cnt):
                    current_page_retry_cnt += 1
                else:
                    break

        self.actuality_dttm = datetime.now()

    def get_run_dict(self, username):
        self._update_run_dict()
        return self.action_run_storage.get_by_username(username)

    def start(self):
        self._update_run_dict()
