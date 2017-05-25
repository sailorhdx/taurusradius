#!/usr/bin/env python
# coding=utf-8
from toughradius.toughlib import utils, dispatch
from toughradius.modules.events.event_basic import BasicEvent
from toughradius.modules.settings import NextNotify
from toughradius.modules.events.settings import EVENT_SENDSMS, EVENT_SENDMAIL, EVENT_SEND_WECHAT

class AccountNextNotifyEvent(BasicEvent):

    def event_account_next(self, account_number, order_id = None):
        userinfo = self.get_customer_info(account_number)
        content_tpl = self.get_content_template(NextNotify)
        if not content_tpl:
            return
        content = content_tpl.replace('{customer_name}', utils.safeunicode(userinfo.realname))
        content = content.replace('{product_name}', utils.safeunicode(userinfo.product_name))
        content = content.replace('{username}', account_number)
        content = content.replace('{expire_date}', userinfo.expire_date)
        params = {}
        params['phone'] = userinfo.mobile
        params['mobile'] = userinfo.mobile
        params['address'] = utils.safestr(userinfo.install_address)
        params['tplname'] = 'tr_renew_notify'
        params['gid'] = ''
        params['username'] = account_number
        params['customer'] = utils.safestr(userinfo.realname)
        params['product'] = utils.safestr(userinfo.product_name)
        params['expire'] = userinfo.expire_date
        dispatch.pub(EVENT_SEND_WECHAT, userinfo.wechat_oid, utils.safeunicode(content))
        dispatch.pub(EVENT_SENDSMS, userinfo.mobile, utils.safeunicode(content), **params)


def __call__(dbengine = None, mcache = None, **kwargs):
    return AccountNextNotifyEvent(dbengine=dbengine, mcache=mcache, **kwargs)