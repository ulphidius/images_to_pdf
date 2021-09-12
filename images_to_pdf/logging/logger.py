import logging
import sys
from datetime import date

class StandardFilter(logging.Filter):
    # pylint: disable=arguments-differ
    def filter(self, rec):
        allow_levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARN
        ]

        for allow_level in allow_levels:
            if rec.levelno == allow_level:
                return True

        return False

class ErrorFilter(logging.Filter):
    # pylint: disable=arguments-differ
    def filter(self, rec):
        allow_levels = [
            logging.ERROR,
            logging.CRITICAL
        ]

        for allow_level in allow_levels:
            if rec.levelno == allow_level:
                return True

        return False

def init_logger(level, path = None):
    main_module_name = __name__.split('.')[0]
    logger = logging.getLogger(main_module_name)
    handler = None

    if not path:
        handler = list()
        handler.append(logging.StreamHandler(stream=sys.stdout))
        handler[-1].addFilter(StandardFilter())
        handler.append(logging.StreamHandler(stream=sys.stderr))
        handler[-1].addFilter(ErrorFilter())
    else:
        current_date = date.today()
        file_formated_date = current_date.strftime('%Y_%m_%d')
        handler = logging.FileHandler(filename='{path}/{date}_{name}.log'.format(
            path=path,
            date=file_formated_date,
            name=main_module_name),
            mode='a',
            encoding=None,
            delay=False
        )

    formater = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S %p'
    )

    if isinstance(handler, list):
        for handler_unit in handler:
            handler_unit.setLevel(level)
            handler_unit.setFormatter(formater)
            logger.addHandler(handler_unit)
    else:
        handler.setLevel(level)
        handler.setFormatter(formater)
        logger.addHandler(handler)

    logger.setLevel(level)
