#data_tracker
#收集之后同意输入
#GANM、SANM分开
import Model
import os
import datetime
import pandas as pd
import numpy as np
import pdb
# def GANM_best_main_1(agents,ScoreType,genes_popu,file_name,aj_filename,process_name,num_nd_gene,Tracker_choice,Tracker_maxSocial):
# 	decode_genes_popu=[[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in ge_popu] for ge_popu in genes_popu]
# 	print('step1')
# 	agents_genes_value=[[[agents[i].value_caculate(p) for p in decode_gene_popu] for decode_gene_popu in decode_genes_popu] for i in range(len(agents))]
# 	##四维嵌套列表[[[cmax,cmax,...],[第二代],...],[agents1],[agent2]]
# 	# agents_choice_Cmax=[sum([agents[i].Cmax_caculate(decode_genes_popu[i_1][Tracker_choice[i_1]]) for i in range(len(agents))] for i_1 in range(len(decode_genes_popu)))]
# 	# print(len(decode_genes_popu))
# 	print('step2')
# 	agents_choice_value=[[agents[i].value_caculate(decode_genes_popu[i_1][Tracker_choice[i_1]]) for i in range(len(agents))] for i_1 in range(len(decode_genes_popu))]
# 	print('step3')
# 	agents_best_value=[[min(agent_gene_value) for agent_gene_value in agent_genes_value] for agent_genes_value in agents_genes_value]
# 	print('step4')
# 	agents_average_value=[[sum(agent_gene_value)/len(agent_gene_value) for agent_gene_value in agent_genes_value] for agent_genes_value in agents_genes_value]
# 	print('step5')
# 	agents_best_value=list(map(list,zip(*agents_best_value)))
# 	print('step6')
# 	agents_average_value=list(map(list,zip(*agents_average_value)))
# 	# agents_best_sum_value=[sum(p) for p in agents_best_value]
# 	# agents_average_sum_value=[sum(p) for p in agents_average_value]
# 	print('step7')
# 	agents_all_value=[agents_best_value[i]+agents_average_value[i]+agents_choice_value[i]+[num_nd_gene[i],Tracker_maxSocial[i]] for i in range(len(agents_best_value))]
# 	############################################################
# 	columns_n=[f'agent_best{i}' for i in range(len(agents))]
# 	columns_n=columns_n+[f'agent_average{i}' for i in range(len(agents))]
# 	columns_n=columns_n+[f'agent_choice{i}' for i in range(len(agents))]
# 	columns_n.append('num_nd')
# 	# columns_n.append('total_choice_value')
# 	columns_n.append('maxSocial')
# 	path='data_save/'+file_name
# 	path=path+'/'+aj_filename
# 	if not os.path.exists(path):
# 		os.makedirs(path)
# 	out_excel=pd.DataFrame(agents_all_value,columns=columns_n)
# 	out_excel.to_excel(path+'/'+str(ScoreType)+'.xlsx',index=False)
def GANM_best_main_2(agents,ScoreType,genes_popu,file_name,aj_filename,process_name,num_nd_gene,Tracker_choice,Tracker_maxSocial):
	import json
	decode_genes_popu=[[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in ge_popu] for ge_popu in genes_popu]
	print('step1')
	agents_genes_value=[[[agents[i].value_caculate(p) for p in decode_gene_popu] for decode_gene_popu in decode_genes_popu] for i in range(len(agents))]
	##四维嵌套列表[[[cmax,cmax,...],[第二代],...],[agents1],[agent2]]
	# agents_choice_Cmax=[sum([agents[i].Cmax_caculate(decode_genes_popu[i_1][Tracker_choice[i_1]]) for i in range(len(agents))] for i_1 in range(len(decode_genes_popu)))]
	# print(len(decode_genes_popu))
	print('step2')
	#  由查找替换计算 agents[i].value_caculate(decode_genes_popu[i_1][Tracker_choice[i_1]])
	agents_choice_value=[[agents_genes_value[i][i_1][Tracker_choice[i_1]] for i in range(len(agents))] for i_1 in range(len(decode_genes_popu))]
	print('step3')
	agents_best_value=[[min(agent_gene_value) for agent_gene_value in agent_genes_value] for agent_genes_value in agents_genes_value]
	print('step4')
	agents_worst_value=[[max(agent_gene_value) for agent_gene_value in agent_genes_value] for agent_genes_value in agents_genes_value]
	print('step5')
	agents_average_value=[[sum(agent_gene_value)/len(agent_gene_value) for agent_gene_value in agent_genes_value] for agent_genes_value in agents_genes_value]
	print('step6')
	agents_best_value=list(map(list,zip(*agents_best_value)))
	agents_worst_value=list(map(list,zip(*agents_worst_value)))
	agents_average_value=list(map(list,zip(*agents_average_value)))
	# agents_best_sum_value=[sum(p) for p in agents_best_value]
	# agents_average_sum_value=[sum(p) for p in agents_average_value]
	agents_all_value=[agents_best_value[i]+agents_worst_value[i]+agents_average_value[i]+agents_choice_value[i]+[num_nd_gene[i],Tracker_maxSocial[i]] for i in range(len(agents_best_value))]
	############################################################
	columns_n=[f'agent_best{i}' for i in range(len(agents))]+[f'agent_worst{i}' for i in range(len(agents))]\
	+[f'agent_average{i}' for i in range(len(agents))]+[f'agent_choice{i}' for i in range(len(agents))]
	columns_n.append('num_nd')
	# columns_n.append('total_choice_value')
	columns_n.append('maxSocial')
	path='data_save/'+file_name
	path=path+'/'+aj_filename
	path=path+'/'+process_name[:-5]
	if not os.path.exists(path):
		os.makedirs(path)
	out_excel=pd.DataFrame(agents_all_value,columns=columns_n)
	out_excel.to_excel(path+'/'+str(ScoreType)+'.xlsx',index=False)
	print('step7')
	output=open(path+'/'+'agents_value_genes.json','w')
	json.dump(agents_genes_value,output)
	output.close()
def GANM2_best_main(agents,genes_popu,file_name,aj_filename,num_propose,num_parent,num_child,r_max):
	decode_genes_popu=[[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in ge_popu] for ge_popu in genes_popu]
	agents_genes_Cmax=[[[agents[i].Cmax_caculate(p) for p in decode_gene_popu] for decode_gene_popu in decode_genes_popu] for i in range(len(agents))]
	agents_sum_Cmax=np.sum(np.array(agents_genes_Cmax),axis=0)
	agents_best_Cmax=[[min(agent_gene_Cmax) for agent_gene_Cmax in agent_genes_Cmax] for agent_genes_Cmax in agents_genes_Cmax]
	agents_average_Cmax=[[sum(agent_gene_Cmax)/len(agent_gene_Cmax) for agent_gene_Cmax in agent_genes_Cmax] for agent_genes_Cmax in agents_genes_Cmax]
	agents_best_Cmax=list(map(list,zip(*agents_best_Cmax)))
	agents_average_Cmax=list(map(list,zip(*agents_average_Cmax)))
	agents_best_sum_Cmax=[[agents_genes_Cmax[_i][i_p][np.argmin(agents_sum_Cmax[i_p])] for _i in range(len(agents))] for i_p in range(len(agents_sum_Cmax))]
	agents_average_sum_Cmax=[sum(p) for p in agents_average_Cmax]
	agents_all_Cmax=[agents_best_Cmax[i]+agents_average_Cmax[i]+agents_best_sum_Cmax[i]+[agents_average_sum_Cmax[i]] for i in range(len(agents_best_Cmax))]
	columns_n=[f'agent{i}_best' for i in range(len(agents))]+[f'agent{i}_average' for i in range(len(agents))]+[f'agent{i}_sumbest' for i in range(len(agents))]
	columns_n.append('total_average_Cmax')
	path='data_save/'+file_name
	if not os.path.exists(path):
		os.makedirs(path)
	path=path+'/'+aj_filename
	if not os.path.exists(path):
		os.makedirs(path)
	curr_time=datetime.datetime.now()
	time_str=datetime.datetime.strftime(curr_time,'%Y_%m_%d_%H_%M_%S_%f')
	out_excel=pd.DataFrame(agents_all_Cmax,columns=columns_n)
	out_excel.to_excel(path+'/'+f'GANM2_c{num_child}_r{r_max}_np{num_parent}'+file_name+time_str+'.xlsx',index=False)
def SANM_active_main(agents,file_name,aj_filename,tracker_active_ps,num_child,r_max,quota):
	decode_active_ps=[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in tracker_active_ps]
	agents_activeps_value=[[agents[i].value_caculate(p) for i in range(len(agents))] for p in decode_active_ps]
	agents_all_value=[p+[sum(p)] for p in agents_activeps_value]
	# agents_all_Cmax=list(map(list,zip(*agents_all_Cmax)))
	columns_n=[f'agent{i}_active' for i in range(len(agents))]
	columns_n.append('total_active_values')
	path='data_save/'+file_name
	if not os.path.exists(path):
		os.makedirs(path)
	path=path+'/'+aj_filename
	if not os.path.exists(path):
		os.makedirs(path)
	curr_time=datetime.datetime.now()
	time_str=datetime.datetime.strftime(curr_time,'%Y_%m_%d_%H_%M_%S_%f')
	out_excel=pd.DataFrame(agents_all_value,columns=columns_n)
	out_excel.to_excel(path+'/'+f'SANM_c{num_child}_r{r_max}_q{quota}'+file_name+time_str+'.xlsx',index=False)
def statistic_gene(file_name,aj_filename,process_name,n_g=100):
	########### 统计最后种群多样性 ######################################
	#i 代表第i个位置，j 代表工件j
	import json
	process_file='data_save/'+file_name+'/'+aj_filename+'/GANM_process/'+process_name
	process_file=open(process_file,'r')
	Gene_popu=json.load(process_file)
	r_max=len(Gene_popu)
	last_genes=Gene_popu[-1-n_g:-1]
	count_gene=[[0]*len(last_genes[0][0]) for i in last_genes[0][0]]
	for gene in last_genes:
		for popu in gene:
			for i,j in enumerate(popu):
				count_gene[i][j]=count_gene[i][j]+1
	columns_n=list(range(len(last_genes[0][0])))
	out_excel=pd.DataFrame(count_gene,columns_n)
	path='data_save/'+file_name+'/'+aj_filename+'/'+process_name[0:-5]
	out_excel.to_excel(path+'/'+f'GANM_statistic_gen{n_g}_round{r_max}'+'.xlsx',index=False)

	