# Person Scraper
This project has been produced to scrape any person information from social networks also from government sites which provides free API functions. The `Person Scraper` is the part of CvCode and HrCode systems which collects person information to common data sampling to train neural network.

## Installation and launching
1. Install requirements:
   
    ```shell
       $ pip3 install -r requirements.txt
    ```

2. Edit the `config.py` file with private app`s information:

3. Script usage:

    ```shell
        Usage: simple_run.py {path to user json-file}
    ```

    User json-file contains user's contact information that the user specified 
    when sign up to `cvcode`. Such information is `Vkontakte ID`, `Facebook ID` and 
    `UserAccessMarker` and e.t.c.  

    <details><summary><b>Example of this file</b></summary>
   
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
                }
            }
        ```
    </details>

## Results

The result is json-file. Examples of result you can research into `Tests/Results/` directory.
