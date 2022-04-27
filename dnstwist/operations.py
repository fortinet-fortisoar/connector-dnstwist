import logging
import json
import time
from concurrent.futures import ThreadPoolExecutor
from connectors.core.connector import Connector, get_logger, ConnectorError

try:
    import dnstwist
    import queue

    MODULE_DNSTWIST = True
except ImportError:
    MODULE_DNSTWIST = False

logger = get_logger('dnstwist')

THREAD_COUNT = 4


def search(config, params):
    try:
        # fuzz = dnstwist.Fuzzer(params.get("domain").strip())
        # TODO use at version 20211204
        fuzz = dnstwist.DomainFuzz(params.get("domain").strip())
        fuzz.generate()
        jobs = queue.Queue()

        with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
            for domain in fuzz.domains:
                jobs.put(domain)
                worker = dnstwist.DomainThread(jobs)
                worker.debug = True
                executor.submit(worker.run)

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
