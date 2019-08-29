from model.kb_prepare.neo4j_prepare import Neo4jPrepare
import numpy as np
class Task_business():

    """
    还书
    """
    def solve_book_back(self, entity):
        resource  = entity['res'][0]
        res = Neo4jPrepare.get_relation(resource,'馆室')

        ans = "\n"+resource+"存放在"
        for r in res[:-1]:
            #print(r)
            ans += r['office_name']+","

        ans += res[-1]['office_name']+"\n"
        card = Neo4jPrepare.get_relation(res[-1]['office_name'],'证件')

        for c in card:
            ans += "年龄"+c['age']+"可持"+c['office_name']+"进入馆室\n"
        return ans

    """
    资源借阅
    """
    def solve_res_read(self, entity):
        resource  = entity['res'][0]
        res = Neo4jPrepare.get_relation(resource,'馆室')

        ans = "\n"+resource+"存放在"
        for r in res[:-1]:
            #print(r)
            ans += r['office_name']+","

        ans += res[-1]['office_name']+"\n"
        card = Neo4jPrepare.get_relation(res[-1]['office_name'],'证件')

        for c in card:
            ans += "年龄"+c['age']+"可持"+c['office_name']+"进入馆室\n"
        return ans

    """
    作废了
    """
    def solve_money_back(self):
        res = Neo4jPrepare.get_property('退押金')
        card = res['card']
        card_arr = card.split("，")
        ans = "\n请到相应阅览室/服务点还清所借图书，确认无欠款后，持"
        for c in card_arr[:-2]:
            ans += c+","
        ans += card_arr[len(card_arr)-2]
        ans += "到办证处办理退押金手续\n"
        return ans


    def solve_money_back_no(self):
        res = Neo4jPrepare.get_property('退押金')
        card = res['card']
        card_arr = card.split("，")
        ans = "\n请到相应阅览室/服务点还清所借图书，确认无欠款后，持"
        for c in card_arr[:-1]:
            ans += c+","
        ans += card_arr[len(card_arr)-1]
        ans += "到办证处办理退押金手续\n"
        return ans

    """
    馆区的资源是否可以外借
    """
    def solve_area_borrow(self,entity):
        area = entity['area'][0]
        ans = "\n"

        room_res = Neo4jPrepare.get_reverse_relation(area,'馆室')
        borrow_room = []
        borrow_floor = []
        copy_room = []
        copy_floor=[]
        copy = []
        for r in room_res:
            if r['borrow'] == 1:
                room_name = r['office_name']
                if r['office_name'].find("_")!=-1:
                    room_name = r['office_name'].split("_")[2]
                borrow_room.append(room_name)
                borrow_floor.append(r['floor'])
            elif r['borrow'] == 2:
                room_name = r['office_name']
                if r['office_name'].find("_") != -1:
                    room_name = r['office_name'].split("_")[2]
                copy_room.append(room_name)
                copy_floor.append(r['floor'])
            elif '复制处' in r['variant_name']:
                if r['floor'] in copy:
                    continue

                copy.append(r['floor'])
        #copy = np.unique(copy)
        if len(borrow_room)>0:
            for b in range(len(borrow_room)-1):
                ans += borrow_floor[b]+"的"+borrow_room[b]+","
            ans += borrow_floor[-1]+"的"+borrow_room[-1]+"的书籍材料资源可以外借\n"
        if len(copy_room)>0:
            for c in range(len(copy_room)-1):
                ans += copy_floor[c]+"的"+copy_room[c]+","
            ans += copy_floor[-1]+"的"+copy_room[-1]+"的书籍材料资源不可以外借，但可以复制或扫描\n"
            for f in copy[:-1]:
                ans += f + ","
            ans += copy[-1]
            ans += "提供复制处，可携带读者卡前往该楼层复制处复制或扫描\n"

        return ans

    """
    馆室的资源是否可以外借
    """
    def solve_room_borrow(self,entity):
        room = entity['room'][0]
        room_name = room
        if room.find("_")!=-1:
            room_name=room.split("_")[2]

        ans = "\n"

        res = Neo4jPrepare.get_property(room)

        if res['borrow'] == 1:
            ans+=room_name+"的资源书籍均可以外借\n"
        elif res['borrow'] == 2:
            ans += room_name + "的资源书籍均不允许外借，但可以复制与扫描\n"
        else:
            ans += room_name + "的资源书籍均不可以外借，仅供借阅\n"
        return ans

    """
    资源是否可以外借
    """
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
        elif room_res[0]['borrow'] == 2:
            ans += res + "不可以外借，但可以复制与扫描\n"
        else:
            ans += res + "不可以外借，仅供借阅\n"
        return ans

    """
    某类资源是否可以外借，需先查出此类资源包括什么资源，具体某个资源是否可以外借
    """
    def solve_restype_borrow(self,entity):
        restype = entity['restype'][0]
        res_res = Neo4jPrepare.get_reverse_relation(restype,'资源')
        #print(res_res)
        yes_room = []
        copy_room = []
        no_room = []

        for res in res_res:
            room_res = Neo4jPrepare.get_relation(res['office_name'],'馆室')
            for r in room_res:
                room = r['office_name']

                if r['borrow'] == 1:
                    yes_room.append(room)
                elif r['borrow'] == 2:
                    copy_room.append(room)
                else:
                    no_room.append(room)
                copy_room = np.unique(copy_room)
        ans = "\n"
        if len(yes_room)>0:
            ans += "存放在"
            for y in yes_room[:-1]:
                ans += y+","
            ans += yes_room[len(yes_room)-1]+"的"+restype+"可以外借\n"
        if len(copy_room)>0:
            ans += "存放在"
            for c in copy_room[:-1]:
                ans += c+","
            ans += copy_room[len(copy_room) - 1] + "的" + restype + "可以不外借，但可以复制和扫描\n"
        if len(no_room)>0:
            ans += "存放在"
            for y in no_room[:-1]:
                ans += y+","
            ans += no_room[len(no_room)-1]+"的"+restype+"不可以外借，仅供借阅\n"
        return ans

    '''
    办理读者卡
    solve__card_yes 中国籍满16岁
    solve__card_no 非中国籍满16岁
    solve__card_thirteen 13-15岁
    solve__card_twelve 未满十三岁
    '''
    def solve__card_yes(self):
        return "国家图书馆读者卡分人工办证和自助办证两种。\n人工办证：每日16：30之前在办证处办理；自助办证：总馆北区和南区办证处设有自助办证机，可于周一至周五9：00--21：00，周六和周日9：00--17：00自助办理。\n年满十六周岁的中国公民须持本人身份证件原件（包括身份证、户口簿、军人证、护照、港澳通行证、台胞回乡证）办理。\n"
    def solve__card_no(self):
        return "国家图书馆读者卡分人工办证和自助办证两种。\n人工办证：每日16：30之前在办证处办理；自助办证：总馆北区和南区办证处设有自助办证机，可于周一至周五9：00--21：00，周六和周日9：00--17：00自助办理。\n年满十六周岁的外籍人士需持护照原件办理。\n"
    def solve__card_thirteen(self):
        return "国家图书馆读者卡分人工办证和自助办证两种。\n人工办证：每日16：30之前在办证处办理；自助办证：总馆北区和南区办证处设有自助办证机，可于周一至周五9：00--21：00，周六和周日9：00--17：00自助办理。\n年满十三至十五周岁的中国公民和外籍人士，需由监护人陪同，并持本人及监护人有效身份证件原件和复印件（包括身份证、户口簿、军人证、护照、港澳通行证、台胞回乡证）办理\n"
    def solve__card_twelve(self):
        return "国家图书馆读者卡分人工办证和自助办证两种。\n人工办证：每日16：30之前在办证处办理；自助办证：总馆北区和南区办证处设有自助办证机，可于周一至周五9：00--21：00，周六和周日9：00--17：00自助办理。\n十二周岁及以下的中国公民和外籍人士，由监护人陪同，持本人及监护人有效身份证件原件和复印件（包括身份证、户口簿、学籍卡、军人证、护照、港澳通行证、台胞回乡证），到办证处填写《国家图书馆少年儿童馆读者卡申请表》即可办理少年儿童馆读者卡。\n"