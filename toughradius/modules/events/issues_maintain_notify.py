#!/usr/bin/env python
# coding=utf-8
from toughradius.toughlib import utils, dispatch
from toughradius.toughlib import logger
from toughradius.modules import models
from toughradius.modules.events.event_basic import BasicEvent
from toughradius.modules.settings import MaintainNotify
from toughradius.modules.events.settings import EVENT_SENDSMS, EVENT_SENDMAIL, EVENT_SEND_WECHAT

class IssuesMaintainNotifyEvent(BasicEvent):

    def event_service_maintain(self, account_number, builder_phone = None, wechat_oid = None):
        userinfo = self.get_customer_info(account_number)
        content_tpl = self.get_content_template(MaintainNotify)
        if not content_tpl or not userinfo.mobile:
            return
        content = content_tpl.replace('{customer_name}', utils.safeunicode(userinfo.realname))
        content = content.replace('{product_name}', utils.safeunicode(userinfo.product_name))
        content = content.replace('{username}', account_number)
        content = content.replace('{mobile}', userinfo.mobile)
        content = content.replace('{install_address}', userinfo.install_address)
        params = {}
        params['phone'] = builder_phone
        params['mobile'] = userinfo.mobile
        params['address'] = utils.safestr(userinfo.install_address)
        params['tplname'] = 'tr_gd_notify'
        params['gid'] = ''
        params['username'] = account_number
        params['customer'] = utils.safestr(userinfo.realname)
        params['product'] = utils.safestr(userinfo.product_name)
        params['expire'] = userinfo.expire_date
        dispatch.pub(EVENT_SEND_WECHAT, wechat_oid, utils.safeunicode(content))
        dispatch.pub(EVENT_SENDSMS, builder_phone, utils.safeunicode(content), **params)


def __call__(dbengine = None, mcache = None, **kwargs):
    return IssuesMaintainNotifyEvent(dbengine=dbengine, mcache=mcache, **kwargs)