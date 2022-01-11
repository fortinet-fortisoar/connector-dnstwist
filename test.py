
try:
    import dnstwist
    import queue
    import time
    MODULE_DNSTWIST = True
except ImportError:
    MODULE_DNSTWIST = False

fuzz = dnstwist.Fuzzer("ipconfig.org")
fuzz.generate()

jobs = queue.Queue()
for j in fuzz.domains:
    jobs.put(j)

# worker = dnstwist.DomainThread(jobs)
##
threads = []
for _ in range(10):
    worker = dnstwist.Scanner(jobs)
    worker.setDaemon(True)
    worker.debug = True
    worker.start()
    threads.append(worker)

while not jobs.empty():
    time.sleep(1)

for worker in threads:
    worker.stop()
    worker.join()

##
# worker = dnstwist.Scanner(jobs)
# worker.setDaemon(True)
# worker.debug = True
# worker.start()
#
# worker.join()

domains = fuzz.permutations(registered=True)
print(dnstwist.create_json(domains))

resolv = Resolver(configure=False)
