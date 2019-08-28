import os
import sys
project_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
sys.path.append(project_path)

from model.config.base_config import GraphBaseConfig
from model.kb_prepare.neo4j_prepare import Neo4jPrepare
from model.grapg_QA.Task_time import Task_time
from model.grapg_QA.Task_contain import Task_contain
from model.grapg_QA.Task_information import Task_information
from model.grapg_QA.Task_condition import Task_condition
from model.grapg_QA.Task_business import Task_business
from model.grapg_QA.Task_position import Task_position

import time
import datetime
import matplotlib.pyplot as plt
from skimage import io
import numpy as np

class Bot():
    @classmethod
    def task_response(cls, task, entity_dict):
        """
        响应hub指派的回答任务，也就是对graphQA类的问题分intent处理
        :param task:
        :return:
        """

        answer = "GraphQA 还不清楚您的问题"
        if task == 'task_res_pos':
            answer = cls.answer_res_pos(entity_dict)
        elif task == 'task_room_pos':
            answer = cls.answer_room_pos(entity_dict)
        elif task == 'task_room_res':
            answer = cls.answer_room_res_a(entity_dict)
        elif task == 'task_room_time':
            answer = cls.answer_room_time(entity_dict)
        elif task == 'task_room_res_time':
            answer = cls.answer_room_res_time(entity_dict)
        elif task == 'task_res_time':
            answer = cls.answer_res_time(entity_dict)
        elif task == 'task_floor_room_a':
            answer = cls.answer_floor_room_a(entity_dict)
        elif task == 'task_room_floor':
            answer = cls.answer_floor_room(entity_dict)
        elif task == "task_res_room":
            answer = cls.answer_res_room(entity_dict)
        elif task == "task_res_floor":
            answer = cls.answer_res_floor(entity_dict)
        elif task == "task_floor_res_a":
            answer = cls.answer_res_floor_a(entity_dict)
        elif task == "task_room_res_a":
            answer = cls.answer_room_res_a(entity_dict)
        elif task == "task_room_borrow":
            answer = cls.answer_room_borrow(entity_dict)
        elif task == "task_res_borrow":
            answer = cls.answer_res_borrow(entity_dict)
        elif task == "task_area_borrow":
            answer = cls.answer_area_borrow(entity_dict)
        elif task == "task_room_phone":
            answer = cls.answer_room_phone(entity_dict)
        elif task == "task_room_describe":
            answer = cls.answer_room_describe(entity_dict)
        elif task == "task_res_describe":
            answer = cls.answer_res_describe(entity_dict)
        elif task == "task_count_res":
            answer = cls.answer_count_res(entity_dict)
        elif task == "task_count_restype":
            answer = cls.answer_count_restype(entity_dict)
        elif task == "task_res_res_h":
            answer = cls.answer_res_res_h(entity_dict)
        elif task == "task_res_res_a":
            answer = cls.answer_res_res_a(entity_dict)
        elif task == "task_res_res_t":
            answer = cls.answer_res_res_t(entity_dict)
        elif task == "task_room_card_a":
            answer = cls.answer_room_card_a(entity_dict)
        elif task == "task_card_yes":
            answer = cls.answer_card_yes()
        elif task == "task_card_no":
            answer = cls.answer_card_no()
        elif task == "task_card_thirteen":
            answer = cls.answer_card_thirteen()
        elif task == "task_card_twelve":
            answer = cls.answer_card_twelve()
        elif task == "task_restype_borrow":
            answer = cls.answer_restype_borrow(entity_dict)
        elif task == "task_restype_describe":
            answer = cls.answer_restype_describe(entity_dict)
        elif task == "task_count_floor":
            answer = cls.answer_count_floor(entity_dict)
        elif task == "task_floor_count_room":
            answer = cls.answer_floor_count_room(entity_dict)
        elif task == "task_room_pos":
            answer = cls.answer_room_pos(entity_dict)
        elif task == 'task_res_pos':
            answer = cls.answer_res_pos(entity_dict)
        elif task == "task_card_describe":
            answer = cls.answer_card_describe(entity_dict)
        elif task == "task_finance_describe":
            answer = cls.answer_finance_describe()
        elif task == "task_money_back":
            answer = cls.answer_money_back()
        elif task == "task_money_back_no":
            answer = cls.answer_money_back_no()
        elif task == "task_restype_pos":
            answer = cls.answer_restype_pos(entity_dict)
        elif task == "task_music_pos":
            answer = cls.answer_music_pos()
        elif task == "task_movie_pos":
            answer = cls.answer_movie_pos()
        elif task == "task_library_describe":
            answer = cls.answer_library_describe()
        elif task == "task_library_area":
            answer = cls.answer_library_area()
        elif task == "task_res_read":
            answer = cls.answer_res_read(entity_dict)
        elif task == 'task_service_describe':
            answer = cls.answer_service_describe(entity_dict)
        return answer

    @classmethod
    def answer_room_time(cls,entity_dict):

        task_time = Task_time()
        res = task_time.solve_room_time(entity_dict)
        return [res]

    @classmethod
    def answer_room_res_time(cls,entity_dict):
        task_time = Task_time()
        res = task_time.solve_room_res_time(entity_dict)
        return [res]

    @classmethod
    def answer_res_time(cls, entity_dict):
        task_time = Task_time()
        res = task_time.solve_res_time(entity_dict)
        return [res]

    @classmethod
    def answer_floor_room_a(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_floor_room_a(entity_dict)
        return [res]

    @classmethod
    def answer_floor_room(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_room_floor(entity_dict)
        return [res]

    @classmethod
    def answer_res_room(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_room(entity_dict)
        return [res]

    @classmethod
    def answer_res_floor(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_floor(entity_dict)
        return [res]

    @classmethod
    def answer_res_floor_a(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_floor_a(entity_dict)
        return [res]

    @classmethod
    def answer_room_res_a(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_room_res_a(entity_dict)
        return [res]

    @classmethod
    def answer_room_borrow(cls, entity_dict):
        task_business = Task_business()
        res = task_business.solve_room_borrow(entity_dict)
        return [res]

    @classmethod
    def answer_res_borrow(cls, entity_dict):
        task_business = Task_business()
        res = task_business.solve_res_borrow(entity_dict)
        return [res]

    @classmethod
    def answer_room_phone(cls, entity_dict):
        task_information = Task_information()
        res = task_information.solve_room_phone(entity_dict)
        return [res]

    @classmethod
    def answer_room_describe(cls, entity_dict):
        task_information = Task_information()
        res = task_information.solve_room_describe(entity_dict)
        return [res]

    @classmethod
    def answer_res_describe(cls, entity_dict):
        task_information = Task_information()
        res = task_information.solve_res_describe(entity_dict)
        return [res]

    @classmethod
    def answer_count_res(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_count_res(entity_dict)
        return [res]

    @classmethod
    def answer_count_restype(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_count_restype(entity_dict)
        return [res]

    @classmethod
    def answer_res_res_h(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_res_h(entity_dict)
        return [res]

    @classmethod
    def answer_res_res_a(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_res_a(entity_dict)
        return [res]

    @classmethod
    def answer_res_res_t(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_res_t(entity_dict)
        return [res]

    @classmethod
    def answer_room_card_a(cls, entity_dict):
        task_condition = Task_condition()
        res = task_condition.solve_room_card_a(entity_dict)
        return [res]

    @classmethod
    def answer_card_yes(cls):
        task_business = Task_business()
        return [task_business.solve__card_yes()]

    @classmethod
    def answer_card_no(cls):
        task_business = Task_business()
        return [task_business.solve__card_no()]

    @classmethod
    def answer_card_thirteen(cls):
        task_business = Task_business()
        return [task_business.solve__card_thirteen()]

    @classmethod
    def answer_card_twelve(cls):
        task_business = Task_business()
        return [task_business.solve__card_twelve()]

    @classmethod
    def answer_restype_borrow(cls, entity_dict):

        task_business = Task_business()
        res = task_business.solve_restype_borrow(entity_dict)
        return [res]

    @classmethod
    def answer_restype_describe(cls, entity_dict):
        task_information = Task_information()
        res = task_information.solve_restype_describe(entity_dict)
        return [res]

    @classmethod
    def answer_count_floor(cls, entity_dict):
        task_condition = Task_condition()
        res = task_condition.solve_count_floor(entity_dict)
        return [res]

    @classmethod
    def answer_floor_count_room(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_floor_count_room(entity_dict)
        return [res]

    @classmethod
    def answer_room_pos(cls, entity_dict):
        task_position = Task_position()
        res = task_position.solve_room_pos(entity_dict)
        return res


    @classmethod
    def answer_res_pos(cls, entity_dict):
        task_position = Task_position()
        res = task_position.solve_res_pos(entity_dict)
        return [res]

    @classmethod
    def answer_area_borrow(cls, entity_dict):
        task_business = Task_business()
        res = task_business.solve_area_borrow(entity_dict)
        return [res]

    @classmethod
    def answer_card_describe(cls, entity_dict):
        task_information = Task_information()
        res = task_information.solve_card_describe()
        return [res]

    @classmethod
    def answer_finance_describe(cls):
        task_information = Task_information()
        res = task_information.solve_finance_describe()
        return [res]

    @classmethod
    def answer_money_back(cls):
        task_business = Task_business()
        res = task_business.solve_money_back()
        return [res]

    @classmethod
    def answer_money_back_no(cls):
        task_business = Task_business()
        res = task_business.solve_money_back_no()
        return [res]

    @classmethod
    def answer_restype_pos(cls,entity):
        task_position = Task_position()
        res = task_position.solve_restype_pos(entity)
        return [res]

    @classmethod
    def answer_music_pos(cls):
        dict = {'room':'视听阅览区'}
        #print("====================")
        task_position = Task_position()
        res = task_position.solve_room_pos(dict)
        return res

    @classmethod
    def answer_movie_pos(cls):
        dict = {'room': ['视听阅览区']}
        task_position = Task_position()
        res = task_position.solve_room_pos(dict)
        return res

    @classmethod
    def answer_library_describe(cls):
        task_information = Task_information()
        res = task_information.solve_library_describe()
        return [res]

    @classmethod
    def answer_library_area(cls):
        task_contain = Task_contain()
        res = task_contain.solve_library_area()
        return [res]

    @classmethod
    def answer_res_read(cls,entity_dict):
        task_business = Task_business()
        res = task_business.solve_res_read(entity_dict)
        return [res]

    @classmethod
    def answer_service_describe(cls,entity_dict):
        task_information = Task_information()
        res = task_information.solve_service_describe(entity_dict)
        return [res]





























