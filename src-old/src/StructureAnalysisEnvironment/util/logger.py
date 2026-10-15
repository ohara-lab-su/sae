#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中身は EM logger とほぼ同じ (Ver_0.6.0 のコピー)

"""
import sys
import multiprocessing
import logging
import logging.handlers

try:
    from logger_support import *
except:
    from StructureAnalysisEnvironment.util.logger_support import *


class Logger(object):
    """
    em_logger Ver_0.6.0
    """

    def __init__(self, loglevel='info', logmode='default', logformat=None, logappname=None):
        """
        Logger __init__

        :param loglevel:
        :param logmode:
        :param logformat:
        :param logappname: ログ名 (Eventlog for Windows)
        """
        if loglevel is None: loglevel = 'info'
        if logappname is None: logappname = 'python: ' + str(self.__class__.__name__)

        self.__loglevel = loglevel
        self.__logmode = logmode
        self.__logappname = logappname

        # create logger instance
        self.init_logger(loglevel=loglevel, logmode=logmode, logappname=logappname)

    @property
    def logger(self):
        # これが logging インスタンスに相当する形になる
        return self.__logger

    def info(self, val):
        return self.__logger.info(val)

    @property
    def INFO(self):
        return logging.INFO

    def debug(self, val):
        return self.__logger.debug(val)

    @property
    def DEBUG(self):
        return logging.DEBUG

    def error(self, val):
        return self.__logger.error(val)

    @property
    def WARNING(self):
        return logging.WARNING

    def warning(self, val):
        return self.__logger.error(val)

    def critical(self, val):
        return self.__logger.critical(val)

    @property
    def CRITICAL(self):
        return logging.CRITICAL

    def get_version(self):
        return __version__

    @classmethod
    def version(cls):
        # @property
        # def version(self):
        return __version__

    def set_logappname(self, _logappname):
        self.__logappname = _logappname

    def get_logappname(self):
        return self.__logappname

    logappname = property(get_logappname, set_logappname)

    def setLevel(self, loglevel_obj):
        self.__logger.setLevel(loglevel_obj)

    def set_loglevel(self, loglevel_):
        """
        :param loglevel:
        :return:
        """
        if isinstance(loglevel_, str):
            loglevel_obj = get_loglevel_object(loglevel_)
            if loglevel_obj is False: sys.exit(MS_LOGGER_INIT_UNKNOWN_LOGLEVEL)
            self.__logger.setLevel(loglevel_obj)

        elif isinstance(loglevel_, int):
            self.__logger.setLevel(loglevel_)

    def get_loglevel(self):
        return self.__loglevel

    loglevel = property(get_loglevel, set_loglevel)

    def set_logmode(self, logmode_):
        """
        handlers の選択と handelr のセット
        windows のときは syslog を選んでも eventlog に強制変更

        :param logmode:
        :param logappname:
        :param dllname: windows のときの log に付くDLL名
        :return:
        """
        logappname_ = self.__logappname

        # if self.chk_windows() and logmode is not None:
        #    logmode = 'windows'

        # print("set logmode = %s" % logmode_)
        fmt = dict()
        fmt["syslog"] = "[%(module)s.%(funcName)s] %(message)s"
        fmt["default"] = "[%(asctime)s] " + fmt["syslog"]
        fmt["windows"] = "[%(asctime)s] " + fmt["syslog"]
        fmt["eventlog"] = fmt["windows"]

        if logmode_ is None:
            fmt = (logging.Formatter(fmt["default"]))
            handler = logging.StreamHandler()
            handler.setFormatter(fmt)
        elif logmode_ in ['syslog']:
            fmt = (logging.Formatter(fmt["syslog"]))
            handler = logging.handlers.SysLogHandler(address='/dev/log')
            handler.setFormatter(fmt)
        elif logmode_ in ['windows', 'eventlog']:
            fmt = (logging.Formatter(fmt["syslog"]))
            handler = logging.handlers.NTEventLogHandler(logappname_, logtype='Application')
            handler.setFormatter(fmt)
        else:
            fmt = (logging.Formatter(fmt["default"]))
            handler = logging.StreamHandler()
            handler.setFormatter(fmt)

        self.__logger.addHandler(handler)
        self.__handler = handler

    def get_logmode(self):
        return self.__logmode

    logmode = property(get_logmode, set_logmode)

    def set_logformat(self, logformat_):
        """
        set log format

        :param logformat:
        :return:
        """
        if logformat_ is None:
            logformat = "[%(module)s.%(funcName)s] %(message)s"
        if logformat_ == 'default':
            logformat = "[%(module)s.%(funcName)s] %(message)s"

        self.__logformat = logformat_
        logging.Formatter(logformat_)

    def get_logformat(self):
        return self.__logformat

    logformat = property(get_logformat, set_logformat)

    #
    # logging の整理/起動
    #

    def init_logger(self, loglevel=None, logmode=None, logappname=None):
        """
        旧来のEmLoggerの核となるMethod
        (2019.02.22 以降はただの初期化まとめメソッド)

        :param loglevel:
        :param logmode:
        :param logappname:
        :return:
        """
        if logappname is None: logappname = self.__logappname
        if loglevel is None: loglevel = self.__loglevel

        # self.__logger = logging.getLogger(__name__)
        self.__logger = multiprocessing.get_logger()

        self.loglevel = loglevel
        self.logmode = logmode
        self.__logger.addHandler(self.__handler)

        return self.__logger

    #
    # support func
    #

    def chk_windows(self):
        return self.is_windows()

    def is_windows(self):
        """
            windows のチェック
        """
        WIN = False
        try:
            sys.getwindowsversion()
        except:
            pass
        else:
            WIN = True

        return WIN


if __name__ == '__main__':
    logger = Logger(loglevel='debug')

    logger.info('INFO BBBB')
    logger.debug('DEBUG BBBB')

