# -*- coding: utf-8 -*-
"""
tdd update focus video
"""
import sys
import csv
import os
import schedule
import datetime
from queue import Queue
from biliapi import BiliUser, TddUpdateFocusVideo
from db import Session, DBOperation, TddFocusVideo
from utils import Producer3, Consumer, Timer
from config import BASE_DIR


update_round = 1

def get_update_aids():
    result = []
    items = DBOperation.query(TddFocusVideo, Session())
    for item in items:
        result.append(item.aid)
    return result


def crawl2db(getsession):
    """多线程只使用一个连接会存在一些问题,建立一个session池每个线程一个session
    视频访问速率有很严格的限制，请调大sleepsec"""
    global update_round
    print("now start update round %d at %s" % (update_round, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    Q = Queue()
    mythreads = []
    aids = get_update_aids()
    print("try update videos with aids " + str(aids))
    pthread = Producer3(Q, video_aids=aids, func=lambda x: (x,), sleepsec=0.5)
    mythreads.append(pthread)
    consumer_num = 4 # 4个消费者线程
    sessions = [getsession() for _ in range(consumer_num)]
    for i in range(consumer_num):
        db_session = sessions[i] # 每个线程一个session
        cthread = Consumer(Q, session=db_session, func=TddUpdateFocusVideo.store_video, sleepsec=0.5)
        mythreads.append(cthread)
    with Timer() as t:
        for thread in mythreads:
            thread.start()
        for thread in mythreads:
            thread.join()
    for session in sessions:
        session.close()
        
    # db_session.close()
    print("update round %d finished, runtime: %s" % (update_round, t.elapsed))
    update_round += 1


'''
def crawl2csv(filename, start, end):
    """sleep sec 可以用random生成在一个范围的正态分布更好些
    start,end: aid范围"""
    Q = Queue()
    
    with open(filename, 'w', encoding='utf8', newline='') as fwriter:
        mycsvwriter = csv.writer(fwriter)
        mythreads = []
        pthread = Producer(Q, start=start, end=end, func=lambda x: (x, ), sleepsec=0.5)
        mythreads.append(pthread)
        consumer_num = 4 # 4个消费者线程
        for _ in range(consumer_num):
            cthread = Consumer(Q, csvwriter=mycsvwriter, func= TddAddFocusVideo.store_video, sleepsec=0.5)
            mythreads.append(cthread)
        with Timer() as t:
            for thread in mythreads:
                thread.start()
            for thread in mythreads:
                thread.join()
        
        print('runtime: %s' % t.elapsed)
        print('======= All Done! ======')
'''


if __name__ == '__main__':

    schedule.every(1).minutes.do(crawl2db(Session))
    
    while True:
        schedule.run_pending()
        time.sleep(10)
