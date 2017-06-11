import threading

from Crawler import Crawler
from Crawler import urlInserter

num_threads = 12
num_consumers = 1
total_pages = 19969
threads = []
consumers = []
            

for i in range(0, num_consumers):
    consumers.append(urlInserter('Asian_woman', 'Xvideos'))
    consumers[i].start()

for i in range(0, num_threads):
    size_blocks = int(total_pages / num_threads)
    start = i*size_blocks
    end = start + size_blocks
    if i == num_threads - 1:
        end = total_pages
    thread = Crawler('Asian_woman', 'https://www.xvideos.com/c/', '/blowjob-15', start, end, 'Xvideos')
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()
for consumer in consumers:
    consumer.join()
print('Donezo')
