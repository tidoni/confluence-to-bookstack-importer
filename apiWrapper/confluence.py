from requests import get
import json


class Confluence:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token

    # Spaces
    def get_spaces_raw_json(self):
        return json.loads(get(self.base_url + '/rest/api/space', headers={'Authorization': f'Bearer {self.auth_token}'}).text)

    def get_spaces_names(self):
        spaces_array = []
        for space in self.get_spaces_raw_json()['results']:
            spaces_array.append(space['name'])
        return spaces_array

    def get_spaces_keys(self):
        spaces_array = []
        for space in self.get_spaces_raw_json()['results']:
            spaces_array.append(space['key'])
        return spaces_array

    def get_iconlink_of_space_by_key(self, space_key):
        result = json.loads(
            get(
                self.base_url + "/rest/api/space/" + space_key + "?expand=icon",
                headers={'Authorization': f'Bearer {self.auth_token}'}
            ).text
        )
        return result['_links']['base'] + result['icon']['path']

    # Pages
    def get_all_results_from_url_raw_json(self, url):
        results = []
        result = json.loads(
            get(
                url,
                headers={'Authorization': f'Bearer {self.auth_token}'}
            ).text
        )
        for entry in result['results']:
            results.append(entry)

        if "next" in result['_links']:
            next_link = result['_links']['next']
        else:
            next_link = ""

        while next_link != "":
            result = json.loads(
                get(
                    self.base_url + next_link,
                    headers={'Authorization': f'Bearer {self.auth_token}'}
                ).text
            )
            for entry in result['results']:
                results.append(entry)

            if "next" in result['_links']:
                next_link = result['_links']['next']
            else:
                next_link = ""

        return results

    def get_pages_from_space_key_raw_json(self, space_key, page_or_blogpost):
        return self.get_all_results_from_url_raw_json(self.base_url + "/rest/api/space/" + space_key + "/content/" + page_or_blogpost + "?depth=root")

    def get_child_pages_from_content_id_raw_json(self, content_id):
        return self.get_all_results_from_url_raw_json(self.base_url + "/rest/api/content/" + content_id + "/child/page")

    def get_page_body_from_content_id(self, content_id):
        result = json.loads(
            get(
                self.base_url + "/rest/api/content/" + content_id + "?expand=space,body.view",
                headers={'Authorization': f'Bearer {self.auth_token}'}
            ).text
        )
        return result['body']['view']['value']

    def get_title_from_content_id(self, content_id):
        result = json.loads(
            get(
                self.base_url + "/rest/api/content/" + content_id,
                headers={'Authorization': f'Bearer {self.auth_token}'}
            ).text
        )
        return result['title']

    # Attachments
    def get_attachments_from_content_id_raw_json(self, content_id):
        return self.get_all_results_from_url_raw_json(self.base_url + "/rest/api/content/" + content_id + "/child/attachment")

    def download_attachment_from_downloadurl_and_path(self, download_url, download_path, file_title):
        try:
            response = get(download_url, headers={'Authorization': f'Bearer {self.auth_token}'})
            open(download_path + file_title, "wb").write(response.content)
            return True
        except Exception as e:
            print(e)
            return False

    def download_all_attachments_from_content_id_and_download_path(self, content_id, download_path):
        try:
            attachments = self.get_attachments_from_content_id_raw_json(content_id)
            for attachment in attachments:
                download_url = self.base_url + attachment['_links']['download']
                self.download_attachment_from_downloadurl_and_path(download_url, download_path, attachment['title'])
            return True
        except Exception:
            return False

    # If no Child is present, return the current id, if children present, recursivly call funktion, apend all returned ids AND the current id
    def get_ids_of_all_childrens_recursive(self, content_id):
        children = self.get_child_pages_from_content_id_raw_json(content_id)
        childIDs = []

        if len(children) == 0:
            return [content_id]
        else:
            for child in children:
                for c_id in self.get_ids_of_all_childrens_recursive(child['id']):
                    childIDs.append(c_id)
            childIDs.append(content_id)
            return childIDs
