# -*- coding: utf-8 -*-
"""
pdd update focus video
"""
import json
import random
import requests
import time
from config import get_user_agents, get_urls, get_key
from logger import bilivideolog
from db import TddFocusVideoRecord, DBOperation
from .support import get_timestamp, get_timestamp_s


class TddUpdateFocusVideo():
    """通过uid获取Bilibili Video Info"""
    field_keys = ('added', 'aid', 'view', 'danmaku', 'reply', 'favorite', 
                  'coin', 'share', 'like')

    def __init__(self, aid):
        """
        aid: video id
        -----info format-----:
        ('added', 'view', 'aid',  'danmaku', 'reply', 'favorite', 
                  'coin', 'share', 'like')
        """
        self.aid = aid
        self.info = None

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
                ajax_info = (get_timestamp_s(), self.aid, data['view'], data['danmaku'],
                             data['reply'], data['favorite'], data['coin'],
                             data['share'], data['like'])
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
        info_ajax = cls(aid).getAjaxInfo()
        try:
            info = info_ajax
        except Exception as e:
            info = None
        return info

    @classmethod
    def store_video(cls, aid, session=None, csvwriter=None):
        """session, csvwriter 二选一都没有直接打印"""
        info = cls.getVideoInfo(aid)
        #print(info)
        if info:
            new_video = TddFocusVideoRecord(**dict(zip(cls.field_keys, info)))
            if session:
                print("update av%s with %d views at %s" % (info[1], info[2], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info[0]))))
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
