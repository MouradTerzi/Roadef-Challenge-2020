#-*- coding:utf-8 -8-
import os
import sys 

sys.path.insert(0,'Solvers/')
sys.path.insert(0,'Outputs/')

import exact_solvers as es 
import output_file as out_f
def example_one_resolution():

  #1. Declaration of the initial informations about the instance
  interventions_number = 3
  resources_number = 1
  horizon = 3
  scenarios = [3,3,3]
  alpha = 0.5
  tau = 0.5
  completion_time = 15

  #2. Declaration of the different model's initial data
  delta_i_t = [[3,3,2],
    [1,1,1],
    [1,1,2]]
             
  l_c_t = [[10,0,6]]
  u_c_t = [[49, 23, 15]]

  #A key (k1,k2) in the exc list refers to the pair (intervention1 ,intervention 2) which are in exclusion
  exclusions_list = {
    (1,2):[0,1,2]
  }
  t_max = [0,2,1]
  list_beta_indexes = list()
  for i in range(interventions_number):
    for t in range(t_max[i] + 1):
      for t1 in range(delta_i_t[i][t]):
        list_beta_indexes.append((i,t,t1))
  
  r_c_i_t_t1 = {
    (0,0): {0:{0:31},1:{0:0},2:{0:8}},
    (1,0): {0:{0:14},1:{0:0, 1:14},2:{0:0, 1:0, 2:14}},
    (2,0): {0:{0:5},1:{0:0, 1:5}, 2:{0:0 , 1:0}}
  }

  risk_s_i_t_t1 = {
    #intervention 0
    0: {0: { 0:[7,4,8]},# t = 0, t' = 0
        1: { 0:[1,10,10]}, #t = 1, t' = 0
        2: { 0:[1,4,4]}  #t = 2, t' = 0
    },
     
    #intervention 1
    1: {0: {0:[5,4,5]}, #t = 0, t' = 0
        1: {0:[0,0,0], 1:[5,4,5]}, #t = 1, (t' =0 and t' = 1)
        2: {0:[0,0,0], 1:[0,0,0], 2:[5,4,5]}   #t = 2, (t' = 0, t' = 1 and t' = 2)
    },

    #Intervention 2 
    2 : {0: {0:[4,8,2]}, #t = 0, t' = 0
        1: {0:[0,0,0], 1:[3,8,1]}, #t = 1, (t' =0 and t' = 1)
        2: {0:[0,0,0], 1:[0,0,0]}  #t = 2, (t' =0 and t' = 1)
    }
  }

  exact_solver = es.ExactSolvers()
  #Create the matematical model
  model = exact_solver.create_mathematical_compact_model(interventions_number,resources_number,horizon,list_beta_indexes,scenarios,alpha,tau,completion_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,'Outputs/Output_models/example_1.lp',t_max)
  
  #Resolution of the instance at hand 
  exact_solver.instance_resolution(model)
  """
  #Save the output file (this file corresponds to the input of the checker)
  output_object = out_f.OutputFilesManaging()
  output_path = 'Outputs/Output_txt_files/gurobi_exact_solver/example_1'
  output_object.create_rte_output_file_from_gurobi_results(model,interventions_number,horizon,[1,2,3],output_path)
  
  output_path = 'Outputs/Output_z_files/example_1'
  out_file_object.create_z_output_file_from_gurobi_results(model,interventions_number,horizon,[1,2,3],t_max,delta_i_t,output_path)
  """
  return 0


def example_two_resolution():

  #1. Declaration of the initial informations about the instance
  interventions_number = 3
  resources_number = 1
  horizon = 3
  scenarios = [1,1,2]
  alpha = 0.5
  tau = 0.5
  completion_time = 15

  #2. Declaration of the different model's initial data
  delta_i_t = [[3,3,2],
    [1,1,1],
    [1,1,2]]
             
  l_c_t = [[10,0,6]]
  u_c_t = [[49, 23, 15]]

  #A key (k1,k2) in the exc list refers to the pair (intervention1 ,intervention 2) which are in exclusion
  exclusions_list = {
    (1,2):[0,1,2]
  }
  
  t_max = [0,2,1]
  list_z_indexes = list()
  for i in range(interventions_number):
    for t in range(t_max[i] + 1):
      for t1 in range(delta_i_t[i][t]):
        list_z_indexes.append((i,t,t1))
  
  r_c_i_t_t1 = {
    (0,0): {0:{0:31},1:{0:0},2:{0:8}},
    (1,0): {0:{0:14, 1: 0, 2: 0},1:{0:0, 1:14, 2:0},2:{0:0, 1:0, 2:14}},
    (2,0): {0:{0:5, 1:0},1:{0:0, 1:5}, 2:{0:0 , 1:0}}
  }
  
  risk_s_i_t_t1 = {
    #intervention 0
    0:{ 0: { 0:[7]},# t = 0, t' = 0, s = 1
        1: { 0:[4]}, #t = 1, t' = 0, s = 1
        2: { 0:[2,20]}  #t = 2, t' = 0, two scenarios
    },
     
    #intervention 1
    1:{ 0: {0:[8]}, #t = 0, t' = 0, s = 1
        1: {0:[0], 1:[5]}, #t = 1, (t' =0 and t' = 1)
        2: {0:[0,0], 1:[0,0], 2:[6,8]}   #t = 2, (t' = 0, t' = 1 and t' = 2), two scenarios
    },

    #Intervention 2 
    2:{ 0: {0:[2]}, #t = 0, t' = 0
        1: {0:[0], 1:[6]}, #t = 1, (t' =0 and t' = 1)
        2: {0:[0,0], 1:[0,0]}  #t = 2, (t' =0 and t' = 1), two scenarios
    }
  }

  exact_solver = es.ExactSolvers()
  #Create the matematical model
  model = exact_solver.create_mathematical_model_v2(interventions_number,resources_number,horizon,list_z_indexes,scenarios,alpha,tau,completion_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,10,'Outputs/Output_models/example_2.lp',t_max)

  #Resolution of the instance at hand 
  exact_solver.instance_resolution(model)

  #Save the output file (this file corresponds to the input of the checker)
  output_object = out_f.OutputFilesManaging()
  output_path = 'Outputs/Output_txt_files/gurobi_exact_solver/example_2'
  output_object.create_rte_output_file_from_gurobi_results(model,interventions_number,horizon,[1,2,3],output_path)

  output_path = 'Outputs/Output_z_files/example_2'
  out_object.create_z_output_file_from_gurobi_results(model,interventions_number,horizon,[1,2,3],t_max,delta_i_t,output_path)

  return 0


if __name__ =="__main__":
  example_one_resolution()
  #example_two_resolution()
  