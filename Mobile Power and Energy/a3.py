import numpy as np
import pandas as pd
import copy

class A3:
    dataset = None

    def __init__(self):
        pass

    def  read_dataset(self):
        dataset = pd.read_csv('dataset.csv')
        self.dataset = dataset.to_numpy()

    # returns energy (J) consumed by a given application
    def app_energy_consumption(self, app_row, weight):
        summation = 0
        for j in range(len(weight)):
            summation += weight[j] * self.dataset[app_row][j + 1]

        return summation

    # return power (W)
    def power_consumption(self, app_row, weight):
        energy = self.app_energy_consumption(app_row, weight)
        power = energy / self.dataset[app_row][-1]
        
        return power        

    '''
    computes and returns the following statistics as a 3-tuple: average energy consumption
    across all applications, application with the highest energy consumption, application with the
    lowest energy consumption.
    '''
    # weight = [CPU_Usage, Memory Usage, Network_Activity, Disk_IO]
    def generate_energy_statistics(self, weight):
        avg_energy_consumption = 0
        highest_energy_consumer_app = None
        lowest_energy_consumer_app = None

        highest_energy_consumption = 0
        lowest_energy_consumption = -1

        for i in range(len(self.dataset)): # apps/rows
            energy_consumed = self.app_energy_consumption(i, weight)        
            
            avg_energy_consumption += energy_consumed
            if energy_consumed > highest_energy_consumption:
                highest_energy_consumption = energy_consumed
                highest_energy_consumer_app = self.dataset[i][0]

            if energy_consumed < lowest_energy_consumption or lowest_energy_consumption == -1:
                lowest_energy_consumption = energy_consumed
                lowest_energy_consumer_app = self.dataset[i][0]

        avg_energy_consumption = avg_energy_consumption / len(self.dataset)
        return (round(avg_energy_consumption, 2), highest_energy_consumer_app, lowest_energy_consumer_app)

    '''
    computes and returns the sensitivities of the following four (4) metrics on
    the energy consumption as a 4-tuple: CPU Usage, Memory Usage, Network Activity, Disk IO.
    '''
    def calculate_energy_sensitivites(self, weight):
        sum_metric_contributions = np.empty(len(weight))

        for i in range(len(self.dataset)):
            for j in range(len(sum_metric_contributions)):
                sum_metric_contributions[j] += weight[j] * self.dataset[i][j + 1]
        
        total_energy_consumption = np.sum(sum_metric_contributions)
        
        for i in range(len(sum_metric_contributions)):
            sum_metric_contributions[i] = (sum_metric_contributions[i] / total_energy_consumption) * 100

        return tuple(np.round(sum_metric_contributions, 2))

    '''
     computes and returns the following statistics as a 3-tuple: average power
     consumption across all applications, application with the highest power consumption,
     application with the lowest power consumption.
    '''
    def generate_power_statistic(self, weight):
        avg_power_consumption = 0
        highest_power_consumer_app = None
        lowest_power_consumer_app = None

        highest_power_consumption = 0
        lowest_power_consumption = -1

        for i in range(len(self.dataset)):
            power = self.power_consumption(i, weight)

            avg_power_consumption += power

            if (power > highest_power_consumption):
                highest_power_consumption = power
                highest_power_consumer_app = self.dataset[i][0]
            
            if (power < lowest_power_consumption or lowest_power_consumption == -1):
                lowest_power_consumption = power
                lowest_power_consumer_app = self.dataset[i][0]

        avg_power_consumption = avg_power_consumption / len(self.dataset)
        return (round(avg_power_consumption, 2), highest_power_consumer_app, lowest_power_consumer_app)

    '''
    computes and returns the sensitivities of the following four (4) metrics on
    the power consumption as a 4-tuple: CPU Usage, Memory Usage, Network Activity, Disk IO.
    '''
    def calculate_power_sensitivity(self, weight):
        power_contribution_of_metric = copy.deepcopy(self.dataset)
        total_power_contribution = np.empty(len(weight))

        for i in range(len(power_contribution_of_metric)):
            for j in range(len(weight)):
                power_contribution_of_metric[i][j + 1] = weight[j] * (power_contribution_of_metric[i][j + 1] / power_contribution_of_metric[i][-1])
                total_power_contribution[j] += power_contribution_of_metric[i][j + 1]

        total_power_consumption = np.sum(total_power_contribution)

        for i in range(len(total_power_contribution)):
            total_power_contribution[i] = (total_power_contribution[i] / total_power_consumption) * 100

        return tuple(np.round(total_power_contribution)) 

a3 = A3()
a3.read_dataset()
energy_stat = a3.generate_energy_statistics([1,2,3,4])
print("energy_stats (J):")
print("avg energy consumed:", energy_stat[0], "|highest energy consumed by:", energy_stat[1],
    "|lowest energy consumed by:", energy_stat[2])
energy_sensitivity = a3.calculate_energy_sensitivites([1,2,3,4])
print("energy_sensitivity (%):")
print("CPU_Usage:", energy_sensitivity[0],
    "|Memory_Usage:", energy_sensitivity[1],
    "|Network_Activity:", energy_sensitivity[2],
    "|Disk_IO:", energy_sensitivity[3])
power_stat = a3.generate_power_statistic([1,2,3,4])
print("power_stat (W):")
print("avg power consumed:", power_stat[0],
    "|highest power consumed by:", power_stat[1],
    "|lowest power consmed by:", power_stat[2])
power_sensitivity = a3.calculate_power_sensitivity([1,1,1,1])
print("idiot:", power_sensitivity)