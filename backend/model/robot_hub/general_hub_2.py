# -*- coding: utf-8 -*-
import os
import sys
# 模块路径引用统一回退到Libbot目录下
project_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
print("hub",project_path)
sys.path.append(project_path)

"""
from model.grapg_QA.bot import Bot
from model.search_QA import similarQuestionBot
from model.aiml_cn import AIMLUtil
from model.nlp import NLPUtil
from model.pedia import TaskManager
"""
from model.grapg_QA.bot import Bot
from model.search_QA import similarQuestionBot
from model.aiml_cn import AIMLUtil
from model.nlp import NLPUtil
from model.pedia.manager import TaskManager
import skimage.io as io
import scipy
import matplotlib.pyplot as plt
#from model.kb_prepare.neo4j_prepare2 import Neo4jPrepare


class GeneralHub():
    """
    总控程序版本2
    """

    @classmethod
    def __init__(cls,age=None,sex=None):
        """
        主控模块的初始化
        1.得到AIML工具类
        2.得到NLP工具类
        """
        cls.aiml_util = AIMLUtil()
        cls.nlp_util = NLPUtil('ltp_data_v3.4.0')
        cls.search_bot = similarQuestionBot()
        cls.age = age
        cls.sex = sex

    @classmethod
    def set_age_sex(cls, age, sex):
        cls.age = age
        cls.sex = sex

    def question_answer_hub(self, question_str):
        """
        问答总控，基于aiml构建问题匹配器
        :param question_str:问句输入
        :return:
        """

        question_str = self.nlp_util.clear_question(question_str)
        print(question_str)

        question_first,question_replaced_normal,question_replaced_spcify,entity_dict = self.nlp_util.repalce_question(question_str)
        aiml_response = self.aiml_util.response(question_first)

        if 'task_' in aiml_response:

            graph_response = Bot.task_response(aiml_response, entity_dict,self.age,self.sex)

        elif aiml_response != '':
            graph_response = [aiml_response]
        else:
            aiml_response_normal = self.aiml_util.response(question_replaced_normal)
            #print(aiml_response_normal, question_replaced_normal)

            if 'task_' in aiml_response_normal:
                graph_response = Bot.task_response(aiml_response_normal, entity_dict,self.age,self.sex)
            elif aiml_response_normal != '':
                graph_response = [aiml_response_normal]
            else:
                aiml_response_specify = self.aiml_util.response(question_replaced_spcify)
                #print(aiml_response_specify, question_replaced_spcify)

                if 'task_' in aiml_response_specify:
                    graph_response = Bot.task_response(aiml_response_specify, entity_dict,self.age,self.sex)
                elif aiml_response_specify != '':
                    graph_response = [aiml_response_specify]
                else:
                    response = dict(self.search_bot.answer_question(question_str)[0])
                    #print(response['answer'], response['score'], question_str, "===")
                    print(response['score'], response['question'])
                    if float(response['score']) > 0.7:

                        graph_response = [response['answer']]

                    else:
                        words, pattern, arcs_dict, postags, hed_index = NLPUtil.get_sentence_pattern(question_str)
                        print(words, pattern, arcs_dict, postags, hed_index)
                        aiml_reponse = AIMLUtil.response(pattern)
                        print(aiml_reponse)
                        answer = TaskManager.task_response(aiml_reponse, words, arcs_dict, postags, hed_index)
                        if answer != None:
                            return [answer]
                        else:
                            import requests, json
                            github_url = "http://openapi.tuling123.com/openapi/api/v2"
                            data = json.dumps({
                                "reqType": 0,
                                "perception": {
                                    "inputText": {
                                        "text": question_str
                                    },
                                },
                                "userInfo": {
                                    "apiKey": "62f1c8991a6d499c8b22e497de6cdd11",
                                    "userId": "219315"
                                }
                            })

                            r = requests.post(github_url, data)
                            print(r.json())
                            res_msg = r.json()['results'][0]['values']['text']
                            return [res_msg]




        '''
        由于服务类同时具有共性与特性，所以生产两个模版，即一份模版将服务实体替换为service进行模版匹配，一类模版
        不讲服务实体替换为service直接用原词汇匹配模版
        '''
        """
        question_first, question_replaced, question_replaced2, entity_dict = self.nlp_util.repalce_question(
            question_str)
        aiml_response = self.aiml_util.response(question_replaced)
        print(aiml_response, question_replaced)
        if 'task_' in aiml_response:

            graph_response = Bot.task_response(aiml_response, entity_dict)

        elif aiml_response!='':
            graph_response=[aiml_response]
        else:
            aiml_response2 = self.aiml_util.response(question_replaced2)
            print(aiml_response2,question_replaced2)

            if 'task_' in aiml_response2:
                graph_response = Bot.task_response(aiml_response2, entity_dict)
            elif aiml_response2 != '':
                graph_response = [aiml_response2]
            else:
                response = dict(self.search_bot.answer_question(question_str)[0])
                print(response['answer'],response['score'],question_str,"===")

                if float(response['score'])>0.7:
                    print(response['score'])
                    graph_response = [response['answer']]
                else:
                    graph_response = ['很抱歉，我好像不明白，请您换一种说法']
        """


        return graph_response


import time

if __name__ == '__main__':


    gh = GeneralHub('12','男')

    while True:
        question_str = input('User:')
        if question_str == 'exit':
            break
        else:
            time_start = time.time()
            response = gh.question_answer_hub(question_str)
            #print("resp",response)
            print('Libot:', response[0])
            #print(response[1])
            #img = io.imread('../../resource/2.png')
            #print(img)
            #scipy.misc.imsave('meelo.png', response[1])
            time_end = time.time()









