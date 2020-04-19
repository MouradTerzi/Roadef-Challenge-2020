import gurobipy as gb
from gurobipy import *

class ExactSolvers:

  def __init__(self):
    print("ExactSolvers class instantiation ....")
  
  def create_mathematical_model(self,interventions_number,resources_number,horizon,list_beta_indexes,scenarios,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,M,model_path,t_max):
   
   #1. Creation of the model
   model = Model('Roadef challenge')

   #2. Add the variables
   z = model.addVars(interventions_number,horizon,vtype = GRB.BINARY,name = "z")
   w = model.addVars(interventions_number,horizon,vtype = GRB.BINARY,name = "w")
   y = model.addVars(max(scenarios),horizon,vtype = GRB.BINARY,name = "y")
   beta = model.addVars(list_beta_indexes,vtype = GRB.BINARY, name = "beta")
   risk_s_t = model.addVars(max(scenarios),horizon,vtype = GRB.CONTINUOUS, name = "risk_s_t")
   risk_bar_t = model.addVars(horizon,vtype = GRB.CONTINUOUS, name="risk_bar_t")
   q_t = model.addVars(horizon,vtype = GRB.CONTINUOUS, name ="q_t")
   excess = model.addVars(horizon,vtype = GRB.CONTINUOUS, name = "excess")
   obj1 = model.addVar(vtype = GRB.CONTINUOUS, name = "obj1")
   obj2=  model.addVar(vtype = GRB.CONTINUOUS, name = "obj2")
       # Create variables
 
   #3. Add constraints
   
   model.addConstrs((quicksum(z[i,t] for t in range(t_max[i] + 1)) == 1 for i in range(interventions_number)))
   model.addConstrs(z[i,t] == 0 for i in range(interventions_number) for t in range(t_max[i] + 1,horizon) )
   #model.addConstrs((w[i, t] >= z[i, t] for i in range(interventions_number) for t in range(horizon)))
   model.addConstrs((z[i, t]*(t + delta_i_t[i][t]) <= horizon for i in range(interventions_number) \
   for t in range(t_max[i],horizon)))
   
   model.addConstrs(w[i,t1]  >= z[i,t] for i in range(interventions_number) \
   for t in range(t_max[i] + 1) for t1 in range(t, t + delta_i_t[i][t]))
   #Contraist related to t_max 
   model.addConstrs((z[i,t]*(t + 1) <= t_max[i] + 1 for i in range(interventions_number) for t in range(horizon)))
   
   model.addConstrs((w[key[0],t] + w[key[1],t] <= 1 for key in exclusions_list.keys() for t in exclusions_list[key]))
   
   model.addConstrs((beta[i,t,t1] >= z[i,t1]+ w[i,t] - 1 for i in range(interventions_number) \
   for t in range(horizon) for t1 in range(t + 1)))
   
   model.addConstrs((quicksum(beta[i,t,t1]*r_c_i_t_t1[(i,res)][t][t1] for i in range(interventions_number) \
   for t1 in range(t + 1) if (i,res) in r_c_i_t_t1 and t in r_c_i_t_t1[(i,res)] 
   and t1 in r_c_i_t_t1[(i,res)][t]) >= l_c_t[res][t] for res in range(resources_number) for t in range(horizon)))
   
   model.addConstrs((quicksum(beta[i,t,t1]*r_c_i_t_t1[(i,res)][t][t1] for i in range(interventions_number) \
   for t1 in range(t + 1) if (i,res) in r_c_i_t_t1 and t in r_c_i_t_t1[(i,res)] \
   and t1 in r_c_i_t_t1[(i,res)][t]) <= u_c_t[res][t] \
   for res in range(resources_number) for t in range(horizon)))
   
   model.addConstrs((risk_s_t[s,t] == quicksum(risk_s_i_t_t1[i][t][t1][s]*beta[i,t,t1] for i in
   range(interventions_number) for t1 in range(t + 1) if t in risk_s_i_t_t1[i] and t1 in risk_s_i_t_t1[i][t]) \
   for t in range(horizon) for s in range(scenarios[t])))
   
   model.addConstrs((risk_bar_t[t] == quicksum(risk_s_t[s,t] for s in
   range(scenarios[t]))*(1/scenarios[t]) for t in range(horizon)))
   
   model.addConstrs((quicksum(y[s,t] for s in range(scenarios[t])) >= tau*scenarios[t] for t in range(horizon)))
   
   model.addConstrs((quicksum(y[s,t] for s in range(scenarios[t])) <= tau*scenarios[t] +1 for t in range(horizon)))
   
   model.addConstrs((risk_s_t[s,t] - risk_s_t[u,t]  + M*(1 + y[s,t] - y[u,t]) >= 0 for t in range(horizon) \
   for s in range(scenarios[t]) for u in range(scenarios[t]) if s != u))

   model.addConstrs((q_t[t] >= risk_s_t[s,t] - M*(1 - y[s,t]) for t in range(horizon) for s in range(scenarios[t])))
   
   model.addConstrs(excess[t] >= 0 for t in range(horizon))
   model.addConstrs(excess[t] >= q_t[t] - risk_bar_t[t] for t in range(horizon))

   model.addConstr(obj1 == quicksum(risk_bar_t[t] for t in range(horizon))*(1/horizon) )
   model.addConstr(obj2 == quicksum(excess[t] for t in range(horizon))*(1/horizon))
   
   # 4. Fix the objective
   obj = alpha*obj1 +  (1 - alpha)*obj2

   model.setObjective(obj,GRB.MINIMIZE)
   
   #5. Upadate the timelimit value according to the input computation time
   #computation time is specified in minutes
   #timelimit parameter of the model is specified in seconds
   model.Params.timelimit = computation_time*60

   # 6. Save the model 
   model.write(model_path)

   return model 

  def instance_resolution(self,mathematical_model): 
    
    #Call the optimizer algorithm
    mathematical_model.optimize()
    '''
    try:
      for v in mathematical_model.getVars():
        if v.X != 0:
          print("%s %f" % (v.Varname, v.X))
      return 0

    except : 
      print("Instance resolution failed !!!")
      return -1
    '''
  
  def output_file_creation(self,mathematical_model,interventions_real_number,output_path,interventions_number,horizon):
    
    f = open(output_path,"w")
    try:
      list_interventions_horizon = list()
      for i in range(interventions_number):
        for t in range(horizon):
          z = mathematical_model.getVarByName("z["+str(i)+","+str(t)+"]")
          if z.X != 0:
            int_json_number = interventions_real_number[i]
            f.write("Intervention_"+str(int_json_number)+" "+str(t+1)+"\n")
            list_interventions_horizon.append([int_json_number,t + 1])
      
      return list_interventions_horizon

    except AttributeError:
      print("Specefied attribute dosesn't existe")

    f.close()
    
  def show_w_values(self,mathematical_model,interventions_number,horizon,interventions_real_number,output_path):
    
    f = open(output_path,"w")
    try:
      for i in range(interventions_number):
        for t in range(horizon):
          w = mathematical_model.getVarByName("w["+str(i)+","+str(t)+"]")
          if w.X != 0:
            int_json_number = interventions_real_number[i]
            #print(w.Varname,w.X) #Show the details of the corresponding w
            #print("Intervention number in the json file :",int_json_number)
            #print("    ")
            f.write("w["+str(i)+","+str(t)+"] = 1 Intervention in json = "+str(int_json_number)+"\n")
      
      f.close()
      return 0

    except AttributeError:
      print("Specefied attribute dosesn't existe")

  def gantt_diagram(self,list_interventions_horizon,interventions_real_number,delta_i_t,gantt_path):
    #The Gantt diagram has three parameters 
    # curve len. corresponds to the y2 - y1 
    # size of text 
    # position of text: actually set to (start time - 1, int_model_number)
    try:
      fig = plt.figure()
      plt.rcParams.update({'font.size': 5})
      for index in range(len(list_interventions_horizon)):
        int_json_number = list_interventions_horizon[index][0]  #The number of the intervention in the json file  
        int_model_number = interventions_real_number.index(int_json_number)  #The number which corresponds to the 
        #intervention number during the execution. between [0 - I-1]
        start_time = list_interventions_horizon[index][1] #The period on which the intervention starts. between [1 - T]
        time_ = delta_i_t[int_model_number][start_time - 1] #Delta[i,t]
        #plt.fill_between(range(start_time, start_time + time_+1), y1 = int_json_number, y2 = int_json_number + 0.5, color='blue', alpha = 0.5)
        plt.fill_between(range(start_time, start_time + time_+1), y1 = int_model_number, y2 = int_model_number + 0.5, color='blue', alpha = 0.5)
        plt.text(start_time - 1,int_model_number, "I"+str(int_json_number))
      plt.show()
      #plt.savefig(gantt_path)
    except :
      print("Error")

    
