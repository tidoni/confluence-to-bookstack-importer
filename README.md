# Confluence to BookStack importer

Import the Content from a Confluence Instance to a (new) BookStack Instance. 

## Install/Requirements


```bash
sudo apt install python3    # Testet with python 3.10
pip3 install bs4
```

You will probably have to set/change the API Limit, see: https://demo.bookstackapp.com/api/docs#rate-limits


## Usage

Edit importer.py to match your Environment.


```python
confluence_token = "********************************"
confluence_baseURL = "https://confluence-server.your-domain.tld"  # No trailing slash

bookstack_baseURL = "https://bookstack.your-domain.tld"  # No trailing slash
bookstack_token_id = "****************"
bookstack_token_secret = "****************"
```

You can create your *Personal Accestoken* for Confluence at `https://<domain-of-confluence-instance>/plugins/personalaccesstokens/usertokens.action`

For BookStack you have to create a *Token ID* & *Token Secret*, which can be created at `https://<domain-of-bookstack-instance>/settings/users/1/create-api-token`.
You may need to change the User-ID to match your Requirements.

You can also find this at *Settings -> Users -> Select a User and scroll down to API-Settings*


After changing the settings for your environment, run the importer
```python
python importer.py
```

## Mode of operation

| Confluence   | Bookstack  | Comment    |
|--------------|------------|------------|
| ---          | Shelvs     |            |           
| Space        | Books      |            |
| ---          | Chapter    |            |
| Page         | Page       |            |
| Blogpost     | Page       |            |

As you can see from the Table above, the *Structure* of the Pages, that can be used in Confluence (Every Page can have Children, which intern can have children and so on...), is not transported to BookStack.

In theory, 4 (or 3 if Spaces (Confluence) -> Shelvs (Bookstack)) hirachies can be used.
In the current state, all Pages that are part of a space, get imported to a book, losing the hierarchical structure.


## Known Issues/Feature Improvements

* Preview-Images are not clickable. Could be resolved by wrapping all image-containers by a link to open the image in a new tab.
* Linked Documents don't get converted to the new attachment link. Attachments can only be downloaded through the attachment section on the left.
* Inter-Site links don't get converted.
* Import parts of the structure
    * Check how long the Text of a Page is, if it is shorten that a given number, create a chapter rather than a page
    * If it contains no images/attachments, create it as a chapter rather then a page
