# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, Integer, String, Text, Boolean
from .basic import Base

class BiliUserInfo(Base):
    """BiliBili user info表
    (mid,name,approve,sex,-face-,DisplayRank,regtime,spacesta,birthday,
        place,-description-,article,fans,attention,-sign-,level,verify,vip)
    """
    __tablename__ = 'biliuserinfo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mid = Column(String(20), unique=True)
    name = Column(String(50), default='')
    approve = Column(Boolean, default=False)
    sex = Column(String(5), default='保密')
    displayrank = Column(String(10),default='0')
    regtime = Column(Integer,default=0)
    spacesta = Column(Integer,default=0)
    birthday = Column(String(12), default='0000-00-00') # 存csv日期有0000-01-01、0000/1/1格式注意清理
    place = Column(String(50), default='')
    article = Column(Integer, default=0)
    fans = Column(Integer, default=0)
    attention = Column(Integer, default=0)
    level = Column(Integer,default=0)
    verify = Column(Integer,default=-1)
    vip = Column(Integer,default=0)

    def __repr__(self):
        return "<BiliUserIno(mid=%s,name=%s)>" % (self.mid, self.name)


class BiliVideoList(Base):
    """Video Submit List"""

    __tablename__ = 'bilivideolist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mid = Column(String(20))
    aid = Column(String(20), unique=True)

    def __repr__(self):
        return "<BiliUserVideo(mid=%s,aid=%s)>" % (self.mid, self.aid)

class BiliVideoInfo(Base):
    """Bili Video Info"""
    __tablename__ = 'bilivideoinfo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mid = Column(String(20))
    aid = Column(String(20), unique=True)
    tid = Column(String(10), default='')
    cid = Column(Integer)
    typename = Column(String(20), default='')
    arctype = Column(String(20), default='')
    title = Column(String(100), default='')
    pic = Column(String(100),default='')
    pages = Column(Integer)
    created = Column(Integer)
    view = Column(String(20))
    danmaku = Column(Integer)
    reply = Column(Integer)
    favorite = Column(Integer)
    coin = Column(Integer)
    share = Column(Integer)
    now_rank = Column(Integer)
    his_rank = Column(Integer)
    like = Column(Integer)
    no_reprint = Column(Integer)
    copyright = Column(Integer)

    def __repr__(self):
        return "<BiliVideo(aid=%s,mid=%s)>" % (self.aid, self.mid)

class BiliVideoSimpleInfo(Base):
    """Bili Video Simple Info"""
    __tablename__ = 'bilivideo_simpleinfo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mid = Column(String(20))
    aid = Column(String(20), unique=True)
    tid = Column(String(10), default='')
    # cid = Column(Integer)
    # typename = Column(String(20), default='')
    # arctype = Column(String(20), default='')
    title = Column(String(100), default='')
    # pic = Column(String(100),default='')
    # pages = Column(Integer)
    created = Column(Integer)
    length = Column(String(10))
    play = Column(String(20))
    comment = Column(Integer)
    danmaku = Column(Integer)
    favorite = Column(Integer)
    hide_click = Column(Boolean)
    #coin = Column(Integer)
    # share = Column(Integer)
    #now_rank = Column(Integer)
    # his_rank = Column(Integer)
    # like = Column(Integer)
    #no_reprint = Column(Integer)
    # copyright = Column(Integer)

    def __repr__(self):
        return "<BiliVideo(aid=%s,mid=%s)>" % (self.aid, self.mid)

class BiliVideoAjaxInfo(Base):
    """Bili Video Info"""
    __tablename__ = 'bilivideo_ajaxinfo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mid = Column(String(20))
    aid = Column(String(20), unique=True)
    view = Column(String(20))
    danmaku = Column(Integer)
    reply = Column(Integer)
    favorite = Column(Integer)
    coin = Column(Integer)
    share = Column(Integer)
    now_rank = Column(Integer)
    his_rank = Column(Integer)
    like = Column(Integer)
    no_reprint = Column(Integer)
    copyright = Column(Integer)

    def __repr__(self):
        return "<BiliVideoAjax(aid=%s,mid=%s)>" % (self.aid, self.mid)

class TddFocusVideo(Base):
    """Tdd Focus Video"""
    __tablename__ = 'tdd_focus_video'

    id = Column(Integer, primary_key=True, autoincrement=True)
    added = Column(Integer)
    mid = Column(String(20))
    aid = Column(String(20), unique=True)
    tid = Column(String(10), default='')
    cid = Column(Integer)
    typename = Column(String(20), default='')
    arctype = Column(String(20), default='')
    title = Column(String(100), default='')
    pic = Column(String(100),default='')
    pages = Column(Integer)
    created = Column(Integer)
    #view = Column(String(20))
    #danmaku = Column(Integer)
    #reply = Column(Integer)
    #favorite = Column(Integer)
    #coin = Column(Integer)
    #share = Column(Integer)
    #now_rank = Column(Integer)
    #his_rank = Column(Integer)
    #like = Column(Integer)
    #no_reprint = Column(Integer)
    copyright = Column(Integer)

    def __repr__(self):
        return "<TddFocusVideo(aid=%s,mid=%s)>" % (self.aid, self.mid)

class TddFocusVideoRecord(Base):
    """Tdd Focus Video Record"""
    __tablename__ = 'tdd_focus_video_record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    added = Column(Integer)
    #mid = Column(String(20))
    aid = Column(String(20))
    #tid = Column(String(10), default='')
    #cid = Column(Integer)
    #typename = Column(String(20), default='')
    #arctype = Column(String(20), default='')
    #title = Column(String(100), default='')
    #pic = Column(String(100),default='')
    #pages = Column(Integer)
    #created = Column(Integer)
    view = Column(String(20))
    danmaku = Column(Integer)
    reply = Column(Integer)
    favorite = Column(Integer)
    coin = Column(Integer)
    share = Column(Integer)
    #now_rank = Column(Integer)
    #his_rank = Column(Integer)
    like = Column(Integer)
    #no_reprint = Column(Integer)
    #copyright = Column(Integer)

    def __repr__(self):
        return "<TddFocusVideoRecord(aid=%s,mid=%s)>" % (self.aid, self.mid)