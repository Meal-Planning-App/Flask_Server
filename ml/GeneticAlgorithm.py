import json
import random

from deap import base, creator, tools
from deap.algorithms import eaSimple

class DataLoader_Mixin():
    """ DataLoader_Mixin"""
    def __init__(self):
        pass

    def data_load(self, file_path: str, return_data: bool = False):
        self.data = file_path

    def model_input_load(self, json_file):
        if isinstance(json_file, type(dict())):
            dict_temp = json_file
        else:
            dict_temp = json.load(json_file)
        # print(dict_temp)
        self.calories = dict_temp["calories"]
        self.proteins = dict_temp["proteins"]
        self.carbohydrates = dict_temp["carbohydrates"]
        self.fat = dict_temp["fat"]
        self.meals_per_day = dict_temp["meals_per_day"]

    def data_sample(self, ind):
        dict_temp = self.data
        instance = []
        for i in range(self.meals_per_day):
            key = random.sample(dict_temp.keys(), 1)[0]
            instance.append([
                key, int(float(dict_temp[key]["calories"])),
                int(float(dict_temp[key]["proteins"])), int(float(dict_temp[key]["carbohydrates"])),
                int(float(dict_temp[key]["fat"]))
            ])
        return ind(instance)

    def data_sample_one(self):
        dict_temp = self.data
        instance = []
        for i in range(self.meals_per_day):
            key = random.sample(dict_temp.keys(), 1)[0]
            instance.append([
                key, int(float(dict_temp[key]["calories"])),
                int(float(dict_temp[key]["proteins"])), int(float(dict_temp[key]["carbohydrates"])),
                int(float(dict_temp[key]["fat"]))
            ])
        return instance[0]
"""
if __name__ == "__main__":
    print('This is running')
    ga = GeneticAlgorithm()
    data_gen = DataLoader_Mixin()
    json_file = data_gen.data_load("./sample.json", True)
    result, _ = ga.run_algorithm("./data.json", json_file)


    result_arr = []
    # print(result)
    test = []
    for day in result:
        results_arr_temp = {"calories" : 0, "proteins" : 0, "carbs" : 0, "fat" : 0}
        for meal in day:
            results_arr_temp["calories"] += meal[1]
            results_arr_temp["proteins"] += meal[2]
            results_arr_temp["carbs"] += meal[3]
            results_arr_temp["fat"] += meal[4]
        test.append(results_arr_temp)"""
    # print(test)
    # print(f"result_array: {result_arr}")
    # print(f"Desired intake: {[ga.calories, ga.proteins, ga.carbohydrates, ga.fat]}")
