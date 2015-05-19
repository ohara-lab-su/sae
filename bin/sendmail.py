#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com   
#
################################################################################
__author__     = "Kengo NAKADA"                                                           
__maintainer__ = "Kengo NAKADA"                                                           
__credits__    = ["Kengo NAKADA"]                                                         
__email__      = "kengo.nakada@gmail.com"                                                 
__copyright__  = "Copyright 2014, Kengo NAKADA"                                           
__license__    = "MIT"                                                                    
#                                                                                         
__status__     = "alpha"                                                                  
__version__    = "0.0.1"                                                                  
################################################################################

import smtplib

from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

if __name__ == "__main__":

    from_address = "kengo.nakada@spring8.or.jp"
    to_address   = "kengo.nakada@gmail.com"
    charset = "ISO-2022-JP"
    subject = u"テストメールです"
    text    = u"てすと。メールの本文です"

    msg = MIMEText(text.encode(charset),"plain",charset)
    msg["Subject"] = Header(subject,charset)
    msg["From"]    = from_address
    msg["To"]      = to_address
    msg["Date"]    = formatdate(localtime=True)

    smtp = smtplib.SMTP("sp8sun.spring8.or.jp")
    smtp.sendmail(from_address,to_address,msg.as_string())

    smtp.close()

