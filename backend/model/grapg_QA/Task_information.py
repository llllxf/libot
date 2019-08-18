from model.kb_prepare.neo4j_prepare import Neo4jPrepare
import numpy as np
class Task_information():
    def solve_room_borrow(self,entity):
        room = entity['room'][0]
        room_name = room
        if room.find("_")!=-1:
            room_name=room.split("_")[2]

        res = Neo4jPrepare.get_property(room)
        ans = "\n"
        print(res)
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

    def solve_room_phone(self, entity):
        room = entity['room'][0]
        room_name = room
        if room.find("_") != -1:
            room_name = room.split("_")[2]

        res = Neo4jPrepare.get_property(room)
        #print(res)
        ans = "\n"
        ans += room_name+"的联系电话为："+res['phone']
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
            ans += resource + "的介绍：" + res['describe']
        else :
            ans += "对不起，暂时没有"+resource+"的描述信息\n"
        return ans

