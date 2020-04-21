#-*- coding: utf-8 -*-
import os
import sys 

class Instance:
   
  def __init__(self,horizon,resources_number,interventions_number,scenarios_number,alpha,tau,computation_time):
    self.horizon = horizon
    self.resources_number = resources_number  #Total of resouces number 
    self.interventions_number = interventions_number  #Total number of interventions 
    self.scenarios_number = scenarios_number   #Total of scenario number 
    self.alpha = alpha
    self.tau = tau 
    self.computation_time = computation_time
    self.t_max = list()
    self.delta_i_t = list()  #Processing times of each intervention in each time period
    self.l_c_t = list()  #Lower capacities of each resource in each time period
    self.u_c_t = list()  #Higher capacities of each resource in each time period 
    self.interventions_json_number = list() #This list will contains the real number of the interventions as defined in the 
    #.json file 
    self.resources_real_number = list() #This list will contains the real numbers of the resources as defined in the .json file
    #, the number in resources_real_number are sorted. The last number in resources_real_number corresponds to "Resources_control"
    self.r_c_i_t_t1 = dict()
    self.risk_s_i_t_t1 = dict()
    self.seasons = dict()
    self.exclusions = dict()

    return 
        

  def show_basic_details(self):
    print("              ##################################################################################################################")
    print("                  ###########################################################################################################")
    print("                      ####################################################################################################")
    print("                         ##################################### Basic details #########################################")
    print("                      ####################################################################################################")
    print("                  ###########################################################################################################")
    print("              ##################################################################################################################")
    print("               ")
    print("horizon :",self.horizon)
    print("resources number :",self.resources_number)
    print("interventions number :", self.interventions_number)
    print("scenarios_number : ",self.scenarios_number)
    print("alpha :",self.alpha)
    print("tau :",self.tau)
    print("computation time :",self.computation_time)
    return 0

  
  def show_interventions_details(self):
    print("              ##################################################################################################################")
    print("                  ###########################################################################################################")
    print("                      ####################################################################################################")
    print("                          ################################ Interventions details #####################################")
    print("                      ####################################################################################################")
    print("                  ###########################################################################################################")
    print("              ##################################################################################################################")
    print("               ")
    print("     Interventions total number : ", self.interventions_number)
    print("     Numbers of Interventions according to the .json file :", self.interventions_real_number)
    print("     Processing times of the interventions :")
    for i in range(len(self.delta_i_t)):
      print("      ",self.interventions_real_number[i],self.delta_i_t[i])
    
    print("    ")
    return 0
  
  def show_resources_details(self):
    print("              ##################################################################################################################")
    print("                  ###########################################################################################################")
    print("                      ####################################################################################################")
    print("                          ################################# Resouces details #########################################")
    print("                      ####################################################################################################")
    print("                  ###########################################################################################################")
    print("              ##################################################################################################################")
    print("               ")
    print("     Resources total number : ", self.resources_number)
    print("     (Numbers - 1) of Resources according to the .json file :", self.resources_real_number)

    print("     Lower capacities of the resources :")
    for i in range(len(self.l_c_t)):
      print("     ",self.resources_real_number[i],self.l_c_t[i])
    
    print("    ")
    print("     Higher capacities of the resources :")
    for i in range(len(self.l_c_t)):
      print("     ",self.resources_real_number[i],self.u_c_t[i])
    
    print("    ")
    return 0

  def show_r_c_i_t_t1_details(self):
    print("              ##################################################################################################################")
    print("                  ###########################################################################################################")
    print("                      ####################################################################################################")
    print("                          ################################# Workload details #########################################")
    print("                      ####################################################################################################")
    print("                  ###########################################################################################################")
    print("              ##################################################################################################################")
    print("               ")
    for key in self.r_c_i_t_t1.keys():
      int_number = self.interventions_real_number[key[0]]
      resource_number = self.resources_real_number[key[1]] + 1
      print("                    &&&&&&&&&&&&&&&&&      [Intervention , Resource] = [",int_number,",",resource_number,"] &&&&&&&&&&&&&&&&&&&&&&")
      print("     ",self.r_c_i_t_t1[key])
      
      print("      ")
  
    return 0
 
  def show_exclusions_details(self):
    print("              ##################################################################################################################")
    print("                  ###########################################################################################################")
    print("                      ####################################################################################################")
    print("                         ################################# Exclusions details #########################################")
    print("                      ####################################################################################################")
    print("                  ###########################################################################################################")
    print("              ##################################################################################################################")
    print("               ")
    for key in self.exclusions.keys():
      print(key)
      int_1_number = self.interventions_real_number[key[0]]
      int_2_number = self.interventions_real_number[key[1]] 
      print("                 &&&&&&&&&&&&&&&&&    [Intervention 1, Intervention 2] = [",int_1_number,",",int_2_number,"] &&&&&&&&&&&&&&&&&&&&&&")
      print("      ",self.exclusions[key])
      
      print("      ")
  
    return 0
  
  def show_risks_details(self):
    print("              ##################################################################################################################")
    print("                  ###########################################################################################################")
    print("                      ####################################################################################################")
    print("                         ################################# Risks details ############################################")
    print("                      ####################################################################################################")
    print("                  ###########################################################################################################")
    print("              ##################################################################################################################")
    print("               ")
    for i in self.risk_s_i_t_t1.keys():
      int_number = self.interventions_real_number[i]
      print("                             &&&&&&&&&&&&&&&&&    Intervention", int_number, "   &&&&&&&&&&&&&&&&&&&&&&")
      for t in self.risk_s_i_t_t1[i].keys():
        print("[t = ",t,"]",self.risk_s_i_t_t1[i][t])
    
    return 0
        

  