#-*- coding:utf-8 -8-
import os
import sys 
import copy
sys.path.insert(0,'Inputs/')
sys.path.insert(0,'Solvers/')

import reader as rd 
import exact_solvers as es 

def show_instance_details(instance_path):

  reader = rd.Reader()
  instance = reader.read_instance(instance_path)
  instance.show_basic_details()
  #instance.show_interventions_details()
  #instance.show_resources_details()
  #instance.show_r_c_i_t_t1_details()
  #instance.show_risks_details()
  #instance.show_exclusions_details()
  return 
  
def set_A_instances_resolution(instance_path,instance_number):

  #instance_path is the path to the considering instance
  #the Set 1 instances are in the folder Instances/SetA/
  reader = rd.Reader()
  instance = reader.read_instance(instance_path)
  
  #1. Declaration of the initial informations about the instance
  interventions_number = instance.interventions_number
  resources_number = instance.resources_number
  horizon = instance.horizon
  scenarios = copy.deepcopy(instance.scenarios_number)
  alpha = instance.alpha
  tau = instance.tau
  computation_time = instance.computation_time
  delta_i_t = copy.deepcopy(instance.delta_i_t)
  l_c_t = copy.deepcopy(instance.l_c_t)
  u_c_t = copy.deepcopy(instance.u_c_t)
  exclusions_list = copy.deepcopy(instance.exclusions)
  r_c_i_t_t1 = copy.deepcopy(instance.r_c_i_t_t1)
  risk_s_i_t_t1 = copy.deepcopy(instance.risk_s_i_t_t1)
  t_max = copy.deepcopy(instance.t_max)
  M = 1000000
  model_path = 'Output_models/setA_instance_'+instance_number+'.lp'
  list_beta_indexes = list()
  for i in range(interventions_number):
    for t in range(horizon):
      for t1 in range(t+1):
        list_beta_indexes.append((i,t,t1))
  
  exact_solver = es.ExactSolvers()
  #Create the mathematical model 
  model = exact_solver.create_mathematical_model(interventions_number,resources_number,horizon,list_beta_indexes,scenarios,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,M,model_path,t_max)

  #Resolution of the instance at hand 
  exact_solver.instance_resolution(model)

  #Create the output txt file 
  output_path = 'Output_txt_files/SetA_'+instance_number+'_output_file'
  list_interventions_horizon = exact_solver.output_file_creation(model,instance.interventions_real_number,output_path,interventions_number,horizon)
  
  #Show w values 
  output_w_path = "Output_w_files/SetA_"+instance_number+'_w_values'
  exact_solver.show_w_values(model,interventions_number,horizon,instance.interventions_real_number,output_w_path)
  gantt_path = "Gantt_diagrams/SetA_"+instance_number+'.jpg'
  exact_solver.gantt_diagram(list_interventions_horizon,instance.interventions_real_number, delta_i_t,gantt_path)
  return 0

if __name__ == "__main__":
  
  instance_path = 'Instances/Set_A/A_07.json'
  set_A_instances_resolution(instance_path,'07')
  #show_instance_details(instance_path)
