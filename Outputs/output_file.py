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
  

  def create_w_output_file_from_gurobi_results(self,model,interventions,horizon,interventions_json_number,rte_w_path):
    
    f1 = open(rte_w_path,"w")  #Save ehe time in w[i,t] == 1 and the corresponding intervention json number 
    f2 = open(rte_w_path+".json","w") #Save the time in which w[i,t] == 1 for each intervention. t in {0, .., horizon - 1}
    w_dict = dict()
    try:
      for i in range(interventions):
        int_json_number = interventions_json_number[i]
        w_dict[int_json_number] = list()
        for t in range(horizon):
          w = model.getVarByName("w["+str(i)+","+str(t)+"]")
          if w.X != 0:
            f1.write("w["+str(i)+","+str(t)+"] = 1 , intervention in json :"+str(int_json_number)+"\n")
            w_dict[int_json_number].append(t)

      json.dump(w_dict,f2)
      f1.close()
      f2.close()
      return 0

    except AttributeError:
      print("Specefied attribute dosesn't existe")
