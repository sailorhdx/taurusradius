#!/usr/bin/env python
# coding=utf-8
import time
import json
import base64
from urllib import urlencode
from toughradius.toughlib import apiutils
from toughradius.toughlib import logger
from toughradius.toughlib import utils
from toughradius.toughlib.btforms import rules
from cyclone import httpclient
from twisted.internet import defer
from hashlib import md5

class SmsApi(object):

    def __init__(self):
        self.gateways = {'toughcloud': 'https://www.toughcloud.net/api/v1',
         'smscn': 'http://api.sms.cn/mt'}
        self.vcode_calls = {'toughcloud': self.send_toughcloud_sms_vcode}
        self.sms_calls = {'toughcloud': self.send_toughcloud_sms,
         'smscn': self.send_smscn_sms}

    def send_vcode(self, gateway, apikey, apisecret, sendphone, vcode):
        """ 发送验证码
        """
        if gateway not in self.gateways:
            raise ValueError(u'gateway [%s] not support' % gateway)
        if not rules.is_mobile.valid(sendphone):
            raise ValueError(u'sendsms: %s mobile format error' % sendphone)
        apiurl = self.gateways[gateway]
        return self.vcode_calls[gateway](apiurl, apikey, apisecret, sendphone, vcode)

    def send_sms(self, gateway, apikey, apisecret, sendphone, content, **params):
        """ 发送一般短信
        """
        if gateway not in self.gateways:
            raise ValueError(u'gateway [%s] not support' % gateway)
        if not rules.is_mobile.valid(sendphone):
            raise ValueError(u'sendsms: %s mobile format error' % sendphone)
        apiurl = self.gateways[gateway]
        d = self.sms_calls[gateway](apiurl, apikey, apisecret, sendphone, content, **params)
        d.addErrback(logger.exception, trace='event')

    @defer.inlineCallbacks
    def send_toughcloud_sms_vcode(self, apiurl, apikey, apisecret, sendphone, vcode):
        """ send toughcloud sms vcode
        """
        smsapiurl = '{0}/sms/vcode'.format(apiurl)
        params = dict(apikey=apikey, phone=sendphone, vcode=vcode, timestamp=int(time.time()))
        params['sign'] = apiutils.make_sign(apisecret, params.values())

        postdata = urlencode(params)
        logger.info(smsapiurl + '?' + postdata, trace='event')
        resp = yield httpclient.fetch(smsapiurl, postdata=postdata)
        ret = json.loads(resp.body)
        if ret['code'] > 0:
            raise ValueError(utils.safeunicode(ret['msg']))
        logger.info(u'发送短信验证码成功 {0}-{1}'.format(sendphone, vcode))
        defer.returnValue(ret)

    @defer.inlineCallbacks
    def send_toughcloud_sms(self, apiurl, apikey, apisecret, sendphone, content, **params):
        """ send toughcloud sms
        """
        smsapiurl = '{0}/toughee/sendsms'.format(apiurl)
        params['apikey'] = apikey
        params['phone'] = sendphone
        params['timestamp'] = int(time.time())
        params['sign'] = apiutils.make_sign(apisecret, params.values())
        postdata = urlencode(params)
        logger.info(smsapiurl + '?' + postdata, trace='event')
        resp = yield httpclient.fetch(smsapiurl, postdata=postdata)
        ret = json.loads(resp.body)
        if ret['code'] > 0:
            raise ValueError(ret)
        logger.info(u'发送短信成功 {0}'.format(sendphone))
        defer.returnValue(ret)

    @defer.inlineCallbacks
    def send_smscn_sms(self, apiurl, apikey, apisecret, sendphone, content, **params):
        """ send sms.cn sms
        """
        smspwd = md5(utils.safestr('%s%s' % (apisecret, apikey))).hexdigest()
        _params = dict(uid=utils.safestr(apikey), pwd=smspwd, mobile=utils.safestr(sendphone), content=content.encode('gbk'), mobileids='', encode='gbk')
        sms_api_url = '%s?%s' % (apiurl, urlencode(_params))
        logger.info(u'send smscn sms: %s ' % sms_api_url, trace='event')
        headrs = {'Content-Type': 'text/html;charset=gbk'}
        resp = yield httpclient.fetch(sms_api_url, headrs=headrs, followRedirect=True)
        _body = utils.safeunicode(resp.body)
        logger.info(u'smscn 短信发送响应; %s %s' % (_body, sms_api_url), trace='event')
        defer.returnValue({'code': 0,
         'msg': 'ok'})


_smsapi = SmsApi()
send_vcode = _smsapi.send_vcode
send_sms = _smsapi.send_sms