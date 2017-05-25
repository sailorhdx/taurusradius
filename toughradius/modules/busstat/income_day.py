#!/usr/bin/env python
#coding:utf-8
import decimal
import datetime
from sqlalchemy import func
from tablib import Dataset
from toughradius.modules import models
from toughradius.modules.customer import customer_forms
from toughradius.modules.base import BaseHandler, authenticated
from toughradius.toughlib.permit import permit
from toughradius.toughlib import utils
from toughradius.modules.settings import *

@permit.suproute('/admin/stat/income/day', u'营业日统计', MenuStat, order=1.0, is_menu=True)

class IncomeDayStatHandler(BaseHandler):

    @authenticated
    def get(self):
        self.post()

    @authenticated
    def post(self):
        node_id = self.get_argument('node_id', None)
        product_id = self.get_argument('product_id', None)
        query_begin_time = self.get_argument('query_begin_time', None)
        query_end_time = self.get_argument('query_end_time', None)
        pay_status = self.get_argument('pay_status', None)
        opr_nodes = self.get_opr_nodes()
        _query = self.db.query(models.TrCustomer.node_id, models.TrNode.node_name, models.TrCustomerOrder.product_id, models.TrProduct.product_name, func.sum(models.TrCustomerOrder.actual_fee).label('actual_fee'), models.TrCustomerOrder.stat_day).filter(models.TrCustomerOrder.product_id == models.TrProduct.id, models.TrCustomerOrder.customer_id == models.TrCustomer.customer_id, models.TrNode.id == models.TrCustomer.node_id)
        if node_id:
            _query = _query.filter(models.TrCustomer.node_id == node_id)
        else:
            _query = _query.filter(models.TrCustomer.node_id.in_([ i.id for i in opr_nodes ]))
        if pay_status:
            _query = _query.filter(models.TrCustomerOrder.pay_status == int(pay_status))
        if product_id:
            _query = _query.filter(models.TrCustomerOrder.product_id == product_id)
        if query_begin_time:
            _query = _query.filter(models.TrCustomerOrder.stat_day >= query_begin_time)
        if query_end_time:
            _query = _query.filter(models.TrCustomerOrder.stat_day <= query_end_time)
        _query = _query.group_by('stat_day', 'node_id', 'node_name', 'product_id', 'product_name')
        _query = _query.order_by('stat_day')
        userqry = _query.subquery()
        fee_total = self.db.query(func.sum(userqry.c.actual_fee)).scalar() or 0
        if self.request.path == '/admin/stat/income/day':
            return self.render('income_day_stat.html', node_list=opr_nodes, fee_total=fee_total, products=self.get_opr_products(), statitems=_query.limit(5000), **self.get_params())
        elif self.request.path == '/admin/stat/income/day/export':
            data = Dataset()
            data.append((u'日期', u'区域', u'资费', u'总金额'))
            _f2y = utils.fen2yuan
            for i in _query:
                data.append((i.stat_day,
                 i.node_name,
                 i.product_name,
                 _f2y(i.actual_fee)))

            name = u'RADIUS-INCOME-DAY-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.xls'
            return self.export_file(name, data)
        else:
            return


@permit.suproute('/admin/stat/income/day/export', u'收入日统计导出', MenuStat, order=2.000001)

class IncomeDayStatExportHandler(IncomeDayStatHandler):
    pass