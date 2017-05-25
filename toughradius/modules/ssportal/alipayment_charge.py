#!/usr/bin/env python
# coding=utf-8
import datetime
import time
import json
import decimal
import string
import base64
from hashlib import md5
from toughradius.toughlib import utils, logger
from toughradius.modules.ssportal.base import BaseHandler, authenticated
from toughradius.modules.ssportal import order_forms
from toughradius.modules.ssportal import alipayment_new
from toughradius.toughlib.permit import permit
from toughradius.toughlib.storage import Storage
from toughradius.modules import models
from toughradius.common import tools
from toughradius.modules.dbservice.account_charge import AccountCharge
from toughradius.modules.settings import order_paycaache_key
from toughradius.modules.settings import PPMonth, PPTimes, BOMonth, BOTimes, PPFlow, BOFlows, PPMFlows, MAX_EXPIRE_DATE

@permit.route('/ssportal/product/charge')

class SSportalChargeOrderHandler(alipayment_new.BasicOrderHandler):
    """ 发起续费支付
    """

    def get_expire_date(self, expire):
        if utils.is_expire(expire):
            return utils.get_currdate()
        else:
            return expire

    @authenticated
    def get(self):
        account_number = self.current_user.username
        account = self.db.query(models.TrAccount).get(account_number)
        product_id = account.product_id
        product = self.db.query(models.TrProduct).get(product_id)
        if not product:
            return self.render_alert(u'错误提示', u'套餐不存在')
        form = order_forms.charge_form()
        form.account_number.set_value(account_number)
        form.product_id.set_value(product_id)
        form.product_name.set_value(product.product_name)
        form.fee_value.set_value(0)
        self.render('charge_modal_form.html', form=form)

    def post(self):
        form = order_forms.charge_form()
        if not form.validates(source=self.get_params()):
            return self.render_json(code=1, msg=form.errors)
        account = self.db.query(models.TrAccount).get(form.d.account_number)
        if not account:
            return self.render_json(code=1, msg=u'账号不存在')
        try:
            order_id = utils.gen_order_id()
            formdata = Storage(form.d)
            formdata['order_id'] = order_id
            formdata['product_id'] = account.product_id
            formdata['fee_value'] = form.d.fee_value
            formdata['accept_source'] = 'ssportal'
            formdata['operate_desc'] = u'用户自助充值'
            self.paycache.set(order_paycaache_key(order_id), formdata)
            self.render_json(code=0, msg=u'订单创建成功', order_id=order_id)
        except Exception as err:
            logger.exception(err)
            return self.render_json(code=0, msg=u'无效的订单')


@permit.route('/ssportal/product/charge/alipay')

class SSportalProductRenewHandler(BaseHandler):
    """ 支付信息确认，跳转支付宝
    """

    def get_product_name(self, pid):
        return self.db.query(models.TrProduct.product_name).filter_by(id=pid).scalar()

    @authenticated
    def get(self):
        order_id = self.get_argument('order_id', '')
        if not order_id:
            return self.render_error(code=1, msg=u'订单不存在')
        formdata = self.paycache.get(order_paycaache_key(order_id))
        if not formdata:
            return self.render_error(code=1, msg=u'订单已过期')
        try:
            formdata.order_id = order_id
            temp_acurl = self.session.get('temp_acurl', '')
            acip = self.session.get('temp_acip', '')
            userip = self.session.get('temp_userip', '')
            nas = self.db.query(models.TrBas).filter_by(ip_addr=acip).first()
            ac_temp_auth_url = ''
            if temp_acurl and nas:
                _user = formdata.account_number
                _timestemp = str(int(time.time()))
                _action = 'temp'
                _userip = base64.b64encode(userip)
                _acip = base64.b64encode(acip)
                signstr = _user + _userip + _timestemp + _action + str(nas.bas_secret) + _acip
                logger.debug('signstr = ' + signstr)
                _sign = md5(signstr).hexdigest()
                logger.info('sign = ' + _sign)
                url_param = 'user={1}&ip={2}&timestemp={3}&action=temp&acip={4}&sign={5}'.format(temp_acurl, _user, _userip, _timestemp, _acip, _sign)
                ac_temp_auth_url = temp_acurl + '?' + url_param
            self.render('charge_alipay.html', formdata=formdata, ac_temp_auth_url=ac_temp_auth_url)
        except Exception as err:
            self.db.rollback()
            logger.exception(err)
            self.render_error(msg=u'订单处理错误，请联系管理员')

    @authenticated
    def post(self):
        order_id = self.get_argument('order_id')
        formdata = self.paycache.get(order_paycaache_key(order_id))
        product_name = self.get_product_name(formdata.product_id)
        self.redirect(self.alipay.create_direct_pay_by_user(order_id, u'账号充值：%s' % product_name, product_name, formdata.fee_value, notify_path='/ssportal/alipay/verify/charge', return_path='/ssportal/alipay/verify/charge'))