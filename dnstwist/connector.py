from connectors.core.connector import Connector, ConnectorError, get_logger
from .operations import _check_health, search

logger = get_logger('dnstwist')


class DnsTwist(Connector):

    def execute(self, config, operation_name, params, **kwargs):
        logger.info("operation_name: {0}".format(operation_name))

        operations = {
            'search': search,
        }
        action = operations.get(operation_name)
        return action(config, params)

    def check_health(self, config):
        try:
            return _check_health(config)
        except Exception as e:
            raise ConnectorError(e)
