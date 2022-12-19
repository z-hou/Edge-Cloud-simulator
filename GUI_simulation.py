import sys
#from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import numpy as np
import os
from theoritical_cal import *
from data_generator import generate_Cdata, generate_Edata
from matplotlib import pyplot as plt
from server import *
import time
import random



class Simulation_Gui(QWidget):
    def __init__(self, parent=None):#
        super(Simulation_Gui, self).__init__(parent)
        self.setWindowTitle('Edge Cloud Simulation')
        self.resize(1400, 900)

        mainLayout = QHBoxLayout(self)

        Basic_boxLayout = QGridLayout()

        system_layout = QVBoxLayout()#
        Cloud_boxLayout = QGridLayout()
        Edge_boxLayout = QGridLayout()
        
        all_resultLayout = QVBoxLayout()
        Visual_boxLayout = QGridLayout()
        result_valueLayout = QGridLayout()

        font = QFont()   
        font.setPointSize(15)
        font.setBold(True)

        lab_B = QLabel('Basic Configuration')
        lab_B.setFixedHeight(20)
        lab_B.setFont(font)

        #lab_B.setGeometry(0,0,100,30)
        label_total_time = QLabel('Total Time:')
        self.time_input = QSpinBox()
        self.time_input.setMaximum(220)
        self.time_input.setGeometry(100, 10, 160, 24)
        self.time_input.valueChanged.connect(self.detect_totaltime)
        

        label_init_lambda = QLabel('Initial lambda')
        self.Initial_lambda = QSpinBox()
        self.Initial_lambda.setGeometry(100, 10, 160, 24)
        self.Initial_lambda.valueChanged.connect(self.detect_Initial_lambda)

        label_server_rate = QLabel('service rate')
        self.service_rate = QSpinBox()
        self.service_rate.setGeometry(100, 10, 160, 24)
        self.service_rate.valueChanged.connect(self.detect_service_rate)

        label_severs_number = QLabel('severs number')
        self.severs_number = QSpinBox()
        self.severs_number.setGeometry(100, 10, 160, 24)
        self.severs_number.valueChanged.connect(self.detect_severs_number)
        
        #lab_B.setStyleSheet("QLabel{background:yellow;}")
        Basic_boxLayout.addWidget(lab_B, 0, 0)
        Basic_boxLayout.addWidget(label_total_time, 1, 0)
        Basic_boxLayout.addWidget(self.time_input, 1, 1)
        Basic_boxLayout.addWidget(label_init_lambda, 2, 0)
        Basic_boxLayout.addWidget(self.Initial_lambda, 2, 1)
        Basic_boxLayout.addWidget(label_server_rate, 3, 0)
        Basic_boxLayout.addWidget(self.service_rate, 3, 1)
        Basic_boxLayout.addWidget(label_severs_number, 4, 0)
        Basic_boxLayout.addWidget(self.severs_number, 4, 1)
        #Basic_boxLayout.setSpacing(1)
        
        lab_C = QLabel('Cloud Configuration')
        lab_C.setFont(font)
        lab_C.setFixedHeight(20)
        #lab_C.setStyleSheet("QLabel{background:yellow;}")
        label_rttC = QLabel('round-trip latency')
        self.rttC = QDoubleSpinBox()
        self.rttC.setGeometry(100, 10, 160, 24)
        self.rttC.setDecimals(2)
        self.rttC.valueChanged.connect(self.detect_rttC)
        
        label_disttiCR = QLabel('request distribution')
        self.dsrtiType_CR = QComboBox()
        self.dsrtiType_CR.addItems(['expntl', 'general', 'norm','k_erlang'])
        self.dsrtiType_CR.currentIndexChanged[str].connect(self.detect_dsrtiType_CR)

        label_disttiCS = QLabel('service distribution')
        self.dsrtiType_CS = QComboBox()
        self.dsrtiType_CS.addItems(['expntl', 'general', 'norm', 'k_erlang'])
        self.dsrtiType_CS.currentIndexChanged[str].connect(self.detect_dsrtiType_CS)

        label_cov_CR = QLabel('request COV')
        self.cov_CR = QDoubleSpinBox()
        self.cov_CR.setGeometry(100, 10, 160, 24)
        self.cov_CR.setDecimals(2)
        self.cov_CR.valueChanged.connect(self.detect_cov_CR)

        label_cov_CS = QLabel('service COV')
        self.cov_CS = QDoubleSpinBox()
        self.cov_CS.setGeometry(100, 10, 160, 24)
        self.cov_CS.setDecimals(2)
        self.cov_CS.valueChanged.connect(self.detect_cov_CS)

        Cloud_boxLayout.addWidget(lab_C, 0, 0)
        Cloud_boxLayout.addWidget(label_rttC, 1, 0)
        Cloud_boxLayout.addWidget(self.rttC, 1, 1)
        Cloud_boxLayout.addWidget(label_disttiCR, 2, 0)
        Cloud_boxLayout.addWidget(self.dsrtiType_CR, 2, 1)
        Cloud_boxLayout.addWidget(label_disttiCS, 3, 0)
        Cloud_boxLayout.addWidget(self.dsrtiType_CS, 3, 1)
        Cloud_boxLayout.addWidget(label_cov_CR, 4, 0)
        Cloud_boxLayout.addWidget(self.cov_CR, 4, 1)
        Cloud_boxLayout.addWidget(label_cov_CS, 5, 0)
        Cloud_boxLayout.addWidget(self.cov_CS, 5, 1)
        system_layout.addLayout(Cloud_boxLayout)

        lab_E = QLabel('Edge Configuration')
        lab_E.setFont(font)
        lab_E.setFixedHeight(20)
        #lab_C.setStyleSheet("QLabel{background:yellow;}")
        label_rttE = QLabel('round-trip latency')
        self.rttE = QDoubleSpinBox()
        self.rttE.setGeometry(100, 10, 160, 24)
        self.rttE.setDecimals(2)
        self.rttE.valueChanged.connect(self.detect_rttE)
        
        label_disttiER = QLabel('request distribution')
        self.dsrtiType_ER = QComboBox()
        self.dsrtiType_ER.addItems(['expntl', 'general', 'norm', 'k_erlang'])
        self.dsrtiType_ER.currentIndexChanged[str].connect(self.detect_dsrtiType_ER)

        label_disttiES = QLabel('service distribution')
        self.dsrtiType_ES = QComboBox()
        self.dsrtiType_ES.addItems(['expntl', 'general', 'norm', 'k_erlang'])
        self.dsrtiType_ES.currentIndexChanged[str].connect(self.detect_dsrtiType_ES)

        label_cov_ER = QLabel('request COV')
        self.cov_ER = QDoubleSpinBox()
        self.cov_ER.setGeometry(100, 10, 160, 24)
        self.cov_ER.setDecimals(2)
        self.cov_ER.valueChanged.connect(self.detect_cov_ER)

        label_cov_ES = QLabel('service COV')
        self.cov_ES = QDoubleSpinBox()
        self.cov_ES.setGeometry(100, 10, 160, 24)
        self.cov_ES.setDecimals(2)
        self.cov_ES.valueChanged.connect(self.detect_cov_ES)

        label_wl_mode = QLabel('workload mode')
        self.wl_mode = QComboBox()
        self.wl_mode.addItems(['balance', 'skew'])
        self.wl_mode.currentIndexChanged[str].connect(self.detect_wl_mode)

        self.btn1 = QPushButton("Start Simulation")
        self.btn1.clicked.connect(self.simulation)

        Edge_boxLayout.addWidget(lab_E, 0, 0)
        Edge_boxLayout.addWidget(label_rttE, 1, 0)
        Edge_boxLayout.addWidget(self.rttE, 1, 1)
        Edge_boxLayout.addWidget(label_disttiER, 2, 0)
        Edge_boxLayout.addWidget(self.dsrtiType_ER, 2, 1)

        Edge_boxLayout.addWidget(label_disttiES, 3, 0)
        Edge_boxLayout.addWidget(self.dsrtiType_ES, 3, 1)
        
        Edge_boxLayout.addWidget(label_cov_ER, 4, 0)
        Edge_boxLayout.addWidget(self.cov_ER, 4, 1)
        Edge_boxLayout.addWidget(label_cov_ES, 5, 0)
        Edge_boxLayout.addWidget(self.cov_ES, 5, 1)
        Edge_boxLayout.addWidget(label_wl_mode, 6, 0)
        Edge_boxLayout.addWidget(self.wl_mode, 6, 1)
        Edge_boxLayout.addWidget(self.btn1, 7, 1)


        system_layout.addLayout(Edge_boxLayout)

        lab_V = QLabel('Visualize')
        lab_V.setFont(font)
        lab_V.setFixedHeight(80)
        self.Label2 = QLabel("result")
        self.Label2.setText('')
        self.Label2.setFixedSize(700,600)
        self.Label2.setAlignment(Qt.AlignHCenter)#设置位置
        
        label_therotic_util = QLabel("Theoretical cut-off utilization")
        self.theo_util_value = QLabel()
        self.theo_util_value.setText('')
        self.theo_util_value.setWordWrap(True)

        label_simulate_util = QLabel("Simulation cut-off utilization")
        self.sim_util_value = QLabel()
        self.sim_util_value.setText('')
        self.sim_util_value.setWordWrap(True)



        #lab_V.setStyleSheet("QLabel{background:yellow;}")
        Visual_boxLayout.addWidget(lab_V, 0, 0)
        Visual_boxLayout.addWidget(self.Label2, 1, 0, 1, 2)
        Visual_boxLayout.addWidget(label_therotic_util, 2, 0)
        Visual_boxLayout.addWidget(self.theo_util_value, 2, 1)
        Visual_boxLayout.addWidget(label_simulate_util, 3, 0)
        Visual_boxLayout.addWidget(self.sim_util_value, 3, 1)

        result_valueLayout.addWidget(label_therotic_util, 0, 0, 2, 1)
        result_valueLayout.addWidget(self.theo_util_value, 0, 1, 2, 1)
        result_valueLayout.addWidget(label_simulate_util, 1, 0, 2, 1)
        result_valueLayout.addWidget(self.sim_util_value, 1, 1, 2, 1)
        all_resultLayout.addLayout(Visual_boxLayout)
        all_resultLayout.addLayout(result_valueLayout)


        
        mainLayout.addLayout(Basic_boxLayout)
        mainLayout.addLayout(system_layout)
        #mainLayout.addLayout(Visual_boxLayout)
        mainLayout.addLayout(all_resultLayout)

        ###simulation input parameters:
        self.total_sim_time = 200
        self.init_lambda_value = 0
        self.mu = 0
        self.k = 0

        self.cloud_rtt = 0
        self.cloud_Rdata_distr = 'expntl'
        self.cloud_Sdata_distr = 'expntl'
        self.cov_cloud_request = 0
        self.cov_cloud_service = 0

        self.edge_rtt = 0
        self.edge_Rdata_distr = 'expntl'
        self.edge_Sdata_distr = 'expntl'
        self.edge_wl_mode = 'balance'
        self.cov_edge_request = 0
        self.cov_edge_service = 0
        
       
    
    def detect_totaltime(self):
        self.total_sim_time = self.time_input.value()
        print("Set Total time: ", self.total_sim_time)
    
    def detect_Initial_lambda(self):
        self.init_lambda_value = self.Initial_lambda.value()
        print("Set initial lamdba: ", self.init_lambda_value)
    
    def detect_service_rate(self):
        self.mu = self.service_rate.value()
        print("Set service rate: ", self.mu)

    def detect_severs_number(self):
        self.k = self.severs_number.value()
        print("Set servers number: ", self.k)

    def detect_rttC(self):
        self.cloud_rtt = self.rttC.value()
        print("Set cloud round trip latency: ", self.cloud_rtt)
    
    def detect_dsrtiType_CR(self):
        self.cloud_Rdata_distr = self.dsrtiType_CR.currentText()
        print("Set cloud request data distribution type: ", self.cloud_Rdata_distr)
    
    def detect_dsrtiType_CS(self):
        self.cloud_Sdata_distr = self.dsrtiType_CS.currentText()
        print("Set cloud service data distribution type: ", self.cloud_Sdata_distr)

    def detect_cov_CR(self):
        self.cov_cloud_request = self.cov_CR.value()
        print("Set Cov of cloud request data: ", self.cov_cloud_request)

    def detect_cov_CS(self):
        self.cov_cloud_service = self.cov_CS.value()
        print("Set Cov of cloud service data", self.cov_cloud_service)


    def detect_rttE(self):
        self.edge_rtt = self.rttE.value()
        print("Set edge round trip latency: ", self.edge_rtt)

    def detect_dsrtiType_ER(self):
        self.edge_Rdata_distr = self.dsrtiType_ER.currentText()
        print("Set edge request data distribution type: ", self.edge_Rdata_distr)

    def detect_dsrtiType_ES(self):
        self.edge_Sdata_distr = self.dsrtiType_ES.currentText()
        print("Set edge service data distribution type: ", self.edge_Sdata_distr)

    def detect_cov_ER(self):
        self.cov_edge_request = self.cov_ER.value()
        print("Set Cov of edge request data: ", self.cov_edge_request)

    def detect_cov_ES(self):
        self.cov_edge_service = self.cov_ES.value()
        print("Set Cov of edge service data: ", self.cov_edge_service)

    def detect_wl_mode(self):
        self.edge_wl_mode = self.wl_mode.currentText()
        print("Set edge workload mode: ", self.edge_wl_mode)



    def simulation(self):
        rtt_cloud = self.cloud_rtt
        server_numbers = self.k
        lambd_cloud = self.init_lambda_value
        mu_cloud = self.mu
        max_lambd_cloud = int(mu_cloud*server_numbers)
        total_time = self.total_sim_time
        cloud_server = Cloud_Sever(rtt_cloud)
        #### parameter setting for Cloud system: G/G/k simulation ########


        #### parameter setting for Edge system:  c x G/G/1 simulation
        rtt_edge = self.edge_rtt
        lambd_edge = lambd_cloud
        mu_edge = mu_cloud
        max_lambd_edge = int(mu_edge*server_numbers)
        total_time_each_edge = total_time

        normalize_lambd_edge_list = []
        latency_list = []

        edge_server = Edge_Server(rtt_edge)
        #### parameter setting for Edge system:  c x G/G/1 simulation

    
        Carr_distri_type = self.cloud_Rdata_distr
        Cserve_distribution_type = self.cloud_Sdata_distr
        cov_cloudA = self.cov_cloud_request
        cov_cloudB = self.cov_cloud_service

        Earr_distri_type = self.edge_Rdata_distr
        Eserve_distribution_type = self.edge_Sdata_distr
        cov_edgeA = self.cov_edge_request
        cov_edgeB = self.cov_edge_service
        workload_mode = self.edge_wl_mode

        cloud_input = generate_Cdata(lambd_cloud, max_lambd_cloud, 
                                  mu_cloud, total_time, server_numbers, 
                                  Carr_distri_type, Cserve_distribution_type, cov_cloudA, cov_cloudB)
        
        if workload_mode == "balance":
            edge_input = generate_Edata(lambd_edge, max_lambd_edge, mu_edge, 
                                 total_time, server_numbers, Earr_distri_type, 
                                 Eserve_distribution_type, cov_edgeA, cov_edgeB, workload_mode)
            ####Calculate the Theoretical value
            rho_cutoff_theo = balance_theo(rtt_cloud, rtt_edge, server_numbers, mu_edge, cov_edgeA, cov_edgeB, cov_cloudA, cov_cloudB,
                                           Earr_distri_type, Eserve_distribution_type, Carr_distri_type, Cserve_distribution_type)

            print("thepritical rho_cutoff is: ", rho_cutoff_theo)
        
        if workload_mode == "skew":
            edge_input, all_weights, all_rho_edge, lambd_list = generate_Edata(lambd_edge, max_lambd_edge, mu_edge, 
                                                         total_time, server_numbers, Earr_distri_type, 
                                                         Eserve_distribution_type, cov_edgeA, cov_edgeB, workload_mode)

            rho_cutoff_theo = skew_theo(rtt_cloud, rtt_edge, server_numbers, mu_edge, lambd_list, all_weights, all_rho_edge)
            print("Delta_n is: ", rtt_cloud - rtt_edge)
            print("thepritical rho_cutoff is: ", rho_cutoff_theo)

        self.theo_util_value.setText(str(round(rho_cutoff_theo, 3)))

        ####Simulation In Cloud
        print("Check server numbers: ", server_numbers)
        cloud_normalize_lambd, cloud_mean_latency = cloud_simulation(cloud_server, lambd_cloud, max_lambd_cloud, cloud_input, server_numbers, perf_level=1)
        edge_normalize_lambd, edge_mean_latency = edge_simulation(edge_server, lambd_edge, max_lambd_edge, edge_input, server_numbers, perf_level=2)

        result = get_crosspoint(cloud_normalize_lambd, cloud_mean_latency, edge_mean_latency)
        if result != None:
            lambd_cutoff = result[0]
            rho_cutoff = result[0]/mu_edge
        else:
            rho_cutoff = 0
    
        print("Simulation rho cutoff is: ", rho_cutoff)
        self.sim_util_value.setText(str(round(rho_cutoff, 3)))

        ###draw picture
        plt.figure()
        plt.plot(cloud_normalize_lambd, cloud_mean_latency, color='b', label='cloud system 1x G/G/{}'.format(server_numbers))
        plt.plot(edge_normalize_lambd, edge_mean_latency, color='g', label='edge system {} x G/G/1'.format(server_numbers))
        #if  result != None:
        #    plt.annotate('rho_cutoff: {}'.format('%.2f%%' % (rho_cutoff * 100)), xy=(result[0], result[1]),xytext=(result[0], result[1]), fontsize=16, arrowprops=dict(arrowstyle="->"))
        plt.xlabel('requests/server/s')
        plt.ylabel('mean end to end latency')
        plt.legend()
        plt.savefig('./result.jpg')
        self.Label2.setPixmap(QPixmap('./result.jpg'))






if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Simulation_Gui()
    demo.show()
    sys.exit(app.exec_())

