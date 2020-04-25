import gurobipy as gb
from gurobipy import *

class ExactSolvers:

  def __init__(self):
    print("ExactSolvers class instantiation ....")
  
  def create_mathematical_model_v1(self,interventions_number,resources_number,horizon,list_beta_indexes,scenarios,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,M,model_path,t_max):
   
   #1. Creation of the model
    model = Model('Roadef challenge model with w and beta .......')

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
  
    #3. Add constraints
    model.addConstrs((quicksum(z[i,t] for t in range(t_max[i] + 1)) == 1 for i in range(interventions_number)))
    model.addConstrs(z[i,t] == 0 for i in range(interventions_number) for t in range(t_max[i] + 1,horizon) )
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
  
  def create_mathematical_model_v2(self,interventions_number,resources_number,horizon,list_z_indexes,scenarios,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,M,model_path,t_max):
    
    #1. Creation of the model
    model = Model('Roadef challenge model with x and z .......')

    #2. Add the variables
    x = model.addVars(interventions_number,horizon,vtype = GRB.BINARY,name = "x")
    z = model.addVars(list_z_indexes,vtype = GRB.BINARY, name = "z")
    y = model.addVars(max(scenarios),horizon,vtype = GRB.BINARY,name = "y")
    
    risk_s_t = model.addVars(max(scenarios),horizon,vtype = GRB.CONTINUOUS, name = "risk_s_t")
    risk_bar_t = model.addVars(horizon,vtype = GRB.CONTINUOUS, name="risk_bar_t")
    q_t = model.addVars(horizon,vtype = GRB.CONTINUOUS, name ="q_t")
    excess = model.addVars(horizon,vtype = GRB.CONTINUOUS, name = "excess")
    obj1 = model.addVar(vtype = GRB.CONTINUOUS, name = "obj1")
    obj2 = model.addVar(vtype = GRB.CONTINUOUS, name = "obj2")

    #3. Add constraints 
    model.addConstrs((quicksum(x[i,t] for t in range(t_max[i] + 1)) == 1 for i in range(interventions_number)))
    model.addConstrs(x[i,t] == 0 for i in range(interventions_number) for t in range(t_max[i] + 1,horizon) )
    model.addConstrs((x[i, t]*(t + delta_i_t[i][t]) <= horizon for i in range(interventions_number) for t in range(t_max[i] + 1)))   
    model.addConstrs((x[i,t]*(t + 1) <= t_max[i] + 1 for i in range(interventions_number) for t in range(t_max[i] + 1)))
    
    model.addConstrs((quicksum(z[i,t,t1] for t1 in range(delta_i_t[i][t]))== x[i,t]*delta_i_t[i][t] for i in range(interventions_number)
    for t in range(t_max[i] + 1)))
     
    model.addConstrs((z[key[0],t1,t - t1] + z[key[1],t2,t-t2] <= 1 for key in exclusions_list.keys()
    for t in exclusions_list[key]
    for t1 in range(t + 1) for t2 in range(t + 1) 
    if  (key[0],t1,t-t1) in z and  (key[1],t2,t-t2) in z))
    
    model.addConstrs((quicksum(r_c_i_t_t1[i,res][t][t1]*z[i,t1,t-t1] for i in range(interventions_number) 
    for t1 in range(t_max[i] + 1) if (i,res) in r_c_i_t_t1 and t in r_c_i_t_t1[(i,res)] 
    and t1 in r_c_i_t_t1[(i,res)][t] and (i,t1,t-t1) in z) >= l_c_t[res][t] for res in range(resources_number) 
    for t in range(horizon)))

    model.addConstrs((quicksum(r_c_i_t_t1[i,res][t][t1]*z[i,t1,t-t1] for i in range(interventions_number) 
    for t1 in range(t_max[i] + 1) if (i,res) in r_c_i_t_t1 and t in r_c_i_t_t1[(i,res)] 
    and t1 in r_c_i_t_t1[(i,res)][t] and (i,t1,t-t1) in z) <= u_c_t[res][t] for res in range(resources_number) 
    for t in range(horizon)))

    model.addConstrs((risk_s_t[s,t] == quicksum(risk_s_i_t_t1[i][t][t1][s]*z[i,t1,t-t1] for i in range(interventions_number)
    for t1 in range(t_max[i] + 1) if t in risk_s_i_t_t1[i] and t1 in risk_s_i_t_t1[i][t] and (i,t1,t-t1) in z) for t in range(horizon) 
    for s in range(scenarios[t])))
    
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

  def create_mathematical_compact_model(self,interventions_number,resources_number,horizon,list_z_indexes,scenarios,alpha,tau,computation_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,model_path,t_max):
    
    #1. Creation of the model
    model = Model('Roadef challenge compact model with only x variable .......')

    #2. Add the variables
    x = model.addVars(interventions_number,horizon,vtype = GRB.BINARY,name = "x")
    y = model.addVars(max(scenarios),horizon,vtype = GRB.BINARY,name = "y")
    
    g_s_t = model.addVars(max(scenarios),horizon,vtype = GRB.CONTINUOUS, name = "g_s_t")
    g_t_bar = model.addVars(horizon,vtype = GRB.CONTINUOUS, name="g_t_bar")
    q_t = model.addVars(horizon,vtype = GRB.CONTINUOUS, name ="q_t")
    excess = model.addVars(horizon,vtype = GRB.CONTINUOUS, name = "excess")
    obj1 = model.addVar(vtype = GRB.CONTINUOUS, name = "obj1")
    obj2 = model.addVar(vtype = GRB.CONTINUOUS, name = "obj2")

    #3. Add constraints 
    model.addConstrs((quicksum(x[i,t] for t in range(t_max[i] + 1)) == 1 for i in range(interventions_number)))
    model.addConstrs(x[i,t] == 0 for i in range(interventions_number) for t in range(t_max[i] + 1,horizon))
    model.addConstrs((x[i, t]*(t + delta_i_t[i][t]) <= horizon for i in range(interventions_number) for t in range(t_max[i] + 1))) 
    model.addConstrs((x[i,t]*(t + 1) <= t_max[i] + 1 for i in range(interventions_number) for t in range(t_max[i] + 1)))

    model.addConstrs((quicksum(x[i,h] for h in range(t+1) if delta_i_t[i][h] + h > t) + \
    quicksum(x[j,h] for h in range(t+1) if delta_i_t[j][h] + h > t) <= 1 for (i,j) in exclusions_list.keys() \
    for t in exclusions_list[(i,j)]))

    model.addConstrs((quicksum(x[i,h]*r_c_i_t_t1[(i,c)][t][h] for i in range(interventions_number)  
    if (i,c) in r_c_i_t_t1 and t in r_c_i_t_t1[(i,c)] for h in r_c_i_t_t1[(i,c)][t].keys()) >= l_c_t[c][t] 
    for c in range(resources_number) for t in range(horizon)))

    model.addConstrs((quicksum(x[i,h]*r_c_i_t_t1[(i,c)][t][h] for i in range(interventions_number)  
    if (i,c) in r_c_i_t_t1 and t in r_c_i_t_t1[(i,c)] for h in r_c_i_t_t1[(i,c)][t].keys()) <= u_c_t[c][t] 
    for c in range(resources_number) for t in range(horizon)))

    model.addConstrs((g_s_t[s,t] == quicksum(x[i,h]*risk_s_i_t_t1[i][t][h][s] for i in range(interventions_number)
    for h in risk_s_i_t_t1[i][t].keys() if t in risk_s_i_t_t1 ) for t in range(horizon) for s in range(scenarios[t])))
    
    model.addConstrs((g_t_bar[t] == quicksum(g_s_t[s,t] for s in
    range(scenarios[t]))*(1/scenarios[t]) for t in range(horizon)))

    model.addConstrs((quicksum(y[s,t] for s in range(scenarios[t])) >= tau*scenarios[t] for t in range(horizon)))
    model.addConstrs((quicksum(y[s,t] for s in range(scenarios[t])) <= tau*scenarios[t] +1 for t in range(horizon)))
    model.addConstrs((q_t[t] >= g_s_t[s,t]*y[s,t] for t in range(horizon) for s in range(scenarios[t])))
    model.addConstrs(excess[t] >= q_t[t] - g_t_bar[t] for t in range(horizon))
    model.addConstrs(excess[t] >= 0 for t in range(horizon))
    
    # 4. Fix the objective
    model.addConstr(obj1 == quicksum(g_t_bar[t] for t in range(horizon))*(1/horizon) )
    model.addConstr(obj2 == quicksum(excess[t] for t in range(horizon))*(1/horizon))
    
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
  
  

    
