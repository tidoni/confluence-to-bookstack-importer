from requests import get
from requests import post
from requests import put
import os
import subprocess
import json


class Bookstack:
    def __init__(self, base_url, auth_token_id, auth_secret):
        self.base_url = base_url
        self.auth_token_id = auth_token_id
        self.auth_secret = auth_secret

    # Demo/Test
    def get_docs_raw_json(self):
        return json.loads(get(self.base_url + '/api/docs.json', headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    # Attachments
    def get_attachments_raw_json(self):
        return json.loads(get(self.base_url + '/api/attachments', headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    def create_attachment_from_filepath_and_page_id(self, file_path, page_id):
        try:
            cmd = 'curl --silent -X POST -H "Authorization: Token ' + self.auth_token_id + ':' + self.auth_secret + '" -F name=\"' + os.path.basename(file_path) + '\" -F uploaded_to=' + page_id + ' -F "file=@\"' + file_path + '\"" \"' + self.base_url + '/api/attachments\"'
            result = subprocess.check_output(cmd, shell=True)
            return json.loads(result)
        except Exception as e:
            print(e)
            return False

    # Shelves
    def get_all_shelves_raw_json(self):
        return json.loads(get(self.base_url + '/api/shelves', headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    def read_shelve_by_id_raw_json(self, shelve_id):
        return json.loads(get(self.base_url + '/api/shelves/' + shelve_id, headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    def create_shelve_from_object(self, shelve_object):
        return json.loads(post(self.base_url + '/api/shelves', json=shelve_object, headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    def create_shelve_from_title_and_description(self, title, description):
        shelve_object = {
            "name": title,
            "description": description
        }
        return self.create_shelve_from_object(shelve_object)

    def update_shelve_by_id_from_object(self, shelve_id, shelve_object):
        return json.loads(put(self.base_url + '/api/shelves/' + shelve_id, params=shelve_object, headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    # Books
    def get_all_books_raw_json(self):
        return json.loads(get(self.base_url + '/api/books', headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    def read_book_by_id_raw_json(self, book_id):
        return json.loads(get(self.base_url + '/api/books/' + book_id, headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    def create_book_from_object(self, book_object):
        return json.loads(post(self.base_url + '/api/books', json=book_object, headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    def create_book_from_title_and_description(self, title, description):
        book_object = {
            "name": title,
            "description": description
        }
        return self.create_book_from_object(book_object)

    # Pages
    def get_all_pages_raw_json(self):
        return json.loads(get(self.base_url + '/api/pages', headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    def read_page_by_id_raw_json(self, book_id):
        return json.loads(get(self.base_url + '/api/pages/' + book_id, headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    def create_page_from_object(self, book_object):
        return json.loads(post(self.base_url + '/api/pages', json=book_object, headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)

    def create_page_from_title_and_content(self, title, html_content):
        book_object = {
            "name": title,
            "html": html_content
        }
        return self.create_page_from_object(book_object)

    def create_page_from_title_and_content_and_book_id(self, title, html_content, book_id):
        # create empty div, if the returned content from confluence does not contain any usefull html content
        if html_content == "":
            html_content = "<div></div>"
        book_object = {
            "name": title,
            "html": html_content,
            "book_id": book_id
        }
        return self.create_page_from_object(book_object)

    def update_page_content_by_id(self, page_id, html_content):
        page_content = {
            "html": html_content
        }
        return json.loads(put(self.base_url + '/api/pages/' + str(page_id), json=page_content, headers={'Authorization': f'Token {self.auth_token_id}:{self.auth_secret}'}).text)
