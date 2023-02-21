import hashlib


class RandomUser(object):
    def __init__(self, user, salt):
        self._user = str(user)
        self._salt = str(salt)
        
    def get_number(self):
        hash_string = self._user + self._name
        hash_object = hashlib.md5(hash_string.encode("utf8"))
        hash_int = int.from_bytes(hash_object.digest(), "big")
        return hash_int
        
    def get_element(self, element_list):
        element_cnt = len(element_list)
        hash_int = self.get_number()
        element_num = hash_int % element_cnt
        return element_list[element_num]
