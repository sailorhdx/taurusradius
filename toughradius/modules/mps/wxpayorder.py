#!/usr/bin/env python
# coding=utf-8
import cyclone.sse
import cyclone.web
from toughradius.modules.mps.base import BaseHandler
from toughradius.modules.dbservice.customer_add import CustomerAdd
from toughradius.common import tools
from toughradius.modules import models
from toughradius.toughlib.btforms import rules
from toughradius.toughlib import logger
from toughradius.toughlib import utils
from toughradius.toughlib.storage import Storage
from toughradius.toughlib.permit import permit
from StringIO import StringIO
from decimal import Decimal as _d
from toughradius.modules.settings import PPMonth, PPTimes, BOMonth, BOTimes, PPFlow, BOFlows, PPMFlows, MAX_EXPIRE_DATE, order_wxpaycaache_key
import os
import json
import string
import decimal
import datetime

class WxBasicOrderHandler(BaseHandler):
    """
    用户开户订购套餐
    """

    def next_account_number(self, node_id):
        node = self.db.query(models.TrNode).get(node_id)
        rule = self.db.query(models.TrAccountRule).get(node.rule_id)
        rule.user_sn = rule.user_sn + 1
        self.db.commit()
        account_number = '%s%s' % (rule.user_prefix, string.rjust(str(rule.user_sn), rule.user_suffix_len, '0'))
        return account_number

    def calc_fee(self, product_id, months = 0, old_expire = None, charge_fee = 100):
        product = self.db.query(models.TrProduct).get(product_id)
        self_recharge_minfee = utils.yuan2fen(self.get_param_value('self_recharge_minfee', 100))
        fee_value, expire_date = (None, None)
        if product.product_policy in (PPTimes, PPFlow):
            fee_value = charge_fee or self_recharge_minfee
            expire_date = MAX_EXPIRE_DATE
        elif product.product_policy in (BOTimes, BOFlows):
            fee_value = utils.fen2yuan(product.fee_price)
            expire_date = MAX_EXPIRE_DATE
        elif product.product_policy == PPMonth:
            fee = decimal.Decimal(months) * decimal.Decimal(product.fee_price)
            fee_value = utils.fen2yuan(int(fee.to_integral_value()))
            start_expire = datetime.datetime.now()
            if old_expire:
                start_expire = datetime.datetime.strptime(old_expire, '%Y-%m-%d')
            expire_date = utils.add_months(start_expire, int(months), days=0)
            expire_date = expire_date.strftime('%Y-%m-%d')
        elif product.product_policy == BOMonth:
            start_expire = datetime.datetime.now()
            if old_expire:
                start_expire = datetime.datetime.strptime(old_expire, '%Y-%m-%d')
            fee_value = utils.fen2yuan(product.fee_price)
            expire_date = utils.add_months(start_expire, product.fee_months, days=0)
            expire_date = expire_date.strftime('%Y-%m-%d')
        elif product.product_policy == PPMFlows:
            fee = decimal.Decimal(months) * decimal.Decimal(product.fee_price)
            fee_value = utils.fen2yuan(int(fee.to_integral_value()))
            expire_date = MAX_EXPIRE_DATE
        return (fee_value, expire_date)


@permit.route('/mps/wxorder/new/(\w+)')

class WxpayNewOrderHandler(WxBasicOrderHandler):
    """
    用户开户订购套餐
    """

    def get(self, pid):
        openid = self.session.get('mps_openid', os.environ.get('DEV_OPEN_ID'))
        if not openid:
            cbk_param = urlencode({'cbk': '/mps/wxorder/new/%s' % pid})
            return self.redirect('/mps/oauth?%s' % cbk_param, permanent=False)
        product = self.db.query(models.TrProduct).filter_by(id=pid).first()
        if not product:
            return self.render('error.html', msg=u'资费不存在')
        mps_node_id = self.get_param_value('default_user_node_id', 1)
        return self.render('wxorder_form.html', node_id=mps_node_id, username=self.next_account_number(mps_node_id), product=product)

    def post(self, pid):
        try:
            openid = self.session.get('mps_openid', os.environ.get('DEV_OPEN_ID'))
            realname = self.get_argument('realname', '').strip()
            node_id = self.get_argument('node_id', '').strip()
            mobile = self.get_argument('mobile', '').strip()
            username = self.get_argument('username', '').strip()
            password = self.get_argument('password', '').strip()
            months = int(self.get_argument('months', '1'))
            wechat_bind = int(self.get_argument('wechat_bind', '0'))
            product = self.db.query(models.TrProduct).filter_by(id=pid).first()
            if not product:
                return self.render('error.html', msg=u'资费不存在')
            if not realname:
                return self.render('wxorder_form.html', product=product, msg=u'姓名不能为空', **self.get_params())
            if not rules.is_alphanum2(6, 16).valid(utils.safestr(username)):
                return self.render('wxorder_form.html', product=product, msg=u'用户名校验错误,必须是长度为6-16位的英文字符数字', **self.get_params())
            if not rules.is_alphanum2(6, 16).valid(password):
                return self.render('wxorder_form.html', product=product, msg=u'密码校验错误,必须是6-16为的英文字符数字', **self.get_params())
            if wechat_bind == 1 and self.db.query(models.TrCustomer).filter_by(wechat_oid=openid).count() > 0:
                return self.render('wxorder_form.html', product=product, msg=u'微信账号已绑定', **self.get_params())
            fee_value, expire_date = self.calc_fee(product.id, months=months, charge_fee=utils.fen2yuan(product.fee_price))
            order_id = tools.gen_num_id(16)
            formdata = Storage({'order_attach': 'neworder'})
            formdata['wxpay_body'] = u'套餐订购：%s' % product.product_name
            formdata['openid'] = openid
            formdata['order_id'] = order_id
            formdata['node_id'] = node_id
            formdata['area_id'] = ''
            formdata['realname'] = realname
            formdata['idcard'] = ''
            formdata['mobile'] = mobile
            formdata['address'] = ''
            formdata['account_number'] = username
            formdata['password'] = password
            formdata['ip_address'] = ''
            formdata['product_id'] = product.id
            formdata['agency_id'] = ''
            formdata['charge_code'] = ''
            formdata['months'] = months
            formdata['giftdays'] = 0
            formdata['giftflows'] = 0
            formdata['fee_value'] = fee_value
            formdata['expire_date'] = expire_date
            formdata['status'] = 1
            formdata['builder_name'] = ''
            formdata['customer_desc'] = u'客户微信自助开户'
            formdata['billing_type'] = 0
            formdata['accept_source'] = 'wechat'
            if wechat_bind == 1:
                formdata['wechat_oid'] = openid
            self.paycache.set(order_wxpaycaache_key(order_id), formdata, 28800)
            self.redirect('/mps/wxorder/pay/%s' % order_id)
        except Exception as err:
            logger.exception(err, trace='wechat')
            self.render('error.html', msg=u'套餐订购失败，请联系客服 %s' % repr(err))


@permit.route('/mps/wxorder/renew')

class WxpayRenewOrderHandler(WxBasicOrderHandler):
    """
    用户续费套餐
    """

    def get(self):
        openid = self.session.get('mps_openid', os.environ.get('DEV_OPEN_ID'))
        if not openid:
            cbk_param = urlencode({'cbk': '/mps/wxorder/renew'})
            return self.redirect('/mps/oauth?%s' % cbk_param, permanent=False)
        customer = self.db.query(models.TrCustomer).filter_by(wechat_oid=openid).first()
        if not customer:
            return self.redirect('/mps/userbind', permanent=False)
        account = self.db.query(models.TrAccount).filter_by(customer_id=customer.customer_id).first()
        product = self.db.query(models.TrProduct).filter_by(id=account.product_id).first()
        return self.render('wxrenew_order_form.html', account=account, product=product)

    def post(self):
        try:
            openid = self.session.get('mps_openid', os.environ.get('DEV_OPEN_ID'))
            customer = self.db.query(models.TrCustomer).filter_by(wechat_oid=openid).first()
            account = self.db.query(models.TrAccount).filter_by(customer_id=customer.customer_id).first()
            product = self.db.query(models.TrProduct).filter_by(id=account.product_id).first()
            months = int(self.get_argument('months', '1'))
            fee_value, expire_date = self.calc_fee(product.id, months=months, old_expire=account.expire_date)
            order_id = tools.gen_num_id(16)
            formdata = Storage({'order_attach': 'reneworder'})
            formdata['wxpay_body'] = u'套餐续费：%s' % product.product_name
            formdata['openid'] = openid
            formdata['account_number'] = account.account_number
            formdata['order_id'] = order_id
            formdata['product_id'] = account.product_id
            formdata['months'] = months
            formdata['fee_value'] = fee_value
            formdata['expire_date'] = expire_date
            formdata['accept_source'] = 'wechat'
            formdata['giftdays'] = 0
            formdata['operate_desc'] = u'用户微信支付续费'
            formdata['old_expire'] = account.expire_date
            self.paycache.set(order_wxpaycaache_key(order_id), formdata, 28800)
            self.redirect('/mps/wxorder/pay/%s' % order_id)
        except Exception as err:
            logger.exception(err, trace='wechat')
            self.render('error.html', msg=u'套餐续费失败，请联系客服 %s' % repr(err))


@permit.route('/mps/wxorder/recharge')

class WxpayRechargeOrderHandler(WxBasicOrderHandler):
    """ 用户充值
    """

    def get(self):
        openid = self.session.get('mps_openid', os.environ.get('DEV_OPEN_ID'))
        if not openid:
            cbk_param = urlencode({'cbk': '/mps/wxorder/recharge'})
            return self.redirect('/mps/oauth?%s' % cbk_param, permanent=False)
        customer = self.db.query(models.TrCustomer).filter_by(wechat_oid=openid).first()
        if not customer:
            return self.redirect('/mps/userbind', permanent=False)
        account = self.db.query(models.TrAccount).filter_by(customer_id=customer.customer_id).first()
        product = self.db.query(models.TrProduct).filter_by(id=account.product_id).first()
        return self.render('wxrecharge_order_form.html', account=account, product=product)

    def post(self):
        try:
            openid = self.session.get('mps_openid', os.environ.get('DEV_OPEN_ID'))
            customer = self.db.query(models.TrCustomer).filter_by(wechat_oid=openid).first()
            account = self.db.query(models.TrAccount).filter_by(customer_id=customer.customer_id).first()
            product = self.db.query(models.TrProduct).filter_by(id=account.product_id).first()
            fee_value = self.get_argument('fee_value', '')
            if not rules.is_rmb.valid(fee_value):
                return self.render('wxrecharge_order_form.html', account=account, product=product, msg=u'金额校验错误', **self.get_params())
            order_id = tools.gen_num_id(16)
            formdata = Storage({'order_attach': 'rechargeorder'})
            formdata['wxpay_body'] = u'套餐充值：%s' % product.product_name
            formdata['openid'] = openid
            formdata['order_id'] = order_id
            formdata['account_number'] = account.account_number
            formdata['product_id'] = account.product_id
            formdata['fee_value'] = fee_value
            formdata['accept_source'] = 'wechat'
            formdata['operate_desc'] = u'用户微信支付充值'
            self.paycache.set(order_wxpaycaache_key(order_id), formdata, 28800)
            self.redirect('/mps/wxorder/pay/%s' % order_id)
        except Exception as err:
            logger.exception(err, trace='wechat')
            self.render('error.html', msg=u'用户充值失败，请联系客服 %s' % repr(err))