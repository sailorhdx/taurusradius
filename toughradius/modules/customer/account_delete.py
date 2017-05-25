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
from toughradius.modules.events.settings import ACCOUNT_DELETE_EVENT
from toughradius.modules.events.settings import DBSYNC_STATUS_ADD

@permit.route('/admin/account/delete', u'用户账号删除', MenuUser, order=2.6)

class AccountDeleteHandler(account.AccountHandler):

    @authenticated
    def get(self):
        account_number = self.get_argument('account_number')
        if not account_number:
            self.render_error(msg=u'account_number is empty')
        account = self.db.query(models.TrAccount).get(account_number)
        customer_id = account.customer_id
        self.db.query(models.TrAcceptLog).filter_by(account_number=account.account_number).delete()
        self.db.query(models.TrAccountAttr).filter_by(account_number=account.account_number).delete()
        self.db.query(models.TrBilling).filter_by(account_number=account.account_number).delete()
        self.db.query(models.TrTicket).filter_by(account_number=account.account_number).delete()
        self.db.query(models.TrOnline).filter_by(account_number=account.account_number).delete()
        self.db.query(models.TrAccount).filter_by(account_number=account.account_number).delete()
        self.db.query(models.TrCustomerOrder).filter_by(account_number=account.account_number).delete()
        self.add_oplog(u'删除用户账号%s' % account_number)
        self.db.commit()
        dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrAcceptLog.__tablename__, dict(account_number=account.account_number)), async=True)
        dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrAccountAttr.__tablename__, dict(account_number=account.account_number)), async=True)
        dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrBilling.__tablename__, dict(account_number=account.account_number)), async=True)
        dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrOnline.__tablename__, dict(account_number=account.account_number)), async=True)
        dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrAccount.__tablename__, dict(account_number=account.account_number)), async=True)
        dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrCustomerOrder.__tablename__, dict(account_number=account.account_number)), async=True)
        dispatch.pub(ACCOUNT_DELETE_EVENT, account.account_number, async=True)
        dispatch.pub(db_cache.CACHE_DELETE_EVENT, account_cache_key(account_number), async=True)
        return self.redirect('/admin/customer')