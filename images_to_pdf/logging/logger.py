import logging
import sys
from datetime import date

# LOGGER = None

class StandardFilter(logging.Filter):
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
    # global LOGGER

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
        handler = logging.FileHandler(filename='{path}/{date}_{name}.log'.format(path=path, date=file_formated_date, name=main_module_name), mode='a', encoding=None, delay=False)
    
    formater = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')

    if type(handler) is list:
        for h in handler:
            h.setLevel(level)
            h.setFormatter(formater)
            logger.addHandler(h)
    else:
        handler.setLevel(level)
        handler.setFormatter(formater)
        logger.addHandler(handler)
    
    logger.setLevel(level)

    # LOGGER = logger

# def get_logger(level, file=None):
#     if not LOGGER:
#         set_logger(level, file)
    
#     return LOGGER
