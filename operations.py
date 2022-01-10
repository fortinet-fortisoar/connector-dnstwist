import logging
import json
import subprocess
import os

from connectors.core.connector import Connector, get_logger, ConnectorError

logger = get_logger('dnstwist')
DNS_TWIST = "/opt/cyops-integrations/.env/bin/dnstwist"


def search(config, params):
    domain = params.get("domain").strip()
    cli_params = [DNS_TWIST,
                  "--registered",
                  "-f",
                  "json",
                  f"{domain}"]
    try:

        result = subprocess.run(cli_params, stdout=subprocess.PIPE)
        result = result.stdout.decode('utf-8')
        result = json.loads(result)

    except Exception as e:
        logger.exception("An exception occurred {0}".format(e))
        raise ConnectorError("{0}".format(e))
    # finally:
    # if os.path.exists(tmp_path): os.remove(tmp_path)
    return result


def _check_health(config):
    binary = DNS_TWIST
    if not os.path.exists(binary):
        raise Exception("Unable to find dnstwist in path {0}".format(binary))
