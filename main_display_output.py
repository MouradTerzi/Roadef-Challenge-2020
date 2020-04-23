import os 
import sys 

sys.path.insert(0,'Inputs/')
sys.path.insert(0,'Outputs/')

import reader as rd 
import display_results as dr 

if __name__ == "__main__":

  instance_path = 'Instances/Set_A/A_01.json'
  #z_path = 'Outputs/Output_z_files/SetA/SetA_01_z_file_wrong.json'
  z_path = 'Outputs/Output_z_files/SetA/SetA_01_z_file.json'
  reader = rd.Reader()
  instance = reader.read_instance(instance_path)
  instance.show_basic_details()
  dr_object = dr.DisplayResults()
  partial_exclusion = dict()
  #for key in instance.exclusions:
    #partial_exclusion[key] = instance.exclusions[key]
    #break 
  i_17 = instance.interventions_json_number.index(17)
  i_18 = instance.interventions_json_number.index(18)
  
  partial_exclusion[(i_17,i_18)] = instance.exclusions[(i_17,i_18)]
  #print(instance.exclusions[(i_17,i_18)])
  #print(instance.delta_i_t[i_17][0])
  #print(instance.delta_i_t[i_18][0])
  #dr_object.basic_gantt_diagram(z_path,instance.interventions_json_number," ")
  #dr_object.check_exclusions(z_path,partial_exclusion,instance.interventions_json_number)
  dr_object.check_exclusions(z_path,instance.exclusions,instance.interventions_json_number)
  
  

