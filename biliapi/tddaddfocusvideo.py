# -*- coding: utf-8 -*-
"""
pdd add focus video
"""
import json
import random
import requests
from config import get_user_agents, get_urls, get_key
from logger import bilivideolog
from db import TddFocusVideo, DBOperation
from .support import get_timestamp, get_timestamp_s


class TddAddFocusVideo():
    """通过uid获取Bilibili Video Info"""
    field_keys = ('added','mid', 'aid', 'tid', 'cid', 'typename', 'arctype', 'title',
                  'pic', 'pages', 'created', 'copyright')

    def __init__(self, aid):
        """
        aid: video id
        -----info format-----:
        ('added','mid', 'aid', 'tid', 'cid', 'typename', 'arctype', 'title',
                  'pic', 'pages', 'created', 'copyright')
        """
        self.aid = aid
        self.info = None

    def getBasicInfo(self):
        url = get_urls('url_view')
        timestamp_ms = get_timestamp()
        appkey = get_key()
        UAS = get_user_agents()
        params = {'type': 'json', 'appkey': appkey, 'id': str(
            self.aid), '_': '{}'.format(timestamp_ms)}
        # print(params)
        headers = {'User-Agent': random.choice(UAS)}
        # print(headers)

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
        except Exception as e:
            # print(e)
            msg = 'aid({}) get error'.format(self.aid)
            bilivideolog.error(msg)
            return None
        data = json.loads(res.text)
        # print(data)
        if 'mid' in data:
            # ('added','mid','aid','tid','cid','typename','arctype','title','pic','pages','created')
            related_info = (get_timestamp_s(), data['mid'], self.aid, data['tid'],
                            data['cid'], data['typename'], data['arctype'],
                            data['title'], data['pic'],
                            data['pages'], data['created'])
            return related_info

        else:
            msg = 'aid({}) basic info request  return error'.format(self.aid)
            bilivideolog.info(msg)
            return None

    def getAjaxInfo(self):
        """获取视频ajax信息"""
        url = get_urls('url_stat')
        timestamp_ms = get_timestamp()
        UAS = get_user_agents()
        params = {'aid': str(self.aid), '_': '{}'.format(timestamp_ms)}
        headers = {'User-Agent': random.choice(UAS)}

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
        except Exception as e:
            # print(e)
            msg = 'aid({}) get error'.format(self.aid)
            bilivideolog.error(msg)
            return None
        text = json.loads(res.text)
        # print(text)
        try:
            if text['code'] == 0:
                data = text['data']
                ajax_info = (data['copyright'], )
                return ajax_info

            else:
                msg = 'aid({}) ajax request code return error'.format(self.aid)
                bilivideolog.info(msg)
                return None
        except TypeError:
            msg = 'aid({}) text return None'.format(self.aid)
            bilivideolog.info(msg)
            return None

    @classmethod
    def getVideoInfo(cls, aid):
        """获取视频全部信息"""
        # info_basic = (aid, )
        info_basic = cls(aid).getBasicInfo() 
        info_ajax = cls(aid).getAjaxInfo()
        try:
            info = info_basic + info_ajax
        except Exception as e:
            info = None
        return info

    @classmethod
    def store_video(cls, aid, session=None, csvwriter=None):
        """session, csvwriter 二选一都没有直接打印"""
        info = cls.getVideoInfo(aid)
        # print(info)
        if info:
            print(dict(zip(cls.field_keys, info)))
            new_video = TddFocusVideo(**dict(zip(cls.field_keys, info)))
            if session:
                DBOperation.add(new_video, session)
                return True
            elif csvwriter:
                csvwriter.writerow(info)
                return True
            else:
                print(info)
                return True
        else:
            return False
