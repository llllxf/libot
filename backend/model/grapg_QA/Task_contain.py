# -*- coding: utf-8 -*-
from model.kb_prepare.neo4j_prepare import Neo4jPrepare
import numpy as np
class Task_contain():
    def solve_floor_count_room(self, entity):
        #print("<<<")
        floor = entity['floor'][0]
        res = Neo4jPrepare.get_reverse_relation(floor, '馆室')
        # print(res)
        l = len(res)
        ans = "\n" + floor + "一共有" + str(l) + "间馆室\n"
        return ans
    def solve_floor_room_a(self,entity):
        floor = entity['floor'][0]
        res = Neo4jPrepare.get_reverse_relation(floor,'馆室')
        ans = "\n"+floor+"有馆室"
        for r in res[:-1]:
            room_name = r['office_name']
            if room_name.find("_")!=-1:
                room_name = room_name.split("_")[2]
            ans += room_name+","
        room_name = res[-1]['office_name']
        if room_name.find("_") != -1:
            room_name = room_name.split("_")[2]
            ans += room_name + "\n"
        #print(ans)
        return ans

    def solve_room_floor(self,entity):
        floor = entity['floor'][0]
        room = entity['room'][0]
        res = Neo4jPrepare.get_relation(room,'楼层')
        ans = "\n"
        room_name = room
        if room.find("_")!=-1:
            room_name = room.split("_")[2]
        #print(res['office_name'])
        #print(res[0]['office_name'],floor)
        if res[0]['office_name'] == floor:
            ans += room_name+"在"+floor
        else:
            ans += room_name+"不在"+floor+"\n"+room_name+"在"+res[0]['office_name']+"\n"
        return ans

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
        else:
            ans += resource+"不存放在"+floor+"\n"+resource+"存放在"+des_floor[0]['office_name']+"的"+room_name
        return ans

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


    def solve_res_room(self, entity):
        room = entity['room'][0]
        resource = entity['res'][0]
        res = Neo4jPrepare.get_relation(resource, '馆室')
        room_name = room
        ans = "\n"
        if room.find("_")!=-1:
            room_name = room.split("_")[2]
        if res[0]['office_name'] == room:
            ans += resource+"存放在"+room_name
        else:
            des_room = res[0]['office_name']
            if res[0]['office_name'].find("_")!=-1:
                des_room = res[0]['office_name'].split("_")[2]
            ans += resource+"不存放在"+room_name+"\n"+resource+"存放在"+des_room+"\n"
        return ans

    def solve_room_res_a(self, entity):
        room = entity['room'][0]
        room_name = room
        if room.find("_")!=-1:
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

    def solve_count_res(self, entity):
        resource = entity['res'][0]
        res = Neo4jPrepare.get_property(resource)
        ans = "\n"
        if res['count']!='':
            ans += resource+"的数量是:"+str(res['count'])+"本（份）\n"
        else:
            ans += "很抱歉，"+resource+"暂时没有数据信息\n"
        return ans

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
                if r['count'] =='':
                    continue
                type_num += int(r['count'])
                num += int(r['count'])
            if type_num != 0:
                describe = "其中包括:\n"+t['office_name'] + str(type_num) + "份\n"

        res_res = Neo4jPrepare.get_reverse_relation(restype, '资源')
        #print(res_res)
        other_num = 0
        for r in res_res:
            if r['count'] == '':
                continue
            num += int(r['count'])
            other_num += int(r['count'])
        if other_num != 0 and describe != '':
            describe += "以及其他" + restype + str(other_num) + "份\n"

        # print(num)
        if num!=0:
            ans += restype+"的数量是:"+str(num)+"本（份）\n"
            ans += describe
        else:
            ans += "很抱歉，"+restype+"暂时没有数据信息\n"
        return ans

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

    def solve_res_res_a(self, entity):
        restype = entity['restype'][0]
        res = Neo4jPrepare.get_reverse_relation(restype,'资源')
        ans = "\n"+restype+"包含的资源有：\n"
        for r in res[:-1]:
            ans += r['office_name']+","
        ans += res[-1]['office_name'] + "\n"
        return ans

    def solve_res_res_t(self, entity):
        restype = entity['restype'][0]
        res = Neo4jPrepare.get_property(restype)
        ans = "\n"+restype+"属于"+res['belong']
        return ans

    def solve_count_floor(self, entity):
        area = entity['area'][0]
        res = Neo4jPrepare.get_reverse_relation(area,'楼层')
        #print(res)
        l = len(res)
        ans = "\n"+area+"一共有"+str(l)+"层\n"
        return ans

    def solve_library_area(self):
        res = Neo4jPrepare.get_relation("国家图书馆","馆区")
        print(res)
        ans = "\n国家图书馆包括"
        for r in res[:-1]:
            ans += r['office_name']+","
        ans += res[-1]['office_name']+"\n"
        return ans
















