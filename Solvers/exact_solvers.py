import gurobipy as gb
from gurobipy import *

class ExactSolvers:

  def __init__(self):
    print("ExactSolvers class instantiation ....")
  
  def create_mathematical_model(self,interventions_number,resources_number,horizon,list_beta_indexes,scenarios,alpha,tau,completion_time, \
  delta_i_t,l_c_t,u_c_t,exclusions_list,r_c_i_t_t1,risk_s_i_t_t1,M,model_path):
   
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
   
   #3. Add constraints
   model.addConstrs((quicksum(z[i,t] for t in range(horizon)) == 1 for i in range(interventions_number)))
   model.addConstrs((w[i, t] >= z[i, t] for i in range(interventions_number) for t in range(horizon)))
   model.addConstrs((z[i, t]*(t + delta_i_t[i][t]) <= horizon for i in range(interventions_number) \
   for t in range(horizon)))

   model.addConstrs((w[key[0],t] + w[key[1],t] <= 1 for key in exclusions_list.keys() for t in exclusions_list[key]))
   
   model.addConstrs((beta[i,t,t1] >= z[i,t1]+ w[i,t] - 1 for i in range(interventions_number) \
   for t in range(horizon) for t1 in range(t + 1)))

   model.addConstrs((quicksum(beta[i,t,t1]*r_c_i_t_t1[(i,res)][t][t1] for i in range(interventions_number) \
   for t1 in range(t+1) if (i,res) in r_c_i_t_t1 and t in r_c_i_t_t1[(i,res)] \
   and t1 in r_c_i_t_t1[(i,res)][t]) >= l_c_t[res][t] \
   for res in range(resources_number) for t in range(horizon)))

   model.addConstrs((quicksum(beta[i,t,t1]*r_c_i_t_t1[(i,res)][t][t1] for i in range(interventions_number) \
   for t1 in range(t+1) if (i,res) in r_c_i_t_t1 and t in r_c_i_t_t1[(i,res)] \
   and t1 in r_c_i_t_t1[(i,res)][t]) <= u_c_t[res][t] \
   for res in range(resources_number) for t in range(horizon)))

   model.addConstrs((risk_s_t[s,t] == quicksum(risk_s_i_t_t1[i][t][t1][s]*beta[i,t,t1] for i in
   range(interventions_number) for t1 in range(t+1) if t1 in risk_s_i_t_t1[i][t]) \
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

   model.addConstrs((quicksum(w[i,t1] for t1 in range(t, horizon)) >= z[i,t]*(delta_i_t[i][t]) for i in range(interventions_number) \
   for t in range(horizon)))

   # 4. Fix the objective
   obj = alpha*quicksum(risk_bar_t[t] for t in range(horizon))*(1/horizon) + \
   (1 - alpha)*(quicksum(excess[t] for t in range(horizon))*(1/horizon))
   model.setObjective(obj,GRB.MINIMIZE)

   # 5. Save the model 
   model.write(model_path)

   return model 

  def instance_resolution(self,mathematical_model): 
    #7. Call the optimizer algorithm
    mathematical_model.optimize()
    """
    for v in mathematical_model.getVars():
      if v.X != 0:
        print("%s %f" % (v.Varname, v.X))
    """



    