#!/usr/bin/env python
# coding=utf-8
import cyclone.auth
import cyclone.escape
import cyclone.web
from toughradius.modules import models
from toughradius.modules.base import BaseHandler, authenticated
from toughradius.modules.region import node_forms
from toughradius.toughlib.permit import permit
from toughradius.toughlib import utils, dispatch
from toughradius.modules.settings import *
from toughradius.common import tools
from toughradius.modules.events.settings import DBSYNC_STATUS_ADD
from toughradius.toughlib.utils import safeunicode as _su

@permit.suproute('/admin/node', u'区域节点管理', MenuNode, order=1.0, is_menu=True)

class NodeListHandler(BaseHandler):

    @authenticated
    def get(self):
        nodes = self.db.query(models.TrNode)
        return self.render('node_list.html', nodes=nodes)


@permit.suproute('/admin/node/add', u'新增区域', MenuNode, order=1.0001)

class NodeAddHandler(BaseHandler):

    @authenticated
    def get(self):
        arules = [ (r.id, r.rule_name) for r in self.db.query(models.TrAccountRule) ]
        form = node_forms.node_add_form(rule_ids=arules)
        self.render('base_form.html', form=form)

    @authenticated
    def post(self):
        arules = [ (r.id, r.rule_name) for r in self.db.query(models.TrAccountRule) ]
        form = node_forms.node_add_form(rule_ids=arules)
        if not form.validates(source=self.get_params()):
            return self.render('base_form.html', form=form)
        node = models.TrNode()
        node.id = utils.get_uuid()
        node.node_name = _su(form.d.node_name)
        node.rule_id = form.d.rule_id
        node.node_desc = _su(form.d.node_desc)
        node.sync_ver = tools.gen_sync_ver()
        self.db.add(node)
        self.add_oplog(u'新增区域信息:%s' % _su(form.d.node_name))
        self.db.commit()
        self.redirect('/admin/node', permanent=False)


@permit.suproute('/admin/node/update', u'修改区域', MenuNode, order=1.0002)

class NodeUpdateHandler(BaseHandler):

    @authenticated
    def get(self):
        arules = [ (r.id, r.rule_name) for r in self.db.query(models.TrAccountRule) ]
        node_id = self.get_argument('node_id')
        form = node_forms.node_update_form(rule_ids=arules)
        node = self.db.query(models.TrNode).get(node_id)
        form.fill(node)
        self.render('base_form.html', form=form)

    @authenticated
    def post(self):
        arules = [ (r.id, r.rule_name) for r in self.db.query(models.TrAccountRule) ]
        form = node_forms.node_update_form(rule_ids=arules)
        if not form.validates(source=self.get_params()):
            return self.render('base_form.html', form=form)
        node = self.db.query(models.TrNode).get(form.d.id)
        node.node_name = _su(form.d.node_name)
        node.rule_id = form.d.rule_id
        node.node_desc = _su(form.d.node_desc)
        node.sync_ver = tools.gen_sync_ver()
        self.add_oplog(u'修改区域信息:%s' % _su(form.d.node_name))
        self.db.commit()
        self.redirect('/admin/node', permanent=False)


@permit.suproute('/admin/node/delete', u'删除区域', MenuNode, order=1.0003)

class NodeDeleteHandler(BaseHandler):

    @authenticated
    def get(self):
        node_id = self.get_argument('node_id')
        if self.db.query(models.TrCustomer.customer_id).filter_by(node_id=node_id).count() > 0:
            return self.render_error(msg=u'该节点下有用户，不允许删除')
        self.db.query(models.TrNode).filter_by(id=node_id).delete()
        abuuilders = []
        for area in self.db.query(models.TrArea).filter_by(node_id=node_id):
            abuuilders.append(area.id)
            self.db.query(models.TrAreaBuilder).filter_by(area_id=area.id).delete()

        self.db.query(models.TrArea).filter_by(node_id=node_id).delete()
        self.add_oplog(u'删除区域信息:%s' % node_id)
        self.db.commit()
        dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrNode.__tablename__, dict(id=node_id)), async=True)
        dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrArea.__tablename__, dict(node_id=node_id)), async=True)
        for abid in abuuilders:
            dispatch.pub(DBSYNC_STATUS_ADD, models.warp_sdel_obj(models.TrAreaBuilder.__tablename__, dict(area_id=abid)), async=True)

        self.redirect('/admin/node', permanent=False)