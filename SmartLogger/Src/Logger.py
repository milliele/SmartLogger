# -*- coding: utf-8 -*-

import logging, logging.config
import os

# ******************************** 软件日志 ***********************************
# 创建logger
if not os.path.exists('Conf'):
    os.mkdir('Conf')
if not os.path.exists('ExeLog'):
    os.mkdir('ExeLog')
logging.config.fileConfig("Conf/logging.conf")  # 采用配置文件
logger = logging.getLogger()
# ******************************** 软件日志 ***********************************