#!/usr/bin/env python
# coding=utf-8
from hashlib import md5
from toughradius.toughlib import utils, dispatch, redis_cache
from toughradius.modules.base import authenticated
from toughradius.modules.customer import account_forms
from toughradius.modules.customer import account
from toughradius.toughlib.permit import permit
from toughradius.modules import models
from toughradius.modules.settings import *
from toughradius.modules.events.settings import CACHE_DELETE_EVENT
from toughradius.common import tools

@permit.route('/admin/account/password', u'用户账号密码修改', MenuUser, order=1.41, is_menu=False)

class PasswordUpdateHandler(account.AccountHandler):

    @authenticated
    def get(self):
        form = account_forms.password_update_form()
        form.fill(account_number=self.get_argument('account_number'))
        return self.render('base_form.html', form=form)

    @authenticated
    def post(self):
        form = account_forms.password_update_form()
        if not form.validates(source=self.get_params()):
            self.render('base_form.html', form=form)
            return
        account = self.db.query(models.TrAccount).get(form.d.account_number)
        if form.d.password:
            account.password = self.aes.encrypt(form.d.password)
            account.sync_ver = tools.gen_sync_ver()
        self.add_oplog(u'修改用户%s密码 ' % form.d.account_number)
        self.db.commit()
        dispatch.pub(CACHE_DELETE_EVENT, account_cache_key(account.account_number), async=True)
        self.redirect(self.detail_url_fmt(account.account_number))