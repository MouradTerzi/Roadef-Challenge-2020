#-*- coding:utf-8 -8-
import os
import sys 
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
  scenarios = instance.scenarios_number[:]
  alpha = instance.alpha
  tau = instance.tau
  completion_time = instance.completion_time
  delta_i_t = instance.delta_i_t
  l_c_t = instance.l_c_t
  u_c_t = instance.u_c_t
  exclusions_list = instance.exclusions
  r_c_i_t_t1 = instance.r_c_i_t_t1
  risk_s_i_t_t1 = instance.risk_s_i_t_t1
  M = 10
  model_path = 'Output_models/setA_instance_'+instance_number+'.lp'
  list_beta_indexes = list()
  for i in range(interventions_number):
    for t in range(horizon):
      for t1 in range(t+1):
        list_beta_indexes.append((i,t,t1))

  exact_solver = es.ExactSolvers()
  #Create the mathematical model 
  model = exact_solver.create_mathematical_model(interventions_number,resources_number,horizon,list_beta_indexes,scenarios,alpha,tau,completion_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,10,model_path)
  #Resolution of the instance at hand 
  exact_solver.instance_resolution(model)
  return 0


if __name__ =="__main__":
  
  instance_path = 'Instances/Set_A/A_09.json'
  #set_A_instances_resolution(instance_path,'09')
  show_instance_details(instance_path)