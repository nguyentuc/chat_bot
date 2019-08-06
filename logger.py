# -*- encoding: utf-8 -*-

import logging
import config, utils
import os


utils.mkdir(config.LOG_DIR)
log_file = os.path.join(config.LOG_DIR, config.LOG_FILE)

logging.basicConfig(filename=log_file,
                    filemode='a',
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger()