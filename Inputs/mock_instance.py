#-*- coding: utf-8 -*-
import os
import sys 

class MockInstance:
   
   
  def __init__(self,horizon,resource,intervention,scenario,alpha,completion_time):
    self.horizon = horizon
    self.resource = resource
    self.intervention = intervention
    self.scenario = scenario
    self.alpha = alpha
    self.completion_time = completion_time
    self.t_max_capacity = list()
    self.t_min_capacity = list()
    self.intervention_time = list()
    self.workload = list()
    self.risks = list()
    self.exclusions = list()

  

