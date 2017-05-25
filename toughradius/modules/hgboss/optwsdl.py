#!/usr/bin/env python
# coding=utf-8
wsdlxml = '<?xml version="1.0" encoding="UTF-8"?>\n<wsdl:definitions targetNamespace="http://www.ly-bns.net/wsdd/" xmlns:apachesoap="http://xml.apache.org/xml-soap" xmlns:impl="http://www.ly-bns.net/wsdd/" xmlns:intf="http://www.ly-bns.net/wsdd/" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:wsdlsoap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n\n   <wsdl:message name="updatePolicyResponse">\n\n      <wsdl:part name="updatePolicyReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="userModifyRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="userCode" type="soapenc:string"/>\n\n      <wsdl:part name="realName" type="soapenc:string"/>\n\n      <wsdl:part name="mobile" type="soapenc:string"/>\n\n      <wsdl:part name="idcard" type="soapenc:string"/>\n\n      <wsdl:part name="ipAddress" type="soapenc:string"/>\n\n      <wsdl:part name="installAddress" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="userUnlockResponse">\n\n      <wsdl:part name="userUnlockReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="insertProductRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="productCode" type="soapenc:string"/>\n\n      <wsdl:part name="productName" type="soapenc:string"/>\n\n      <wsdl:part name="productStatus" type="xsd:int"/>\n\n      <wsdl:part name="feeNum" type="xsd:int"/>\n\n      <wsdl:part name="feePrice" type="xsd:int"/>\n\n      <wsdl:part name="bindMac" type="xsd:int"/>\n\n      <wsdl:part name="bindVlan" type="xsd:int"/>\n\n      <wsdl:part name="concurNumber" type="xsd:int"/>\n\n      <wsdl:part name="bandwidthCode" type="soapenc:string"/>\n\n      <wsdl:part name="inputMaxLimit" type="xsd:int"/>\n\n      <wsdl:part name="outputMaxLimit" type="xsd:int"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="deleteAreaRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="areaCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="userUnlockRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="basIpAddress" type="soapenc:string"/>\n\n      <wsdl:part name="acctSessionId" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="updateCourtyardResponse">\n\n      <wsdl:part name="updateCourtyardReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="insertProductResponse">\n\n      <wsdl:part name="insertProductReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="updateCourtyardRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="areaCode" type="soapenc:string"/>\n\n      <wsdl:part name="courtyardCode" type="soapenc:string"/>\n\n      <wsdl:part name="courtyardName" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="deleteCourtyardResponse">\n\n      <wsdl:part name="deleteCourtyardReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="updateProductRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="productCode" type="soapenc:string"/>\n\n      <wsdl:part name="productName" type="soapenc:string"/>\n\n      <wsdl:part name="productStatus" type="xsd:int"/>\n\n      <wsdl:part name="bindMac" type="xsd:int"/>\n\n      <wsdl:part name="bindVlan" type="xsd:int"/>\n\n      <wsdl:part name="concurNumber" type="xsd:int"/>\n\n      <wsdl:part name="bandwidthCode" type="soapenc:string"/>\n\n      <wsdl:part name="inputMaxLimit" type="xsd:int"/>\n\n      <wsdl:part name="outputMaxLimit" type="xsd:int"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="insertCourtyardResponse">\n\n      <wsdl:part name="insertCourtyardReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="insertAreaRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="areaCode" type="soapenc:string"/>\n\n      <wsdl:part name="areaName" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="deleteProductResponse">\n\n      <wsdl:part name="deleteProductReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="deleteProductRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="productCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="userReleaseBindResponse">\n\n      <wsdl:part name="userReleaseBindReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="userPasswordUpdateRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="userCode" type="soapenc:string"/>\n\n      <wsdl:part name="password" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="updateProductResponse">\n\n      <wsdl:part name="updateProductReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="userOnlineQueryResponse">\n\n      <wsdl:part name="userOnlineQueryReturn" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="updateAreaRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="areaCode" type="soapenc:string"/>\n\n      <wsdl:part name="areaName" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="userModifyResponse">\n\n      <wsdl:part name="userModifyReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="updateAreaResponse">\n\n      <wsdl:part name="updateAreaReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="updatePolicyRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="userCode" type="soapenc:string"/>\n\n      <wsdl:part name="domainCode" type="soapenc:string"/>\n\n      <wsdl:part name="concurNumber" type="xsd:int"/>\n\n      <wsdl:part name="bindMac" type="xsd:int"/>\n\n      <wsdl:part name="bindVlan" type="xsd:int"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="queryUserBindRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="userCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="insertAreaResponse">\n\n      <wsdl:part name="insertAreaReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="insertCourtyardRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="areaCode" type="soapenc:string"/>\n\n      <wsdl:part name="courtyardCode" type="soapenc:string"/>\n\n      <wsdl:part name="courtyardName" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="queryUserBindResponse">\n\n      <wsdl:part name="queryUserBindReturn" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="deleteAreaResponse">\n\n      <wsdl:part name="deleteAreaReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="userPasswordUpdateResponse">\n\n      <wsdl:part name="userPasswordUpdateReturn" type="xsd:int"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="userReleaseBindRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="userCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="userOnlineQueryRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="userCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:message name="deleteCourtyardRequest">\n\n      <wsdl:part name="nodeId" type="soapenc:string"/>\n\n      <wsdl:part name="areaCode" type="soapenc:string"/>\n\n      <wsdl:part name="courtyardCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorCode" type="soapenc:string"/>\n\n      <wsdl:part name="operatorIp" type="soapenc:string"/>\n\n   </wsdl:message>\n\n   <wsdl:portType name="OperateGw">\n\n      <wsdl:operation name="insertArea" parameterOrder="nodeId areaCode areaName operatorCode operatorIp">\n\n         <wsdl:input message="impl:insertAreaRequest" name="insertAreaRequest"/>\n\n         <wsdl:output message="impl:insertAreaResponse" name="insertAreaResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="updateArea" parameterOrder="nodeId areaCode areaName operatorCode operatorIp">\n\n         <wsdl:input message="impl:updateAreaRequest" name="updateAreaRequest"/>\n\n         <wsdl:output message="impl:updateAreaResponse" name="updateAreaResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="deleteArea" parameterOrder="nodeId areaCode operatorCode operatorIp">\n\n         <wsdl:input message="impl:deleteAreaRequest" name="deleteAreaRequest"/>\n\n         <wsdl:output message="impl:deleteAreaResponse" name="deleteAreaResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="insertCourtyard" parameterOrder="nodeId areaCode courtyardCode courtyardName operatorCode operatorIp">\n\n         <wsdl:input message="impl:insertCourtyardRequest" name="insertCourtyardRequest"/>\n\n         <wsdl:output message="impl:insertCourtyardResponse" name="insertCourtyardResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="updateCourtyard" parameterOrder="nodeId areaCode courtyardCode courtyardName operatorCode operatorIp">\n\n         <wsdl:input message="impl:updateCourtyardRequest" name="updateCourtyardRequest"/>\n\n         <wsdl:output message="impl:updateCourtyardResponse" name="updateCourtyardResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="deleteCourtyard" parameterOrder="nodeId areaCode courtyardCode operatorCode operatorIp">\n\n         <wsdl:input message="impl:deleteCourtyardRequest" name="deleteCourtyardRequest"/>\n\n         <wsdl:output message="impl:deleteCourtyardResponse" name="deleteCourtyardResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="insertProduct" parameterOrder="nodeId productCode productName productStatus feeNum feePrice bindMac bindVlan concurNumber bandwidthCode inputMaxLimit outputMaxLimit operatorCode operatorIp">\n\n         <wsdl:input message="impl:insertProductRequest" name="insertProductRequest"/>\n\n         <wsdl:output message="impl:insertProductResponse" name="insertProductResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="updateProduct" parameterOrder="nodeId productCode productName productStatus bindMac bindVlan concurNumber bandwidthCode inputMaxLimit outputMaxLimit operatorCode operatorIp">\n\n         <wsdl:input message="impl:updateProductRequest" name="updateProductRequest"/>\n\n         <wsdl:output message="impl:updateProductResponse" name="updateProductResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="deleteProduct" parameterOrder="nodeId productCode operatorCode operatorIp">\n\n         <wsdl:input message="impl:deleteProductRequest" name="deleteProductRequest"/>\n\n         <wsdl:output message="impl:deleteProductResponse" name="deleteProductResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="userReleaseBind" parameterOrder="nodeId userCode operatorCode operatorIp">\n\n         <wsdl:input message="impl:userReleaseBindRequest" name="userReleaseBindRequest"/>\n\n         <wsdl:output message="impl:userReleaseBindResponse" name="userReleaseBindResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="userOnlineQuery" parameterOrder="nodeId userCode operatorCode operatorIp">\n\n         <wsdl:input message="impl:userOnlineQueryRequest" name="userOnlineQueryRequest"/>\n\n         <wsdl:output message="impl:userOnlineQueryResponse" name="userOnlineQueryResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="userUnlock" parameterOrder="nodeId basIpAddress acctSessionId operatorCode operatorIp">\n\n         <wsdl:input message="impl:userUnlockRequest" name="userUnlockRequest"/>\n\n         <wsdl:output message="impl:userUnlockResponse" name="userUnlockResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="queryUserBind" parameterOrder="nodeId userCode operatorCode operatorIp">\n\n         <wsdl:input message="impl:queryUserBindRequest" name="queryUserBindRequest"/>\n\n         <wsdl:output message="impl:queryUserBindResponse" name="queryUserBindResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="userPasswordUpdate" parameterOrder="nodeId userCode password operatorCode operatorIp">\n\n         <wsdl:input message="impl:userPasswordUpdateRequest" name="userPasswordUpdateRequest"/>\n\n         <wsdl:output message="impl:userPasswordUpdateResponse" name="userPasswordUpdateResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="userModify" parameterOrder="nodeId userCode realName mobile idcard ipAddress installAddress operatorCode operatorIp">\n\n         <wsdl:input message="impl:userModifyRequest" name="userModifyRequest"/>\n\n         <wsdl:output message="impl:userModifyResponse" name="userModifyResponse"/>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="updatePolicy" parameterOrder="nodeId userCode domainCode concurNumber bindMac bindVlan operatorCode operatorIp">\n\n         <wsdl:input message="impl:updatePolicyRequest" name="updatePolicyRequest"/>\n\n         <wsdl:output message="impl:updatePolicyResponse" name="updatePolicyResponse"/>\n\n      </wsdl:operation>\n\n   </wsdl:portType>\n\n   <wsdl:binding name="operategwSoapBinding" type="impl:OperateGw">\n\n      <wsdlsoap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>\n\n      <wsdl:operation name="insertArea">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="insertAreaRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="insertAreaResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="updateArea">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="updateAreaRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="updateAreaResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="deleteArea">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="deleteAreaRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="deleteAreaResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="insertCourtyard">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="insertCourtyardRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="insertCourtyardResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="updateCourtyard">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="updateCourtyardRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="updateCourtyardResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="deleteCourtyard">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="deleteCourtyardRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="deleteCourtyardResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="insertProduct">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="insertProductRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="insertProductResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="updateProduct">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="updateProductRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="updateProductResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="deleteProduct">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="deleteProductRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="deleteProductResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="userReleaseBind">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="userReleaseBindRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="userReleaseBindResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="userOnlineQuery">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="userOnlineQueryRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="userOnlineQueryResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="userUnlock">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="userUnlockRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="userUnlockResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="queryUserBind">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="queryUserBindRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="queryUserBindResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="userPasswordUpdate">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="userPasswordUpdateRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="userPasswordUpdateResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="userModify">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="userModifyRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="userModifyResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n      <wsdl:operation name="updatePolicy">\n\n         <wsdlsoap:operation soapAction=""/>\n\n         <wsdl:input name="updatePolicyRequest">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:input>\n\n         <wsdl:output name="updatePolicyResponse">\n\n            <wsdlsoap:body encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" namespace="http://www.ly-bns.net/wsdd/" use="encoded"/>\n\n         </wsdl:output>\n\n      </wsdl:operation>\n\n   </wsdl:binding>\n\n   <wsdl:service name="OperateGwService">\n\n      <wsdl:port binding="impl:operategwSoapBinding" name="operategw">\n\n         <wsdlsoap:address location="{wsurl}/interface/operategw"/>\n\n      </wsdl:port>\n\n   </wsdl:service>\n\n</wsdl:definitions>'.format