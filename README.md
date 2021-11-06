# Social Network Scraper

![GitHub](https://badgen.net/badge/icon/github?icon=github&label)
![version](https://img.shields.io/badge/version-1.1-blue)
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen)

## What is scraping?

Web scraping is simply the process of using a social media web scraper to gather data automatically. It saves users time, effort and sometimes money since it’s an automatic process performed by bots. You could take the time to search the web for all mentions of a certain word or find all prices for a certain product, but that would take a lot of time.

In certain cases, it might even be impossible for one person to do it on their own. I mean, think about it. Can you imagine scrolling through page after page of a website, writing down every single mention of a word, analyzing the context of that word and putting it all in an easy-to-read format that other people can understand? I can’t imagine doing that, and I don’t think I’m the only one.

That’s why we have social media web scrapers to do that work for us. Web scraping these sites is easy as pie, especially if you have the right tools to help you. (More on that later.) All you have to do is tell the scraper what information you want to collect and it will parse through hypertext markup language on the social media platform. This information can range anywhere from collecting usernames, finding followers, collecting comments and analyzing conversations that include your keywords. Of course, it’s possible to use this information to gather sensitive data and manipulate others, and some people do it. But that’s not (and shouldn’t be) the goal. Done correctly, web scraping can really help individuals accomplish their personal and professional goals by helping them collect valuable data and give that data meaning.

***

## Installation project

First need install requirements:
```shell
$ pip3 install -r requirements.txt
```

## Setting up config file
Edit the `config.py` file with private app`s information.

<details><summary>Config data details</summary>

1. Flask backend config data: host-address and port:
```python
HOST = '127.0.0.1'  # host of flask backend
PORT = 7654         # port
```

2. Vkontakte config data:
```python
VK_APP_VERSION=''       # version of vk user application
VK_APP_ID=''            # vk application id
VK_APP_SECRET_KEY=''    # secret key of vk application (see preferences...)
VK_APP_SERVICE_KEY=''   # service key of vk application (see preferences...)
VK_APP_ACCESS_TOKEN=''  # access token of vk application (see preferences...)
```

3. Facebook config data:
```python
FB_APP_VERSION=''       # version of facebook application
FB_APP_ID=''            # facebook application id
FB_CLIENT_MARKER=''     # client marker-token to get access user info
FB_APP_SECRET_KEY=''    # secret key of facebook application (see preferences...)
FB_APP_ACCESS_KEY=''    # access key of facebook application (see preferences...)
```

4. Twitter config data:
```python
TW_CONSUMER_KEY=''          # consumer key (see preferences...)
TW_CONSUMER_SECRET=''       # consumer secret token (see preferences...)
TW_ACCESS_TOKEN_KEY=''      # access token of twitter application (see preferences...)
TW_ACCESS_TOKEN_SECRET=''   # access secret token of twitter application (see preferences...)
```

5. LinkedIn config data:
```python
LI_USERNAME=''  # username to linkedIn account
LI_PASSWORD=''  # password to specified username
```

6. MyMainRu config data:
```python
MM_APP_ID=0             # MyMailRu application id
MM_USERNAME=''          # username to MyMailRu account
MM_PASSWORD=''          # password to specified username
MM_APP_SECRET_KEY=''    # secret key of MyMailRu application (see preferences...)
MM_APP_PRIVATE_KEY=''   # private key of MyMainRu application (see preferences...)
```

7. OSINT sites config data:
```python
EMAILREP_API_KEY=''     # API token to https://emailrep.io
DEHASHED_API_KEY=''     # API token to https://dehashed.com
```

</details>

***

## Launching 

There are several process launching modes: 

First mode - python script.

```shell
   Usage: simple_run.py {path to user json-file}
```

Second mode if backend based on Flask microframework. The host and port of backend you can set by changing `config.py` file. Command to launch backend:
```shell
   python3 flask_backed_run.py
```

or 

```shell
   ./flask_backed_run.py
```

There are several available REST API:
   - `/osint_scraping` scraping all data from osint-sites (Now accessible only two resources: https://emailrep.io and https://dehashed.com); 
   - `/social_scraping` scraping all data from social network sites/application like (Vk, Facebook, Twitter, LinkedIn ...); 
   - `/full_scraping` scraping all data from all resources.

### Input json file/data
User json-file contains user's contact information that the user specified 
when sign up to `cvcode`. Such information is `Vkontakte ID`, `Facebook ID` and 
`UserAccessMarker` and e.t.c.

<details><summary><b>Example of this json</b></summary>

```json
{
    "Vkontakte": {
        "id": "123456789"
    },
    "LinkedIn": {
        "id": "ivan-ivanov-123456789"
    },
    "Twitter": {
        "id": "Ivan123456789"
    },
    "Facebook": {
        "id": "101313123456789",
    "user_access_token": "EAAMTR2pPmqUBACIvzm..."
    },
    "MyMailRu": {
        "id": "ivan.ivanov@bk.ru",
        "session_key": "dec21acb9b62bdaabe6ef89965d58e56"
    },
   "OSINT": {
      "email": "ivan.ivanov@bk.ru"
   }
}
```

</details>

### Output json file/data
The result is json-file or json-response from backend. Examples of result you can research into `Tests/Reulst/` directory ([see input json-file](#Tests/Users/yuliya_chesnokova.json))

***

## Contacts

telegram: @sudo_udo
email: breadrock1@gmail.com
