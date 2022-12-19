import os
import numpy as np
#from Distribution_generator import *


def FCFS_py(arrival_moment, service_time_series, servers_number):
# arrival_moment:      The arrival time of each request
# service_time_series: The service duration for each request
# waiting_time:        The waiting duration for each request
# leaving_time:        The leaving time for each request
    arrival_moment = np.array(arrival_moment)
    service_time_series = np.array(service_time_series)
    waiting_time = np.zeros(len(arrival_moment))
    total_requests = len(arrival_moment)

    #events[1, :] = service_time_series       ##service time for each resquests
    #waiting_time = np.zeros(total_requests)    ##first batch of requests don't need waiting, so waiting time is zero
    leaving_time = np.zeros(total_requests)
    leave_time = np.zeros(servers_number)    ##

    for i in range(servers_number):
        leaving_time[i] = arrival_moment[i] + service_time_series[i]
        leave_time[i] = leaving_time[i]
    
    for ind in range(servers_number, total_requests):
        #print("check python: ", np.argmin(leave_time), " ", np.min(leave_time))
        if arrival_moment[ind] <= np.min(leave_time): #the ind th requests arrive time point
            #The proceed is undering serving, need wait
            waiting_time[ind] = np.min(leave_time) - arrival_moment[ind]#current request's waiting time
            leaving_time[ind] = arrival_moment[ind] + service_time_series[ind] + waiting_time[ind]
        else:
            waiting_time[ind] = 0#no need to wait as idle server exits
            leaving_time[ind] = arrival_moment[ind] + service_time_series[ind] + waiting_time[ind]
        
        leave_time[np.argmin(leave_time)] = leaving_time[ind]

    stay_time =  waiting_time + service_time_series
    #print("len of stay_time: ", len(stay_time))
    ave_stay_time = np.mean(stay_time)

    return ave_stay_time


if __name__ == '__main__':
    arrival_gap, service_time = General(1000)
    stay_time = FCFS(arrival_gap, service_time, 10)
    print(stay_time)
