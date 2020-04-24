import sys 
import os 

class DataPreProcessing:

  def __init__(self):
    print("DataProceProcessing object instantiation ....")
  
  #risk_s_t computes the sum (risk[i][t'][t][s]) for each intervention
  #risk_s_t assumes that all the interventions are activated at time period t and each one is launched at every t' leq to t
  def risk_s_t(self,instance,t,s):
    risk_s_t = 0
    for i in range(instance.interventions_number):
      for t1 in range(t+1):
        if t in instance.risk_s_i_t_t1[i] and t1 in instance.risk_s_i_t_t1[i][t]:
          risk_s_t += instance.risk_s_i_t_t1[i][t][t1][s]

    return risk_s_t

  #reduce_scenarios_using_risk_s_t keep one scenario from the input instance for each t
  #the scenario to keep is selected using the risk_s_t for each t 
  def reduce_scenarios_using_risk_s_t(self,instance,tau):
    for t in range(instance.horizon):
      self.select_scenarios(instance,t,tau)
    
    return 
  
  def select_scenarios(self,instance,t,tau):
    
    #Compute risk (s,t)
    risk_t_all_s = list()
    for s in range(instance.scenarios_number[t]):
      r_s_t = self.risk_s_t(instance,t,s)
      risk_t_all_s.append([s,r_s_t])
    
    #Sort the list risk_t_all_s
    risk_t_all_s = sorted(risk_t_all_s,key = lambda x:x[1],reverse = False)

    #Get the scenario that corresponds to the quantile (tau)
    if int(tau*instance.scenarios_number[t]) == tau*instance.scenarios_number[t]:
      pos = tau*instance.scenarios_number[t] - 1
    else:
      pos = int(tau*instance.scenarios_number[t])
    
    #Keep only the scenario which corresponds to the position : pos
    for i in range(instance.interventions_number):
       for t1 in range(t + 1):
          if t in instance.risk_s_i_t_t1[i] and t1 in instance.risk_s_i_t_t1[i][t]:
            instance.risk_s_i_t_t1[i][t][t1].insert(0,instance.risk_s_i_t_t1[i][t][t1][risk_t_all_s[pos][0]])
            instance.risk_s_i_t_t1[i][t][t1] = instance.risk_s_i_t_t1[i][t][t1][:1]
    
    instance.scenarios_number[t] = 1
    return 0   

  
  def reduce_scenarios_using_risk_s_t_i_t_t1(self,instance):

    for i in range(instance.interventions_number):
      for t in range(instance.horizon):
        for t1 in range(t + 1):
          if t in instance.risk_s_i_t_t1[i] and t1 in instance.risk_s_i_t_t1[i][t]:
            min_ = min(instance.risk_s_i_t_t1[i][t][t1])
            instance.risk_s_i_t_t1[i][t][t1].insert(0,min_)
            instance.risk_s_i_t_t1[i][t][t1] = instance.risk_s_i_t_t1[i][t][t1][:1]

    instance.scenarios_number = [1]*len(instance.scenarios_number)
    return 

  
  def reduce_scenarios_using_risk_s_t_i_t_t1_tau(self,instance,tau):

    for i in range(instance.interventions_number):
      for t in range(instance.horizon):
        for t1 in range(t + 1):
          if t in instance.risk_s_i_t_t1[i] and t1 in instance.risk_s_i_t_t1[i][t]:
            instance.risk_s_i_t_t1[i][t][t1] = sorted(instance.risk_s_i_t_t1[i][t][t1],reverse = False)
            
            #Get the scenario that corresponds to the quantile (tau)
            if int(tau*instance.scenarios_number[t]) == tau*instance.scenarios_number[t]:
             pos = tau*instance.scenarios_number[t] - 1
            else:
              pos = int(tau*instance.scenarios_number[t])
        
            instance.risk_s_i_t_t1[i][t][t1].insert(0,instance.risk_s_i_t_t1[i][t][t1][pos])
            instance.risk_s_i_t_t1[i][t][t1] = instance.risk_s_i_t_t1[i][t][t1][:1]
        
    instance.scenarios_number = [1]*len(instance.scenarios_number)
    return 