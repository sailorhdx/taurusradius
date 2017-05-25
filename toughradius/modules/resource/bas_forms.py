#!/usr/bin/env python
# coding=utf-8
import os
from toughradius.toughlib import btforms
from toughradius.toughlib.btforms import dataform
from toughradius.toughlib.btforms import rules
from toughradius.toughlib.btforms.rules import button_style, input_style
button_style = {'class': 'btn btn-sm bg-navy'}
boolean = {0: u'否',
 1: u'是'}
timetype = {0: u'标准时区,北京时间',
 1: u'时区和时间同区'}
bastype = {'0': u'标准',
 '3041': u'阿尔卡特',
 '2352': u'爱立信',
 '2011': u'华为',
 '25506': u'H3C',
 '3902': u'中兴',
 '14988': u'RouterOS/Smart6/神行者/Panabit',
 '10055': u'爱快路由'}
portaltype = {'0': u'无',
 'cmccv1': u'中国移动 V1',
 'cmccv2': u'中国移动 V2',
 'huaweiv1': u'华为 V1',
 'huaweiv2': u'华为 V2'}

def bas_add_form(nodes = []):
    return btforms.Form(btforms.Textbox('ip_addr', rules.is_ip, description=u'接入设备地址', **input_style), btforms.Textbox('bas_name', rules.len_of(2, 64), description=u'接入设备名称', required='required', **input_style), btforms.Textbox('nas_id', rules.len_of(4, 32), description=u'接入设备标识', help=u'动态IP专用', **input_style), btforms.Textbox('bas_secret', rules.is_alphanum2(4, 32), description=u'共享秘钥', required='required', **input_style), btforms.Dropdown('vendor_id', description=u'接入设备类型', args=bastype.items(), required='required', **input_style), btforms.Dropdown('portal_vendor', description=u'portal协议', args=portaltype.items(), required='required', **input_style), btforms.Textbox('coa_port', rules.is_number, description=u'授权端口', default=3799, required='required', **input_style), btforms.Textbox('ac_port', rules.is_number, description=u'无线控制器端口', default=2000, **input_style), btforms.Dropdown('time_type', description=u'时间类型', args=timetype.items(), required='required', **input_style), btforms.Dropdown('nodes', description=u'绑定区域(多选)', args=nodes, required='required', multiple='multiple', size=6, **input_style), btforms.Button('submit', type='submit', html=u'<b>提交</b>', **button_style), attrs=dict(mselect=['nodes']), title=u'创建接入设备', htopic='bas', action='/admin/bas/add')


def bas_update_form(nodes = []):
    return btforms.Form(btforms.Hidden('id', description=u'编号'), btforms.Textbox('ip_addr', rules.is_ip, description=u'接入设备地址', **input_style), btforms.Textbox('bas_name', rules.len_of(2, 64), description=u'接入设备名称', required='required', **input_style), btforms.Textbox('nas_id', rules.len_of(4, 32), description=u'接入设备标识', help=u'动态IP专用', **input_style), btforms.Textbox('bas_secret', rules.is_alphanum2(4, 32), description=u'共享秘钥', required='required', **input_style), btforms.Dropdown('vendor_id', description=u'接入设备类型', args=bastype.items(), required='required', **input_style), btforms.Dropdown('portal_vendor', description=u'portal协议', args=portaltype.items(), required='required', **input_style), btforms.Textbox('ac_port', rules.is_number, description=u'无线控制器端口', default=2000, **input_style), btforms.Textbox('coa_port', rules.is_number, description=u'授权端口', default=3799, required='required', **input_style), btforms.Dropdown('time_type', description=u'时间类型', args=timetype.items(), required='required', **input_style), btforms.Dropdown('nodes', description=u'绑定区域(多选)', args=nodes, required='required', multiple='multiple', size=6, **input_style), btforms.Button('submit', type='submit', html=u'<b>更新</b>', **button_style), attrs=dict(mselect=['nodes']), title=u'修改接入设备', htopic='bas', action='/admin/bas/update')