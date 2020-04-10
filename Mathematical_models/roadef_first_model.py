import gurobipy as gb 
from gurobipy import *

#1. Declaration of the initial informations about the instance
inter_numbers = 3
resou_number = 1
horizon = 3
scenario = 3
alpha = 0.5
compl_time = 15

#2. Declaration of the different model's initial data 
delta_i_t = [[3,3,2],[1,1,1],[1,1,2]] 
l_c_t = [[10,0,6]]
u_c_t = [[49, 23, 15]]

#A key (k1,k2) in the exc list refers to the pair (intervention1 , intervention 2) which are in exclusion 
exc_list = {
    (1,2):[0,1,2]
}
list_beta_indexes = list()
for i in range(inter_numbers):
  for t in range(horizon):
    for t1 in range(t+1):
      list_beta_indexes.append((i,t,t1))

#A key in r_c_i_t_t1 refers to the pair (intervention , resource)
#Each line in the r_c_i_t_t1[key] corresponds to a given t
#Each column int r_c_i_t_t1[key] corresponds to a given t' leq than t 

r_c_i_t_t1 = {
    (0,0): [[3],[0],[8]], 
    (1,0): [[14],[0,14],[0,0,14]],
    (2,0): [[5],[0,5],[0,0]]
}

#A key in risk_s_i_t_t1 refers to the pair (intervention , scenario)
#Each line in the risk_s_i_t_t1[key] corresponds to a given t
#Each column int risk_s_i_t_t1[key] corresponds to a given t' leq than t 
risk_s_i_t_t1 = {
    (0,0) : [[7],[1],[1]],
    (0,1) : [[4],[10],[4]],
    (0,2) : [[8],[10],[4]],
    (1,0) : [[5],[0,5],[0,0,5]],
    (1,1) : [[4],[0,4],[0,0,4]],
    (1,2) : [[5],[0,5],[0,0,5]],
    (2,0) : [[4],[0,3],[0,0]],
    (2,1) : [[8],[0,8],[0,0]],
    (2,2) : [[2],[0,1],[0,0]]
}

#3. Creation of the model 
model = Model('Roadef challenge')
z = model.addVars(inter_numbers,horizon,vtype = GRB.BINARY,name = "z")
w = model.addVars(inter_numbers,horizon,vtype = GRB.BINARY,name = "w")
y = model.addVars(scenario,horizon,vtype = GRB.BINARY,name = "y")
beta = model.addVars(list_beta_indexes,vtype = GRB.BINARY, name = "beta")
risk_s_t = model.addVars(scenario,horizon,vtype = GRB.CONTINUOUS, name = "risk_s_t")  
risk_bar_t = model.addVars(horizon,vtype = GRB.CONTINUOUS, name ="risk_bar_t")
q_t = model.addVars(horizon,vtype = GRB.CONTINUOUS, name ="q_t")
excess = model.addVars(horizon,vtype = GRB.CONTINUOUS, name = "excess")

#4. Add constraints 
model.addConstrs((quicksum(z[i,t] for t in range(horizon)) == 1 for i in range(inter_numbers)))
model.addConstrs((w[i, t] >= z[i, t] for i in range(inter_numbers) for t in range(horizon)))
model.addConstrs((z[i, t]*(t + delta_i_t[i][t]) <= horizon for i in range(inter_numbers) \
for t in range(horizon)))

model.addConstrs((w[key[0],t] + w[key[1],t] <= 1 for key in exc_list.keys() for t in exc_list[key]))
model.addConstrs((beta[i,t,t1] >= z[i,t1]+ w[i,t] - 1 for \
i in range(inter_numbers) for t in range(horizon) for t1 in range(t + 1)))

model.addConstrs((quicksum(beta[i,t,t1]*r_c_i_t_t1[(i,res)][t][t1] \
for i in range(inter_numbers) for t1 in range(t+1) if (i,res) in r_c_i_t_t1 and len(r_c_i_t_t1[(i,res)][t]) > t1) >= l_c_t[res][t] for res in range(resou_number) \
for t in range(horizon))) 

model.addConstrs((quicksum(beta[i,t,t1]*r_c_i_t_t1[(i,res)][t][t1] \
for i in range(inter_numbers) for t1 in range(t+1) if (i,res) in r_c_i_t_t1 and len(r_c_i_t_t1[(i,res)][t]) > t1) <= u_c_t[res][t] for res in range(resou_number) \
for t in range(horizon))) 

model.addConstrs((risk_s_t[s,t] == quicksum(risk_s_i_t_t1[(i,s)][t][t1]*beta[i,t,t1] for i in range(inter_numbers) for t1 in range(t+1) if (i,s) in risk_s_i_t_t1 and \
len(risk_s_i_t_t1[(i,s)][t]) > t1 ) for s in range(scenario) for t in range(horizon)))

model.addConstrs((risk_bar_t[t] == quicksum(risk_s_t[s,t] for s in range(scenario))*round(1/scenario,2) for t in range(horizon)))

model.addConstrs((quicksum(y[s,t] for s in range(scenario)) >= int(alpha*scenario) for t in range(horizon)))
model.addConstrs((quicksum(y[s,t] for s in range(scenario)) <= int(alpha*scenario) +1 for t in range(horizon)))

model.addConstrs((risk_s_t[s,t] - risk_s_t[u,t]  + 1000*(1 + y[s,t] - y[u,t]) >= 0 for t in range(horizon) \
for s in range(scenario) for u in range(scenario) if s != u) )

model.addConstrs((q_t[t] >= risk_s_t[s,t] - 1000*(1 - y[s,t]) for t in range(horizon) for s in range(scenario)))
model.addConstrs(excess[t] >= 0 for t in range(horizon))
model.addConstrs(excess[t] >= q_t[t] - risk_bar_t[t] for t in range(horizon))

#Fix the objective
obj = alpha*quicksum(risk_bar_t[t] for t in range(horizon))*round(1/horizon,2) + \
(1 - alpha)*(quicksum(excess[t] for t in range(horizon))*(round(1/horizon,2)))

model.setObjective(obj,GRB.MINIMIZE)

#6. Save the model 
model.write('first_model.lp')

#7. Call the optimizer algorithm 
model.optimize()
for v in model.getVars():
  if v.X != 0:
    print("%s %f" % (v.Varname, v.X))

