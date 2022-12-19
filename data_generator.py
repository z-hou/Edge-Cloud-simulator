
import numpy as np
from Distribution_factory import *



def generate_Cdata(initial_lambd, max_lambd, mu_cloud, 
                   total_time, server_numbers, arr_distri_type, 
                   serve_distribution_type, cov_cloudA, cov_cloudB):
    #Assuming that servers' number at edge system and cloud system are equal


    lambd_timedata_dict = {}
    #service_time = generate_series("g", mu, que_length)##generate service time, it's up to 
    for lambd_ in range(initial_lambd, max_lambd):
        #print("check lambd: ", lambd_)
        arr_ser_dict = {}
        que_length = lambd_*total_time

        stddev = cov_cloudA*(1/lambd_)

        arr_time_interval = generate_series(arr_distri_type, lambd_, que_length, stddev)
        arrival_moment = np.cumsum(arr_time_interval)

        #print("check: ", serve_distribution_type, mu_cloud, que_length, cov_cloudB*(1/mu_cloud))

        service_time = generate_series(serve_distribution_type, mu_cloud, que_length, cov_cloudB*(1/mu_cloud))##generate service time, it's up to 

        #stay_time = np.zeros(que_length)

        arr_ser_dict["arrival_moment"] = arrival_moment.tolist()
        arr_ser_dict["service_time"] = service_time.tolist()
        #arr_ser_dict["stay_time"] = stay_time.tolist()
        lambd_timedata_dict[lambd_] = arr_ser_dict

    return lambd_timedata_dict



def generate_Edata(initial_lambd, max_lambd, mu_edge, 
                   total_time, server_numbers, arr_distri_type, 
                   serve_distribution_type, cov_edgeA, cov_edgeB, mode):
    
    lambd_timedata_dict = {}
    if mode == "skew":
        all_weights = []
        all_rho_edge = []
        lambd_list = []

    for lambd_ in range(initial_lambd, max_lambd):

        kth_edge_timedata_dict = {}
        

        if mode == "balance":
            edge_lambd = [lambd_/server_numbers for i in range(server_numbers)]
            
            #print(edge_lambd)
        elif mode == "skew":
            edge_lambd, weight_list, rho_edgei_list = gen_skew(server_numbers, lambd_, mu_edge)
            all_weights.append(weight_list)
            all_rho_edge.append(rho_edgei_list)
            lambd_list.append(lambd_)

        #print("Check edge lambda: ", edge_lambd)
        stddev_list = [cov_edgeA*(1/edge_lambd[i]) for i in range(server_numbers)]
        for i in range(server_numbers):
            #print("Gen_edge data")
        
            arr_ser_dict = {}
            que_length = edge_lambd[i] * total_time
            arr_time_interval = generate_series(arr_distri_type, edge_lambd[i], que_length, stddev_list[i])

            arrival_moment = np.cumsum(arr_time_interval)
            
            #print("Check queue length of edge skew: ", que_length)
            service_time = generate_series(serve_distribution_type, mu_edge, que_length, stddev=cov_edgeB*(1/mu_edge))

            if len(arrival_moment) != len(service_time):
                #print("Length of request queue and serve should be the same")
                print("length 0f request: ", len(arrival_moment), "length of service: ", len(service_time))
            
            #stay_time = np.zeros(int(que_length))

            arr_ser_dict["arrival_moment"] = arrival_moment.tolist()
            arr_ser_dict["service_time"] = service_time.tolist()
            #arr_ser_dict["stay_time"] = stay_time.tolist()

            kth_edge_timedata_dict[i] = arr_ser_dict
        lambd_timedata_dict[lambd_] = kth_edge_timedata_dict
    
    if mode == "balance":
        return lambd_timedata_dict
    else:
        return lambd_timedata_dict, all_weights, all_rho_edge, lambd_list