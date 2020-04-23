#-*- coding:utf-8 -*-
import os 
import sys 
import json 

class OutputFilesManaging:
  
  def __init__(self):
    print("OutputFilesManaging class managing .....")
    return 
  
  def create_rte_output_file_from_gurobi_results(self,model,interventions,horizon,interventions_json_number,rte_output_path):
    
    f = open(rte_output_path,"w")
    try: 
      for i in range(interventions):
        for t in range(horizon):
          x = model.getVarByName("x["+str(i)+","+str(t)+"]")
          if x.X != 0:
            #Get the real number of the intervention 
            int_json_number = interventions_json_number[i]
            #Save the results in the created file
            f.write("Intervention_"+str(int_json_number)+" "+str(t+1)+"\n")
      
      f.close()
      return 0  

    except AttributeError:  
      print("Requested attribute doesn't exist in the input mathamatical model !!!")
      return -1 
  
  #f1 will be a json file. The master key of f1 will be the intervention number in the instance
  #json file. the second key will be t which corresponds to the start time of the intervention.   
  #the t values start from 0... horizon - 1
  #t' values start from 0 ... delta[i][t]
  #t_max corresponds to t_max -1 in the instance json file.
  def create_z_output_file_from_gurobi_results(self,model,interventions,horizon,interventions_json_number,t_max,delta_i_t,rte_z_path):
    
    f = open(rte_z_path,"w") 
    z_dict = dict()
    try:
      for i in range(interventions):
        int_json_number = interventions_json_number[i]
        z_dict[int_json_number] = dict()
        for t in range(t_max[i] + 1):
          for t1 in range(delta_i_t[i][t]):
            z = model.getVarByName("z["+str(i)+","+str(t)+","+str(t1)+"]")
            if z.X != 0:
              if t not in z_dict[int_json_number].keys():
                z_dict[int_json_number][t] = list()
            
              z_dict[int_json_number][t].append(t1)
 
          
      json.dump(z_dict,f)
      f.close()
    
      return 0

    except AttributeError:
      print("Specefied attribute dosesn't existe")
