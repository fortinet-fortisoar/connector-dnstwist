import logging
import json
import time

try:
    import dnstwist
    import queue

    MODULE_DNSTWIST = True
except ImportError:
    MODULE_DNSTWIST = False

from connectors.core.connector import Connector, get_logger, ConnectorError

logger = get_logger('dnstwist')

THREAD_COUNT = 4


def search(config, params):
    try:
        # fuzz = dnstwist.Fuzzer(params.get("domain").strip())
        # TODO use at version 20211204
        fuzz = dnstwist.DomainFuzz(params.get("domain").strip())
        fuzz.generate()

        jobs = queue.Queue()
        for j in fuzz.domains:
            jobs.put(j)

        threads = []
        for _ in range(THREAD_COUNT):
            # worker = dnstwist.Scanner(jobs)
            # TODO use at version 20211204
            worker = dnstwist.DomainThread(jobs)
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
        domains = dnstwist.create_json(domains)
        domains = json.loads(domains)
    except Exception as e:
        logger.exception("An exception occurred {0}".format(e))
        raise ConnectorError("{0}".format(e))

    return domains


def _check_health(config):
    if not MODULE_DNSTWIST:
        raise ConnectorError("Unable to find dnstwist library")
