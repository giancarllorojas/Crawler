"""
Uses urlFetcher to fetch the data from a page and get video information
"""
from classes.urlFetcher import urlFetcher
import sys
import json

consumers   = []

if(len(sys.argv) < 2):
    print("Run with: Batch.py job_file.json")
    sys.exit()

try:
    config = json.loads(open("jobs/fetches/" + sys.argv[1] + ".json", "r").read())
except:
    print("Could not open job json file.")
    sys.exit()

try:
    category    = config['category']
    parser      = config['parser']
    num_threads = config['num_threads']
    collection  = config['collection']
    bulk_size   = config['bulk_size']
except:
    print("Insert a valid job.json document")

for i in range(0, num_threads):
    consumers.append(urlFetcher(category, parser, collection, bulk_size))
    consumers[i].start()

for consumer in consumers:
    consumer.join()

print("Job Fetcher finished: " + str(category) + " - " + str(parser))