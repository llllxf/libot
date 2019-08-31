# -*- coding: utf-8 -*-
# File: general_hub_1.py
# Author: Hualong Zhang <nankaizhl@gmail.com>
# CreateDate: 19-03-09
import os
import sys
# 模块路径引用统一回退到Libbot目录下
project_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
sys.path.append(project_path)


from model.grapg_QA.neo4j_bot import neo4jBot
from model.grapg_QA.bot import Bot
from model import aiml_cn
from model.kb_prepare.neo4j_prepare2 import Neo4jPrepare
import jieba

"""
加载aiml模块
"""
aiml_kernal = aiml_cn.Kernel()
aiml_kernal.learn('../../resource/navi_template.aiml')
aiml_kernal.learn('../../resource/contain_template.aiml')
aiml_kernal.learn('../../resource/time.aiml')
aiml_kernal.learn('../../resource/condition.aiml')
aiml_kernal.learn('../../resource/information.aiml')
aiml_kernal.learn('../../resource/business.aiml')

class GeneralHub():
    """
    总控程序版本2
    """

    @classmethod

    def __init__(cls):
        """
        主控模块的初始化
        1.获取字典
        2.加载结巴的自定义文档
        3.定义停用词
        """
        '''
        cls._aiml_kernal = aiml_cn.Kernel()
        cls._aiml_kernal.learn('../../resource/navi_template.aiml')
        cls._aiml_kernal.learn('../../resource/contain_template.aiml')
        cls._aiml_kernal.learn('../../resource/time.aiml')
        cls._aiml_kernal.learn('../../resource/condition.aiml')
        cls._aiml_kernal.learn('../../resource/information.aiml')
        cls._aiml_kernal.learn('../../resource/business.aiml')
        '''
        cls.room_list, cls.room_alias_list, cls.floor_list, cls.floor_alias_list, cls.area_list, cls.area_alias_list, cls.resource_list, cls.resource_alias_list,cls.restype_list,cls.restype_alias_list,cls.card_list,cls.card_alias_list,cls.library,cls.library_alias_list,cls.service_list,cls.service_alias_list = Neo4jPrepare.get_all_varname()
        jieba.load_userdict("../../resource/guotu_dict.txt")
        cls.stopwords = ['什么', '哪里', '怎么', '有', '走', '去', '可以', '如何', '怎样', '的', '地', '得']
        '''
        print("=======================================")
        print(cls.room_list, cls.room_variant_list, cls.floor_list, cls.floor_variant_list, cls.area_list, cls.area_variant_list, cls.resource_list, cls.resource_variant_list,cls.restype_list,cls.restype_variant_list,cls.card_list,cls.card_variant_list,cls.library_list,cls.library_variant_list,cls.service_list,cls.service_variant_list)
        '''
    '''
    抽取出句子中的实体，同时将实体替换为模版符号：ROOM,AREA,FLOOR,CARD,AREA,SERVICE,RES
    
    SERVICE实体比较特别，他们的统一属性通过转为SERVICE查询，但是他们有具有个性，所以最终生成两个替换后的句子，
    一个将服务实体替换为SERVICE，一个不替换，优先匹配不替换的，如果不替换的找不到对应的模板则再匹配替换的。
    '''
    @classmethod
    def repalce_question(cls, question):

        question2 = question

        entity_dict = {}
        word_list = jieba.cut(question, cut_all=False)

        room_entity = []
        resource_entity = []
        floor_entity  = []
        area_entity  = []
        restype_entity =[]
        card_entity  = []
        library_entity =[]
        service_entity =[]

        for word in word_list:

            if word in cls.stopwords:
                continue

            for (room_alias,room) in zip(cls.room_alias_list,cls.room_list):
                if word in room_alias:
                    room_entity.append(room)
                    question = question.replace(word, 'ROOM')
                    question2 = question2.replace(word, 'ROOM')
                    break
            for (resource_alias,resource) in zip(cls.resource_alias_list,cls.resource_list):
                if word in resource_alias:
                    resource_entity.append(resource)
                    question = question.replace(word, 'RES')
                    question2 = question2.replace(word, 'RES')
                    break
            for (floor_alias,floor) in zip(cls.floor_alias_list,cls.floor_list):
                if word in floor_alias:
                    floor_entity.append(floor)
                    question = question.replace(word, 'FLOOR')
                    question2 = question2.replace(word, 'FLOOR')
                    break
            for (restype_alias,restype) in zip(cls.restype_alias_list,cls.restype_list):
                if word in restype_alias:
                    restype_entity.append(restype)
                    question = question.replace(word, 'RESTYPE')
                    question2 = question2.replace(word, 'RESTYPE')
                    break
            for (area_alias,area) in zip(cls.area_alias_list,cls.area_list):
                if word in area_alias:
                    area_entity.append(area)
                    question = question.replace(word, 'AREA')
                    question2 = question2.replace(word, 'AREA')
                    break
            for (card_alias,card) in zip(cls.card_alias_list,cls.card_list):
                if word in card_alias:
                    card_entity.append(card)
                    question = question.replace(word, 'CARD')
                    question2 = question2.replace(word, 'CARD')
                    break
            for (service_alias,service) in zip(cls.service_alias_list,cls.service_list):
                if word in service:
                    service_entity.append(service)
                    question2 = question2.replace(word, 'SERVICE')
                    break
        """
        如果句子不存在除了国家图书馆以外的实体，则将国家图书馆考虑为实体处理
        """
        if len(room_entity) < 1 and len(floor_entity) < 1 and len(area_entity) < 1 and len(restype_entity) < 1 and len(
                card_entity) < 1 \
                and len(resource_entity) < 1 and len(service_entity) < 1:
            for library_alias in cls.library_alias_list[0]:
                if question.find(library_alias)!=-1:
                    question = question.replace(library_alias,"LIBRARY")
                    library_entity.append(cls.library)

        entity_dict['room'] = room_entity
        entity_dict['res'] = resource_entity
        entity_dict['floor'] = floor_entity
        entity_dict['area'] = area_entity
        entity_dict['restype'] = restype_entity
        entity_dict['card'] = card_entity
        entity_dict['service'] = service_entity
        entity_dict['library'] = library_entity

        return question,question2,entity_dict

    def question_answer_hub(self, question_str):
        """
        问答总控，基于aiml构建问题匹配器
        :param question_str:问句输入
        :return:
        """


        question_replaced,question_replaced2,entity_dict = GeneralHub.repalce_question(question_str)
        aiml_response = aiml_kernal.respond(question_replaced)
        #print(question_replaced,question_replaced2)

        '''
        由于服务类同时具有共性与特性，所以生产两个模版，即一份模版将服务实体替换为service进行模版匹配，一类模版
        不讲服务实体替换为service直接用原词汇匹配模版
        
        '''

        if 'task_' in aiml_response:

            graph_response = Bot.task_response(aiml_response, entity_dict)
        elif aiml_response!='':
            graph_response=[aiml_response]
        else:

            aiml_response2 = aiml_kernal.respond(question_replaced2)
            if 'task_' in aiml_response2:
                graph_response = Bot.task_response(aiml_response2, entity_dict)
            elif aiml_response2 != '':
                graph_response = [aiml_response2]
            else:
                graph_response=['很抱歉，我好像不明白，请您换一种说法']
        return graph_response


import time

if __name__ == '__main__':
    Neo4jPrepare()

    gh = GeneralHub()



    while True:
        question_str = input('User:')
        if question_str == 'exit':
            break
        else:
            time_start = time.time()
            print('Libot:', gh.question_answer_hub(question_str)[0])
            time_end = time.time()







