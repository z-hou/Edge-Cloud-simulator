import math
import random
import numpy as np
from scipy import stats
from numpy.random import exponential
#from simpy import *


def gen_pair(average):
    numarr = []
    i = 0
    while (1):
 
      num_first = np.random.rand()
 
      num_second = average * 2 - num_first

      if (num_first > 0 and num_second > 0):
          numarr.append(num_first)
          i = i + 1
          numarr.append(num_second)
          break
    #print("len of aum_arr: ", len(numarr))
    return numarr


def general_distribution(lambd, length):

    average = 1/lambd
    final_list = []
    for i in range(int(length/2)):
        array_pair = gen_pair(average)
        final_list += array_pair
    if len(final_list) < int(length):
        final_list.append(average)
    #print("length in general_distribution: ", len(final_list))
    generate_series = np.array(final_list)
    np.random.shuffle(generate_series)
    #print(len(generate_series))

    return generate_series




def expntl(lambd, length):
    """
    negative exponential distribution
    """
    length = int(length)
    result = np.zeros(length)
    for i in range(length):
        u = random.random()
        result[i] = (-1/lambd) * math.log(u)
    #result = stats.expon.rvs(1/lambd, size=int(length)) 
    return result

#def possion(lambd, length):

    #return np.random.poisson(1/lambd, size=int(length))
#    return stats.poisson.rvs(1/lambd, size=int(length))


def Gaussion(lambd, stddev, length):
    
    low = 0
    high = 1
    mean = 1.0/lambd
    a = (low - mean) / stddev
    b = (high - mean) / stddev
    #print("check mean: ", round(1/lambd, 2), "check stddev: ", stddev)
    #print(type(a)," ",a, " ", type(b)," ",b, " ",mean, " ", stddev, " ", length)
    result = stats.truncnorm.rvs(a, b, loc=mean, scale=stddev, size=int(length))
    
    return result

def k_erlang(k, lambd, length):
    generator=rng(erlang(k), 1/lambd)
    result=[]
    for i in range(int(length)):
        result.append(generator())
    result = np.array(result)

    return result

    


def generate_series(distribution_type, lambd, length, stddev):

    if distribution_type == "expntl":
    
        return expntl(lambd, length)
        
    if distribution_type == "general":
    
        return general_distribution(lambd, length)
    
    if distribution_type == "norm":
    
        return Gaussion(lambd, stddev, length)

    #if distribution_type == "possion":
    
    #    return possion(lambd, length)
    
    if distribution_type == "k_erlang":

        return k_erlang(9, lambd, length)

    
def rng(dis,param):
    """random number generator"""
    def generate():
        return dis(lam=param,size=1)[0]
    return generate

def erlang(k):

    def exp2erlang(lam,size):
        res=[]
        for n in range(size):
            k_poisson= exponential(lam/k,size=k)
            sum=0
            for x in k_poisson:
                sum = sum + x
            res.append(sum)
        return res
    return exp2erlang

   


def gen_skew(n, max_value, mu_edge):

    ave_lamdba = max_value/n
    edge_lambda_list = [ave_lamdba for i in range(n)]
    donate_range_max = ave_lamdba
    accpet_range_max = mu_edge - ave_lamdba
    ture_range = min(donate_range_max, accpet_range_max)
    for i in range(int(n/2)):
        gap = random.uniform(0.01, ture_range-0.01)
        edge_lambda_list[i] -= gap
        edge_lambda_list[i+int(n/2)] +=  gap

    weight_list = [ item/max_value for item in edge_lambda_list]
    rho_edgei_list = [ item/mu_edge for item in edge_lambda_list]

    #print("Edge lambda list in skew mode: ", edge_lambda_list)
    #print("check each weight in skew mode: ", weight_list)
    #print("sum of weights: ", sum(weight_list))
    return edge_lambda_list, weight_list, rho_edgei_list

if __name__ == '__main__':
    a = possion(15, 1000)
    print(np.mean(a))
    print(np.std(a))
    print(np.std(a)/np.mean(a))
    #arr=k_erlang(4, 5, 1000)
    #print(np.mean(arr))
    #print(np.std(arr))
    #print(np.std(arr)/np.mean(arr))