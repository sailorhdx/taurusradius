#!/usr/bin/env python
# coding=utf-8
import datetime
from toughradius.modules.settings import *
from toughradius.toughlib import redis_cache
from hashlib import md5
from toughradius.modules import models
from toughradius.toughlib import utils, dispatch, logger
from toughradius.modules.dbservice import BaseService
from toughradius.modules.dbservice import logparams
from toughradius.common import tools
from toughradius.modules.events.settings import DBSYNC_STATUS_ADD

class ProductService(BaseService):

    def add_attr(self, pid, attr_name, attr_value, attr_desc, attr_type = 0):
        attr = models.TrProductAttr()
        attr.id = utils.get_uuid()
        attr.product_id = pid
        attr.attr_type = attr_type
        attr.attr_name = attr_name
        attr.attr_value = attr_value
        attr.attr_desc = attr_desc
        attr.sync_ver = tools.gen_sync_ver()
        self.db.add(attr)

    def update_attr(self, pid, attr_name, attr_value, attr_type = 0):
        self.db.query(models.TrProductAttr).filter_by(product_id=pid, attr_name=attr_name).update({'attr_value': attr_value,
         'attr_type': attr_type})

    @logparams
    def add_ppmf(self, formdata, **kwargs):
        """ 新增流量包月资费
        """
        try:
            product = models.TrProduct()
            product.id = utils.get_uuid()
            product.product_name = formdata.product_name
            product.ispub = formdata.get('ispub', 0)
            product.product_policy = PPMFlows
            product.product_status = 0
            product.fee_months = 1
            product.fee_times = 0
            product.fee_flows = utils.gb2kb(formdata.get('fee_flows', 0))
            product.bind_mac = formdata.bind_mac
            product.bind_vlan = formdata.bind_vlan
            product.concur_number = formdata.concur_number
            product.fee_price = utils.yuan2fen(formdata.fee_price)
            product.fee_period = ''
            product.input_max_limit = utils.mbps2bps(formdata.input_max_limit)
            product.output_max_limit = utils.mbps2bps(formdata.output_max_limit)
            product.free_auth = formdata.free_auth
            product.free_auth_uprate = utils.mbps2bps(formdata.free_auth_uprate or 0)
            product.free_auth_downrate = utils.mbps2bps(formdata.free_auth_downrate or 0)
            _datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            product.create_time = _datetime
            product.update_time = _datetime
            product.sync_ver = tools.gen_sync_ver()
            self.db.add(product)
            opsdesc = u'新增资费信息:%s' % utils.safeunicode(product.product_name)
            self.add_oplog(opsdesc)
            self.add_attr(product.id, 'flow_price', formdata.get('flow_price', 0), u'流量充值单价(元)')
            self.add_attr(product.id, 'max_giftflows', formdata.get('max_giftflows', 0), u'最大赠送流量值(G)')
            self.add_attr(product.id, 'max_giftdays', formdata.get('max_giftdays', 0), u'最大赠送天数')
            self.db.commit()
            return product
        except Exception as err:
            self.db.rollback()
            logger.exception(err, tag='product_add_error')
            self.last_error = u'操作失败:%s' % utils.safeunicode(err)
            return False

    @logparams
    def update_ppmf(self, formdata, **kwargs):
        """ 修改流量包月资费
        """
        try:
            product = self.db.query(models.TrProduct).get(formdata.id)
            product.product_name = formdata.product_name
            product.ispub = formdata.get('ispub', 0)
            product.product_status = formdata.product_status
            product.fee_flows = utils.gb2kb(formdata.get('fee_flows', 0))
            product.bind_mac = formdata.bind_mac
            product.bind_vlan = formdata.bind_vlan
            product.concur_number = formdata.concur_number
            product.fee_period = ''
            product.fee_price = utils.yuan2fen(formdata.fee_price)
            product.input_max_limit = utils.mbps2bps(formdata.input_max_limit)
            product.output_max_limit = utils.mbps2bps(formdata.output_max_limit)
            product.free_auth = formdata.free_auth
            product.free_auth_uprate = utils.mbps2bps(formdata.free_auth_uprate or 0)
            product.free_auth_downrate = utils.mbps2bps(formdata.free_auth_downrate or 0)
            product.update_time = utils.get_currtime()
            product.sync_ver = tools.gen_sync_ver()
            opsdesc = u'修改资费信息:%s' % utils.safeunicode(product.product_name)
            self.add_oplog(opsdesc)
            self.update_attr(product.id, 'flow_price', formdata.get('flow_price', 0))
            self.update_attr(product.id, 'max_giftflows', formdata.get('max_giftflows', 0))
            self.update_attr(product.id, 'max_giftdays', formdata.get('max_giftdays', 0))
            self.db.commit()
            dispatch.pub(redis_cache.CACHE_DELETE_EVENT, product_cache_key(product.id), async=True)
            dispatch.pub(redis_cache.CACHE_DELETE_EVENT, product_attrs_cache_key(product.id), async=True)
            return product
        except Exception as err:
            self.db.rollback()
            logger.exception(err, tag='product_update_error')
            self.last_error = u'操作失败:%s' % utils.safeunicode(err)
            return False

    @logparams
    def add(self, formdata, **kwargs):
        try:
            product = models.TrProduct()
            product.id = formdata.product_id if 'product_id' in formdata else utils.get_uuid()
            product.product_name = formdata.product_name
            product.ispub = formdata.get('ispub', 0)
            product.product_policy = formdata.product_policy
            product.product_status = 0
            product.fee_months = int(formdata.get('fee_months', 0))
            product.fee_times = utils.hour2sec(formdata.get('fee_times', 0))
            product.fee_flows = utils.gb2kb(formdata.get('fee_flows', 0))
            product.bind_mac = formdata.bind_mac
            product.bind_vlan = formdata.bind_vlan
            product.concur_number = formdata.concur_number
            product.fee_price = utils.yuan2fen(formdata.fee_price)
            product.fee_period = ''
            product.input_max_limit = utils.mbps2bps(formdata.input_max_limit)
            product.output_max_limit = utils.mbps2bps(formdata.output_max_limit)
            product.free_auth = formdata.free_auth
            product.free_auth_uprate = utils.mbps2bps(formdata.free_auth_uprate or 0)
            product.free_auth_downrate = utils.mbps2bps(formdata.free_auth_downrate or 0)
            _datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            product.create_time = _datetime
            product.update_time = _datetime
            product.sync_ver = tools.gen_sync_ver()
            self.db.add(product)
            opsdesc = u'新增资费信息:%s' % utils.safeunicode(product.product_name)
            self.add_oplog(opsdesc)
            for charge_code in kwargs.get('item_charges', []):
                pcharges = models.TrProductCharges()
                pcharges.charge_code = charge_code
                pcharges.product_id = product.id
                pcharges.sync_ver = tools.gen_sync_ver()
                self.db.add(pcharges)

            self.add_attr(product.id, 'flow_price', formdata.get('flow_price', 0), u'流量充值单价(元)')
            self.add_attr(product.id, 'max_giftflows', formdata.get('max_giftflows', 0), u'最大赠送流量值(G)')
            self.add_attr(product.id, 'max_giftdays', formdata.get('max_giftdays', 0), u'最大赠送天数')
            if 'bandwidthCode' in formdata:
                self.add_attr(product.id, 'limit_rate_code', formdata.get('bandwidthCode'), '资费扩展限速标识')
            self.db.commit()
            return product
        except Exception as err:
            self.db.rollback()
            logger.exception(err, tag='product_add_error')
            self.last_error = u'操作失败:%s' % utils.safeunicode(err)
            return False

    @logparams
    def update(self, formdata, **kwargs):
        try:
            product = self.db.query(models.TrProduct).get(formdata.id)
            product.product_name = formdata.product_name
            product.ispub = formdata.get('ispub', 0)
            product.product_status = formdata.product_status
            product.fee_months = int(formdata.get('fee_months', 0))
            product.fee_times = utils.hour2sec(formdata.get('fee_times', 0))
            product.fee_flows = utils.gb2kb(formdata.get('fee_flows', 0))
            product.bind_mac = formdata.bind_mac
            product.bind_vlan = formdata.bind_vlan
            product.concur_number = formdata.concur_number
            product.fee_period = ''
            product.fee_price = utils.yuan2fen(formdata.fee_price)
            product.input_max_limit = utils.mbps2bps(formdata.input_max_limit)
            product.output_max_limit = utils.mbps2bps(formdata.output_max_limit)
            product.free_auth = formdata.free_auth
            product.free_auth_uprate = utils.mbps2bps(formdata.free_auth_uprate or 0)
            product.free_auth_downrate = utils.mbps2bps(formdata.free_auth_downrate or 0)
            product.update_time = utils.get_currtime()
            product.sync_ver = tools.gen_sync_ver()
            opsdesc = u'修改资费信息:%s' % utils.safeunicode(product.product_name)
            self.add_oplog(opsdesc)
            self.db.query(models.TrProductCharges).filter_by(product_id=product.id).delete()
            for charge_code in kwargs.get('item_charges', []):
                pcharges = models.TrProductCharges()
                pcharges.charge_code = charge_code
                pcharges.product_id = product.id
                pcharges.sync_ver = tools.gen_sync_ver()
                self.db.add(pcharges)

            self.update_attr(product.id, 'flow_price', formdata.get('flow_price', 0))
            self.update_attr(product.id, 'max_giftflows', formdata.get('max_giftflows', 0))
            self.update_attr(product.id, 'max_giftdays', formdata.get('max_giftdays', 0))
            if 'bandwidthCode' in formdata:
                self.update_attr(product.id, 'limit_rate_code', formdata.get('bandwidthCode'))
            self.db.commit()
            dispatch.pub(redis_cache.CACHE_DELETE_EVENT, product_cache_key(product.id), async=True)
            dispatch.pub(redis_cache.CACHE_DELETE_EVENT, product_attrs_cache_key(product.id), async=True)
            return product
        except Exception as err:
            self.db.rollback()
            logger.exception(err, tag='product_update_error')
            self.last_error = u'操作失败:%s' % utils.safeunicode(err)
            return False

    @logparams
    def delete(self, product_id, **kwargs):
        try:
            if self.db.query(models.TrAccount).filter_by(product_id=product_id).count() > 0:
                raise Exception(u'该套餐有用户使用，不允许删除')
            self.db.query(models.TrProduct).filter_by(id=product_id).delete()
            self.db.query(models.TrProductCharges).filter_by(product_id=product_id).delete()
            self.db.query(models.TrProductAttr).filter_by(product_id=product_id).delete()
            opsdesc = u'删除资费信息:%s' % product_id
            self.add_oplog(opsdesc)
            self.db.commit()
            dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrProduct.__tablename__, dict(id=product_id)), async=True)
            dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrProductCharges.__tablename__, dict(product_id=product_id)), async=True)
            dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrProductAttr.__tablename__, dict(product_id=product_id)), async=True)
            dispatch.pub(redis_cache.CACHE_DELETE_EVENT, product_cache_key(product_id), async=True)
            dispatch.pub(redis_cache.CACHE_DELETE_EVENT, product_attrs_cache_key(product_id), async=True)
            return True
        except Exception as err:
            self.db.rollback()
            logger.exception(err, tag='product_delete_error')
            self.last_error = u'操作失败:%s' % utils.safeunicode(err)
            return False