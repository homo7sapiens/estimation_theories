import random
import csv
from random import randint
from datetime import datetime

sprint_tasks_size = 10
points = [1,2,3,5,8,13,20]

class Employee:
    #у каждого сотрудника есть свойство - насколько качественно он оценивает задачи разработки и тестирования
    def __init__(self, devtasks_accuracy, testtask_accuracy):
        self.devtasks_accuracy = devtasks_accuracy # проценты, насколько человек может максимально отклониться от реальной оценки
        self.testtask_accuracy = testtask_accuracy

    def get_estimate(self, expected_estimate):
        devtask_estimation = expected_estimate.devtask_estimation * ( 1 + random.uniform(-self.devtasks_accuracy, self.devtasks_accuracy))
        testtask_estimation = expected_estimate.testtask_estimation * (1 + random.uniform(-self.testtask_accuracy, self.testtask_accuracy))
        return Estimation(devtask_estimation, testtask_estimation)

class Estimation:
    def __init__(self, devtask_estimation, testtask_estimation):
        self.devtask_estimation = devtask_estimation
        self.testtask_estimation = testtask_estimation

    def get_summ(self):
        return self.devtask_estimation + self.testtask_estimation

    def get_max(self):
        return max(self.devtask_estimation, self.testtask_estimation)

    def get_avg(self):
        return (self.devtask_estimation + self.testtask_estimation)/2

class EstimationStrategy:
    def get_total_diff(self, expected_estimations, actual_developer_estimations, actual_tester_estimations):
        zipped = zip(expected_estimations, actual_developer_estimations, actual_tester_estimations)
        total_diff = sum(self.get_diff(*row) for row in zipped)
        return abs(total_diff)

class CommonEstimationStrategy(EstimationStrategy):
    def get_diff(self, expected_estimation, actual_developer_estimation, actual_tester_estimation):
        dev_diff = expected_estimation.get_summ() - actual_developer_estimation.get_summ()
        test_diff = expected_estimation.get_summ() - actual_tester_estimation.get_summ()
        return dev_diff + test_diff

class SeparateGetMaxEstimationStrategy(EstimationStrategy):
    def get_diff(self, expected_estimation, actual_developer_estimation, actual_tester_estimation):
        expected_max = expected_estimation.get_max()
        actual_max = max(actual_developer_estimation.devtask_estimation, actual_tester_estimation.testtask_estimation)
        return expected_max - actual_max

class SeparateGetAvgEstimationStrategy(EstimationStrategy):
    def get_diff(self, expected_estimation, actual_developer_estimation, actual_tester_estimation):
        expected_avg = expected_estimation.get_avg()
        actual_avg = (actual_developer_estimation.devtask_estimation + actual_tester_estimation.testtask_estimation)/2
        return expected_avg - actual_avg

def simulate(simulations_count):
    result = []
    common_strategy = CommonEstimationStrategy()
    separate_max_strategy = SeparateGetMaxEstimationStrategy()
    separate_avg_strategy = SeparateGetAvgEstimationStrategy()
    for _ in range(simulations_count):
        dev_dev_accuracy = random.uniform(0, 0.5)
        dev_test_accuracy = random.uniform(0.2, 1)
        test_dev_accuracy = random.uniform(0.2, 1)
        test_test_accuracy = random.uniform(0, 0.5)
        developer = Employee(dev_dev_accuracy, dev_test_accuracy)
        tester = Employee(test_dev_accuracy, test_test_accuracy)
        accuracies = (dev_dev_accuracy, dev_test_accuracy, test_dev_accuracy, test_test_accuracy)

        simulation = simulate_once(developer, tester, common_strategy, separate_max_strategy, separate_avg_strategy)
        result.append(accuracies + simulation)
    return result

def simulate_once(developer, tester, common_strategy, separate_avg_strategy, separate_max_strategy):
    random.seed(datetime.now())
    expected_estimations = [get_random_estimations() for i in range(sprint_tasks_size)]
    actual_developer_estimations =  [developer.get_estimate(expected_estimation) for expected_estimation in expected_estimations]
    actual_tester_estimations = [tester.get_estimate(expected_estimation) for expected_estimation in expected_estimations]
    
    total_common = common_strategy.get_total_diff(expected_estimations, actual_developer_estimations, actual_tester_estimations)
    total_max = separate_avg_strategy.get_total_diff(expected_estimations, actual_developer_estimations, actual_tester_estimations)
    total_avg = separate_max_strategy.get_total_diff(expected_estimations, actual_developer_estimations, actual_tester_estimations)    
    return (total_common, total_max, total_avg)    

#получаем оценки фибоначчи
def get_random_estimations():
    dev_points = points[randint(0, len(points)-1)]
    test_points = points[randint(0, len(points)-1)]
    return Estimation(dev_points, test_points)

def print_simulation_result(simulation_result, filepath):
    with open(filepath, mode='w', newline='') as csv_file:
        employee_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(['dev_dev_accuracy', 'dev_test_accuracy', 'test_dev_accuracy', 'test_test_accuracy', 'total_common_diff', 'total_max_diff', 'total_avg_diff'])

        for row in simulation_result:
            employee_writer.writerow(row)

if __name__ == '__main__':
    simulation_result = simulate(1000)
    print_simulation_result(simulation_result, 'simulation.csv')

