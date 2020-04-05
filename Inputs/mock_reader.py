#-*- coding:utf-8 -*-
import os 
import sys 
import mock_instance 

class MockReader:
     
  def __init__(self):
    print("Mock reader instantiation")
  

  def read_instance(self,instance_path):
     
    try:
      file_ = open(instance_path,"r")
      content = file_.read().split('\n')
      
      #Get the different details about the instance 
      line_one = list(map(int,content[0].split(' ')))
      
      instance = mock_instance.MockInstance(line_one[0],line_one[1],line_one[2],line_one[3],float(content[1]),line_one[4])
      
      #Get the resources and theirs corresponding min and max 
      index = self.__get_resources_details(instance,content)
    
      #Get the interventions and theirs corresponding (workload and risks)
      while content[index][0] != 'E':
        intervention_number = int(content[index][1:])
        instance.intervention_time.append(list(map(int,content[index+1].split(' '))))
        index = self.__read_workload(instance,content,index+3,intervention_number)
        index = self.__read_risks(instance,content,index,intervention_number)
      
      #Get the exclusion list
      self.__get_exclusion_list(instance,content,index+1)
      return instance
    except FileNotFoundError:
      print("The input instance path doesn't correspond to any file !!!")
      return []
    
  def __get_resources_details(self,instance,instance_file_content):
    
    index = 3 
    while instance_file_content[index][0] != 'I':
     
      instance.t_min_capacity.append(list(map(int,instance_file_content[index+1].split(' '))))
      instance.t_max_capacity.append(list(map(int,instance_file_content[index+2].split(' '))))
      index += 4 
    
    return index
  
  def __read_workload(self,instance,instance_file_content,index,intervention_number):

    list_all_workload = list()
    list_all_workload.append(intervention_number)
    
    while instance_file_content[index][0] != 'R':
      resource_number = int(instance_file_content[index][2:])
      index += 1
      list_workload_intervention_resource = list()
      while instance_file_content[index] != '':
        list_workload_intervention_resource.append(list(map(int,instance_file_content[index].split(' '))))
        index += 1

      index += 1
      list_all_workload.append([resource_number,list_workload_intervention_resource])

    instance.workload.append(list_all_workload)
    return index 

  def __read_risks(self,instance,instance_file_content,index,intervention_number):
    
    list_all_risks = list()
    list_all_risks.append(intervention_number)
    while instance_file_content[index][0] !='I' and instance_file_content[index][0] != 'E':
      index += 1 
      list_risks_per_scenario = list()
      while instance_file_content[index] != '':  
        list_risks_per_scenario.append(list(map(int,instance_file_content[index].split(' '))))
        index += 1
  
      list_all_risks.append(list_risks_per_scenario)
      index += 1
     
    instance.risks.append(list_all_risks) 
    return index  
      
  def __get_exclusion_list(self,instance,instance_file_content,index):

    while instance_file_content[index] != '':
      curent_line = list(map(int,instance_file_content[index].split(' ')))
      instance.exclusions.append([(curent_line[0],curent_line[1]),curent_line[2:]])
      index += 1
    
    return 

          
 
     
              
          
