from model.kb_prepare.neo4j_prepare import Neo4jPrepare
import numpy as np
class Task_information():
    def solve_room_borrow(self,entity):
        room = entity['room'][0]
        room_name = room
        if room.find("_")!=-1:
            room_name=room.split("_")[2]

        ans = "\n"

        res = Neo4jPrepare.get_property(room)

        if res['borrow'] == 1:
            ans+=room_name+"的资源书籍均可以外借\n"
        else:
            ans += room_name + "的资源书籍均不可以外借\n"
        return ans

    def solve_res_borrow(self,entity):
        res = entity['res'][0]
        room_res = Neo4jPrepare.get_relation(res,'馆室')
        #print(room_res)
        room = room_res[0]['office_name']
        room_name = room
        if room.find("_")!=-1:
            room_name=room.split("_")[2]
        ans = "\n"
        if room_res[0]['borrow'] == 1:
            ans+=res+"可以外借\n"
        else:
            ans += res + "不可以外借\n"
        return ans

    def solve_restype_borrow(self,entity):
        restype = entity['restype'][0]
        room_res = Neo4jPrepare.get_relation(restype,'馆室')
        #print(room_res)
        yes_room = []
        no_room = []
        for r in room_res:
            room = r['office_name']
            room_name = room
            if room.find("_") != -1:
                room_name = room.split("_")[2]
            if r['borrow'] == 1:
                yes_room.append(room_name)
            else:
                no_room.append(room_name)
        #print(yes_room,no_room)
        ans = "\n"
        if len(yes_room)>0:
            ans += "存放在"
            for y in yes_room[:-1]:
                ans += y+","
            ans += yes_room[len(yes_room)-1]+"的"+restype+"可以外借\n"
        if len(no_room)>0:
            ans += "存放在"
            for y in no_room[:-1]:
                ans += y+","
            ans += no_room[len(no_room)-1]+"的"+restype+"不可以外借\n"
        return ans

    def solve_room_phone(self, entity):
        room = entity['room'][0]
        room_name = room
        if room.find("_") != -1:
            room_name = room.split("_")[2]

        res = Neo4jPrepare.get_property(room)
        #print(res)
        ans = "\n"
        if res['phone'] != '':
            ans += room_name+"的联系电话为："+res['phone']+"\n"
        else:
            ans += "很抱歉，"+room_name+"暂无联系电话\n"
        return ans

    def solve_room_describe(self, entity):
        room = entity['room'][0]
        room_name = room
        if room.find("_") != -1:
            room_name = room.split("_")[2]

        res = Neo4jPrepare.get_property(room)
        #print(res)
        ans = "\n"
        if res['describe'] != '':
            ans += room_name + "：" + res['describe']
        else :
            ans += "对不起，暂时没有"+room_name+"的描述信息\n"

        return ans

    def solve_res_describe(self, entity):
        resource = entity['res'][0]

        res = Neo4jPrepare.get_property(resource)
        #print(res)
        ans = "\n"
        if res['describe'] != '':
            ans += resource + "：" + res['describe']
        else :
            ans += "对不起，暂时没有"+resource+"的描述信息\n"
        return ans

    def solve_restype_describe(self, entity):
        restype = entity['restype'][0]

        res = Neo4jPrepare.get_reverse_relation(restype,'资源')
        res_arr = []
        yes_room = []
        no_room = []
        describe = []
        ans = "\n"
        for r in res:
            #print(r)

            sub_res = Neo4jPrepare.get_property(r['office_name'])
            res_arr.append(sub_res['office_name'])

            if sub_res['describe'] != '':
                yes_room.append(sub_res['office_name'])
                describe.append(sub_res['describe'])

            else :
                no_room.append(sub_res['office_name'])
        ans += restype+"包括"
        for r in res_arr[:-1]:
            ans+=r+","
        ans+=res_arr[-1]+"\n很抱歉，没有"
        for n in no_room[:-1]:
            ans += n+","
        ans += no_room[-1]+"的介绍\n"
        for y in range(len(yes_room)):
            ans += yes_room[y]+":"+describe[y]+"\n"

        return ans



