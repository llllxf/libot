# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
project_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
sys.path.append(project_path)
from model.aiml_cn import  Kernel

"""
AIML工具类
"""
class AIMLUtil(object):

    @classmethod
    def __init__(cls):

        cls.aiml_kernal = Kernel()

        cls.aiml_kernal.learn('../../resource/navi_template.aiml')
        cls.aiml_kernal.learn('../../resource/contain_template.aiml')
        cls.aiml_kernal.learn('../../resource/time.aiml')
        cls.aiml_kernal.learn('../../resource/condition.aiml')
        cls.aiml_kernal.learn('../../resource/information.aiml')
        cls.aiml_kernal.learn('../../resource/business.aiml')
        cls.aiml_kernal.learn('../../resource/pattern_for_cyclopedia.aiml')

        '''
        cls.aiml_kernal.learn('../resource/navi_template.aiml')
        cls.aiml_kernal.learn('../resource/contain_template.aiml')
        cls.aiml_kernal.learn('../resource/time.aiml')
        cls.aiml_kernal.learn('../resource/condition.aiml')
        cls.aiml_kernal.learn('../resource/information.aiml')
        cls.aiml_kernal.learn('../resource/business.aiml')
        '''


    @classmethod
    def response(cls, question):
        aiml_response = cls.aiml_kernal.respond(question)
        return aiml_response


if __name__ == '__main__':
    AIMLUtil()
    ans = AIMLUtil.response("HED")
    #ans = AIMLUtil.response("SBVHEDPOB")

    print(ans)

