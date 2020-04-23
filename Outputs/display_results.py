import os
import matplotlib 
import matplotlib.pyplot as plt 
import json 
import numpy as np 

class DisplayResults:
  
  def __init__(self):
    print("Display result class instantiation .....")

  # basic_gantt_diagram function display a basic gantt diagram that corresponds to the input solution in the json file : z_rte
  # when the input solution is wrong ( an intervention has tw start times, .. ) the corresponding intervention will be shown 
  # using the red color
  # the values of t start from 1 to horizon 
  def basic_gantt_diagram(self,z_rte_path,intervnetions_json_number,output_gantt_path):
    
    plt.rcParams.update({'font.size': 8})
    fig = plt.figure()
    z_file = open(z_rte_path)
    content = json.load(z_file)
    text = 0

    for intervention in content.keys():
      if len(content[intervention].keys()) > 1:
        print("Intervention ",intervention,"has ",len(content[intervention].keys())," start time ...")
        color = 'red'
        text = 1

      else:
        color = 'green'

      for t in content[intervention].keys():
        int_index = intervnetions_json_number.index(int(intervention))
        content[intervention][t].append(len(content[intervention][t]))      
        x = np.array([int(t)+1]*len(content[intervention][t])) + np.array(content[intervention][t])
        plt.fill_between(x, y1 = int_index,y2 = int_index + 0.5, color = color)
        if text == 1:
          plt.text(int(t)+0.5,int_index,"I "+intervention)
     
      text = 0
    
    plt.show()
    return 0

  #the following function checks if the exclusions between the interventions are respected 
  #if for a pair (i1,i2), an exclusion in a given t is not respected, the corresponding intervetions will be shown in 
  #a gantt diagram with red color in the non respected exclution time
  #the values of t start from 1 to horizon 
  def check_exclusions(self,z_file,exclusions_list,intervnetions_json_number):

    f = open(z_file)
    content = json.load(f)
    fig = plt.plot()
    for i1, i2 in exclusions_list.keys():
    
      #Get the json number of the intervention 
      i1_json_number = intervnetions_json_number[i1]
      i2_json_number = intervnetions_json_number[i2]
      
      #Get the start time of each intervention in the input solution
      i1_start_time = list(map(int,list(content[str(i1_json_number)].keys())))[0] + 1
      i2_start_time = list(map(int,list(content[str(i2_json_number)].keys())))[0] + 1
      
      #Create the period on which the interventions are in processing 
      i1_processing_period = np.array([i1_start_time]*len(content[str(i1_json_number)][str(i1_start_time - 1)])) + np.array(content[str(i1_json_number)][str(i1_start_time - 1)])
      i2_processing_period = np.array([i2_start_time]*len(content[str(i2_json_number)][str(i2_start_time - 1)])) + np.array(content[str(i2_json_number)][str(i2_start_time - 1)])
      
      list_not_res_excl_period = list()
      for t in exclusions_list[(i1,i2)]:
        if (t + 1) in i1_processing_period and (t + 1) in i2_processing_period:
          print("Exclusion contraint between I_",i1_json_number," and I_",i2_json_number," at a period", t+1," is not respected !!")
          list_not_res_excl_period.append(t + 1)

      #Show the gantt of the corresponding exclusions
      for t in i1_processing_period:
        if t not in list_not_res_excl_period:
          plt.fill_between([t,t+1],y1 = i1, y2 = i1 + 0.5, color = 'green')
        
        else:
          plt.fill_between([t,t+1],y1 = i1, y2 = i1 + 0.5, color = 'red')
      
      for t in i2_processing_period:
        if t not in list_not_res_excl_period:
          plt.fill_between([t,t+1],y1 = i2, y2 = i2 + 0.5, color = 'green')
        
        else:
          plt.fill_between([t,t+1],y1 = i2, y2 = i2 + 0.5, color = 'red')
     
    plt.show()
    return 