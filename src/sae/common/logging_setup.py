#!/usr/bin/env python
# codoing: utf-8
# Copyright Kengo NAKADA; SAE class library.
import multiprocessing
import logging


class LoggingSetup:

    def get_loglevel_object(self, loglevel_):
        """
        文字列から logging のオブジェクトを返す

        :param loglevel_: string の文字列 info,debug,,,
        :return:
        """
        if loglevel_ is None:
            return logging.ERROR
        elif loglevel_ in ["DEBUG", "debug"]:
            return logging.DEBUG
        elif loglevel_ in ["INFO", "info"]:
            return logging.INFO
        elif loglevel_ in ["ERROR", "error"]:
            return logging.ERROR
        elif loglevel_ in ["WARNING", "warning"]:
            return logging.ERROR
        else:
            return False

    def init_logger(self, logging=None, loglevel=None, logmode=None):
        """
        logging(logger)の初期設定, デフォルト処理など
        support関数版なのでインスタンス変数の処理などはしない

        :param loging: logging のインスタンス logger と表現することが多い
        :param loglevel: Info,Debug,,,,
        :param logmode:  Syslog,,,
        :return: logging, logger
        """
        from sae.common.logging_setup import LoggingSetup

        # メモリ上の logger インスタンス（生）を用いる
        # 新たに EmLogger() (multiprocessing.get_logger() ) で生成したインスタンスを引いた場合
        # changed logmode
        if logging is None:
            logger = multiprocessing.get_logger()
            try:
                if loglevel is not None:
                    logger.setLevel(LoggingSetup().get_loglevel_object(loglevel))
            except Exception:
                pass
        else:
            # 互換（logging として logger を食わせた場合
            try:
                logger = logging.logger
            except Exception:
                logger = logging
            try:
                if loglevel is not None:
                    logging.set_loglevel(loglevel)
            except Exception:
                pass
        return (logging, logger)
