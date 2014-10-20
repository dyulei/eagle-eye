#!/usr/bin/env python
# coding=utf-8
import operator
import re
import time
import datetime
import traceback

from flask import json
from flask import g
from collections import OrderedDict

from eagle.model.entity import apple
#from eagle.common import zexception
from eagle.common.utils import row2dict
from eagle.common import utils
from eagle.common import elog

LOG = elog.getLogger()

class AppleMixIn():
    def _get_game_type(self,session,app_ids):
        datas = app_ids
        sql_app_category = '''SELECT DISTINCT app_id,category_id from tb_app_category WHERE app_id in (%s) ''' % (",".join(["'%s'" % x for x in datas]))

        category_id = session.execute(sql_app_category).fetchall()

        sql_category_name = '''SELECT category_id,category_name from tb_category'''

        category_name = session.execute(sql_category_name).fetchall()
        category_id2name_hash = {}
        for category in category_name:
            category_id2name_hash[str(category[0])] = category[1]

        category_hash =  {}
        type_list = []
        for category_app in category_id:
            if category_app[1] < 7001:
                continue
            if category_hash.get(category_id2name_hash[str(category_app[1])]):
                category_hash[category_id2name_hash[str(category_app[1])]]+=1
            else:
                category_hash[category_id2name_hash[str(category_app[1])]] = 1
        for (k,v) in category_hash.items():
            ilist = []
            ilist.append(k)
            ilist.append(v)
            type_list.append(ilist)

        type_list.sort(key=lambda x:x[1],reverse=True)

        return type_list


    def _get_top_ten_company(self,session,app_ids,country="cn"):
        datas = app_ids

        sql_company = '''SELECT  company_id,company_name from tb_app where app_id in (%s) ''' % (",".join(["'%s'" % x for x in datas]))
        sql_company += ''' AND country = '%s' ''' %(country)

        companys = session.execute(sql_company).fetchall()
        company_dict = {}
        for company in companys:
            if company_dict.get(company[1]):
                company_dict[company[1]] += 1
            else:
                company_dict[company[1]] = 1


        company_list = OrderedDict([(k,v) for k,v in company_dict.iteritems()])
        company_order_dict = OrderedDict(sorted(company_list.items(), key=lambda x: x[1],reverse=True))
        new_dict = {}
        company_top_list = []
        for k in company_order_dict.keys()[0:10]:
            ilist = []
            ilist.append(k)
            ilist.append(company_order_dict[k])
            company_top_list.append(ilist)
            new_dict[k] = company_order_dict[k]



        session.commit()
        return company_top_list
        #return new_dict


class Apple(AppleMixIn):

    def _get_control1_data(self, start_time, end_time, app_type, page):
        session = self.get_session("apple")

        sql = "select t.app_id, t.rank, t.created_at, a.app_name, a.icon_Url\
                from db_rankapp.tb_rank t, db_rankapp.tb_app a \
                where t.app_id = a.app_id and t.created_at >= '%s'\
                and t.created_at <= '%s' and t.rank_type = '%s'\
                order by app_id, created_at" % (start_time, end_time, app_type)

        res = session.execute(sql)
        datas = res.fetchall()
        res_list = []
        for data in datas:
            data = row2dict(data)
            res_list.append(data)
        res.close()
        session.commit()

        return res_list

    def _get_index_game_type(self,app_type,start_time,end_time,country="cn"):
        session = self.get_session("apple")

        sql_release = '''SELECT app_id FROM tb_app WHERE release_date > "%s" and release_date < "%s"''' %(start_time,end_time)
        sql_release += ''' AND country = '%s' ''' %(country)

        res = session.execute(sql_release)
        datas = res.fetchall()
        release_apps = [row2dict(data)['app_id'] for data in datas]
        index_game_type = self._get_game_type(session,release_apps)

        return index_game_type

    def _get_app_detail_with_id(self,app_id):
        session = self.get_session("apple")
        app_id = int(app_id)
        #app_detail = session.query(self.apple.tb_app).filter(self.apple.tb_app.columns.app_id == 459023855)
        #app_detail = row2dict(app_detail.first())
        #app_detail = row2dict(app_detail)
        #sql = 'SELECT * FROM tb_app where tb_app.app_id = 459023855'
        start = time.time()
        sql = '''SELECT app_id FROM tb_app WHERE release_date < "2014-09-30T23:59:59Z" AND release_date > "2014-09-01T00:00:00Z" ORDER BY release_date DESC'''
        res = session.execute(sql)
        datas = res.fetchall()
        release_number = len(datas)
        use_time = time.time()-start

        release_app = [row2dict(data)['app_id'] for data in datas]
        release_app = tuple(release_app)
        sql_rank = '''SELECT COUNT(DISTINCT app_id )  FROM tb_rank WHERE app_id \
                IN (%s) and rank_type=0 and rank <101''' % (",".join(["'%s'" % x.app_id for x in datas]))
        rank_100 = session.execute(sql_rank).fetchone()[0]


        use_time = time.time()-start



        session.commit()

        return release_number

    def _get_release_count(self,start_time,end_time,country="cn"):
        session = self.get_session("apple")

        sql_release = '''SELECT app_id FROM tb_app WHERE release_date > "%s" and release_date < "%s"''' %(start_time,end_time)
        sql_release += ''' AND country = '%s' ''' %(country)

        res = session.execute(sql_release)
        datas = res.fetchall()
        release_number = len(datas)
        release_app = [row2dict(data)['app_id'] for data in datas]
        release_app = tuple(release_app)
        sql_rank = '''SELECT COUNT(DISTINCT app_id )  FROM tb_rank WHERE app_id \
                IN (%s) and rank_type=0 and rank <101''' % (",".join(["'%s'" % x.app_id for x in datas]))
        sql_rank += ''' AND country = '%s' ''' %(country)

        rank_100 = session.execute(sql_rank).fetchone()[0]

        #sql_app_category = '''SELECT DISTINCT app_id,category_id from tb_app_category WHERE app_id in (%s) ''' % (",".join(["'%s'" % x.app_id for x in datas]))

        #category_id = session.execute(sql_app_category).fetchall()
        #print category_id[0]
        #print type(category_id)
        #print len(category_id)

        #sql_category_name = '''SELECT category_id,category_name from tb_category'''

        #category_name = session.execute(sql_category_name).fetchall()
        #category_id2name_hash = {}
        #for category in category_name:
        #    category_id2name_hash[str(category[0])] = category[1]
        #print category_name

        #category_hash =  {}
        #for category in category_id:
        #    if category_hash.get(category_id2name_hash[str(category[1])]):
        #        category_hash[category_id2name_hash[str(category[1])]]+=1
        #    else:
        #        category_hash[category_id2name_hash[str(category[1])]] = 1

        #print category_hash

        return_msg = {"release_count":release_number,
                        "top_100":rank_100}

       # print category_id
        session.commit()

        return return_msg


    def _get_app_info_with_release_date(self,start_time,end_time,country="cn"):
        session = self.get_session("apple")

        sql_app_info = '''SELECT app_id,app_name,icon_Url as icon_url  FROM tb_app WHERE release_date > "%s" and release_date < "%s"''' %(start_time,end_time)
        sql_app_info += ''' AND country = '%s' ''' %(country)

        res = session.execute(sql_app_info).fetchall()

        app_list = [row2dict(data) for data in res]

        session.commit()

        return app_list


    def _get_rank_list(self,app_type=0,start=1,end=100,rank_time=None,country="cn"):
        session = self.get_session("apple")

        sql_rank = '''SELECT app_id,rank FROM tb_rank where rank BETWEEN %d AND  %d ''' % (start,end)
        if app_type in [0,1,2]:
            sql_rank += '''AND rank_type = %d''' % app_type
        else:
            sql_rank += '''AND rank_type = 0'''

        sql_rank += ''' AND created_at = "%s"''' % rank_time
        sql_rank += ''' AND country = '%s' ''' %(country)

        res = session.execute(sql_rank).fetchall()

        rank_list = [row2dict(data) for data in res]
        return_list = []

        for date in rank_list:
            app_id  = date['app_id']
            app_rank_now = date['rank']
            sql_rank_early =  '''SELECT rank FROM tb_rank where app_id = %d AND created_at = "%s" ''' %(app_id,rank_time-datetime.timedelta(days =1))
            sql_rank_early += ''' AND country = '%s' ''' %(country)
            if app_type in [0,1,2]:
                sql_rank_early += '''AND rank_type = %d''' % app_type
            app_res = session.execute(sql_rank_early).fetchall()
            try:
                app_rank_early = app_res[0][0]
            except:
                app_rank_early = 1001
            sql_app_info = '''SELECT app_name,icon_Url FROM tb_app where app_id = %d''' %(app_id)
            sql_app_info += ''' AND country = '%s' ''' %(country)
            app_info = row2dict(session.execute(sql_app_info).fetchone())
            rank_change =  app_rank_early-app_rank_now
            app_info["rank_change"] = rank_change
            app_info["rank_now"] = app_rank_now
            app_info["app_id"] = app_id
            return_list.append(app_info)


        session.commit()
        return return_list
    def _get_monitor_company_type(self,app_type=0,rank_start=1,rank_end = 10,rank_time=None,rank_country="cn"):
        session = self.get_session("apple")

        sql_rank = '''SELECT app_id FROM tb_rank where rank BETWEEN %d AND  %d ''' % (rank_start,rank_end)
        sql_rank += ''' AND country = '%s' ''' %(rank_country)
        if app_type in [0,1,2]:
            sql_rank += '''AND rank_type = %d''' % app_type

        sql_rank += ''' AND created_at = "%s"''' % rank_time

        datas = session.execute(sql_rank).fetchall()
        app_ids = [data.app_id for data in datas]

        monitor_company_type = self._get_top_ten_company(session,app_ids,rank_country)

        return monitor_company_type

    def _get_monitor_game_type(self,app_type=0,rank_start=1,rank_end = 10,rank_time=None,rank_country=None):
        session = self.get_session("apple")

        sql_rank = '''SELECT app_id FROM tb_rank where rank BETWEEN %d AND  %d ''' % (rank_start,rank_end)
        sql_rank += ''' AND country = '%s' ''' %(rank_country)
        if app_type in [0,1,2]:
            sql_rank += '''AND rank_type = %d''' % app_type

        sql_rank += ''' AND created_at = "%s"''' % rank_time

        datas = session.execute(sql_rank).fetchall()
        app_ids = [data.app_id for data in datas]

        monitor_game_type = self._get_game_type(session,app_ids)

        return monitor_game_type

        #sql_app_category = '''SELECT DISTINCT app_id,category_id from tb_app_category WHERE app_id in (%s) ''' % (",".join(["'%s'" % x.app_id for x in datas]))

        #category_id = session.execute(sql_app_category).fetchall()
        #print category_id[0]
        #print type(category_id)
        #print len(category_id)

        #sql_category_name = '''SELECT category_id,category_name from tb_category'''

        #category_name = session.execute(sql_category_name).fetchall()
        #category_id2name_hash = {}
        #for category in category_name:
        #    category_id2name_hash[str(category[0])] = category[1]
        #print category_name

        #category_hash =  {}
        #for category_app in category_id:
        #    if category_app[1] < 7001:
        #        continue
        #    if category_hash.get(category_id2name_hash[str(category_app[1])]):
        #        category_hash[category_id2name_hash[str(category_app[1])]]+=1
        #    else:
        #        category_hash[category_id2name_hash[str(category_app[1])]] = 1


        #sql_company = '''SELECT  company_id,company_name from tb_app where app_id in (%s) ''' % (",".join(["'%s'" % x.app_id for x in datas]))

        #companys = session.execute(sql_company).fetchall()
        #company_dict = {}
        #for company in companys:
        #    if company_dict.get(company[1]):
        #        company_dict[company[1]] += 1
        #    else:
        #        company_dict[company[1]] = 1

        #print "="*100
        ##print company_dict

        #company_list = OrderedDict([(k,v) for k,v in company_dict.iteritems()])
        #company_order_dict = OrderedDict(sorted(company_list.items(), key=lambda x: x[1],reverse=True))
        #new_dict = {}
        #for k in company_order_dict.keys()[0:10]:
        #    print "^"*10
        #    new_dict[k] = company_order_dict[k]
        #    print k,company_order_dict[k]

        ##return new_dict
        ##print company_list


        #print "="*100
        #session.commit()
        #return category_hash,new_dict

    def _get_online_list(self,app_type,start_time,end_time,country="cn"):
        print country
        session = self.get_session("apple")
        online_sql = '''SELECT distinct tb_app.app_id,
            tb_app.app_name,
            tb_app.release_date,
            tb_app.icon_Url as icon_url
            FROM tb_app ,tb_rank
            WHERE
            tb_app.app_id = tb_rank.app_id AND
            tb_rank.rank_type = %d AND
            tb_app.release_date BETWEEN "%s" AND "%s"
            ''' % (app_type,start_time,end_time)
        online_sql += ''' AND tb_app.country = '%s' AND tb_rank.country = '%s' ''' %(country,country)
        online_sql += ''' ORDER BY release_date '''
        print online_sql

        res = session.execute(online_sql).fetchall()
        datas = [row2dict(data) for data in res]
        session.commit()

        return datas

    def _get_offline_list(self,app_type,start_time,end_time,country="cn"):
        session = self.get_session("apple")

        online_before = '''SELECT distinct app_id
            FROM tb_rank
            WHERE
            rank_type = %d
            AND created_at  BETWEEN "%s" AND "%s"
            ''' % (app_type, start_time, end_time-datetime.timedelta(days =1))

        online_before += ''' AND country = '%s' ''' % country

        online_end = '''SELECT distinct app_id
            FROM tb_rank
            WHERE
            rank_type = %d
            AND created_at BETWEEN "%s" AND "%s"
            ''' % (app_type,end_time-datetime.timedelta(hours=23,minutes=59,seconds=59),end_time)
        online_end += ''' AND country = '%s' ''' % country

        app_ids_before = [row2dict(data)["app_id"] for data in session.execute(online_before).fetchall()]
        app_ids_end = [row2dict(data)["app_id"] for data in session.execute(online_end).fetchall()]

        offline_app_ids = list(set(app_ids_before)-set(app_ids_end))

        app_info = '''SELECT app_id,app_name,
            icon_Url as icon_url
            FROM
            tb_app
            WHERE
            app_id in (%s)
            ''' % (",".join(["'%s'" % x for x in offline_app_ids]))
        app_info += ''' AND country = '%s' ''' % country
        datas = [row2dict(data) for data in session.execute(app_info).fetchall()]

        session.commit()


        return datas

    def _get_online_game_type(self,app_type,start_time,end_time,country="cn"):
        session = self.get_session("apple")

        online_sql = '''SELECT distinct tb_app.app_id,
            tb_app.app_name,
            tb_app.release_date,
            tb_app.icon_Url as icon_url
            FROM tb_app ,tb_rank
            WHERE
            tb_app.app_id = tb_rank.app_id AND
            tb_rank.rank_type = %d AND
            tb_app.release_date BETWEEN "%s" AND "%s"
            ''' % (app_type,start_time,end_time)
        online_sql += ''' AND tb_app.country = '%s' AND tb_rank.country = '%s' ''' %(country,country)
        online_sql += ''' ORDER BY release_date '''

        res = session.execute(online_sql).fetchall()
        datas = [row2dict(data)["app_id"] for data in res]

        result = self._get_game_type(session,datas)
        session.commit()

        return result
    def _get_online_company_type(self,app_type,start_time,end_time,country="cn"):
        session = self.get_session("apple")

        online_sql = '''SELECT distinct tb_app.app_id,
            tb_app.app_name,
            tb_app.release_date,
            tb_app.icon_Url as icon_url
            FROM tb_app ,tb_rank
            WHERE
            tb_app.app_id = tb_rank.app_id AND
            tb_rank.rank_type = %d AND
            tb_app.release_date BETWEEN "%s" AND "%s"
            ''' % (app_type,start_time,end_time)
        online_sql += ''' AND tb_app.country = '%s' AND tb_rank.country = '%s' ''' %(country,country)
        online_sql += ''' ORDER BY release_date '''

        res = session.execute(online_sql).fetchall()
        datas = [row2dict(data)["app_id"] for data in res]

        result = self._get_top_ten_company(session,datas,country)
        session.commit()

        return result

    def _get_offline_game_type(self,app_type,start_time,end_time,country="cn"):
        session = self.get_session("apple")

        online_before = '''SELECT distinct app_id
            FROM tb_rank
            WHERE
            rank_type = %d
            AND created_at  BETWEEN "%s" AND "%s"
            ''' % (app_type, start_time, end_time-datetime.timedelta(days =1))
        online_before += ''' AND country = '%s' ''' % country

        online_end = '''SELECT distinct app_id
            FROM tb_rank
            WHERE
            rank_type = %d
            AND created_at BETWEEN "%s" AND "%s"
            ''' % (app_type,end_time-datetime.timedelta(hours=23,minutes=59,seconds=59),end_time)
        online_end += ''' AND country = '%s' ''' % country

        app_ids_before = [row2dict(data)["app_id"] for data in session.execute(online_before).fetchall()]
        app_ids_end = [row2dict(data)["app_id"] for data in session.execute(online_end).fetchall()]

        offline_app_ids = list(set(app_ids_before)-set(app_ids_end))

        result = self._get_game_type(session,offline_app_ids)
        session.commit()

        return result
    def _get_offline_company_type(self,app_type,start_time,end_time,country):
        session = self.get_session("apple")

        online_before = '''SELECT distinct app_id
            FROM tb_rank
            WHERE
            rank_type = %d
            AND created_at  BETWEEN "%s" AND "%s"
            ''' % (app_type, start_time, end_time-datetime.timedelta(days =1))
        online_before += ''' AND country = '%s' ''' % country

        online_end = '''SELECT distinct app_id
            FROM tb_rank
            WHERE
            rank_type = %d
            AND created_at BETWEEN "%s" AND "%s"
            ''' % (app_type,end_time-datetime.timedelta(hours=23,minutes=59,seconds=59),end_time)
        online_end += ''' AND country = '%s' ''' % country

        app_ids_before = [row2dict(data)["app_id"] for data in session.execute(online_before).fetchall()]
        app_ids_end = [row2dict(data)["app_id"] for data in session.execute(online_end).fetchall()]

        offline_app_ids = list(set(app_ids_before)-set(app_ids_end))

        result = self._get_top_ten_company(session,offline_app_ids,country)
        session.commit()

        return result

    ## app rank trend sql

    def _get_trend_up_list(self,app_type,start_time,end_time,country="cn"):
        session = self.get_session("apple")

        rank_today = '''SELECT tb_rank.app_id,tb_rank.rank,tb_app.app_name,tb_app.icon_Url as icon_url
            FROM tb_rank,tb_app
            WHERE
            rank_type = %d
            AND tb_rank.app_id = tb_app.app_id
            AND tb_rank.created_at BETWEEN "%s" AND "%s"
            ''' % (app_type,end_time-datetime.timedelta(hours=23,minutes=59,seconds=59),end_time)
        rank_today += ''' AND tb_app.country = '%s' AND tb_rank.country = '%s' ''' %(country,country)

        app_ids_rank_today = [row2dict(data) for data in session.execute(rank_today).fetchall()]

        rank_max_before = '''SELECT app_id,max(rank) AS max_rank
            FROM tb_rank
            WHERE
            rank_type = %d
            AND app_id in (%s)
            AND created_at BETWEEN "%s" AND "%s"
            ''' % (app_type,",".join(["'%s'" % x["app_id"] for x in app_ids_rank_today]),
                    start_time,end_time-datetime.timedelta(days =1))
        rank_max_before += ''' AND country = '%s' ''' % country
        rank_max_before += ''' GROUP BY app_id '''
        rank_max_dict = {}
        rank_max_list = [row2dict(data) for data in session.execute(rank_max_before).fetchall()]
        for rank_max in rank_max_list:
            rank_max_dict[rank_max["app_id"]] = rank_max["max_rank"]

        rank_change_list = []
        for i in app_ids_rank_today:
            rank_change_dict = {}
            rank_i_max = rank_max_dict.get(i["app_id"]) if rank_max_dict.get(i["app_id"]) else 1001
            rank_change = rank_i_max - i["rank"]
            if rank_change <= 0:
                continue
            #rank_change_dict[i["app_id"]] = rank_change
            rank_change_dict["app_id"] = i["app_id"]
            rank_change_dict["rank_change"] = rank_change
            rank_change_dict["app_name"] = i["app_name"]
            rank_change_dict["icon_url"] = i["icon_url"]
            rank_change_list.append(rank_change_dict)


        rank_change_list.sort(key=lambda x:x['rank_change'],reverse=True)

        session.commit()

        return rank_change_list
    def _get_trend_down_list(self,app_type,start_time,end_time,country="cn"):
        session = self.get_session("apple")

        rank_today = '''SELECT tb_rank.app_id,tb_rank.rank,tb_app.app_name,tb_app.icon_Url as icon_url
            FROM tb_rank,tb_app
            WHERE
            rank_type = %d
            AND tb_rank.app_id = tb_app.app_id
            AND tb_rank.created_at BETWEEN "%s" AND "%s"
            ''' % (app_type,end_time-datetime.timedelta(hours=23,minutes=59,seconds=59),end_time)
        rank_today += ''' AND tb_app.country = '%s' AND tb_rank.country = '%s' ''' %(country,country)

        app_ids_rank_today = [row2dict(data) for data in session.execute(rank_today).fetchall()]

        rank_max_before = '''SELECT app_id,min(rank) AS max_rank
            FROM tb_rank
            WHERE
            rank_type = %d
            AND app_id in (%s)
            AND created_at BETWEEN "%s" AND "%s"
            ''' % (app_type,",".join(["'%s'" % x["app_id"] for x in app_ids_rank_today]),
                    start_time,end_time-datetime.timedelta(days =1))
        rank_max_before += ''' AND country = '%s' ''' % country
        rank_max_before += ''' GROUP BY app_id '''
        rank_max_dict = {}
        rank_max_list = [row2dict(data) for data in session.execute(rank_max_before).fetchall()]
        for rank_max in rank_max_list:
            rank_max_dict[rank_max["app_id"]] = rank_max["max_rank"]

        rank_change_list = []
        for i in app_ids_rank_today:
            rank_change_dict = {}
            rank_i_min = rank_max_dict.get(i["app_id"]) if rank_max_dict.get(i["app_id"]) else 1001
            rank_change =  i["rank"] - rank_i_min
            if rank_change <= 0:
                continue
            #rank_change_dict[i["app_id"]] = rank_change
            rank_change_dict["app_id"] = i["app_id"]
            rank_change_dict["rank_change"] = rank_change
            rank_change_dict["app_name"] = i["app_name"]
            rank_change_dict["icon_url"] = i["icon_url"]
            rank_change_list.append(rank_change_dict)


        rank_change_list.sort(key=lambda x:x['rank_change'],reverse=True)

        session.commit()

        return rank_change_list

    def _get_trend_up_type(self,app_type,start_time,end_time,country="cn"):
        session = self.get_session("apple")
        up_list = self._get_trend_up_list(app_type,start_time,end_time,country)
        up_app_ids = [data["app_id"] for data in up_list]
        up_type = self._get_game_type(session,up_app_ids)

        session.commit()

        return up_type

    def _get_trend_down_type(self,app_type,start_time,end_time,country="cn"):
        session = self.get_session("apple")
        down_list = self._get_trend_up_list(app_type,start_time,end_time,country)
        down_app_ids = [data["app_id"] for data in down_list]
        down_type = self._get_game_type(session,down_app_ids)

        session.commit()

        return down_type

    def _get_trend_up_company(self,app_type,start_time,end_time,country="cn"):
        session = self.get_session("apple")
        up_list = self._get_trend_up_list(app_type,start_time,end_time,country)
        up_app_ids = [data["app_id"] for data in up_list]
        up_company = self._get_top_ten_company(session,up_app_ids,country)

        session.commit()

        return up_company

    def _get_trend_down_company(self,app_type,start_time,end_time,country="cn"):
        session = self.get_session("apple")
        down_list = self._get_trend_up_list(app_type,start_time,end_time,country)
        down_app_ids = [data["app_id"] for data in down_list]
        down_company = self._get_top_ten_company(session,down_app_ids)

        session.commit()

        return down_company

    def _get_app_detail_info(self,app_id,country):
        session = self.get_session("apple")
        app_sql = '''SELECT company_name,size,version,star,created_at as date
                    FROM tb_app
                    WHERE
                    app_id = %s AND
                    country = '%s' ''' %(app_id,country)

        sql_result = session.execute(app_sql).fetchone()
        if not sql_result:
            return None
        app_result = row2dict(sql_result)
        session.commit()
        session.close()
        return app_result

    def _get_app_version_list(self,app_id):
        session = self.get_session("apple")
        version_sql = '''SELECT version,DATE_FORMAT(created_at,'%%Y-%%m-%%d') as date
                        FROM tb_version
                        WHERE
                        app_id = %s
                        ORDER BY date DESC''' % app_id

        sql_result = session.execute(version_sql).fetchall()
        if not sql_result:
            return []
        version_list = [row2dict(data) for data in sql_result]
        session.commit()
        session.close()
        return version_list

    def _get_app_rank_with_id(self,app_id,app_type,start_time,end_time,rank_country):
        session = self.get_session("apple")
        rank_sql = '''SELECT rank,DATE_FORMAT(created_at,'%%Y-%%m-%%d') as date,rank_type FROM tb_rank
                    WHERE
                    app_id = %s AND country = '%s'
                    AND created_at BETWEEN '%s' AND '%s' 
                    ORDER BY date DESC''' %(app_id,rank_country,
                            start_time,end_time)
        print rank_sql

        rank_result = session.execute(rank_sql).fetchall()
        rank_list = [row2dict(data) for data in rank_result]
        session.commit()
        session.close()

        return rank_list

