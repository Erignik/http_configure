# -*- coding: utf-8 -*-
import logging.config
import logging
import os

logging.config.fileConfig(os.path.join("conf", "logging.conf"))
logger = logging.getLogger()
