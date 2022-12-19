import numpy as np
import os
#from Distribution_generator import *
from theoritical_cal import *
from data_generator import generate_Cdata, generate_Edata
from matplotlib import pyplot as plt
from server import Cloud_Sever, Edge_Server
import time
import random


    


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

    normalize_lambd = []
    mean_latency = []
    
    for lambd_ in range(initial_lambd, max_lambd):
        input_dict = edge_input[lambd_]


        final_ave_lantency = edge_server.execution(input_dict, server_numbers, perf_level)##可以用多线程
        #final_ave_lantency = np.mean(latency_all)

        normalize_lambd.append(lambd_ / server_numbers)
        mean_latency.append(final_ave_lantency)
    
    return normalize_lambd, mean_latency





if __name__ == '__main__':

    ####SETTING PARAMETERS
    #### parameter setting for Cloud system: G/G/k simulation ########
    rtt_cloud = 0.2
    server_numbers = 4
    lambd_cloud = 5
    mu_cloud = 15
    max_lambd_cloud = int(mu_cloud*server_numbers)
    total_time = 200
    cloud_server = Cloud_Sever(rtt_cloud)
    #### parameter setting for Cloud system: G/G/k simulation ########


    #### parameter setting for Edge system:  c x G/G/1 simulation
    rtt_edge = 0.01
    lambd_edge = lambd_cloud
    mu_edge = mu_cloud
    max_lambd_edge = int(mu_edge*server_numbers)
    total_time_each_edge = total_time

    normalize_lambd_edge_list = []
    latency_list = []

    edge_server = Edge_Server(rtt_edge)
    #### parameter setting for Edge system:  c x G/G/1 simulation

    
    Carr_distri_type = "general"
    Cserve_distribution_type = "general"
    cov_cloudA = 0.5
    cov_cloudB = 0.5
    #### Generate Distribution data for cloud
    cloud_input = generate_Cdata(lambd_cloud, max_lambd_cloud, 
                                  mu_cloud, total_time, server_numbers, 
                                  Carr_distri_type, Cserve_distribution_type, cov_cloudA, cov_cloudB)

    
    Earr_distri_type = "general"
    Eserve_distribution_type = "general"
    cov_edgeA = 0.5
    cov_edgeB = 0.5
    #### Generate Distribution data for edge
    workload_mode = "skew"
    if workload_mode == "balance":
        edge_input = generate_Edata(lambd_edge, max_lambd_edge, mu_edge, 
                                 total_time, server_numbers, Earr_distri_type, 
                                 Eserve_distribution_type, cov_edgeA, cov_edgeB, workload_mode)
        ####Calculate the Theoretical value
        rho_cutoff_theo = balance_theo(rtt_cloud, rtt_edge, server_numbers, mu_edge, cov_edgeA, cov_edgeB, cov_cloudA, cov_cloudB,
                                       Earr_distri_type, Eserve_distribution_type, Carr_distri_type, Cserve_distribution_type)
        print("thepritical rho_cutoff is: {:.1%}".format(rho_cutoff_theo))
        
    if workload_mode == "skew":
        edge_input, all_weights, all_rho_edge, lambd_list = generate_Edata(lambd_edge, max_lambd_edge, mu_edge, 
                                                         total_time, server_numbers, Earr_distri_type, 
                                                         Eserve_distribution_type, cov_edgeA, cov_edgeB, workload_mode)
        all_gap = skew_theo(rtt_cloud, rtt_edge, server_numbers, mu_edge, lambd_list, all_weights, all_rho_edge)
        print("Delta_n is: ", rtt_cloud - rtt_edge)
        print("thepritical rho_cutoff is: {:.1%}".format(all_gap))
        ####Calculate the Theoretical value

        
    #### Generate Distribution data



    ####Calculate the Theoretical value

    ####Simulation In Cloud
    cloud_normalize_lambd, cloud_mean_latency = cloud_simulation(cloud_server, lambd_cloud, max_lambd_cloud, cloud_input, server_numbers, perf_level=1)
    edge_normalize_lambd, edge_mean_latency = edge_simulation(edge_server, lambd_edge, max_lambd_edge, edge_input, server_numbers, perf_level=2)
    ####Simulation In Cloud

    #print("Check Horizontal coordinate_1: ", cloud_normalize_lambd)
    #print("Check Horizontal coordinate_1: ", edge_normalize_lambd)

    result = get_crosspoint(cloud_normalize_lambd, cloud_mean_latency, edge_mean_latency)
    if result != None:
        lambd_cutoff = result[0]
        rho_cutoff = result[0]/mu_edge
    else:
        rho_cutoff = 0
    
    print("Simulation rho cutoff is: {:.1%}".format(rho_cutoff))

    
    ###draw picture
    plt.figure()
    plt.plot(cloud_normalize_lambd, cloud_mean_latency, color='b', label='cloud system 1x G/G/{}'.format(server_numbers))
    plt.plot(edge_normalize_lambd, edge_mean_latency, color='g', label='edge system {} x G/G/1'.format(server_numbers))
    #if  result != None:
    #    plt.annotate('rho_cutoff: {}'.format('%.2f%%' % (rho_cutoff * 100)), xy=(result[0], result[1]),xytext=(result[0], result[1]), fontsize=16, arrowprops=dict(arrowstyle="->"))
    plt.xlabel('requests/server/s')
    plt.ylabel('mean end to end latency')
    
    plt.legend()
    plt.savefig('./report_source/result_test.jpg')
    #plt.show()
    
    

    '''
    #draw delta_n and gap picture to see the cutoff value
    delta_n = [rtt_cloud - rtt_edge for i in range(len(cloud_normalize_lambd))]
    plt.figure()
    plt.plot(cloud_normalize_lambd, delta_n, color='b', label='delta_n')
    plt.plot(cloud_normalize_lambd, all_gap, color='g', label='changed gap')

    plt.xlabel('requests/server/s')
    plt.ylabel('cutoff utilization')
    plt.legend()
    plt.show()
    '''
    

