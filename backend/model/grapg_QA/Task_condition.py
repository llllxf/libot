from model.kb_prepare.neo4j_prepare import Neo4jPrepare

class Task_condition():
    def solve_room_card_a(self, entity):
        room = entity['room'][0]
        room_name = room
        if room.find("_")!=-1:
            room_name = room.split("_")[2]

        res = Neo4jPrepare.get_property(room)
        ans = "\n"
        if res['card'] != '':
            ans += "进"+room_name+"需要满足的条件为：\n"
            if res['card'].find("，") != -1:
                card_arr = res['card'].split("，")
                for c in card_arr:
                    c_res = Neo4jPrepare.get_property(c)
                    ans += "年龄"+c_res['age']+"的读者可以持"+c_res['office_name'] + "进入"+room_name+"\n"
            else :
                c_res = Neo4jPrepare.get_property(res['card'])
                ans += "年龄" + c_res['age'] + "的读者可以持" + c_res['office_name'] + "进入" + room_name + "\n"
        else:
            ans += "进入该馆室无需证件\n"
        return ans










