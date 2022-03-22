users = 'DATA'
href = {}
href_for_parser = {}
class UserHREF: 
    "Класс создания ссылки для парсера"

    def __init__(self, user_id):
        global href
        self.id = user_id 
        href[user_id] = {}

    def set_href(self, user_id, name, value):
        global href 

        href[user_id][name] = value

    def get_existed_href(self, user_id):
        global href 
        href_for_parser[user_id] = {}

        href_for_parser[user_id]['href'] = 'https://raspisanie.rusoil.net/index.php?filial=' + str(href[user_id]['fil']) + '&fob='+ str(href[user_id]['fob']) + '&fak='+ str(href[user_id]['fak']) + \
        '&kurs=' + str(href[user_id]['kurs']) + '&gruppa=' + str(href[user_id]['gruppa']) + '&sem=' + str(href[user_id]['sem'])

        return href_for_parser

    def get_href(self, user_id):
        global href

        return href
    
