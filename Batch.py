import threading
import json
import sys

from Crawler import Crawler
from Crawler import urlInserter

if(len(sys.argv) < 2):
    print("Run with: Batch.py config_name")
    sys.exit()

config = json.loads(open("batches/" + sys.argv[1] + ".json", "r").read())

threads = []
consumers = []
            

for i in range(0, config['num_consumers']):
    consumers.append(urlInserter(config['category'], config['parser'], config['num_batch_insert'], config['num_threads']))
    consumers[i].start()

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
for consumer in consumers:
    consumer.join()