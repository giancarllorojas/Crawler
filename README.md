# Python3 Crawler

----
## What is it?
This is a generic multi-thread, multi-process crawling application to get massive amount of data fast.

It uses **SqLite3** as a **Job Queue** for storing all the links crawled, then fetches it and save the information into **MongoDb**.

----
## Requirements
At the moment it only supports Python3 and uses some good open-source libraries. You can easily install them:

    pip3 install requests
    pip3 install beautifulsoup4
    pip3 install pymongo

----
## Usage

* Clone this repository
* Create a job file inside the **jobs** folder, this file will contain the necessary parameters for crawling
* Create a **Parser** class inside the **parsers** folder, this class should inherit the **classes.parser** class and should have the 2 methods described there. You parse it the way you want, but I recommend using **BeautifulSoup4** as it is the best python html parsing library in my opinion.
* Run **python3 Batch.py job_config.json** to run a Batch that will get all the pages and call your parser based on the job_config file. This step will create a temporary **SqLite3** database file inside the **databases** folder that will contains all the **URLs** that you got with your parser.
* Run **python3 Fetch.py job_config.json** to run the Fetcher, this will get all the links in the SqLite database file that have not been fetched, get the data, call your parser and then insert it into MongoDb.