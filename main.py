import random
import csv
from random import randint
from datetime import datetime

estimates_count = 1000
points = [1,2,3,5,8,13,20]

class Employee:
    #у каждого сотрудника есть свойство - насколько качественно он оценивает задачи разработки и тестирования
    def __init__(self, devtasks_accuracy, testtask_accuracy):
        self.devtasks_accuracy = devtasks_accuracy # проценты, насколько человек отклоняется от реальной оценки задачи
        self.testtask_accuracy = testtask_accuracy

    def get_estimate(self, expected_estimate):
        devtask_estimate = expected_estimate.devtask_estimate + random.uniform(-self.devtasks_accuracy, self.devtasks_accuracy)
        testtask_estimate = expected_estimate.testtask_estimate + random.uniform(-self.testtask_accuracy, self.testtask_accuracy)
        return Estimation(devtask_estimate, testtask_estimate)

class Estimation:
    def __init__(self, devtask_estimate, testtask_estimate):
        self.devtask_estimate = devtask_estimate
        self.testtask_estimate = testtask_estimate

def simulate(simulations_count):
    result = []
    for _ in range(simulations_count):
        dev_dev_accuracy = random.uniform(0, 0.5)
        dev_test_accuracy = random.uniform(0.2, 1)
        test_dev_accuracy = random.uniform(0.2, 1)
        test_test_accuracy = random.uniform(0, 0.5)
        developer = Employee(dev_dev_accuracy, dev_test_accuracy)
        tester = Employee(test_dev_accuracy, test_test_accuracy)
        accuracies = (dev_dev_accuracy, dev_test_accuracy, test_dev_accuracy, test_test_accuracy)
        simulation = simulate_once(developer, tester)
        result.append(accuracies + simulation)
    return result

def simulate_once(developer, tester):
    random.seed(datetime.now())
    expected_estimates = [get_random_points() for i in range(estimates_count)]
    dev_actual_estimates =  [developer.get_estimate(expected_estimate) for expected_estimate in expected_estimates]
    test_actual_estimates = [tester.get_estimate(expected_estimate) for expected_estimate in expected_estimates]
    
    total_common = get_total_estimate_diff_common_case(developer, tester, expected_estimates, dev_actual_estimates, test_actual_estimates)
    total_max = get_total_estimate_diff_max_case(developer, tester, expected_estimates, dev_actual_estimates, test_actual_estimates)
    total_avg = get_total_estimate_diff_avg_case(developer, tester, expected_estimates, dev_actual_estimates, test_actual_estimates)
    return (total_common, total_max, total_avg)    

#когда всё вместе оценивается
def get_total_estimate_diff_common_case(developer, tester, expected_estimates, dev_actual_estimates, test_actual_estimates):
    dev_total = sum_all_estimates(dev_actual_estimates)
    test_total = sum_all_estimates(test_actual_estimates)
    actual_total = dev_total + test_total

    expected_total = sum_all_estimates(expected_estimates) * 2
    return abs(expected_total - actual_total)

#по отдельности, берем максимум
def get_total_estimate_diff_max_case(developer, tester, expected_estimates, dev_actual_estimates, test_actual_estimates):
    dev_total = sum(estimate.devtask_estimate for estimate in dev_actual_estimates)
    test_total = sum(estimate.testtask_estimate for estimate in test_actual_estimates)
    actual_max = max(dev_total,test_total)

    expected_dev = sum(estimate.devtask_estimate for estimate in expected_estimates)
    expected_test = sum(estimate.testtask_estimate for estimate in expected_estimates)
    expected_max = max(expected_dev, expected_test)
    return abs(expected_max - actual_max)

#по отдельности, берем среднее
def get_total_estimate_diff_avg_case(developer, tester, expected_estimates, dev_actual_estimates, test_actual_estimates):
    dev_total = sum(estimate.devtask_estimate for estimate in dev_actual_estimates)
    test_total = sum(estimate.testtask_estimate for estimate in test_actual_estimates)
    actual_avg = (dev_total + test_total)/2

    expected_dev = sum(estimate.devtask_estimate for estimate in expected_estimates)
    expected_test = sum(estimate.testtask_estimate for estimate in expected_estimates)
    expected_avg = (expected_dev + expected_test)/2
    return abs(expected_avg - actual_avg)

def sum_all_estimates(estimates):
    return sum(estimate.devtask_estimate + estimate.testtask_estimate for estimate in estimates)

#получаем оценки фибоначчи
def get_random_points():
    dev_points = points[randint(0, len(points)-1)]
    test_points = points[randint(0, len(points)-1)]
    return Estimation(dev_points, test_points)

def print_simulation_result(simulation_result, filepath):
    with open(filepath, mode='w', newline='') as csv_file:
        employee_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(['dev_dev_accuracy', 'dev_test_accuracy', 'test_dev_accuracy', 'test_test_accuracy', 'total_common_diff', 'total_max_diff', 'total_avg_diff'])

        for row in simulation_result:
            employee_writer.writerow(row)

simulation_result = simulate(100)
print_simulation_result(simulation_result, 'simulations.csv')

