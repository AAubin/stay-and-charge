import logging
from logging_manager import setup_logging
# logger = logging.getLogger(__name__)
setup_logging()

from data.cache import search_lodgings


test = search_lodgings('Bordeaux')
print(len(test))
print(test[0])

