#-*- coding:utf-8 -*-
import os 
import sys 
import instance as inst
import json 
import copy 
import numpy as np 

class Reader:
     
  def __init__(self):
    print("Reader instantiation")
  

  def read_instance(self,instance_path):
    try: 
      with open(instance_path) as f:
        content = json.load(f)
       
        #1. Get the different details of the instance
        horizon = content['T']
        resources_number = len(content['Resources'].keys())
        interventions_number = len(content['Interventions'])
        scenarios_number = content['Scenarios_number']
        alpha = content['Alpha']
        tau = content['Quantile']
        completion_time = content['ComputationTime']        
        
        #2. Create an object of type instance
        instance = inst.Instance(horizon,resources_number,interventions_number,scenarios_number,alpha,tau,completion_time)
        
        #2.1 Get the delta_i_t values
        self.__get_delta_i_t(content,instance)
      
        #2.2 Get the l_c_t  and u_c_t values for each resource 
        self.__get_l_c_t(content,instance)
        self.__get_u_c_t(content,instance)
            
        #2.3 Get the r_c_i_t_t1 for each pair (intervention, resource)
        self.__get_r_c_i_t_t1(content,instance)
        
        #2.4 Get the seasons 
        self.__get_seasons(content,instance)
        
        #2.5 Get the exclusions 
        self.__get_exclusions(content,instance)
        
        #2.6 Get the risks 
        self.__get_risks(content,instance)

        return instance 
        
    except FileNotFoundError: 
      print("The input path dosen't correspond to any instance file !!")
      return -1
   
    
  def __get_delta_i_t(self,content,instance):
    
    if "Interventions" in content:
      for key in content["Interventions"].keys():
        instance.interventions_real_number.append(int(key[13:]))
        instance.delta_i_t.append(content["Interventions"][key]["Delta"])
        instance.t_max.append(int(content["Interventions"][key]["tmax"])-1)
      
      return 0

    else:
      print("The input content must contain a key : Interventions")
      return -1
              

  def __get_l_c_t(self,content,instance):
    
    if "Resources" in content:
      list_keys = list()
      #Sort the resources according to theirs corresponding number
      for key in content["Resources"].keys():
        if "control" not in key:
          list_keys.append([key , int(key[11:])-1])

      list_keys = sorted(list_keys, key = lambda x:x[1] , reverse = False)
      if "Resources_control" in content["Resources"]:
        list_keys.append(["Resources_control",len(list_keys)])
      
      for e in list_keys:
        instance.l_c_t.append(content["Resources"][e[0]]["min"])
        instance.resources_real_number.append(e[1])
      
      return 0

    else:
      print("The input content must contain a key : Resources")
      return -1

  
  def __get_u_c_t(self,content,instance):
    
    if "Resources" in content:
      #Sort the resources according to theirs corresponding number
      list_keys = list()
      for key in content["Resources"].keys():
        if "control" not in key:
          list_keys.append([key , int(key[11:])])

      list_keys = sorted(list_keys, key = lambda x:x[1] , reverse = False)
      if "Resources_control" in content["Resources"]:
        list_keys.append(["Resources_control",len(list_keys)+1])
      
      for e in list_keys:
        instance.u_c_t.append(content["Resources"][e[0]]["max"])
        
      return 0

    else:
      print("The input content must contain a key : Resources")
      return -1 
  

  def __get_r_c_i_t_t1(self,content,instance):
    
    if "Interventions" in content:
    
      for intervention in content["Interventions"].keys():
        intervention_number_json = int(intervention[13:]) #Get the number of the intervention as defined in the json file
        int_ = instance.interventions_real_number.index(intervention_number_json) #int_ corresponds to the number in the table
        #interventions_real_number. int_ will be used in the instance resolution 
        for resource in content["Interventions"][intervention]["workload"].keys():
          #Get the number of the resource. res_ will be used in the instance resolution 
          if "control" not in resource:
            res_ = int(resource[11:]) - 1
          else:
            res_  = len(instance.resources_real_number) - 1

          instance.r_c_i_t_t1[(int_,res_)] = dict()  #Add the pair (intervention number, resource) as a key to the r_c_t_t1 dictionary
          #Get for each t, its related r_c_t_t' with t'<t
          for t in content["Interventions"][intervention]["workload"][resource].keys(): 
            instance.r_c_i_t_t1[(int_,res_)][int(t) - 1] = dict()
            for t1 in content["Interventions"][intervention]["workload"][resource][t].keys():
              instance.r_c_i_t_t1[(int_,res_)][int(t) - 1][int(t1) - 1] = float(content["Interventions"][intervention]["workload"][resource][t][t1])
      
      return 0   
  
    else:
      print("The input content must contain a key : Interventions")
      return -1
  
  
  def __get_seasons(self,content,instance):
    
    if "Seasons" in content:
      
      for key in content["Seasons"].keys():
        if len(content["Seasons"][key]) != 0:
          instance.seasons[key] = list(np.array(list(map(int,content["Seasons"][key]))) - np.array([1]*len(content["Seasons"][key])))
        
        else:
          instance.seasons[key] = []
      
      return 0
      
    else:
      print("The input content must contain a key : Seasons")
      return -1


  def __get_exclusions(self,content,instance):
    
    if "Exclusions" in content:
      for key in content["Exclusions"].keys():
        intervention_1_number_json = int(content["Exclusions"][key][0][13:])
        intervention_2_number_json = int(content["Exclusions"][key][1][13:])
        int_1 = instance.interventions_real_number.index(intervention_1_number_json)
        int_2 = instance.interventions_real_number.index(intervention_2_number_json)
        if len(instance.seasons[content["Exclusions"][key][2]]) != 0:
          if (int_1,int_2) not in instance.exclusions:
            instance.exclusions[(int_1,int_2)] = instance.seasons[content["Exclusions"][key][2]][:]
          
          else:
            instance.exclusions[(int_1,int_2)].extend(instance.seasons[content["Exclusions"][key][2]])
          
      return 0
    
    else:
      print("The input content must contain a key : Exclusions")
      return -1
  

  def __get_risks(self,content,instance):
    
    if "Interventions" in content:
      for intervention in content["Interventions"].keys():
        intervention_number_json = int(intervention[13:]) #Get the number of the intervention as defined in the json file
        int_ = instance.interventions_real_number.index(intervention_number_json) #int_ corresponds to the number in the table
        #interventions_real_number. int_ will be used in the instance resolution   
        instance.risk_s_i_t_t1[int_] = dict()
        for t in content["Interventions"][intervention]["risk"].keys():
          instance.risk_s_i_t_t1[int_][int(t) - 1] = dict()
          for t1 in content["Interventions"][intervention]["risk"][t].keys():
            instance.risk_s_i_t_t1[int_][int(t) - 1][int(t1) - 1] = content["Interventions"][intervention]["risk"][t][t1]
      
      return 0
      
    else:
      print("The input content must contain a key : Interventions")
      return -1 

    