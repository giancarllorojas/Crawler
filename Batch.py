import threading

from Crawler import Crawler
from Crawler import urlInserter

num_threads = 16
num_consumers = 4
total_pages = 9228
threads = []
consumers = []
            

for i in range(0, num_consumers):
    consumers[i] = urlInserter('anal', 'Xvideos')
    consumers[i].start()

for i in range(0, num_threads):
    size_blocks = int(total_pages / num_threads)
    start = i*size_blocks
    end = start + size_blocks
    if(i == num_threads - 1):
        end = total_pages
    thread = Crawler('anal', 'https://www.xvideos.com/c/', '/anal-12', start, end, 'Xvideos')
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()
for consumer in consumers:
    consumer.join()
print('Donezo')
