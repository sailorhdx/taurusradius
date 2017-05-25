#!/usr/bin/env python
# coding=utf-8
from toughradius.toughlib import utils, dispatch
from toughradius.toughlib import logger
from toughradius.modules import models
from toughradius.modules.events.event_basic import BasicEvent
from toughradius.modules.settings import OpenNotify
from toughradius.modules.events.settings import EVENT_SENDSMS, EVENT_SENDMAIL

class AccountOpenNotifyEvent(BasicEvent):

    def event_account_open(self, account_number, order_id = None):
        userinfo = self.get_customer_info(account_number)
        content_tpl = self.get_content_template(OpenNotify)
        if not content_tpl:
            return
        content = content_tpl.replace('{customer_name}', utils.safeunicode(userinfo.realname))
        content = content.replace('{product_name}', utils.safeunicode(userinfo.product_name))
        content = content.replace('{username}', account_number)
        content = content.replace('{expire_date}', userinfo.expire_date)
        content = content.replace('{password}', self.aes.decrypt(userinfo.password))
        params = {}
        params['phone'] = userinfo.mobile
        params['mobile'] = userinfo.mobile
        params['address'] = utils.safestr(userinfo.install_address)
        params['tplname'] = 'tr_open_notify'
        params['gid'] = ''
        params['password'] = self.aes.decrypt(userinfo.password)
        params['username'] = account_number
        params['customer'] = utils.safestr(userinfo.realname)
        params['product'] = utils.safestr(userinfo.product_name)
        params['expire'] = userinfo.expire_date
        dispatch.pub(EVENT_SENDSMS, userinfo.mobile, utils.safeunicode(content), **params)


def __call__(dbengine = None, mcache = None, aes = None, **kwargs):
    return AccountOpenNotifyEvent(dbengine=dbengine, mcache=mcache, aes=aes, **kwargs)