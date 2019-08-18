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

        answer = "GraphQA 什么也没说！"
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

        return answer

    @classmethod
    def answer_room_time(cls,entity_dict):

        task_time = Task_time()
        res = task_time.solve_room_time(entity_dict)
        return res

    @classmethod
    def answer_room_res_time(cls,entity_dict):
        task_time = Task_time()
        res = task_time.solve_room_res_time(entity_dict)
        return res

    @classmethod
    def answer_res_time(cls, entity_dict):
        task_time = Task_time()
        res = task_time.solve_res_time(entity_dict)
        return res

    @classmethod
    def answer_floor_room_a(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_floor_room_a(entity_dict)
        return res

    @classmethod
    def answer_floor_room(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_room_floor(entity_dict)
        return res

    @classmethod
    def answer_res_room(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_room(entity_dict)
        return res

    @classmethod
    def answer_res_floor(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_floor(entity_dict)
        return res

    @classmethod
    def answer_res_floor_a(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_floor_a(entity_dict)
        return res

    @classmethod
    def answer_room_res_a(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_room_res_a(entity_dict)
        return res

    @classmethod
    def answer_room_borrow(cls, entity_dict):
        task_information = Task_information()
        res = task_information.solve_room_borrow(entity_dict)
        return res

    @classmethod
    def answer_res_borrow(cls, entity_dict):
        task_information = Task_information()
        res = task_information.solve_res_borrow(entity_dict)
        return res

    @classmethod
    def answer_room_phone(cls, entity_dict):
        task_information = Task_information()
        res = task_information.solve_room_phone(entity_dict)
        return res

    @classmethod
    def answer_room_describe(cls, entity_dict):
        task_information = Task_information()
        res = task_information.solve_room_describe(entity_dict)
        return res

    @classmethod
    def answer_res_describe(cls, entity_dict):
        task_information = Task_information()
        res = task_information.solve_res_describe(entity_dict)
        return res

    @classmethod
    def answer_count_res(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_count_res(entity_dict)
        return res

    @classmethod
    def answer_count_restype(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_count_restype(entity_dict)
        return res

    @classmethod
    def answer_res_res_h(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_res_h(entity_dict)
        return res

    @classmethod
    def answer_res_res_a(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_res_a(entity_dict)
        return res

    @classmethod
    def answer_res_res_t(cls, entity_dict):
        task_contain = Task_contain()
        res = task_contain.solve_res_res_t(entity_dict)
        return res

    @classmethod
    def answer_room_card_a(cls, entity_dict):
        task_condition = Task_condition()
        res = task_condition.solve_room_card_a(entity_dict)
        return res



