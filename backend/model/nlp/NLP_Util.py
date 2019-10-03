# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
project_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
sys.path.append(project_path)
from model.kb_prepare import Neo4jPrepare
import jieba
"""
NLP工具类
"""
class NLPUtil(object):

    @classmethod
    def __init__(cls):
        """
        1.获取字典
        2.加载结巴的自定义文档
        3.定义停用词
        """

        cls.neo_util = Neo4jPrepare()
        cls.room_list, cls.room_alias_list, cls.floor_list, cls.floor_alias_list, cls.area_list, cls.area_alias_list, cls.resource_list, cls.resource_alias_list, cls.restype_list, cls.restype_alias_list, cls.card_list, cls.card_alias_list, cls.library, cls.library_alias_list, cls.service_list, cls.service_alias_list,cls.task_list, cls.task_alias_list, cls.multype_list,cls.multype_alias_list,cls.ttype_list,cls.ttype_alias_list = cls.neo_util.get_all_varname()
        cls.stopwords = ['什么', '哪里', '怎么', '有', '走', '去', '可以', '如何', '怎样', '的', '地', '得']
        """
        for i in cls.service_list:
            print(i)
        for i in cls.service_alias_list:
            for j in i:
                print(j)
        """


        jieba.load_userdict("../../resource/guotu_dict.txt")



    '''
    抽取出句子中的实体，同时将实体替换为模版符号：ROOM,AREA,FLOOR,CARD,AREA,SERVICE,RES
    SERVICE实体比较特别，他们的统一属性通过转为SERVICE查询，但是他们有具有个性，所以最终生成两个替换后的句子，
    一个将服务实体替换为SERVICE，一个不替换，优先匹配不替换的，如果不替换的找不到对应的模板则再匹配替换的。
    '''
    @classmethod
    def repalce_question(cls, question_n):
        question_s = question_n
        question_first = question_n
        if '国图' in question_first:
            question_first = question_first.replace('国图','')
        if '国家图书馆' in question_first:
            question_first = question_first.replace('国家图书馆','')
        if '图书馆' in question_first:
            question_first = question_first.replace('国家图书馆','')

        entity_dict = {}
        word_list = jieba.cut(question_n, cut_all=False)
        room_entity = []
        resource_entity = []
        floor_entity = []
        area_entity = []
        restype_entity = []
        multype_entity = []
        ttype_entity = []
        card_entity = []
        library_entity = []
        service_entity = []
        task_entity = []

        for word in word_list:
            #print(word)

            if word in cls.stopwords:
                continue

            for (room_alias, room) in zip(cls.room_alias_list, cls.room_list):
                if word in room_alias:
                    room_entity.append(room)
                    question_first = question_first.replace(word, 'ROOM')
                    question_n = question_n.replace(word, 'ROOM')
                    question_s = question_s.replace(word, 'ROOM')
                    break
            for (resource_alias, resource) in zip(cls.resource_alias_list, cls.resource_list):
                if word in resource_alias:
                    resource_entity.append(resource)
                    question_first = question_first.replace(word, 'RES')
                    question_n = question_n.replace(word, 'RES')
                    question_s = question_s.replace(word, 'RES')
                    break
            for (floor_alias, floor) in zip(cls.floor_alias_list, cls.floor_list):
                if word in floor_alias:
                    floor_entity.append(floor)
                    question_first = question_first.replace(word, 'FLOOR')
                    question_n = question_n.replace(word, 'FLOOR')
                    question_s = question_s.replace(word, 'FLOOR')
                    break
            for (restype_alias, restype) in zip(cls.restype_alias_list, cls.restype_list):
                #print(restype_alias)
                if word in restype_alias:
                    restype_entity.append(restype)
                    question_first = question_first.replace(word, 'RTYPE')
                    question_n = question_n.replace(word, 'RTYPE')
                    question_s = question_s.replace(word, 'RTYPE')
                    break
            for (multype_alias, multype) in zip(cls.multype_alias_list, cls.multype_list):
                if word in multype_alias:
                    multype_entity.append(multype)
                    #question_first = question_first.replace(word, 'MTYPE')
                    #question = question.replace(word, 'MTYPE')
                    question_s = question_s.replace(word, 'MTYPE')
                    break
            #print(cls.ttype_alias_list,cls.ttype_list)
            for (ttype_alias, ttype) in zip(cls.ttype_alias_list, cls.ttype_list):
                if word in ttype_alias:
                    #print(word)
                    ttype_entity.append(ttype)
                    question_first = question_first.replace(word, 'TTYPE')
                    question_n = question_n.replace(word, 'TTYPE')
                    #question2 = question2.replace(word, 'TTYPE')
                    break
            for (area_alias, area) in zip(cls.area_alias_list, cls.area_list):
                if word in area_alias:
                    area_entity.append(area)
                    question_first = question_first.replace(word, 'AREA')
                    question_n = question_n.replace(word, 'AREA')
                    question_s = question_s.replace(word, 'AREA')
                    break
            for (card_alias, card) in zip(cls.card_alias_list, cls.card_list):
                if word in card_alias:
                    card_entity.append(card)
                    question_s = question_s.replace(word, 'CARD')
                    break
            for library_alias in cls.library_alias_list:
                if word in library_alias:
                    library_entity.append(cls.library)

                    question_n = question_n.replace(word, 'LIBRARY')
                    question_s = question_s.replace(word, 'LIBRARY')
                    break

            for (service_alias, service) in zip(cls.service_alias_list, cls.service_list):
                if word in service_alias:
                    service_entity.append(service)
                    #print("service_entity",service_entity)
                    """
                    由于借书需要优先考虑为借书，所以优先不替换service
                    """
                    question_first = question_first.replace(word, 'SERVICE')
                    question_n = question_n.replace(word, 'SERVICE')

                    break
            for (task_alias, task) in zip(cls.task_alias_list, cls.task_list):

                if word in task_alias:
                    task_entity.append(task)
                    """
                    由于借书需要优先考虑为借书，所以优先不替换service
                    """
                    #question_first = question_first.replace(word, 'TASK')
                    question_s = question_s.replace(word, 'TASK')
                    break

        """
        如果句子不存在除了国家图书馆以外的实体，则将国家图书馆考虑为实体处理
        """
        """
        if len(room_entity) < 1 and len(floor_entity) < 1 and len(area_entity) < 1 and len(restype_entity) < 1 and len(
                card_entity) < 1 and len(ttype_entity)<1\
                and len(resource_entity) < 1 and len(service_entity) < 1 and len(task_entity) < 1:
            for library_alias in cls.library_alias_list[0]:
                if question2.find(library_alias) != -1:
                    question2 = question2.replace(library_alias, "LIBRARY")
                    library_entity.append(cls.library)
        """

        entity_dict['room'] = room_entity
        entity_dict['res'] = resource_entity
        entity_dict['floor'] = floor_entity
        entity_dict['area'] = area_entity
        entity_dict['restype'] = restype_entity
        entity_dict['multype'] = multype_entity
        entity_dict['ttype'] = ttype_entity
        entity_dict['card'] = card_entity
        entity_dict['service'] = service_entity
        entity_dict['library'] = library_entity
        entity_dict['task'] = task_entity
        #print("question_first,question_n,question_s",question_first,question_n,question_s)
        return question_first,question_n,question_s, entity_dict



if __name__=='__main__':
    pass
