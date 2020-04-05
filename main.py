#-*- coding:utf-8 -8-
import os
import sys 
sys.path.insert(0,'Inputs/')

import mock_reader as mr 

instance_path = 'test_instance'

def show_instances_details(instance):
  print("############################################### General details #################################################")
  print("Horizon:",instance.horizon)
  print("Resource:",instance.resource)
  print("Interventions:",instance.intervention)
  print("Scenario:",instance.scenario)
  print("Alpha:",instance.alpha)
  print("Completion time:",instance.completion_time)

  print("############################################ Resources capacities ##############################################")
  for i,line in enumerate(instance.t_min_capacity):
    print("Resource ",i+1,"min capacities:",line)

  print(" ")
  for i,line in enumerate(instance.t_max_capacity):
    print("Resource ",i+1,"max capacities:",line)
  
  print("############################################ Interventions details ##############################################")

mock_reader = mr.MockReader()
instance = mock_reader.read_instance(instance_path)
show_instances_details(instance)