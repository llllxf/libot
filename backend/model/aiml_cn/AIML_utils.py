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

        """

        主控aiml
        """
        cls.mask_aiml_kernal = Kernel()

        cls.mask_aiml_kernal.learn('../../resource/navi_template.aiml')
        cls.mask_aiml_kernal.learn('../../resource/contain_template.aiml')
        cls.aimlmask_aiml_kernal_kernal.learn('../../resource/time.aiml')
        cls.mask_aiml_kernal.learn('../../resource/condition.aiml')
        cls.mask_aiml_kernal.learn('../../resource/information.aiml')
        cls.mask_aiml_kernal.learn('../../resource/business.aiml')
        cls.mask_aiml_kernal.learn('../../resource/pattern_for_cyclopedia.aiml')

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

