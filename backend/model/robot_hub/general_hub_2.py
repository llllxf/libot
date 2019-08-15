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
from model import aiml_cn
from model.kb_prepare.neo4j_prepare import Neo4jPrepare
import jieba



class GeneralHub():
    """
    总控程序版本2
    """



    def __init__(cls):
        cls._aiml_kernal = aiml_cn.Kernel()
        cls._aiml_kernal.learn('../../resource/navi_template.aiml')
        cls.room_list, cls.room_variant_list, cls.floor_list, cls.floor_variant_list, cls.area_list, cls.area_variant_list, cls.resource_list, cls.resource_variant_list = Neo4jPrepare.get_all_varname()
        jieba.load_userdict("../../resource/guotu_dict.txt")
        cls.stopwords = ['什么', '哪里', '怎么', '有', '走', '去', '可以', '如何', '怎样', '的', '地', '得']
        #self._aiml_kernal.learn('../../resource/contain_template.aiml')

    def question_answer_hub(self, question_str):
        """
        问答总控，基于aiml构建问题匹配器
        :param question_str:问句输入
        :return:
        """


        question_replaced,entity_dict = Neo4jPrepare.repalce_question(question_str)
        #print(question_replaced)
        #question_replaced = "RES去哪里看"
        aiml_respons = self._aiml_kernal.respond(question_replaced)
        print(aiml_respons)
        #return aiml_respons



        if 'task_' in aiml_respons:
                graph_respons = neo4jBot.task_response(aiml_respons,entity_dict)

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






