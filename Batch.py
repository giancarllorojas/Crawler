import threading
import json
import sys

from classes.Crawler import Crawler
from classes.Crawler import urlInserter

if(len(sys.argv) < 2):
    print("Run with: Batch.py job_name.json")
    sys.exit()

config = json.loads(open("jobs/batches/" + sys.argv[1] + ".json", "r").read())

threads = []
            

#Start consumer class
consumer = urlInserter(config['category'], config['parser'], config['bulk_size'], config['num_threads'])
consumer.start()

for i in range(0, config['num_threads']):
    total_pages = int(config['last_page'] - config['first_page'])
    size_blocks = int(total_pages / config['num_threads'])
    start = config['first_page'] + i*size_blocks
    end = start + size_blocks
    if i == config['num_threads'] - 1:
        end = config['first_page'] + total_pages
    thread = Crawler(config['category'], config['url_start'], config['url_end'], start, end, config['parser'])
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()

consumer.join()

print("Job batch finished: " + config['parser'] + " " + config['category'])