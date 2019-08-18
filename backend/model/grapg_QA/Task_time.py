from model.kb_prepare.neo4j_prepare import Neo4jPrepare
class Task_time():
    def solve_room_time(self,entity):
        room = entity['room'][0]
        res = Neo4jPrepare.get_property(room)
        #print(res)
        open_day = res['open_date']
        workday_time = res['monday_open']
        weekend_time = res['sunday_open']
        ans = "\n"+room+"开放日为："+open_day+"\n工作日开放时间为："+workday_time+"\n周末开放时间为："+weekend_time+"\n"

        return ans

    def solve_room_res_time(self,entity):
        room = entity['room'][0]
        #print(entity)
        res = Neo4jPrepare.get_property(room)
        #print("================================",res)
        workday_time = res['monday_borrow']
        weekend_time = res['sunday_borrow']
        ans = "\n"+room+"的书籍材料借阅时间为："
        if workday_time != '':
            ans += "\n工作日："+workday_time
        if weekend_time != '':
            ans += "\n周未：" + weekend_time
        return ans+"\n"


    def solve_res_time(self,entity):
        resource = entity['res'][0]
        #print(Neo4jPrepare.get_property(resource))
        room = Neo4jPrepare.get_property(resource)['room']
        res = Neo4jPrepare.get_property(room)
        workday_time = res['monday_borrow']
        weekend_time = res['sunday_borrow']
        #ans = "\n" + resource + "的借阅时间为：\n工作日：" + workday_time + "\n周未：" + weekend_time + "\n"
        ans = "\n" + room + "的借阅时间为："
        if workday_time != '':
            ans += "\n工作日：" + workday_time
        if weekend_time != '':
            ans += "\n周未：" + weekend_time
        return ans + "\n"











