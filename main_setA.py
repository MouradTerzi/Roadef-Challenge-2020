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
import data_preprocessing as dp

def show_instance_details(instance_path,instance_number):

  reader = rd.Reader()
  instance = reader.read_instance(instance_path)
  exclusions_xls_path = 'Inputs/instances_details/SetA_instance_'+instance_number+"_exclusions_.xls"
  #instance.show_basic_details()
  instance.get_exclusions_details(list(instance.seasons.keys()),exclusions_xls_path)
  #instance.show_exclusions_details()
  #print(instance.seasons)
  #instance.show_basic_details()
  #instance.show_interventions_details()
  #instance.show_resources_details()
  #instance.show_r_c_i_t_t1_details()
  #instance.show_risks_details()
  #instance.show_exclusions_details()
  return 

def read_instance(instance_path):
  reader = rd.Reader()
  #instance_path is the path to the considering instance
  #the Set 1 instances are in the folder Instances/SetA/
  instance = reader.read_instance(instance_path)
  
  #1. Declaration of the initial informations about the instance
  interventions_number = instance.interventions_number
  interventions_json_number = copy.deepcopy(instance.interventions_json_number)
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
  
  list_z_indexes = list()
  for i in range(interventions_number):
    for t in range(t_max[i] + 1):
      for t1 in range(delta_i_t[i][t]):
        list_z_indexes.append((i,t,t1))
  
  return interventions_number,resources_number,horizon,list_z_indexes,scenarios,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,t_max,interventions_json_number,instance


def set_A_instances_exact_resolution(interventions_number,resources_number,horizon,list_z_indexes,scenarios,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,t_max,interventions_json_number,instance_number):
  
  #Create the mathematical model 
  M = 1000000
  model_path = 'Outputs/Output_models/gurobi_exact_solver/SetA/setA_instance_'+instance_number+'.lp'
  exact_solver = es.ExactSolvers()
  model = exact_solver.create_mathematical_model_v2(interventions_number,resources_number,horizon,list_z_indexes,scenarios,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,M,model_path,t_max)

  #Resolution of the instance at hand 
  exact_solver.instance_resolution(model)

  #Create the output txt file
  out_file_object = out_f.OutputFilesManaging()
  output_path = 'Outputs/Output_txt_files/gurobi_exact_solver/SetA/SetA_'+instance_number+'_output_file'
  out_file_object.create_rte_output_file_from_gurobi_results(model,interventions_number,horizon,interventions_json_number,output_path)
  output_path = 'Outputs/Output_z_files/gurobi_exact_solver/SetA/SetA_'+instance_number+'_z_file.json'
  out_file_object.create_z_output_file_from_gurobi_results(model,interventions_number,horizon,interventions_json_number,t_max,delta_i_t,output_path)
  return 0


def set_A_instances_heuristic_1_resolution(interventions_number,resources_number,horizon,list_z_indexes,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,t_max,interventions_json_number,instance_number,instance):

  dp_object = dp.DataPreProcessing()
  dp_object.reduce_scenarios_using_risk_s_t(instance,tau)

  #Create the mathematical model 
  M = 1000000
  model_path = 'Outputs/Output_models/heuristic_h1/SetA/setA_instance_'+instance_number+'.lp'
  exact_solver = es.ExactSolvers()
  scenarios = instance.scenarios_number
  risk_s_i_t_t1 = instance.risk_s_i_t_t1

  model = exact_solver.create_mathematical_model_v2(interventions_number,resources_number,horizon,list_z_indexes,scenarios,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,M,model_path,t_max)

  #Resolution of the instance at hand 
  exact_solver.instance_resolution(model)

  #Create the output txt file
  out_file_object = out_f.OutputFilesManaging()
  output_path = 'Outputs/Output_txt_files/heuristic_h1/SetA/SetA_'+instance_number+'_output_file'
  out_file_object.create_rte_output_file_from_gurobi_results(model,interventions_number,horizon,interventions_json_number,output_path)

  output_path = 'Outputs/Output_z_files/heuristic_h1/SetA/SetA_'+instance_number+'_z_file.json'
  out_file_object.create_z_output_file_from_gurobi_results(model,interventions_number,horizon,interventions_json_number,t_max,delta_i_t,output_path)
  
  return 

def set_A_instances_heuristic_2_resolution(interventions_number,resources_number,horizon,list_z_indexes,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,t_max,interventions_json_number,instance_number,instance):

  dp_object = dp.DataPreProcessing()
  dp_object.reduce_scenarios_using_risk_s_t_i_t_t1_tau(instance,0.95)

  #Create the mathematical model 
  M = 1000000
  model_path = 'Outputs/Output_models/heuristic_h2/SetA/setA_instance_'+instance_number+'.lp'
  exact_solver = es.ExactSolvers()
  scenarios = instance.scenarios_number
  risk_s_i_t_t1 = instance.risk_s_i_t_t1
  
  model = exact_solver.create_mathematical_model_v2(interventions_number,resources_number,horizon,list_z_indexes,scenarios,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,M,model_path,t_max)

  #Resolution of the instance at hand 
  exact_solver.instance_resolution(model)

  #Create the output txt file
  out_file_object = out_f.OutputFilesManaging()
  output_path = 'Outputs/Output_txt_files/heuristic_h2/SetA/SetA_'+instance_number+'_output_file'
  out_file_object.create_rte_output_file_from_gurobi_results(model,interventions_number,horizon,interventions_json_number,output_path)
  
  output_path = 'Outputs/Output_z_files/heuristic_h2/SetA/SetA_'+instance_number+'_z_file.json'
  out_file_object.create_z_output_file_from_gurobi_results(model,interventions_number,horizon,interventions_json_number,t_max,delta_i_t,output_path)
  
  return


if __name__ == "__main__":
  
  instance_path = 'Instances/Set_A/A_07.json'
  show_instance_details(instance_path,"07")
  
  """
  interventions_number,resources_number,horizon,list_z_indexes,scenarios,alpha,tau,computation_time, delta_i_t,l_c_t,\
  u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,t_max,interventions_json_number,instance = read_instance(instance_path)
  
  set_A_instances_exact_resolution(interventions_number,resources_number,horizon,list_z_indexes,scenarios,alpha,tau,computation_time, delta_i_t,l_c_t,\
  u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,t_max,interventions_json_number,'09')
  
  set_A_instances_heuristic_2_resolution(interventions_number,resources_number,horizon,list_z_indexes,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,t_max,interventions_json_number,'09',instance)
  """
