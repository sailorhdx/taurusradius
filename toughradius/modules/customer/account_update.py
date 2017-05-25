#!/usr/bin/env python
# coding=utf-8
import cyclone.auth
import cyclone.escape
import cyclone.web
import decimal
from toughradius.modules import models
from toughradius.modules.base import BaseHandler, authenticated
from toughradius.modules.customer import account, account_forms
from toughradius.toughlib.permit import permit
from toughradius.toughlib import utils, dispatch, db_cache
from toughradius.modules.settings import *
from toughradius.common import tools

@permit.route('/admin/account/update', u'用户策略修改', MenuUser, order=2.2)

class AccountUpdatetHandler(account.AccountHandler):

    @authenticated
    def get(self):
        account_number = self.get_argument('account_number', None)
        account = self.db.query(models.TrAccount).get(account_number)
        form = account_forms.account_update_form()
        form.fill(account)
        self.render('base_form.html', form=form)
        return

    @authenticated
    def post(self):
        form = account_forms.account_update_form()
        if not form.validates(source=self.get_params()):
            return self.render('base_form.html', form=form)
        account = self.db.query(models.TrAccount).get(form.d.account_number)
        account.ip_address = form.d.ip_address
        account.install_address = form.d.install_address
        account.user_concur_number = form.d.user_concur_number
        account.bind_mac = form.d.bind_mac
        account.bind_vlan = form.d.bind_vlan
        account.domain = form.d.domain
        account.account_desc = form.d.account_desc
        account.sync_ver = tools.gen_sync_ver()
        if form.d.new_password:
            account.password = self.aes.encrypt(form.d.new_password)
        self.add_oplog(u'修改上网账号信息:%s' % account.account_number)
        self.db.commit()
        dispatch.pub(db_cache.CACHE_DELETE_EVENT, account_cache_key(account.account_number), async=True)
        self.redirect(self.detail_url_fmt(account.account_number))