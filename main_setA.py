#-*- coding:utf-8 -8-
import os
import sys 
import copy
sys.path.insert(0,'Inputs/')
sys.path.insert(0,'Solvers/')
sys.path.insert(0,'Outputs/')

import reader as rd 
import exact_solvers as es 
import output_file as out_f 

def show_instance_details(instance_path):

  reader = rd.Reader()
  instance = reader.read_instance(instance_path)
  instance.show_basic_details()
  print(instance.t_max)
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
  model_path = 'Outputs/Output_models/SetA/setA_instance_'+instance_number+'.lp'
  list_z_indexes = list()
  for i in range(interventions_number):
    for t in range(t_max[i] + 1):
      for t1 in range(delta_i_t[i][t]):
        list_z_indexes.append((i,t,t1))

  exact_solver = es.ExactSolvers()
  #Create the mathematical model 
  model = exact_solver.create_mathematical_model_v2(interventions_number,resources_number,horizon,list_z_indexes,scenarios,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,M,model_path,t_max)

  #Resolution of the instance at hand 
  exact_solver.instance_resolution(model)

  #Create the output txt file
  out_file_object = out_f.OutputFilesManaging()
  output_path = 'Outputs/Output_txt_files/gurobi_exact_solver/SetA/SetA_'+instance_number+'_output_file'
  out_file_object.create_rte_output_file_from_gurobi_results(model,interventions_number,horizon,instance.interventions_json_number,output_path)
  output_path = 'Outputs/Output_z_files/SetA/SetA_'+instance_number+'_z_file.json'
  out_file_object.create_z_output_file_from_gurobi_results(model,interventions_number,horizon,instance.interventions_json_number,t_max,delta_i_t,output_path)
  return 0

if __name__ == "__main__":
  
  instance_path = 'Instances/Set_A/A_09.json'
  set_A_instances_resolution(instance_path,'09')
  #show_instance_details(instance_path)
