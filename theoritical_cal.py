import numpy as np
import math


distriType_cov_dict = {"expntl": 1,
                       "k_erlang": 0.333}


def get_crosspoint(hori_aix, latency_cloud, latency_edge):
    
    for i in range(len(latency_cloud)-1):
        if latency_cloud[i] > latency_edge[i] and latency_cloud[i+1] < latency_edge[i+1]:
            x1 = hori_aix[i]
            y1 = latency_cloud[i]
            x2 = hori_aix[i+1]
            y2 = latency_cloud[i+1]
    
            x3 = x1
            y3 = latency_edge[i]
            x4 = x2
            y4 = latency_edge[i+1]

            k1=(y2-y1)*1.0/(x2-x1)
            b1=y1*1.0-x1*k1*1.0
            if (x4-x3)==0:
                k2=None
                b2=0
            else:
                k2=(y4-y3)*1.0/(x4-x3)
                b2=y3*1.0-x3*k2*1.0
            if k2==None:
                x=x3
            else:
                x=(b2-b1)*1.0/(k1-k2)
                y=k1*x*1.0+b1*1.0
            return [x,y]
        
    return None


def balance_theo(rtt_c, rtt_e, server_numbers, u_edge, 
                 cov_edgeA, cov_edgeB, cov_cloudA, cov_cloudB,
                 cov_edgeA_distriType, cov_edgeB_distriType, cov_cloudA_distriType, cov_cloudB_distriType):

    
    delta_rtt = rtt_c - rtt_e
    
    if cov_edgeA_distriType in ["expntl", "k_erlang", "possion"]:
        cov_edgeA = distriType_cov_dict[cov_edgeA_distriType]

    if cov_edgeB_distriType in ["expntl", "k_erlang", "possion"]:
        cov_edgeB = distriType_cov_dict[cov_edgeB_distriType]

    if cov_cloudA_distriType in ["expntl", "k_erlang", "possion"]:
        cov_cloudA = distriType_cov_dict[cov_cloudA_distriType]
    
    if cov_cloudB_distriType in ["expntl", "k_erlang", "possion"]:
        cov_cloudB = distriType_cov_dict[cov_cloudB_distriType]
    
    print("cov_cloudA: ", cov_cloudA)
    print("cov_cloudB: ", cov_cloudB)
    print("cov_edgeA: ", cov_cloudA)
    print("cov_edgeB: ", cov_cloudB)
    #below implemention for k -> OO
    #m = 2*delta_rtt*u_edge/(math.pow(cov_edgeA,2) + math.pow(cov_edgeB,2))
    #rho_cutoff = m/(m+1)
    m1 = (math.pow(cov_edgeA,2) + math.pow(cov_edgeB,2))/2
    m2 = (math.pow(cov_cloudA,2) + math.pow(cov_cloudB,2))/(2*server_numbers)
    n = delta_rtt*u_edge/(m1 - (3*m2)/4)
    #n = delta_rtt*u_edge/(m1 - m2)

    rho_cutoff = n/(n+1)

    return rho_cutoff




def skew_theo(rtt_c, rtt_e, server_numbers, u_edge, lambd_list, all_weights, all_rho_edge):

    delta_rtt = rtt_c - rtt_e
    if len(lambd_list) == len(all_weights) and len(all_weights) == len(all_rho_edge):
        all_gap = []
        #print("The length of lambda: ", len(lambd_list))
        for i in range(len(lambd_list)):
            rho_cloud = lambd_list[i] / (server_numbers*u_edge)
            #print("Check Lambda: ", lambd_list[i])
            #print("check rho_cloud in skew_theo: ", rho_cloud)
            m1 = 1/(math.pow(server_numbers, 0.5) * (1 - rho_cloud))
            w_j =  np.array(all_weights[i])
            rho_edge_j = np.array(all_rho_edge[i])
            #print("Check rho_edge_j: ", rho_edge_j)
            temp = w_j/(1-rho_edge_j)
            m2 = np.sum(temp)/server_numbers
            gap = math.pow(2, 0.5) * (m2 - m1)
            #all_gap.append(gap)
            if gap > delta_rtt:
                print("find cutoff utilization: ", rho_cloud)
                return rho_cloud

        #return all_gap
            


