#!/usr/bin/env python
# coding=utf-8
import datetime
import time
import os
import json
import decimal
import string
from hashlib import md5
from toughradius.toughlib import utils, logger
from toughradius.common import safefile
from toughradius.common import tools
from toughradius.common import smsapi
from twisted.internet import reactor, defer
from cyclone import httpclient
from toughradius.modules.ssportal.base import BaseHandler, authenticated
from toughradius.modules.ssportal import order_forms
from toughradius.toughlib.permit import permit
from toughradius.toughlib.storage import Storage
from toughradius.modules import models
from toughradius.modules.dbservice.customer_add import CustomerAdd
from toughradius.modules.settings import order_paycaache_key
from toughradius.modules.settings import PPMonth, PPTimes, BOMonth, BOTimes, PPFlow, BOFlows, PPMFlows, APMonth, MAX_EXPIRE_DATE
product_policys = {PPMonth: u'预付费包月',
 APMonth: u'后付费包月',
 PPTimes: u'预付费时长',
 BOMonth: u'买断包月',
 BOTimes: u'买断时长',
 PPFlow: u'预付费流量',
 BOFlows: u'买断流量'}

@permit.route('/ssportal/product')

class SSportalProductHandler(BaseHandler):

    def get(self):
        products = self.db.query(models.TrProduct).filter(models.TrProduct.product_policy.in_([BOMonth,
         BOFlows,
         BOTimes,
         PPMonth,
         PPTimes,
         PPFlow]), models.TrProduct.ispub == 1)
        self.render('product.html', products=products, policys=product_policys)


class BasicOrderHandler(BaseHandler):

    def gen_account_number(self):
        node_id = self.get_param_value('default_user_node_id', 1)
        node = self.db.query(models.TrNode).get(node_id)
        rule = self.db.query(models.TrAccountRule).get(node.rule_id)
        rule.user_sn = rule.user_sn + 1
        self.db.commit()
        account_number = '%s%s' % (rule.user_prefix, string.rjust(str(rule.user_sn), rule.user_suffix_len, '0'))
        return account_number

    def order_calc(self, product_id, old_expire = None, charge_fee = 100):
        months = int(self.get_argument('months', 0))
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


@permit.route('/ssportal/product/order')

class SSportalProductOrderHandler(BasicOrderHandler):
    """  支付宝支付第一步：进入订购表单，发起订购支付
    """

    def get_product_name(self, pid):
        return self.db.query(models.TrProduct.product_name).filter_by(id=pid).scalar()

    def get(self):
        product_id = self.get_argument('product_id')
        product = self.db.query(models.TrProduct).get(product_id)
        if not product:
            self.render_error(msg=u'套餐不存在')
            return
        account_number = self.get_argument('account_number', '')
        if account_number and self.db.query(models.TrAccount).get(account_number):
            form = order_forms.smsvcode_form(product_id, account_number)
            self.render('order_smsvcode_form.html', form=form, msg=u'手机号码已经注册')
            return
        smsvcode = self.get_argument('vcode', '')
        if account_number and not smsvcode:
            form = order_forms.smsvcode_form(product_id, account_number)
            self.render('order_smsvcode_form.html', form=form, msg=u'验证码不能为空')
            return
        if account_number and smsvcode and self.cache.get('ssportal.sms.vcode.{}'.format(account_number)) != smsvcode:
            form = order_forms.smsvcode_form(product_id, account_number)
            self.render('order_smsvcode_form.html', form=form, msg=u'验证码不匹配')
            return
        is_smsvcode = int(self.get_param_value('ssportal_smsvcode_required', 0))
        if not account_number and is_smsvcode:
            form = order_forms.smsvcode_form(product_id, '')
            self.render('order_smsvcode_form.html', form=form)
            return
        is_idcard = int(self.get_param_value('ssportal_idcard_required', 0))
        is_address = int(self.get_param_value('ssportal_address_required', 0))
        is_month = product.product_policy in (PPMonth, PPMFlows)
        account_number = account_number or self.gen_account_number()
        form = order_forms.order_form(is_month=is_month, is_idcard=is_idcard, is_address=is_address)
        form.product_id.set_value(product_id)
        form.product_name.set_value(product.product_name)
        form.months.set_value(product.fee_months)
        form.account_number.set_value(account_number)
        self.render('neworder_form.html', form=form, is_idcard=is_idcard)

    def do_vcard(self, form, product):
        vcard_code = form.d.vcard_code
        vcard_pwd = form.d.vcard_pwd
        _feevalue, _expire = self.order_calc(form.d.product_id)
        order_id = utils.gen_order_id()
        formdata = Storage(form.d)
        formdata.order_id = order_id
        formdata['node_id'] = self.get_param_value('default_user_node_id', 1)
        formdata['area_id'] = ''
        formdata['fee_value'] = _feevalue
        formdata['expire_date'] = _expire
        formdata['accept_source'] = 'ssportal'
        formdata['giftdays'] = 0
        formdata['giftflows'] = 0
        formdata['ip_address'] = ''
        formdata['status'] = 1
        formdata['vcard_code'] = vcard_code
        formdata['vcard_pwd'] = vcard_pwd
        formdata['customer_desc'] = u'客户自助充值卡开户'
        formdata['product_name'] = product.product_name
        manager = CustomerAdd(self.db, self.aes)
        ret = manager.add(formdata)
        if ret:
            order = self.db.query(models.TrCustomerOrder).get(order_id)
            logger.info(u'充值卡开户成功')
            self.render('alipay_return.html', order=order)
        else:
            return self.render_error(code=1, msg=u'充值卡订单处理失败 %s' % manager.last_error)

    def post(self):
        try:
            product_id = self.get_argument('product_id', '')
            product = self.db.query(models.TrProduct).get(product_id)
            if not product:
                return self.render('neworder_form.html', form=form, msg=u'套餐不存在')
            is_idcard = int(self.get_param_value('ssportal_idcard_required', 0))
            is_address = int(self.get_param_value('ssportal_address_required', 0))
            is_month = product.product_policy in (PPMonth, PPMFlows)
            form = order_forms.order_form(is_month=is_month, is_idcard=is_idcard, is_address=is_address)
            if not form.validates(source=self.get_params()):
                return self.render('neworder_form.html', form=form, msg=form.errors)
            account_count = self.db.query(models.TrCustomer).filter_by(email=form.d.email).count()
            if account_count > 0:
                return self.render('neworder_form.html', form=form, msg=u'电子邮件已经存在')
            if form.d.vcard_code and form.d.vcard_pwd:
                return self.do_vcard(form, product)
            _feevalue, _expire = self.order_calc(form.d.product_id, charge_fee=utils.fen2yuan(product.fee_price))
            order_id = utils.gen_order_id()
            formdata = Storage(form.d)
            formdata.order_id = order_id
            formdata['node_id'] = self.get_param_value('default_user_node_id', 1)
            formdata['area_id'] = ''
            formdata['fee_value'] = _feevalue
            formdata['expire_date'] = _expire
            formdata['accept_source'] = 'ssportal'
            formdata['giftdays'] = 0
            formdata['giftflows'] = 0
            formdata['ip_address'] = ''
            formdata['status'] = 1
            formdata['customer_desc'] = u'客户自助开户'
            formdata['product_name'] = product.product_name
            self.paycache.set(order_paycaache_key(order_id), formdata)
            return self.render('order_alipay.html', formdata=formdata)
        except Exception as err:
            logger.exception(err)
            return self.render('neworder_form.html', form=form, msg=u'无效的订单')


@permit.route('/ssportal/product/order/alipay')

class SSportalProductOrderHandler(BaseHandler):
    """ 支付宝支付第二步： 支付信息确认，跳转支付宝
    """

    def post(self):
        order_id = self.get_argument('order_id')
        formdata = self.paycache.get(order_paycaache_key(order_id))
        product_name = self.db.query(models.TrProduct.product_name).filter_by(id=formdata.product_id).scalar()
        self.redirect(self.alipay.create_direct_pay_by_user(order_id, product_name, product_name, formdata.fee_value, notify_path='/ssportal/alipay/verify/new', return_path='/ssportal/alipay/verify/new'))


@permit.suproute('/ssportal/idcard/upload/(\w+)')

class ParamUploadHandler(BaseHandler):

    def post(self, username):
        try:
            f = self.request.files['Filedata'][0]
            filename = os.path.basename(f['filename'])
            fsname = self.get_argument('fsname')
            savename = '{0}.{1}.{2}'.format(username, fsname, filename)
            if fsname not in ('IDCARD1', 'IDCARD2'):
                self.write(u'文件名错误')
                return
            default_dir = '/var/toughee/userfs'
            if not os.path.exists(default_dir):
                os.makedirs(default_dir)
            save_path = os.path.join(self.settings.config.admin.get('userfs', default_dir), savename)
            tf = open(save_path, 'wb')
            tf.write(f['body'])
            tf.close()
            if not safefile.isimg(save_path):
                os.remove(save_path)
                logger.error('error upload file %s' % save_path)
                self.write(u'上传的文件不是图片类型')
                return
            attr = self.db.query(models.TrAccountAttr).filter_by(account_number=username, attr_name='fsname').first()
            if not attr:
                attr = models.TrAccountAttr()
                attr.id = tools.gen_num_id(16)
                attr.account_number = username
                attr.attr_type = 0
                attr.attr_name = fsname
                attr.attr_value = save_path
                attr.attr_desc = u'用户身份证图片-%s' % fsname
                attr.sync_ver = tools.gen_sync_ver()
                self.db.add(attr)
            else:
                attr.attr_value = save_path
                attr.sync_ver = tools.gen_sync_ver()
            self.db.commit()
            logger.info('write {0}'.format(save_path))
            self.write(u'upload ok')
        except Exception as err:
            logger.error(err)
            self.write(u'上传失败 %s' % utils.safeunicode(err))


@permit.route('/ssportal/sms/sendvcode')

class SendSmsVcodeHandler(BaseHandler):

    @defer.inlineCallbacks
    def get(self):
        yield self.post()

    @defer.inlineCallbacks
    def post(self):
        try:
            phone = self.get_argument('phone')
            last_send = self.session.get('sms_last_send', 0)
            if last_send > 0:
                sec = int(time.time()) - last_send
                if sec < 60:
                    self.render_json(code=1, msg=u'还需等待%s秒' % sec)
                    return
            self.session['sms_last_send'] = int(time.time())
            self.session.save()
            vcode = str(time.time()).replace('.', '')[-6:]
            self.cache.set('ssportal.sms.vcode.{}'.format(phone), vcode, expire=300)
            gateway = self.get_param_value('sms_gateway')
            apikey = self.get_param_value('sms_api_user')
            apisecret = self.get_param_value('sms_api_pwd')
            resp = yield smsapi.send_vcode(gateway, apikey, apisecret, phone, vcode)
            self.render_json(code=0, msg='ok')
        except Exception as err:
            logger.exception(err)
            self.render_json(code=1, msg=u'发送短信失败')