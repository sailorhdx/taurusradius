#!/usr/bin/env python
# coding=utf-8
import cyclone.auth
import cyclone.escape
import cyclone.web
import time
from toughradius.modules import models
from toughradius.modules.base import BaseHandler, authenticated
from toughradius.modules.resource import bas_forms
from toughradius.toughlib.permit import permit
from toughradius.toughlib import utils, dispatch
from toughradius.toughlib import redis_cache
from toughradius.modules.settings import *
from toughradius.modules.events.settings import DBSYNC_STATUS_ADD
from toughradius.common import tools

@permit.suproute('/admin/bas', u'接入设备管理', MenuRes, order=2.0, is_menu=True)

class BasListHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render('bas_list.html', bastype=bas_forms.bastype, bas_list=self.db.query(models.TrBas))


@permit.suproute('/admin/bas/add', u'新增接入设备', MenuRes, order=2.0001)

class BasAddHandler(BaseHandler):

    @authenticated
    def get(self):
        nodes = [ (n.id, n.node_name) for n in self.get_opr_nodes() ]
        form = bas_forms.bas_add_form(nodes)
        form.portal_vendor.set_value('0')
        form.coa_port.set_value(3799)
        form.ac_port.set_value(2000)
        self.render('base_form.html', form=form)

    @authenticated
    def post(self):
        nodes = [ (n.id, n.node_name) for n in self.get_opr_nodes() ]
        form = bas_forms.bas_add_form(nodes)
        if not form.validates(source=self.get_params()):
            return self.render('base_form.html', form=form)
        if not form.d.ip_addr:
            return self.render('base_form.html', form=form, msg=u'ip地址必须填写')
        if self.db.query(models.TrBas.id).filter_by(ip_addr=form.d.ip_addr).count() > 0:
            return self.render('base_form.html', form=form, msg=u'接入设备地址已经存在')
        bas = models.TrBas()
        bas.id = utils.get_uuid()
        bas.ip_addr = form.d.ip_addr
        bas.dns_name = ''
        bas.bas_name = form.d.bas_name
        bas.nas_id = form.d.nas_id
        bas.time_type = form.d.time_type
        bas.vendor_id = form.d.vendor_id
        bas.portal_vendor = form.d.portal_vendor
        bas.bas_secret = form.d.bas_secret
        bas.coa_port = form.d.coa_port
        bas.sync_ver = tools.gen_sync_ver()
        self.db.add(bas)
        self.db.flush()
        self.db.refresh(bas)
        for node_id in self.get_arguments('nodes'):
            basnode = models.TrBasNode()
            basnode.bas_id = bas.id
            basnode.node_id = node_id
            basnode.sync_ver = tools.gen_sync_ver()
            self.db.add(basnode)

        self.add_oplog(u'新增接入设备信息:%s' % bas.ip_addr)
        self.db.commit()
        self.redirect('/admin/bas', permanent=False)


@permit.suproute('/admin/bas/update', u'修改接入设备', MenuRes, order=2.0002)

class BasUpdateHandler(BaseHandler):

    @authenticated
    def get(self):
        bas_id = self.get_argument('bas_id')
        nodes = [ (n.id, n.node_name) for n in self.get_opr_nodes() ]
        basnodes = [ bn.node_id for bn in self.db.query(models.TrBasNode).filter_by(bas_id=bas_id) ]
        form = bas_forms.bas_update_form(nodes)
        form.fill(self.db.query(models.TrBas).get(bas_id))
        form.nodes.set_value(basnodes)
        self.render('base_form.html', form=form)

    @authenticated
    def post(self):
        nodes = [ (n.id, n.node_name) for n in self.get_opr_nodes() ]
        form = bas_forms.bas_update_form(nodes)
        if not form.validates(source=self.get_params()):
            return self.render('base_form.html', form=form)
        bas = self.db.query(models.TrBas).get(form.d.id)
        bas.ip_addr = form.d.ip_addr
        bas.dns_name = ''
        bas.bas_name = form.d.bas_name
        bas.nas_id = form.d.nas_id
        bas.time_type = form.d.time_type
        bas.vendor_id = form.d.vendor_id
        bas.portal_vendor = form.d.portal_vendor
        bas.bas_secret = form.d.bas_secret
        bas.coa_port = form.d.coa_port
        bas.sync_ver = tools.gen_sync_ver()
        self.db.query(models.TrBasNode).filter_by(bas_id=bas.id).delete()
        for node_id in self.get_arguments('nodes'):
            basnode = models.TrBasNode()
            basnode.bas_id = bas.id
            basnode.node_id = node_id
            basnode.sync_ver = tools.gen_sync_ver()
            self.db.add(basnode)

        self.add_oplog(u'修改接入设备信息:%s' % bas.ip_addr)
        self.db.commit()
        dispatch.pub(redis_cache.CACHE_DELETE_EVENT, bas_cache_key(bas.ip_addr), async=True)
        self.redirect('/admin/bas', permanent=False)


@permit.suproute('/admin/bas/delete', u'删除接入设备', MenuRes, order=2.0003)

class BasDeleteHandler(BaseHandler):

    @authenticated
    def get(self):
        bas_id = self.get_argument('bas_id')
        bas_ip = self.db.query(models.TrBas.ip_addr).filter_by(id=bas_id).scalar()
        self.db.query(models.TrBas).filter_by(id=bas_id).delete()
        self.add_oplog(u'删除接入设备信息:%s' % bas_id)
        self.db.commit()
        dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrBas.__tablename__, dict(id=bas_id)), async=True)
        dispatch.pub(redis_cache.CACHE_DELETE_EVENT, bas_cache_key(bas_ip), async=True)
        self.redirect('/admin/bas', permanent=False)