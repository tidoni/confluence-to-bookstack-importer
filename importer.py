#
# importer.py
# Created: 2022-11-02
#

import os
import re
import urllib.parse
from bs4 import BeautifulSoup

from apiWrapper.confluence import Confluence
from apiWrapper.bookstack import Bookstack

confluence_token = "********************************"
confluence_baseURL = "https://confluence-server.your-domain.tld"  # No trailing slash

bookstack_baseURL = "https://bookstack.your-domain.tld"  # No trailing slash
bookstack_token_id = "****************"
bookstack_token_secret = "****************"

confluence = Confluence(confluence_baseURL, confluence_token)
bookstack = Bookstack(bookstack_baseURL, bookstack_token_id, bookstack_token_secret)

temp_folder_for_file_transfers = "/tmp/confluence_to_bookstock/"
os.makedirs(temp_folder_for_file_transfers, exist_ok=True)

for space in confluence.get_spaces_raw_json()['results']:
    print(space['name'] + " (" + space['key'] + ") | " + str(space['id']))
    book = bookstack.create_book_from_title_and_description(space['name'], space['key'])

    for page in confluence.get_pages_from_space_key_raw_json(space['key'], "page"):
        for page_ids in confluence.get_ids_of_all_childrens_recursive(page['id']):
            print("\t" + confluence.get_title_from_content_id(page_ids) + " | " + page_ids)
            bookstack_page = bookstack.create_page_from_title_and_content_and_book_id(confluence.get_title_from_content_id(page_ids), confluence.get_page_body_from_content_id(page_ids), book['id'])

            raw_html_content = confluence.get_page_body_from_content_id(page_ids).replace(confluence_baseURL, bookstack_baseURL)
            soup_mysite = BeautifulSoup(raw_html_content, features="html.parser")

            attachments = confluence.get_attachments_from_content_id_raw_json(page_ids)
            for attachment in attachments:
                soup_mysite = BeautifulSoup(raw_html_content, features="html.parser")

                download_url = confluence_baseURL + attachment['_links']['download']
                fileName = re.sub('[^a-zA-Z0-9\.]', '', attachment['title'])
                confluence.download_attachment_from_downloadurl_and_path(download_url, temp_folder_for_file_transfers, fileName)

                bookstack_attachment = bookstack.create_attachment_from_filepath_and_page_id(os.path.join(temp_folder_for_file_transfers, fileName), str(bookstack_page['id']))
                print("\t\t" + str(bookstack_attachment['name']))
                os.remove(os.path.join(temp_folder_for_file_transfers, fileName))

                # Replace Links to images with the newly uploaded attachments
                embedded_images = soup_mysite.find_all(class_="confluence-embedded-image")
                for image in embedded_images:
                    imageString = str(image)
                    if imageString.__contains__(urllib.parse.quote(attachment['title'])):
                        if imageString.__contains__("/download/attachments/"):
                            old_embedded = imageString[imageString.index("/download/attachments/"):]
                            old_embedded = old_embedded[:old_embedded.index('"')]
                            new_embedded = bookstack_baseURL + "/attachments/" + str(bookstack_attachment['id']) + "?open=true"
                            raw_html_content = raw_html_content.replace(old_embedded, new_embedded)
                        if imageString.__contains__("/download/thumbnails/"):
                            old_embedded = imageString[imageString.index("/download/thumbnails/"):]
                            old_embedded = old_embedded[:old_embedded.index('"')]
                            new_embedded = bookstack_baseURL + "/attachments/" + str(bookstack_attachment['id']) + "?open=true"
                            raw_html_content = raw_html_content.replace(old_embedded, new_embedded)

                # Replace links to videos with the newly uploaded attachments
                embedded_objects = soup_mysite.find_all(class_="embeddedObject")
                for objects in embedded_objects:
                    objectsString = str(objects)
                    if objectsString.__contains__(urllib.parse.quote(attachment['title'])):
                        if objectsString.__contains__("/download/attachments/"):
                            old_embedded = objectsString[objectsString.index("/download/attachments/"):]
                            old_embedded = old_embedded[:old_embedded.index('"')]
                            new_embedded = bookstack_baseURL + "/attachments/" + str(bookstack_attachment['id']) + "?open=true"
                            raw_html_content = raw_html_content.replace(old_embedded, new_embedded)

            soup_mysite = BeautifulSoup(raw_html_content, features="html.parser")
            bookstack.update_page_content_by_id(bookstack_page['id'], str(soup_mysite))

    for blog in confluence.get_pages_from_space_key_raw_json(space['key'], "blogpost"):
        print("\t" + blog['title'] + " | " + blog['id'])
        bookstack.create_page_from_title_and_content_and_book_id(blog['title'], confluence.get_page_body_from_content_id(blog['id']), book['id'])

        attachments = confluence.get_attachments_from_content_id_raw_json(blog['id'])
        for attachment in attachments:
            soup_mysite = BeautifulSoup(raw_html_content, features="html.parser")

            download_url = confluence_baseURL + attachment['_links']['download']
            fileName = re.sub('[^a-zA-Z0-9\.]', '', attachment['title'])
            confluence.download_attachment_from_downloadurl_and_path(download_url, temp_folder_for_file_transfers, fileName)

            bookstack_attachment = bookstack.create_attachment_from_filepath_and_page_id(os.path.join(temp_folder_for_file_transfers, fileName), str(bookstack_page['id']))
            print("\t\t" + str(bookstack_attachment['name']))
            os.remove(os.path.join(temp_folder_for_file_transfers, fileName))

            # Replace Links to images with the newly uploaded attachments
            embedded_images = soup_mysite.find_all(class_="confluence-embedded-image")
            for image in embedded_images:
                imageString = str(image)
                if imageString.__contains__(urllib.parse.quote(attachment['title'])):
                    if imageString.__contains__("/download/attachments/"):
                        old_embedded = imageString[imageString.index("/download/attachments/"):]
                        old_embedded = old_embedded[:old_embedded.index('"')]
                        new_embedded = bookstack_baseURL + "/attachments/" + str(bookstack_attachment['id']) + "?open=true"
                        raw_html_content = raw_html_content.replace(old_embedded, new_embedded)
                    if imageString.__contains__("/download/thumbnails/"):
                        old_embedded = imageString[imageString.index("/download/thumbnails/"):]
                        old_embedded = old_embedded[:old_embedded.index('"')]
                        new_embedded = bookstack_baseURL + "/attachments/" + str(bookstack_attachment['id']) + "?open=true"
                        raw_html_content = raw_html_content.replace(old_embedded, new_embedded)

            # Replace links to videos with the newly uploaded attachments
            embedded_objects = soup_mysite.find_all(class_="embeddedObject")
            for objects in embedded_objects:
                objectsString = str(objects)
                if objectsString.__contains__(urllib.parse.quote(attachment['title'])):
                    if objectsString.__contains__("/download/attachments/"):
                        old_embedded = objectsString[objectsString.index("/download/attachments/"):]
                        old_embedded = old_embedded[:old_embedded.index('"')]
                        new_embedded = bookstack_baseURL + "/attachments/" + str(bookstack_attachment['id']) + "?open=true"
                        raw_html_content = raw_html_content.replace(old_embedded, new_embedded)

        soup_mysite = BeautifulSoup(raw_html_content, features="html.parser")
        bookstack.update_page_content_by_id(bookstack_page['id'], str(soup_mysite))
