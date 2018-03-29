#! /usr/bin/python
#! coding=UTF-8
import sys
reload(sys)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
sys.path.append(BASE_DIR)
# print 'ffffmmmm:',BASE_DIR
import json
import requests
# import sys
from base.Config import riskbell_interface_envs, riskbell_login_user
import business.riskbell.test.unittest_flv4.case.config.configuration as configuration


username = riskbell_login_user[configuration.env]['username']
password = riskbell_login_user[configuration.env]['password']

class LoginAPI_v4(object):
    def __init__(self):
        # self.env = configuration.env
        self.base_url = riskbell_interface_envs[configuration.env]

    def  login(self,username=username,password=password):
        payload = {'username':username,'password':password}
        # payload = riskbell_login_user[self.env]
        child_url = 'v4/api/tokens'
        url = '/'.join([self.base_url, child_url])
        # rsdata = requests.post(url, data=json.dumps(payload), headers=groupHeader(env), verify=False)
        headers = {'Content-Type': 'application/json'}
        res = requests.post(url, data=json.dumps(payload), headers=headers)
        return res

    def  add_subs(self,entname,token):
        payload = { 
            "keyword": [entname]
        }
        child_url = 'v4/api/subs'
        url = '/'.join([self.base_url, child_url])
        headers = {
            'Content-Type': 'application/json',
            'X-Token': token
        }
        res = requests.post(url, data=json.dumps(payload), headers=headers)
        return res
    # 通过entId添加订阅
    def  ent_id_subs(self,entId,ent_type,token):
        payload = [{
            "ent_id": entId,
            "ent_type":ent_type
        }]
        child_url = 'v4/api/ent_id_subs'
        url = '/'.join([self.base_url, child_url])
        headers = {
            'Content-Type': 'application/json',
            'X-Token': token
        }
        res = requests.post(url, data=json.dumps(payload), headers=headers)
        return res

    #订阅清单
    def subs_list(self,token,per_page=10,page=1,count='true',sort='-created_at'):
        child_url = 'v4/api/subs'
        url = '/'.join([self.base_url, child_url])
        params = {
            "per_page":per_page,
            "page":page,
            "count":count,
            "sort":sort
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Token': token
        }
        res = requests.get(url,params=params,headers=headers)
        # print res.content
        # print res.headers['X-Total-Count']
        return res

    def  sub_detail(self,id,token):
        child_url = 'v4/api/subs/'
        url = '/'.join([self.base_url, child_url])
        url = '%s%s'%(url,id)
        headers = {
            'Content-Type': 'application/json',
            'X-Token': token
        }
        res = requests.get(url, headers=headers)
        return res
    #暂停订阅
    def inactive_subs(self,id,token):
        child_url = 'v4/api/subs/'
        url = '/'.join([self.base_url, child_url])
        url = '%s%s' % (url, id)
        payload ={
            "status": "INACTIVE"
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Token': token
        }
        res = requests.patch(url,data=json.dumps(payload),headers=headers)
        return res

    # 恢复订阅
    def active_subs(self,id,token):
        child_url = 'v4/api/subs/'
        url = '/'.join([self.base_url, child_url])
        url = '%s%s' % (url, id)
        payload = {
            "status": "ACTIVE"
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Token': token
        }
        res = requests.patch(url, data=json.dumps(payload), headers=headers)
        return res

    #终止订阅
    def remove_subs(self,id,token):
        child_url = 'v4/api/subs/'
        url = '/'.join([self.base_url, child_url])
        url = '%s%s' % (url, id)
        payload ={
            "status": "REMOVED"
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Token': token
        }
        res = requests.patch(url,data=json.dumps(payload),headers=headers)
        return res

    # 变更列表
    def change_list(self,token,count='true',sort='-date',limit='10'):
        headers = {
            'Content-Type': 'application/json',
            'X-Token': token
        }
        # url = '%s%s%s' % (self.base_url, '/v4/api/changes', '?count=true&sort=-date')
        url ='%s%s' % (self.base_url, '/v4/api/changes')
        params = {
            "count":count,
            "sort":sort,
            "limit":limit
        }
        # print url
        rsdata = requests.get(url,params=params,headers=headers)
        return rsdata

    # 变更详情
    def change_detail(self,date='20171205'):
        token = json.loads(self.login().content)['token']
        headers = {
            'Content-Type': 'application/json',
            'X-Token': token
        }
        url = '%s%s%s%s' % (self.base_url, '/v4/api/changes/', date, '/items')
        # print url
        rsdata = requests.get(url, headers=headers)
        return rsdata

if __name__=='__main__':
    LoginAPI_v4 = LoginAPI_v4()
    ent_id = '150000\u000117c9a2cb-0146-1000-e147-19f77f000001\u00011949100100000011813619'
    ent_type = "2"
    token = json.loads(LoginAPI_v4.login().content)['token']
    res = LoginAPI_v4.ent_id_subs(ent_id,ent_type,token)
