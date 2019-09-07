# -*- coding: utf-8 -*-
from model.kb_prepare.neo4j_prepare2 import Neo4jPrepare
import numpy as np
class Task_contain():

    """
    统计某层馆室数量
    """
    def solve_floor_count_room(self, entity):
        floor = entity['floor'][0]
        res = Neo4jPrepare.get_reverse_relation(floor, '馆室')
        l = len(res)
        ans = "\n" + floor + "一共有" + str(l) + "间馆室\n"
        return ans

    """
    查出楼层是否有某一间馆室
    """
    def solve_floor_room_a(self,entity):
        floor = entity['floor'][0]
        res = Neo4jPrepare.get_reverse_relation(floor,'馆室')
        ans = "\n"+floor+"有馆室"
        for r in res[:-1]:
            room_name = r['office_name']
            if room_name.find(u"_")!=-1:
                room_name = room_name.split("_")[2]
            ans += room_name+","
        room_name = res[-1]['office_name']
        if room_name.find(u"_") != -1:
            room_name = room_name.split("_")[2]
            ans += room_name + "\n"
        #print(ans)
        return ans

    """
    查出楼层所有的馆室
    """
    def solve_room_floor(self,entity):
        floor = entity['floor'][0]
        room = entity['room'][0]
        res = Neo4jPrepare.get_relation(room,'楼层')
        ans = "\n"
        room_name = room
        if room.find("_")!=-1:
            room_name = room.split("_")[2]
        if res[0]['office_name'] == floor:
            ans += room_name+"在"+floor
        else:
            ans += room_name+"不在"+floor+"\n"+room_name+"在"+res[0]['office_name']+"\n"
        return ans

    """
    处理资源是否在某个楼层的问题，查询资源所在的馆室以及馆室所在的楼层来得到判断结果
    """
    def solve_res_floor(self, entity):
        resource = entity['res'][0]
        floor = entity['floor'][0]
        res = Neo4jPrepare.get_relation(resource,'馆室')
        room_name = res[0]['office_name']
        if room_name.find("_")!=-1:
            room_name = res[0]['office_name'].split("_")[2]
        des_floor = Neo4jPrepare.get_relation(res[0]['office_name'],'楼层')
        ans = "\n"
        if floor == des_floor[0]['office_name']:
            ans += resource+"存放在"+floor
            ans += self.solve_count_res(entity)
        else:
            ans += resource+"不存放在"+floor+"\n"+resource+"存放在"+des_floor[0]['office_name']+"的"+room_name
        return ans

    """
    楼层包括什么资源，通过查询楼层包含馆室的资源类型来汇总得到楼层包含的资源类型
    """
    def solve_res_floor_a(self, entity):

        floor = entity['floor'][0]
        res = Neo4jPrepare.get_reverse_relation(floor,'馆室')
        resource_arr = []
        for r in res:
            res_arr = Neo4jPrepare.get_reverse_relation(r['office_name'],'资源')
            for sub_r in res_arr:
                resource_arr.append(sub_r['belong'])

        resource_arr = np.unique(resource_arr)

        ans = "\n"
        ans += floor+"存放有"
        for sub_r in resource_arr[:-1]:
            ans += sub_r+","
        ans += resource_arr[-1]+"等类型的资源\n"
        return ans

    """
    查出馆室所具有的全部资源
    """
    def solve_res_room(self, entity):
        room = entity['room'][0]

        resource = entity['res'][0]
        res = Neo4jPrepare.get_relation(resource, '馆室')
        ans = "\n"
        if res[0]['office_name'] == room:
            ans += resource+"存放在"+room
            ans += self.solve_count_res(entity)
        else:
            des_room = res[0]['office_name']
            if res[0]['office_name'].find(u"_")!=-1:
                des_room = res[0]['office_name'].split("_")[2]
            ans += resource+"不存放在"+room+"\n"+resource+"存放在"+des_room+"\n"
        return ans
    """
    处理馆室是否有某个资源的问题
    """
    def solve_room_res_a(self, entity):
        room = entity['room'][0]
        room_name = room
        if room.find(u"_")!=-1:
            room_name = room.split("_")[2]
        res = Neo4jPrepare.get_reverse_relation(room,'资源')
        res_dict = {}
        for r in res:
            res_dict[r['belong']]=[]
        res_type = list(res_dict.keys())
        #print(res_type)
        if res_type == []:
            return room_name+"不存放任何资源\n"
        ans = "\n"
        ans += room_name + "存放的资源类型包括："
        for t in res_type[:-1]:
            ans += t+","
        ans += res_type[-1]+"\n"

        for r in res:
            res_dict[r['belong']].append(r['office_name'])
        for t in res_type:
            ans += t+"："
            for r in res_dict[t][:-1]:
                ans += r+","
            ans += res_dict[t][-1] +"\n"
        return ans

    """
    资源数量问题
    """

    def solve_count_res(self, entity):
        resource = entity['res'][0]
        res = Neo4jPrepare.get_property(resource)
        ans = "\n"
        if res['count']!='nan':
            ans += resource+"的数量是:"+str(res['count'])+"本（份）\n"
        else:
            ans += "很抱歉，"+resource+"暂时没有数据信息\n"
        return ans

    """
    某一类资源数量问题
    """
    def solve_count_restype(self, entity):
        restype = entity['restype'][0]
        #res = Neo4jPrepare.get_property(restype)
        ans = "\n"
        describe = ""
        num = 0

        type = Neo4jPrepare.get_reverse_relation(restype,'资源类型')
        #print(type)
        for t in type:
            type_num = 0
            res_r = Neo4jPrepare.get_reverse_relation(t['office_name'],'资源')
            for r in res_r:
                if r['count'] =='nan':
                    continue
                type_num += int(r['count'])
                num += int(r['count'])
            if type_num != 0:
                describe = "其中包括:\n"+t['office_name'] + str(type_num) + "份\n"

        res_res = Neo4jPrepare.get_reverse_relation(restype, '资源')
        #print(res_res)
        other_num = 0
        for r in res_res:
            if r['count'] == 'nan':
                continue
            num += int(r['count'])
            other_num += int(r['count'])
        if other_num != 0 and describe != 'nan':
            describe += "以及其他" + restype + str(other_num) + "份\n"

        # print(num)
        if num!=0:
            ans += restype+"的数量是:"+str(num)+"本（份）\n"
            ans += describe
        else:
            ans += "很抱歉，"+restype+"暂时没有数据信息\n"
        return ans

    """
    某资源是否是某类资源问题
    """
    def solve_res_res_h(self, entity):
        restype = entity['restype'][0]
        resource = entity['res'][0]
        res_arr = []
        res = Neo4jPrepare.get_reverse_relation(restype,'资源')
        ans = "\n"
        for r in res[:-1]:
            res_arr.append(r['office_name'])
        if resource in res_arr:

            ans += "是的,"+resource + "属于"+restype+"\n"
        else:
            ans += "很抱歉," + resource + "不属于" + restype + "\n"
        return ans

    """
    某类资源包含的所有资源
    """
    def solve_res_res_a(self, entity):
        restype = entity['restype'][0]
        res = Neo4jPrepare.get_reverse_relation(restype,'资源')
        ans = "\n"+restype+"包含的资源有：\n"
        for r in res[:-1]:
            ans += r['office_name']+","
        ans += res[-1]['office_name'] + "\n"
        return ans

    """
    资源类型（资源的中级类别）属于哪一大类问题（资源的最高类别）
    """
    def solve_res_res_t(self, entity):
        restype = entity['restype'][0]
        res = Neo4jPrepare.get_property(restype)
        ans = "\n"+restype+"属于"+res['belong']
        return ans

    """
    馆室有几楼的
    """
    def solve_count_floor(self, entity):
        area = entity['area'][0]
        res = Neo4jPrepare.get_reverse_relation(area,'楼层')
        #print(res)
        l = len(res)
        ans = "\n"+area+"一共有"+str(l)+"层\n"
        return ans

    """
    国图有几个馆区
    """
    def solve_library_area(self):
        res = Neo4jPrepare.get_relation("国家图书馆","馆区")
        print(res)
        ans = "\n国家图书馆包括"
        for r in res[:-1]:
            ans += r['office_name']+","
        ans += res[-1]['office_name']+"\n"
        return ans

    """
    国图包含哪些资源类型，查出所有的资源类别
    """

    def solve_library_res_a(self):
        res = Neo4jPrepare.get_entity("资源类型")
        ans = "\n国家图书馆馆藏的资源类别包括:\n"
        for r in res[:-1]:
            ans += r['office_name']+","
        ans += res[-1]['office_name']+"\n"
        return ans
    """
    国图是否提供某一服务
    """

    def solve_service_exit(self, entity):
        # print(entity)
        service = entity['service']
        # res = Neo4jPrepare.get_property(service)
        ans = "\n"
        if len(service) > 0:
            ans += "国家图书馆提供" + service[0] + "\n"
            #print("aaa",ans)
            room = Neo4jPrepare.get_relation(service[0], "馆室")
            if len(room)<=0:
                return ans
            ans += "您可以去"
            for r in room[:-1]:
                ans += r['office_name'] + ","
            ans += room[-1]['office_name'] + "接受该服务\n"
        else:
            ans += "很抱歉，国家图书馆不提供该服务"
        return ans

    """
    国图提供什么服务
    """

    def solve_service_exit_all(self):
        # print(entity)
        #service = entity['service']
        res = Neo4jPrepare.get_entity('服务')
        ans = "\n国家图书馆提供的服务包括"
        for sub_result in res[:-1]:
            ans += sub_result['office_name']+","
        ans += res[-1]['office_name']+"\n"
        return ans

    """
    查出国图资源分布，即查出国图所有馆区所包含的资源
    """
    def solve_library_res(self):
        res = Neo4jPrepare.get_relation("国家图书馆","馆区")
        ans = ""
        for r in res:
            area_dict = {'area':[r['office_name']]}
            ans += self.solve_area_res_a(area_dict)
        return ans

    """"
    馆区包含什么资源类型
    """
    def solve_area_res_a(self,entity):
        area = entity['area'][0]
        res = Neo4jPrepare.get_reverse_relation(area, '馆室')
        resource_arr = []
        for r in res:
            res_arr = Neo4jPrepare.get_reverse_relation(r['office_name'], '资源')
            for sub_r in res_arr:
                resource_arr.append(sub_r['belong'])

        resource_arr = np.unique(resource_arr)

        ans = "\n"
        ans += area + "存放有"
        for sub_r in resource_arr[:-1]:
            ans += sub_r + ","
        ans += resource_arr[-1] + "等类型的资源\n"
        return ans

    """
    馆室有什么服务
    """
    def solve_service_room_all(self,entity):
        room = entity['room'][0]
        res = Neo4jPrepare.get_reverse_relation(room, '服务')
        ans = "\n"
        if len(res)>0:
            ans += room+"提供的服务包括"
            for r in res[:-1]:
                ans+=r['office_name']+","
            ans += res[-1]['office_name']+"\n"
        else:
            ans += room+"不提供任何服务\n"
        return ans

    """
    馆室有没有某一服务
    """

    def solve_service_room_exit(self, entity):
        room = entity['room'][0]
        service = entity['service'][0]
        res = Neo4jPrepare.get_reverse_relation(room, '服务')
        ans = "\n"
        for r in res:
            if r['office_name'] == service:
                ans += room + "提供"+service+"\n"
                return ans

        ans += room + "不提供"+service+"\n"
        #print(ans)
        return ans

    """
    开架阅览室有哪些
    """

    def solve_open_room(self):
        res = Neo4jPrepare.get_entity('馆室')
        room_arr = []
        for r in res:
            if r['open'] == '1':
                room_arr.append(r['office_name'])
        ans = "\n开架阅览室包括"
        for sub_room in room_arr[:-1]:
            ans += sub_room + ","
        ans += room_arr[-1] + "\n"
        return ans

























