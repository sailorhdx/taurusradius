#!/usr/bin/env python
# coding=utf-8
from toughradius.toughlib import utils, dispatch
from toughradius.modules.events.event_basic import BasicEvent
from toughradius.modules.settings import ExpireNotify
from toughradius.modules.events.settings import EVENT_SENDSMS, EVENT_SENDMAIL, EVENT_SEND_WECHAT

class AccountExpireNotifyEvent(BasicEvent):

    def get_content(self, account_number):
        userinfo = self.get_customer_info(account_number)
        content_tpl = self.get_content_template(ExpireNotify)
        if not content_tpl:
            return (userinfo, '')
        content = content_tpl.replace('{customer_name}', utils.safeunicode(userinfo.realname))
        content = content.replace('{product_name}', utils.safeunicode(userinfo.product_name))
        content = content.replace('{username}', account_number)
        content = content.replace('{mobile}', userinfo.mobile)
        content = content.replace('{expire_date}', userinfo.expire_date)
        return (userinfo, content)

    def event_wechat_account_expire(self, account_number):
        userinfo, content = self.get_content(account_number)
        if content:
            dispatch.pub(EVENT_SEND_WECHAT, userinfo.wechat_oid, utils.safeunicode(content))

    def event_sms_account_expire(self, account_number):
        userinfo, content = self.get_content(account_number)
        params = {}
        params['phone'] = userinfo.mobile
        params['mobile'] = userinfo.mobile
        params['address'] = utils.safestr(userinfo.install_address)
        params['tplname'] = 'tr_expire_notify'
        params['gid'] = ''
        params['username'] = account_number
        params['customer'] = utils.safestr(userinfo.realname)
        params['product'] = utils.safestr(userinfo.product_name)
        params['expire'] = userinfo.expire_date
        dispatch.pub(EVENT_SENDSMS, userinfo.mobile, utils.safeunicode(content), **params)

    def event_mail_account_expire(self, account_number):
        userinfo, content = self.get_content(account_number)
        if content:
            dispatch.pub(EVENT_SENDMAIL, userinfo.email, u'用户到期通知邮件', utils.safeunicode(content))


def __call__(dbengine = None, mcache = None, **kwargs):
    return AccountExpireNotifyEvent(dbengine=dbengine, mcache=mcache, **kwargs)