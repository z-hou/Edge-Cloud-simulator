import os
import numpy as np
#from Distribution_generator import generate_series
from scheduler_python import FCFS_py
from matplotlib import pyplot as plt
from scheduler import FCFS_CPP, FCFS_CPP_Mthreads
from abc import ABCMeta, abstractmethod


class Base_Sever(metaclass=ABCMeta):
    def __init__(self, round_trip_latency):
        self.rtt = round_trip_latency

    @abstractmethod
    def execution(self):
        """
        Scheduler execution
        :return:
        """
        pass



class Cloud_Sever(Base_Sever):

    def execution(self, requests_series, service_sequence, k, perf_level):

        if perf_level == 0:
            return FCFS_py(requests_series, service_sequence, k) + self.rtt

        elif perf_level == 1:
            return FCFS_CPP(requests_series, service_sequence, k) + self.rtt



class Edge_Server(Base_Sever):

    def execution(self, input_dict, server_numbers, perf_level):

        if perf_level == 2:
            return FCFS_CPP_Mthreads(input_dict, server_numbers) + self.rtt
        
        #out_staytime = []
        for i in range(server_numbers):
            requests_series = input_dict[i]["arrival_moment"]
            service_sequence = input_dict[i]["service_time"]
            stay_time_list = input_dict[i]["stay_time"]

            #execution in G/G/1 mode

            if high_perf == 0:
                kedge_staytime = FCFS_py(requests_series, service_sequence, stay_time_list, 1) + self.rtt
            
            elif high_perf == 1:
                kedge_staytime = FCFS_CPP(requests_series, service_sequence, 1) + self.rtt

            #out_staytime.append(kedge_staytime)
        
        return kedge_staytime

def cloud_simulation(cloud_server, initial_lambd, max_lambd, cloud_input, server_numbers, perf_level):

    normalize_lambd = []
    mean_latency = []

    for lambd_ in range(initial_lambd, max_lambd):

        arrival_moment_list = cloud_input[lambd_]["arrival_moment"]
        service_time_list = cloud_input[lambd_]["service_time"]
        #stay_time_list = cloud_input[lambd_]["stay_time"]

        ave_latency = cloud_server.execution(arrival_moment_list, service_time_list, server_numbers, perf_level)
            #ave_latency = np.mean(latency_all)
        
        normalize_lambd.append(lambd_ / server_numbers)
        mean_latency.append(ave_latency)
    
    return normalize_lambd, mean_latency

def edge_simulation(edge_server, initial_lambd, max_lambd, edge_input, server_numbers, perf_level):

    ei = edge_input
    normalize_lambd = []
    mean_latency = []
    
    for lambd_ in range(initial_lambd, max_lambd):
        input_dict = ei[lambd_]


        final_ave_lantency = edge_server.execution(input_dict, server_numbers, perf_level)
        #final_ave_lantency = np.mean(latency_all)

        normalize_lambd.append(lambd_ / server_numbers)
        mean_latency.append(final_ave_lantency)
    
    return normalize_lambd, mean_latency


if __name__ == '__main__':

    rtt = 20
    k = 1
    lambd = 5
    mu = 10
    max_lambd = int(mu*k)

    total_time = 200
    que_length = int(total_time*lambd*k)
    sever = Base_sever(rtt)
    horizontal_axis = []
    vertical_axis = []
    service_time = generate_series("m", mu, que_length)
    
    for lambd_ in range(lambd, max_lambd):

        arr_time_interval = generate_series("m", lambd_, que_length)


        latency_all = sever.execution(arr_time_interval, service_time, k)
        latency = np.mean(latency_all)
        horizontal_axis.append(lambd_)
        vertical_axis.append(latency)

    plt.plot(horizontal_axis, vertical_axis)
    plt.show()
