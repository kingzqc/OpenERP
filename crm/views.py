# Create your views here.
from __future__ import print_function
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.http import HttpResponse
from random import randint
from crm.models import *
'''
Dummy_id规则 后三位：
    workflow： （100-199）
    contact : (200-299)
    customer: (300-399)
    Opportunity: (400-499)
    Project: (500-599)
    Document:(600-699)
    Resource:(700-799)
    Service:(800-899)
    User:(900-999)
'''
@login_required
@permission_required('crm.CONTACT_OP', login_url='/PSMProject/forbid/')
def contact_confirm_detail(request):
    # 获取搜索框参数

    try:
        dummyid = request.POST.get('dummy_id', '')
        lineid = request.POST.get('line_id', '')
        lineskucode = request.POST.get('line_skucode', '')
        purchaseorder = request.POST.get('purchase_order', '')


        pol = ContactMaster.objects.get(id=lineid)

        pol.line_dummyid = dummyid
        pol.line_purchaseorder = purchaseorder
        pol.line_skucode = lineskucode

        product = product_frame.objects.filter(sku=lineskucode)
        pol.line_skuname = product[0].name # get SKU name

        pol.line_thisrcvqty = linethisrcvqty
        pol.line_thisrcvdate = linethisrcvdate
        # get user and time
        pol.save()
        return JsonResponse(code=0, msg='保存 Success！')
    except Exception as e:
        return JsonResponse(code=-1, msg=e)
#--------------------------------------------------------------
# 个人名片 图像识别
# -*- coding: utf-8 -*-

import ssl, hmac, base64, hashlib
from datetime import datetime as pydatetime

try:
    from urllib import urlencode
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen

# 云市场分配的密钥Id
secretId = "AKIDKMQFnWm2MaaLNxUK47G35Q9K9iU8V9CL3fy3"
# 云市场分配的密钥Key
secretKey = "3e6d7zeXsi32ksux4wA9ht5ru5lb8YLV10ux78gt@"
source = "thinkin"

# 签名
datetime = pydatetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
signStr = "x-date: %s\nx-source: %s" % (datetime, source)
sign = base64.b64encode(hmac.new(secretKey.encode('utf-8'), signStr.encode('utf-8'), hashlib.sha1).digest())
auth = 'hmac id="%s", algorithm="hmac-sha1", headers="x-date x-source", signature="%s"' % (
secretId, sign.decode('utf-8'))

# 请求方法
method = 'POST'
# 请求头
headers = {
    'X-Source': source,
    'X-Date': datetime,
    'Authorization': auth,

}
# 查询参数
queryParams = {

}
# body参数（POST方法下存在）
bodyParams = {
    "imgBase64": "",
    "imgUrl": "/medias/微信图片_20220916165802.jpg"}
# url参数拼接
url = 'https://service-nwq8ehpc-1303991992.gz.apigw.tencentcs.com/release/businessCard/'
if len(queryParams.keys()) > 0:
    url = url + '?' + urlencode(queryParams)
    print(url)

request = Request(url, headers=headers)
request.get_method = lambda: method
if method in ('POST', 'PUT', 'PATCH'):
    request.data = urlencode(bodyParams).encode('utf-8')
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
print(request.data)
response = urlopen(request, context=ctx)
content = response.read()
if content:
    print(content.decode('utf-8'))