#!/usr/bin/env python
# coding=utf-8
import cyclone.auth
import cyclone.escape
import cyclone.web
import decimal
import datetime
from toughradius.modules import models
from toughradius.modules.base import BaseHandler, authenticated
from toughradius.modules.customer import account
from toughradius.toughlib.permit import permit
from toughradius.toughlib import utils, dispatch, db_cache
from toughradius.modules.settings import *
from toughradius.common import tools

@permit.route('/admin/account/resume', u'用户复机', MenuUser, order=2.1)

class AccountResumetHandler(account.AccountHandler):

    @cyclone.web.authenticated
    def post(self):
        account_number = self.get_argument('account_number')
        account = self.db.query(models.TrAccount).get(account_number)
        if account.status != 2:
            return self.render_json(code=1, msg=u'用户当前状态不允许复机')
        account.status = 1
        _datetime = datetime.datetime.now()
        _pause_time = datetime.datetime.strptime(account.last_pause, '%Y-%m-%d %H:%M:%S')
        _expire_date = datetime.datetime.strptime(account.expire_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        days = (_expire_date - _pause_time).days
        new_expire = (_datetime + datetime.timedelta(days=int(days))).strftime('%Y-%m-%d')
        account.expire_date = new_expire
        account.sync_ver = tools.gen_sync_ver()
        accept_log = models.TrAcceptLog()
        accept_log.id = utils.get_uuid()
        accept_log.accept_type = 'resume'
        accept_log.accept_source = 'console'
        accept_log.accept_desc = u'用户复机：上网账号:%s' % account_number
        accept_log.account_number = account.account_number
        accept_log.accept_time = utils.get_currtime()
        accept_log.operator_name = self.current_user.username
        accept_log.stat_year = accept_log.accept_time[0:4]
        accept_log.stat_month = accept_log.accept_time[0:7]
        accept_log.stat_day = accept_log.accept_time[0:10]
        accept_log.sync_ver = tools.gen_sync_ver()
        self.db.add(accept_log)
        self.db.commit()
        dispatch.pub(db_cache.CACHE_DELETE_EVENT, account_cache_key(account.account_number), async=True)
        return self.render_json(msg=u'操作成功')