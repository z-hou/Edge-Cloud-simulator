#include<iostream>
#include<algorithm>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include<thread>
#include <mutex>
#include <future>
using std::vector;
namespace py = pybind11;

double FCFS_CPP(vector<double>& requests_series, vector<double>& service_time_series,  size_t servers_number) {

     if (requests_series.size() != service_time_series.size()){
         throw std::runtime_error("length of request and service should be same");
     }

     size_t queue_length = requests_series.size();


     //vector<double> stay_time(queue_length);
     vector<double> waiting_time(queue_length);
     vector<double> leaving_time(queue_length);
     vector<double> leave_time(servers_number);
     double stay_time;

     for (size_t idx = 0; idx < servers_number; idx++) {
        //double temp =  arrival_moment[i] + service_time_series[i]
        leaving_time[idx] = requests_series[idx] + service_time_series[idx];
        leave_time[idx] = leaving_time[idx];
     }

     for (size_t ind = servers_number; ind < queue_length; ind++) {

         size_t min_ind = min_element(leave_time.begin(),leave_time.end()) - leave_time.begin();
         float current_min_lt = *min_element(leave_time.begin(), leave_time.end());
         //std::cout << "check cpp: " << min_ind << " "<< current_min_lt << std::endl;
         if (requests_series[ind] <= current_min_lt) {
             waiting_time[ind] = current_min_lt - requests_series[ind];
             leaving_time[ind] = requests_series[ind] + waiting_time[ind] + service_time_series[ind];
         }
         else{
             waiting_time[ind] = 0;
             leaving_time[ind] = requests_series[ind] + service_time_series[ind] + waiting_time[ind];
         }
         leave_time[min_ind] = leaving_time[ind];
     }

     for (size_t i = 0; i < queue_length; i++){
         stay_time += waiting_time[i] + service_time_series[i];
     }

     double ave_stay_time = stay_time/queue_length;

     return ave_stay_time;
 
}


double FCFS_CPP_Mthreads(std::map<int, std::map<std::string, vector<double>>>& input_dict, size_t servers_number) {

    vector<std::shared_future<double>> fcfs_tasks;

    for (size_t idx = 0; idx < servers_number; idx++) {

        vector<double>& requests_series = input_dict[idx]["arrival_moment"];
        vector<double>& service_time_series = input_dict[idx]["service_time"];

        //std::shared_future<vector<double>> result = std::async(FCFS_CPP, std::ref(requests_series), std::ref(service_time_series), std::ref(stay_time), 1);
        std::shared_future<double> result = std::async(FCFS_CPP, std::ref(requests_series), std::ref(service_time_series), 1);

        fcfs_tasks.push_back(result);
    }


    vector<double> stay_time_list;
    for (size_t idx = 0; idx < servers_number; idx++){

        stay_time_list.push_back(fcfs_tasks[idx].get());

    }
    
    double stay_time;
    for (size_t idx = 0; idx < servers_number; idx++){
        stay_time += stay_time_list[idx];
    }

    double ave_stay_time = stay_time/servers_number;

    return ave_stay_time;

}


PYBIND11_MODULE(scheduler, m) {
	m.doc() = "calculate FCFS model for edge or cloud system";
	m.def("FCFS_CPP", &FCFS_CPP, "FCFS algorithm");
    m.def("FCFS_CPP_Mthreads", &FCFS_CPP_Mthreads, "FCFS algorithm for edge with multithreads");
}



















