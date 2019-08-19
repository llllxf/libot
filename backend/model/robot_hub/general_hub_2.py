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
from model.kb_prepare.neo4j_prepare import Neo4jPrepare
import jieba



class GeneralHub():
    """
    总控程序版本2
    """

    @classmethod
    def __init__(cls):
        cls._aiml_kernal = aiml_cn.Kernel()
        cls._aiml_kernal.learn('../../resource/navi_template.aiml')
        cls._aiml_kernal.learn('../../resource/contain_template.aiml')
        cls._aiml_kernal.learn('../../resource/time.aiml')

        cls._aiml_kernal.learn('../../resource/condition.aiml')
        cls._aiml_kernal.learn('../../resource/information.aiml')
        cls._aiml_kernal.learn('../../resource/business.aiml')
        cls.room_list, cls.room_variant_list, cls.floor_list, cls.floor_variant_list, cls.area_list, cls.area_variant_list, cls.resource_list, cls.resource_variant_list,cls.restype_list,cls.restype_variant_list,cls.card_list,cls.card_variant_list = Neo4jPrepare.get_all_varname()
        jieba.load_userdict("../../resource/guotu_dict.txt")
        cls.stopwords = ['什么', '哪里', '怎么', '有', '走', '去', '可以', '如何', '怎样', '的', '地', '得']


    @classmethod
    def repalce_question(cls, question):

        entity_dict = {}
        word_list = jieba.cut(question, cut_all=False)
        #print("==================",list(word_list))
        room_temp = []
        resource_temp = []
        floor_temp = []
        area_temp = []
        restype_temp=[]
        card_temp = []
        #print(cls.stopwords)
        for word in word_list:

            if word in cls.stopwords:
                continue

            for room_index in range(len(cls.room_variant_list)):
                room = cls.room_variant_list[room_index]
                if word in room:
                    room_temp.append(cls.room_list[room_index])
                    question = question.replace(word, 'ROOM')
                    break
            for resource_index in range(len(cls.resource_variant_list)):
                resource = cls.resource_variant_list[resource_index]
                if word in resource:
                    resource_temp.append(cls.resource_list[resource_index])
                    question = question.replace(word, 'RES')
                    break
            for floor_index in range(len(cls.floor_variant_list)):
                floor = cls.floor_variant_list[floor_index]
                if word in floor:
                    floor_temp.append(cls.floor_list[floor_index])
                    question = question.replace(word, 'FLOOR')
                    break
            #print(cls.restype_variant_list)
            for restype_index in range(len(cls.restype_variant_list)):
                restype = cls.restype_variant_list[restype_index]
                #print(restype,word)
                if word in restype:
                    #print(word)
                    restype_temp.append(cls.restype_list[restype_index])
                    question = question.replace(word, 'RESTYPE')
                    break

            for area_index in range(len(cls.area_variant_list)):
                area = cls.area_variant_list[area_index]
                if word in area:
                    area_temp.append(cls.area_list[area_index])
                    question = question.replace(word, 'AREA')
                    break
            for card_index in range(len(cls.card_variant_list)):
                card = cls.card_variant_list[card_index]
                if word in card:
                    card_temp.append(cls.card_list[card_index])
                    question = question.replace(word, 'CARD')
                    break

        entity_dict['room'] = room_temp
        entity_dict['res'] = resource_temp
        entity_dict['floor'] = floor_temp
        entity_dict['area'] = area_temp
        entity_dict['restype'] = restype_temp
        entity_dict['card'] = card_temp

        return question, entity_dict

    def question_answer_hub(self, question_str):
        """
        问答总控，基于aiml构建问题匹配器
        :param question_str:问句输入
        :return:
        """


        question_replaced,entity_dict = GeneralHub.repalce_question(question_str)
        #print(question_replaced)
        aiml_respons = GeneralHub._aiml_kernal.respond(question_replaced)
        #print(aiml_respons)
        #return aiml_respons

        if 'task_' in aiml_respons:
                graph_respons = Bot.task_response(aiml_respons,entity_dict)
        else:
            return aiml_respons

        return graph_respons





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
            print('Libot:', gh.question_answer_hub(question_str))
            time_end = time.time()
            #print('time cost', time_end - time_start, 's')






