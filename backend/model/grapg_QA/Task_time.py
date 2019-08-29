from model.kb_prepare.neo4j_prepare import Neo4jPrepare
"""
时间类问答模块
作者:lxf
"""
class Task_time():
    """
    馆室开放时间
    """
    def solve_room_time(self,entity):
        room = entity['room'][0]
        res = Neo4jPrepare.get_property(room)
        #print(res)
        open_day = res['open_date']
        ans = "\n" + room + "开放日为：" + open_day+"\n"
        workday_time = res['monday_open']
        weekend_time = res['sunday_open']
        if workday_time != '':

            ans += "工作日开放时间为："+workday_time+"\n"
        if weekend_time != '':
            ans += "周末开放时间为："+weekend_time+"\n"

        return ans
    """
    馆室的资源借阅时间
    """
    def solve_room_res_time(self,entity):
        room = entity['room'][0]
        #print(entity)
        res = Neo4jPrepare.get_property(room)
        #print("================================",res)
        workday_time = res['monday_borrow']
        weekend_time = res['sunday_borrow']
        if workday_time == '' and weekend_time == '':
            return "很抱歉，"+room+"的资源材料不提供借阅\n"
        ans = "\n"+room+"的书籍材料借阅时间为："
        if workday_time != '':
            ans += "\n工作日："+workday_time
        if weekend_time != '':
            ans += "\n周未：" + weekend_time
        return ans+"\n"

    """
    资源借阅时间
    """
    def solve_res_time(self,entity):
        resource = entity['res'][0]
        #print(Neo4jPrepare.get_property(resource))
        room = Neo4jPrepare.get_property(resource)['room']
        res = Neo4jPrepare.get_property(room)
        workday_time = res['monday_borrow']
        weekend_time = res['sunday_borrow']
        if workday_time == '' and weekend_time == '':
            return "很抱歉，"+room+"的资源材料不提供借阅\n"
        #ans = "\n" + resource + "的借阅时间为：\n工作日：" + workday_time + "\n周未：" + weekend_time + "\n"
        ans = "\n" + resource + "存放在"+room+","
        ans += room + "的借阅时间为："
        if workday_time != '':
            ans += "\n工作日：" + workday_time
        if weekend_time != '':
            ans += "\n周未：" + weekend_time
        return ans + "\n"

    """
    服务时间
    """
    def solve_service_time(self,entity):
        service = entity['service'][0]
        res = Neo4jPrepare.get_property(service)
        ans = "\n"
        if res['date']!='':
            ans += "服务日期："+res['date']+"\n"
        if res['worktime'] != '':
            ans += "工作日服务时间为"+str(res['worktime'])+"\n"
        if res['weektime'] != '':
            ans += "工作日服务时间为"+str(res['weektime'])+"\n"
        return ans


    #============================












