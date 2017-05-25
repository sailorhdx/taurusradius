#!/usr/bin/env python
# coding=utf-8
import datetime
import time
from hashlib import md5
from toughradius.modules.ssportal.base import BaseHandler
from toughradius.toughlib.permit import permit
from toughradius.toughlib import utils
from toughradius.modules import models

@permit.route('/acforward')

class AcForwardHandler(BaseHandler):
    """
    http://182.254.146.116:1819/acforward?action=new&user=
    
    http://182.254.146.116:1819/acforward?
    user=test
    &ip=192.168.2.91
    &timestemp=1484018336
    &action=renew
    &sign=803238d4b472d474d3dcd7db09ea90ec
     // sign = md5(user+ip+timestemp+action+share_secret)
    """

    def get(self):
        action = self.get_argument('action', '')
        if action == 'new':
            self.redirect('/ssportal/product')
            return
        if action == 'renew':
            user = self.get_argument('user')
            ip = self.get_argument('ip')
            timestemp = self.get_argument('timestemp')
            action = self.get_argument('action')
            sign = self.get_argument('sign')
            nass = self.db.query(models.TrBas)
            if nass.count() == 0:
                self.redirect('/ssportal')
                return
            sign_ok = False
            for nas in nass:
                _sign = md5(user + ip + timestemp + action + str(nas.bas_secret)).hexdigest()
                if sign == _sign:
                    sign_ok = True
                    break

            if not sign_ok:
                self.redirect('/ssportal')
                return
            account = self.db.query(models.TrAccount).get(user)
            if not account:
                self.redirect('/ssportal')
                return
            self.set_session_user(account.customer_id, account.account_number, ip, utils.get_currtime())
            self.redirect('/ssportal/account')