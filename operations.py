import logging
import json

try:
    import dnstwist
    import queue
    import time

    MODULE_DNSTWIST = True
except ImportError:
    MODULE_DNSTWIST = False

from connectors.core.connector import Connector, get_logger, ConnectorError

logger = get_logger('dnstwist')


def search(config, params):
    fuzz = dnstwist.Fuzzer(params.get("domain").strip())
    fuzz.generate()

    jobs = queue.Queue()
    for j in fuzz.domains:
        jobs.put(j)

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

    domains = fuzz.permutations(registered=True)

    return dnstwist.create_json(domains)


def _check_health(config):
    if not MODULE_DNSTWIST:
        raise Exception("Unable to find dnstwist library")
