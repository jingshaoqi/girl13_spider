# -*- coding: utf-8 -*-

import user_agent
import requests
import scrapy


class Girl13_UA_Middleware(object):
    def process_request(self, request, spider):
        request.headers['User_Agent'] =  user_agent.generate_user_agent()
        referer = request.url
        if referer:
            request.headers['Referer'] = referer



class Girl13_proxy_Middleware(object):

    def __init__(self):
        self.url = 'http://188.131.212.24:5010/get/'
        self.ip = ''
        self.ip_num = 0

    def process_request(self, request, spider):
        if self.ip_num == 0 or self.ip_num >= 10:
            res = requests.get(url=self.url).content.decode()
            if not 'no' in res:
                # 115.159.31.195:8080 该ip有问题    ..... 好几个ip有问题,被迫中断了好几次
                if not '115.159.31.195' in res:
                    if not '219.239.142.253' in res:
                        self.ip = res
                    self.ip_num = 1

        if self.ip:
            request.meta['proxy'] = 'http://' + self.ip
            self.ip_num += 1
            print('ip地址>>>{} --- 使用次数{}'.format(self.ip,self.ip_num))
        else:
            self.ip_num += 3
            print('使用的是本机ip......')



    # 如果出现403无权访问,有可能是ip被gan,因为之前一直都是这个配置爬取,但是有时候出现403的位置不同,只能是ip问题
    # 除了403 还可以配置404 50x 系列
    def process_response(self, request, response, spider):
        http_code = response.status
        if http_code == 403:
            print('这个url>{} 403 重新抓取'.format(request.url))
            self.ip_num += 10
            # with open('403.txt', 'a')as f:
            #     f.write(request.url)
            #     f.write('\n')
            return scrapy.Request(url=request.url,dont_filter=True)

        return response


    # 如果是ip本身就有问题,貌似没用,不是给你返回timeouterror的异常,而是直接抛出链接不上,一定次数(5)之后结束程序
    def process_exception(self, request, exception, spider):
        try:
            if isinstance(exception,TimeoutError):
                print('超时',request.url)
                self.ip_num += 10
                return request


            return request
        except:
            return request


