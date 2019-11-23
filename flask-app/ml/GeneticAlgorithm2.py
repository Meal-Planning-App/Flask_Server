import json
import random

from deap import base, creator, tools
from deap.algorithms import eaSimple
from ml.GeneticAlgorithm import DataLoader_Mixin

class GeneticAlgorithm(DataLoader_Mixin):
    """ Genetic Algorithm class"""
    def __init__(self, ind_size: int = 10):
        super().__init__()
        self.ind_size = ind_size
        # 0, because ID needs to be stored
        creator.create("FitnessMulti", base.Fitness, weights=(0, -1, -0.5, -0.5, -0.5))
        creator.create("Individual", list, fitness=creator.FitnessMulti)

        self.toolbox = base.Toolbox()
        # Register functions
        self.toolbox.register("attribute", super().data_sample, ind=creator.Individual)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual,
                              self.toolbox.attribute, n=self.ind_size)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("mate", tools.cxOnePoint) # no need to change
        self.toolbox.register("mutate", self._mutate, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", self._evaluate)

    def run_algorithm(self, loaded_data: str, json_file) -> dict():
        super().data_load(loaded_data)
        super().model_input_load(json_file)
        pop = self.toolbox.population(n=100)[0]
        CXPB, MUTPB, NGEN = 0.5, 0.5, 5
        # Evaluate the entire population
        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        for g in range(NGEN):
            # Select the next generation individuals
            offspring = self.toolbox.select(pop, len(pop))
            #print(f"offspring: {offspring}")
            #print(f"\npop: {pop}")
            # Clone the selected individuals
            offspring = list(map(self.toolbox.clone, offspring))

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < MUTPB:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # The population is entirely replaced by the offspring
            pop[:] = offspring
            result_arr = []
            for day in pop:
                results_arr_temp = {"calories" : 0, "proteins" : 0, "carbs" : 0, "fat" : 0}
                for meal in day:
                    results_arr_temp["calories"] += meal[1]
                    results_arr_temp["proteins"] += meal[2]
                    results_arr_temp["carbs"] += meal[3]
                    results_arr_temp["fat"] += meal[4]
                result_arr.append(results_arr_temp)
            # print(f"result_array: {result_arr}")
            # print(f"Desired intake: {[self.calories, self.proteins, self.carbohydrates, self.fat]}")
        return pop, self.convert_back_to_dict(pop)

    def convert_back_to_dict(self, result_arr):
        day = result_arr[0]
        ids = []
        result_dict = []
        for i in range(self.meals_per_day):
            id = day[i][0]
            result_dict.append(self.data[id])
        return result_dict

    def run_fake_algorithm(self, loaded_data: str, json_file) -> dict():
        super().data_load(loaded_data)
        super().model_input_load(json_file)
        keys = random.sample(list(self.data), self.meals_per_day)
        return [self.data[k] for k in keys]

    def _mutate(self, instance, indpb):
        indpb = [indpb]
        if len(indpb) == 1:
            indpb = list(indpb) * self.meals_per_day
        if len(indpb) != self.meals_per_day:
            # print("Weird mutation error!")
            # print(indpb)
            indpb = indpb[:1] * self.meals_per_day
            # print(f"New probs: {indpb}")

        for i, proba in enumerate(indpb):
            rand_float = random.uniform(0, 1)
            if rand_float <= proba:
                instance_new = super().data_sample_one()
                instance[i] = instance_new
        return instance

    def _select(self, individuals, k, tournsize):
        pass

    def _evaluate(self, instance):
        cals = 0
        prots = 0
        carbs = 0
        fats = 0
        # Compute a squared error
        for i in range(self.meals_per_day):
            cals += instance[i][1]
            prots += instance[i][2]
            carbs += instance[i][3]
            fats += instance[i][4]
        cals = (self.calories - cals) ** 2
        prots = (self.proteins - prots) ** 2
        carbs = (self.carbohydrates - carbs) ** 2
        fats = (self.fat - fats) ** 2
        return (0, cals, prots, carbs, fats)
