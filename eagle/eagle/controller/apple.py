#!/usr/bin/pytyhon
# coding=utf-8

import calendar
from flask import json
from datetime import datetime
from datetime import date
from datetime import timedelta


class BaseApple():

    def _format_query_string(self,payload):
        query_string = payload
        time_today = datetime.now().strftime( '%Y-%m-%d' )
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = query_string.get('start_time',[time_today])[0]
        rank_end = query_string.get('end_time',[time_today])[0]
        rank_country = query_string.get('country',['cn'])[0]
        start_time_list = rank_start.split("-")
        end_time_list = rank_end.split("-")
        start_year,start_month,start_day = int(start_time_list[0]),int(start_time_list[1]),int(start_time_list[2])
        end_year,end_month,end_day = int(end_time_list[0]),int(end_time_list[1]),int(end_time_list[2])
        start_time = datetime(start_year,start_month,start_day,0,0)
        end_time = datetime(end_year,end_month,end_day,23,59,59)
        params = {}
        params["rank_type"] = rank_type
        params["rank_country"] = rank_country
        params["start_time"] = start_time
        params["end_time"] = end_time

        return params




class Apple(BaseApple):


    def _get_control1_data(self):
        data =  self.db_inst._get_app_detail_with_id("123")
        payload = {"datas":data}
        return json.dumps(payload)

    def _get_month_online(self,query_string):
        time_today = datetime.now().strftime( '%Y-%m-%d' )
        start = query_string.get('start_time',[time_today])[0].split("-")
        end = query_string.get('end_time',[time_today])[0].split("-")
        start_year = int(start[0])
        start_month = int(start[1])

        end_year = int(end[0])
        end_month = int(end[1])

        country = query_string.get('country',['cn'])[0]
        return_list = []
        if start_year < end_year:
            for online_year in xrange(start_year,end_year+1):
                if online_year == start_year:
                    for online_month in xrange(start_month,13):

                        month_days = calendar.monthrange(online_year,online_month)[1]
                        start_time = datetime(online_year,online_month,1,0,0,1)
                        end_time = datetime(online_year,online_month,month_days,23,59,59)
                        return_msg = self.db_inst._get_release_count(start_time,end_time,country)
                        return_msg["year"] = online_year
                        return_msg["month"] = online_month
                        return_list.append(return_msg)
                elif online_year == end_year:
                    for online_month in xrange(1,end_month+1):
                        month_days = calendar.monthrange(online_year,online_month)[1]
                        start_time = datetime(online_year,online_month,1,0,0,1)
                        end_time = datetime(online_year,online_month,month_days,23,59,59)
                        return_msg = self.db_inst._get_release_count(start_time,end_time,country)
                        return_msg["year"] = online_year
                        return_msg["month"] = online_month
                        return_list.append(return_msg)

                else:
                    for online_month in xrange(1,13):
                        month_days = calendar.monthrange(online_year,online_month)[1]
                        start_time = datetime(online_year,online_month,1,0,0,1)
                        end_time = datetime(online_year,online_month,month_days,23,59,59)
                        return_msg = self.db_inst._get_release_count(start_time,end_time,country)
                        return_msg["year"] = online_year
                        return_msg["month"] = online_month
                        return_list.append(return_msg)
        elif start_year == end_year:
            online_year = start_year
            for online_month in xrange(start_month,end_month+1):
                        month_days = calendar.monthrange(online_year,online_month)[1]
                        start_time = datetime(online_year,online_month,1,0,0,1)
                        end_time = datetime(online_year,online_month,month_days,23,59,59)
                        return_msg = self.db_inst._get_release_count(start_time,end_time,country)
                        return_msg["year"] = online_year
                        return_msg["month"] = online_month
                        return_list.append(return_msg)

        payload = {"status":0,"message":"success","data":return_list}
        return json.dumps(payload)

    def _get_index_online_type(self,year,month,query):
        time_today = datetime.now().strftime( '%Y-%m-%d' )
        rank_start = query.get('start_time',[time_today])[0]
        rank_end = query.get('end_time',[time_today])[0]
        rank_country = query.get('country',['cn'])[0]
        game_type = query.get("type",[0])[0]
        month_days = calendar.monthrange(year,month)[1]
        start_time = datetime(year,month,1,0,0,1)
        end_time = datetime(year,month,month_days,23,59,59)

        result = self.db_inst._get_index_game_type(game_type,start_time,end_time)

        payload = { "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                         "game_type",
                         "count"],
                        "list":result}}
        return json.dumps(payload)


    def _get_day_online(self,query_string):
        time_today = datetime.now().strftime( '%Y-%m-%d' )
        index_time= query_string.get('start_time',[time_today])[0].split("-")
        online_year = int(index_time[0])
        online_month = int(index_time[1])
        country = query_string.get('country',['cn'])[0]
        online_day_hash = []
        month_days = calendar.monthrange(online_year,online_month)[1]
        for day in xrange(1,month_days+1):
            start_time = datetime(online_year,online_month,day,0,0,1)
            end_time = datetime(online_year,online_month,day,23,59,59)
            app_list = self.db_inst._get_app_info_with_release_date(start_time,end_time,country)
            if day<10:
                day = "0"+str(day)
            if online_month<10:
                month = "0"+str(online_month)
            else:
                month = online_month
            key = "%s-%s-%s" %(online_year,month,day)
            for i in app_list:
                i["date"] = key
                online_day_hash.append(i)

        payload = {"status":0,"message":"success","data":{"list":online_day_hash}}

        return json.dumps(payload)


    def _get_monitor_rank_list(self,query_string):
        today = query_string.get('time',[date.today().strftime('%Y-%m-%d')])[0]
        today = today.split("-")
        year = int(today[0])
        month = int(today[1])
        day = int(today[2])
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = int(query_string.get('start',[1])[0])
        rank_end = int(query_string.get('end',[1000])[0])
        rank_country = query_string.get('country',['cn'])[0]
        rank_time =  datetime(year,month,day,0,0,0)
        rank_list = self.db_inst._get_rank_list(rank_type,rank_start,rank_end,rank_time,rank_country)
        payload = {"status":0,"message":"success","data":{"list":rank_list}}

        return json.dumps(payload)


    def _get_monitor_game_type(self,query_string):
        today = query_string.get('time',[date.today().strftime('%Y-%m-%d')])[0]
        today = today.split("-")
        year = int(today[0])
        month = int(today[1])
        day = int(today[2])
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = int(query_string.get('start',[1])[0])
        rank_end = int(query_string.get('end',[1000])[0])
        rank_country = query_string.get('country',['cn'])[0]
        rank_time =  datetime(year,month,day,0,0,0)

        rank_game_type = self.db_inst._get_monitor_game_type(rank_type,rank_start,rank_end,rank_time,rank_country)

        #print rank_game_type
        payload = { "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                         "game_type",
                         "count"],
                        "list":rank_game_type}
                    }
        return json.dumps(payload)

    def _get_monitor_company_type(self,query_string):
        today = query_string.get('time',[date.today().strftime('%Y-%m-%d')])[0]
        today = today.split("-")
        year = int(today[0])
        month = int(today[1])
        day = int(today[2])
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = int(query_string.get('start',[1])[0])
        rank_end = int(query_string.get('end',[1000])[0])
        rank_country = query_string.get('country',['cn'])[0]
        rank_time =  datetime(year,month,day,0,0,0)

        company_type = self.db_inst._get_monitor_company_type(rank_type,rank_start,rank_end,rank_time,rank_country)
        payload = { "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                         "company_name",
                         "count"],
                        "list":company_type}
                    }
        return json.dumps(payload)


    ### About app get online & offline func below

    def _get_online_list(self, query_string):
        time_today = datetime.now().strftime( '%Y-%m-%d' )
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = query_string.get('start_time',[time_today])[0]
        rank_end = query_string.get('end_time',[time_today])[0]
        rank_country = query_string.get('country',['cn'])[0]
        start_time_list = rank_start.split("-")
        end_time_list = rank_end.split("-")
        start_year,start_month,start_day = int(start_time_list[0]),int(start_time_list[1]),int(start_time_list[2])
        end_year,end_month,end_day = int(end_time_list[0]),int(end_time_list[1]),int(end_time_list[2])
        start_time = datetime(start_year,start_month,start_day,0,0)
        end_time = datetime(end_year,end_month,end_day,23,59,59)
        result = self.db_inst._get_online_list(rank_type,start_time,end_time,rank_country)
        payload = { "status":0,"message": "success",
                    "data":{"list":result}
                }

        return json.dumps(payload)


    def _get_offline_list(self, query_string):
        time_today = datetime.now().strftime( '%Y-%m-%d' )
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = query_string.get('start_time',[time_today])[0]
        rank_end = query_string.get('end_time',[time_today])[0]
        rank_country = query_string.get('country',['cn'])[0]
        start_time_list = rank_start.split("-")
        end_time_list = rank_end.split("-")
        start_year,start_month,start_day = int(start_time_list[0]),int(start_time_list[1]),int(start_time_list[2])
        end_year,end_month,end_day = int(end_time_list[0]),int(end_time_list[1]),int(end_time_list[2])
        start_time = datetime(start_year,start_month,start_day,0,0)
        end_time = datetime(end_year,end_month,end_day,23,59,59)

        result = self.db_inst._get_offline_list(rank_type,start_time,end_time,rank_country)
        payload = { "status":0,"message": "success",
                    "data":{"list":result}
                }

        return json.dumps(payload)

    def _get_online_type(self, query_string):

        time_today = datetime.now().strftime( '%Y-%m-%d' )
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = query_string.get('start_time',[time_today])[0]
        rank_end = query_string.get('end_time',[time_today])[0]
        rank_country = query_string.get('country',['cn'])[0]
        start_time_list = rank_start.split("-")
        end_time_list = rank_end.split("-")
        start_year,start_month,start_day = int(start_time_list[0]),int(start_time_list[1]),int(start_time_list[2])
        end_year,end_month,end_day = int(end_time_list[0]),int(end_time_list[1]),int(end_time_list[2])
        start_time = datetime(start_year,start_month,start_day,0,0)
        end_time = datetime(end_year,end_month,end_day,23,59,59)

        result = self.db_inst._get_online_game_type(rank_type,start_time,end_time,rank_country)
        payload = { "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                         "game_type",
                         "count"],
                        "list":result}
                    }


        return json.dumps(payload)
    def _get_online_company_type(self, query_string):

        time_today = datetime.now().strftime( '%Y-%m-%d' )
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = query_string.get('start_time',[time_today])[0]
        rank_end = query_string.get('end_time',[time_today])[0]
        rank_country = query_string.get('country',['cn'])[0]
        start_time_list = rank_start.split("-")
        end_time_list = rank_end.split("-")
        start_year,start_month,start_day = int(start_time_list[0]),int(start_time_list[1]),int(start_time_list[2])
        end_year,end_month,end_day = int(end_time_list[0]),int(end_time_list[1]),int(end_time_list[2])
        start_time = datetime(start_year,start_month,start_day,0,0)
        end_time = datetime(end_year,end_month,end_day,23,59,59)

        result = self.db_inst._get_online_company_type(rank_type,start_time,end_time,rank_country)
        payload = { "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                         "company_name",
                         "count"],
                        "list":result}
                    }

        return json.dumps(payload)
    def _get_offline_type(self, query_string):

        time_today = datetime.now().strftime( '%Y-%m-%d' )
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = query_string.get('start_time',[time_today])[0]
        rank_end = query_string.get('end_time',[time_today])[0]
        rank_country = query_string.get('country',['cn'])[0]
        start_time_list = rank_start.split("-")
        end_time_list = rank_end.split("-")
        start_year,start_month,start_day = int(start_time_list[0]),int(start_time_list[1]),int(start_time_list[2])
        end_year,end_month,end_day = int(end_time_list[0]),int(end_time_list[1]),int(end_time_list[2])
        start_time = datetime(start_year,start_month,start_day,0,0)
        end_time = datetime(end_year,end_month,end_day,23,59,59)

        result = self.db_inst._get_offline_game_type(rank_type,start_time,end_time,rank_country)
        payload = { "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                         "game_type",
                         "count"],
                        "list":result}
                    }

        return json.dumps(payload)
    def _get_offline_company_type(self, query_string):

        time_today = datetime.now().strftime( '%Y-%m-%d' )
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = query_string.get('start_time',[time_today])[0]
        rank_end = query_string.get('end_time',[time_today])[0]
        rank_country = query_string.get('country',['cn'])[0]
        start_time_list = rank_start.split("-")
        end_time_list = rank_end.split("-")
        start_year,start_month,start_day = int(start_time_list[0]),int(start_time_list[1]),int(start_time_list[2])
        end_year,end_month,end_day = int(end_time_list[0]),int(end_time_list[1]),int(end_time_list[2])
        start_time = datetime(start_year,start_month,start_day,0,0)
        end_time = datetime(end_year,end_month,end_day,23,59,59)

        result = self.db_inst._get_offline_company_type(rank_type,start_time,end_time,rank_country)
        payload = { "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                         "company_name",
                         "count"],
                        "list":result}
                    }

        return json.dumps(payload)

    ## About app rank trend func below

    def _get_trend_up_list(self,payload):
        query_string = payload
        time_today = datetime.now().strftime( '%Y-%m-%d' )
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = query_string.get('start_time',[time_today])[0]
        rank_end = query_string.get('end_time',[time_today])[0]
        rank_country = query_string.get('country',['cn'])[0]
        start_time_list = rank_start.split("-")
        end_time_list = rank_end.split("-")
        start_year,start_month,start_day = int(start_time_list[0]),int(start_time_list[1]),int(start_time_list[2])
        end_year,end_month,end_day = int(end_time_list[0]),int(end_time_list[1]),int(end_time_list[2])
        start_time = datetime(start_year,start_month,start_day,0,0)
        end_time = datetime(end_year,end_month,end_day,23,59,59)

        up_list = self.db_inst._get_trend_up_list(rank_type,start_time,end_time,rank_country)
        payload = { "status":0,"message": "success",
                    "data":{"list":up_list}
                }

        return json.dumps(payload)


    def _get_trend_down_list(self,payload):
        query_string = payload
        time_today = datetime.now().strftime( '%Y-%m-%d' )
        rank_type = int(query_string.get('type',[0])[0])
        rank_start = query_string.get('start_time',[time_today])[0]
        rank_end = query_string.get('end_time',[time_today])[0]
        rank_country = query_string.get('country',['cn'])[0]
        start_time_list = rank_start.split("-")
        end_time_list = rank_end.split("-")
        start_year,start_month,start_day = int(start_time_list[0]),int(start_time_list[1]),int(start_time_list[2])
        end_year,end_month,end_day = int(end_time_list[0]),int(end_time_list[1]),int(end_time_list[2])
        start_time = datetime(start_year,start_month,start_day,0,0)
        end_time = datetime(end_year,end_month,end_day,23,59,59)

        down_list = self.db_inst._get_trend_down_list(rank_type,start_time,end_time,rank_country)
        payload = { "status":0,"message": "success",
                    "data":{"list":down_list}
                }

        return json.dumps(payload)

    def _get_trend_up_type(self,payload):
        params = self._format_query_string(payload)
        rank_type = params["rank_type"]
        rank_country = params["rank_country"]
        start_time = params["start_time"]
        end_time = params["end_time"]

        return_list = self.db_inst._get_trend_up_type(rank_type,start_time,end_time,rank_country)
        payload = { "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                         "game_type",
                         "count"],
                        "list":return_list}
                    }

        payload = json.dumps(payload)
        return payload

    def _get_trend_down_type(self,payload):
        params = self._format_query_string(payload)
        rank_type = params["rank_type"]
        rank_country = params["rank_country"]
        start_time = params["start_time"]
        end_time = params["end_time"]
        return_list = self.db_inst._get_trend_down_type(rank_type,start_time,end_time,rank_country)
        payload = { "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                         "game_type",
                         "count"],
                        "list":return_list}
                    }

        payload = json.dumps(payload)

        return payload

    def _get_trend_up_company(self,payload):
        params = self._format_query_string(payload)
        rank_type = params["rank_type"]
        rank_country = params["rank_country"]
        start_time = params["start_time"]
        end_time = params["end_time"]
        return_list = self.db_inst._get_trend_up_company(rank_type,start_time,end_time,rank_country)
        payload = { "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                         "company_name",
                         "count"],
                        "list":return_list}
                    }

        payload = json.dumps(payload)

        return payload

    def _get_trend_down_company(self,payload):
        params = self._format_query_string(payload)
        rank_type = params["rank_type"]
        rank_country = params["rank_country"]
        start_time = params["start_time"]
        end_time = params["end_time"]
        return_list = self.db_inst._get_trend_down_company(rank_type,start_time,end_time,rank_country)

        payload = { "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                         "company_name",
                         "count"],
                        "list":return_list}
                    }
        payload = json.dumps(payload)

        return payload

    def _get_company_rank_list(self,payload):
        pass

    def _get_company_type(self,payload):
        pass

    def _get_company_line(self,payload):
        pass

    def _get_app_detail_info(self,payload):
        app_id = payload.get("id",[None])[0]
        country = payload.get("country",["cn"])[0]
        if not app_id:
            payload = {
                "status": 0,
                "message": "操作成功",
                "data": {
                    "company_name": None,
                    "size": None,
                    "version": None,
                    "date": None,
                    "star": None}
            }
            payload = json.dumps(payload)
            return payload
        app_info = self.db_inst._get_app_detail_info(app_id,country)
        payload = {
            "status": 0,
            "message": "success",
            "data": app_info
        }
        payload = json.dumps(payload)
        return payload

    def _get_app_version_list(self,payload):
        app_id = payload.get("id",[None])[0]
        if not app_id:
            payload = {
                "status": 0,
                "message": "success",
                "data": {
                    "list": []
                }
            }
            payload = json.dumps(payload)
            return payload
        version_list = self.db_inst._get_app_version_list(app_id)
        payload = {
            "status": 0,
            "message": "success",
            "data": {
                "list":version_list
            }
        }
        payload = json.dumps(payload)
        return payload

    def _get_app_chart_data(self,payload):
        time_today = datetime.now().strftime('%Y-%m-%d')
        app_id = payload.get("id",[None])[0]
        rank_start = payload.get("start_time",[time_today])[0]
        rank_end = payload.get("end_time",[time_today])[0]
        start_time_list = rank_start.split("-")
        end_time_list = rank_end.split("-")
        start_year,start_month,start_day = int(start_time_list[0]),int(start_time_list[1]),int(start_time_list[2])
        end_year,end_month,end_day = int(end_time_list[0]),int(end_time_list[1]),int(end_time_list[2])
        start_time = datetime(start_year,start_month,start_day,0,0)
        end_time = datetime(end_year,end_month,end_day,23,59,59)
        return_list = []
        while start_time < end_time:
            data_list = []
            data_list.append(start_time.strftime('%Y-%m-%d'))
            data_list.append(0)
            data_list.append(0)
            data_list.append(0)
            new_end_time = start_time + timedelta(hours=23,minutes=59,seconds=59)
            rank_list = self.db_inst._get_app_rank_with_id(app_id,0,start_time,new_end_time,'cn')
            for rank in rank_list:
                if rank['rank_type'] == 0:
                    data_list[1] = rank['rank']
                elif rank['rank_type'] == 1:
                    data_list[2] = rank['rank']
                elif rank['rank_type'] == 2:
                    data_list[3] = rank['rank']
            return_list.append(data_list)

            start_time += timedelta(days=1)

        payload = {
                    "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns": [
                            "date",
                            "free",
                            "paid",
                            "grossing"
                            ],
                        "list":return_list
                    }
                }
        payload = json.dumps(payload)
        return payload

    def _get_index_chart_data(self,payload):
        result = self._get_month_online(payload)
        result_list = json.loads(result)["data"]
        return_list = []
        for i in result_list:
            chart_list = []
            chart_list.append(str(i['year'])+'-'+str(i['month']))
            chart_list.append(i['release_count'])
            chart_list.append(i['top_100'])
            return_list.append(chart_list)

        payload = {
                    "status": 0,
                    "message": "success",
                    "data": {
                        "alias": {},
                        "columns":[
                            "month",
                            "release_count",
                            "top_100"
                            ],
                        "list": return_list
                        }
                }
        payload = json.dumps(payload)
        return payload

