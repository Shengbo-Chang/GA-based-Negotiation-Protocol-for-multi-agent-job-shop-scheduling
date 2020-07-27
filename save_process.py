import os
import datetime
import json
import GA_NM
import Data_tracker
import Agent
import Model
import numpy as np
def Main():
	# ScoreType:0-sum-total-score;1.1-sum-limited-score-10, 1.2-prod-limited-score-10; 
	# 2.1-pord-rank-to-Borda; 2.2-sum-rank-to-Borda==prod-rank-to-lexca; 2.3-prod-rank-to-kAp; 2.4-sum-rank-to-kAp
	# 3.1-obj-prod; 3.2-obj-sum; 4.1-normal-obj-prod

	ScoreTypes=[0,1.1,1.2,2.1,2.2,3.1,3.2,4.1]
	# ScoreTypes=[4.1]
	file_name='abz5'
	aj_filename='abz5_ajs_instance2020_06_23_14_15_45_518179.json'
	process_name='r_10000_c_1002020_07_02_21_18_11_859379.json'
	# process_name='nos_r_10000_c_1002020_06_29_22_15_54_215131.json'
	num_gen=100
	##指南：首次保存协商过程，先运行load_GANM_process函数，生成agents_value_genes文件
	##然后，其他评分方法可运行load_GANM_genesvalue函数，生成不同评分方法选择
	##generate##########################################################
	####################################################################
	if len(ScoreTypes)>1:
		ScoreType=ScoreTypes[0]
		load_GANM_process(file_name,aj_filename,process_name,ScoreType)
	#####################################################################
	####################################################################
		for ScoreType in ScoreTypes[1:]:
			load_GANM_genesvalue(file_name,aj_filename,process_name,ScoreType)
	else:
		ScoreType=ScoreTypes[0]
		load_GANM_genesvalue(file_name,aj_filename,process_name,ScoreType)
	##Statistic##########################################################
	# process_statistic(file_name,aj_filename,process_name,num_gen)
	####################################################################
	# last_genes(file_name,aj_filename,process_name,ScoreType)
	####################################################################
	####################################################################
	# list_scater(file_name,aj_filename,process_name)
def save_GANM(file_name,num_child,r_max,aj_filename,Tracker_Gene_popu,b_block,asa_round):
	path='data_save/'+file_name
	if not os.path.exists(path):
		os.makedirs(path)
	path=path+'/'+aj_filename+'/GANM_process'
	if not os.path.exists(path):
		os.makedirs(path)
	curr_time=datetime.datetime.now()
	time_str=datetime.datetime.strftime(curr_time,'%Y_%m_%d_%H_%M_%S_%f')
	output=open(path+'/'+f'r_{r_max}_apr_{b_block[0]}sa{asa_round}_c_{num_child}'+time_str+'.json','w')
	json.dump(Tracker_Gene_popu[:-1],output)
	output.close()
def load_GANM_genesvalue(file_name,aj_filename,process_name,ScoreType):
	## 暂时不行 ##########
	import pandas as pd
	ST=ScoreType
	aj_instance_name=aj_filename
	instance_0=Model.instance(1,file_name,aj_filename,ST)
	agents=[]
	for i in range(len(instance_0.aj_list)):
		agents.append(Agent.Agent(i,instance_0))
	if instance_0.shop_a!=0:
		agents.append(Agent.Shop_agent(i+1,instance_0))
	path='data_save/'+file_name+'/'+aj_filename+'/'+process_name[0:-5]+'/'
	genesvalue_file=path+'agents_value_genes.json'
	genesvalue=open(genesvalue_file,'r')
	genesvalue=json.load(genesvalue)
	print(len(genesvalue[0]))
	agents_genes_value=np.array(genesvalue)
	avgs=agents_genes_value.swapaxes(1,0)
	# print(len(avgs[0][0]))
	# print(len(avgs[0][0]))
	if ScoreType==4.1:
		global_minmax=[[min(genesvalue[j][-1]),max(genesvalue[j][-1])] for j in range(len(agents))]
		print(global_minmax)
		# print(len(global_minmax[0][0]))
		ascore_gs=[[agents[j].GANM_A_valueToscore(np.array(avgs[i][j]),ag_minmax=global_minmax[j]) for j in range(len(agents))] for i in range(len(avgs))]
	else:
		ascore_gs=[[agents[j].GANM_A_valueToscore(np.array(avgs[i][j])) for j in range(len(agents))] for i in range(len(avgs))]
	# print(ascore_gs)
	if ScoreType==0 or ScoreType==1.1 or ScoreType==2.2 or ScoreType==2.4:
		Tracker_choice=[np.argmax(np.array(ascore_gs[i]).sum(axis=0)) for i in range(len(ascore_gs))]
	if ScoreType==1.2 or ScoreType==2.1 or ScoreType==2.3 or ScoreType==4.1:
		Tracker_choice=[np.argmax(np.array(ascore_gs[i]).prod(axis=0)) for i in range(len(ascore_gs))]
	if ScoreType==3.1:
		Tracker_choice=[np.argmin(np.array(ascore_gs[i]).prod(axis=0)) for i in range(len(ascore_gs))]
	if ScoreType==3.2:
		Tracker_choice=[np.argmin(np.array(ascore_gs[i]).sum(axis=0)) for i in range(len(ascore_gs))]
	# Tracker_choice=np.array(ascore_gs).sum(axis=1).argmax(axis=1).tolist()
	agents_choice_value=[[agents_genes_value[i][i_1][Tracker_choice[i_1]] for i in range(len(agents))] for i_1 in range(len(avgs))]
	############################################################
	columns_n=[f'agent_choice{i}' for i in range(len(agents))]
	path='data_save/'+file_name+'/'+aj_filename+'/'+process_name[:-5]+'/'
	out_excel=pd.DataFrame(agents_choice_value,columns=columns_n)
	out_excel.to_excel(path+str(ScoreType)+'.xlsx',index=False)
def load_GANM_process(file_name,aj_filename,process_name,ScoreType):
	ST=ScoreType
	aj_instance_name=aj_filename
	instance_0=Model.instance(1,file_name,aj_filename,ST)
	agents=[]
	for i in range(len(instance_0.aj_list)):
		agents.append(Agent.Agent(i,instance_0))
	if instance_0.shop_a!=0:
		agents.append(Agent.Shop_agent(i+1,instance_0))
	path='data_save/'+file_name+'/'+aj_filename+'/'+'GANM_process/'
	process_file=path+process_name
	process_file=open(process_file,'r')
	genes_popu=json.load(process_file)
	print(len(genes_popu))
	Tracker_num_nd,Tracker_choice,Tracker_maxSocial=GA_NM.Traker_get_GANM(agents,genes_popu,ScoreType)
	print(len(genes_popu),len(Tracker_num_nd),len(Tracker_choice),len(Tracker_maxSocial))
	Data_tracker.GANM_best_main_2(agents,ScoreType,genes_popu,file_name,aj_instance_name,process_name,Tracker_num_nd,Tracker_choice,Tracker_maxSocial)	
def process_statistic(file_name,aj_filename,process_name,num_gen):
	Data_tracker.statistic_gene(file_name,aj_filename,process_name,num_gen)
def last_genes(file_name,aj_filename,process_name,ScoreType):
	import pandas as pd
	ST=ScoreType
	aj_instance_name=aj_filename
	instance_0=Model.instance(1,file_name,aj_filename,ST)
	agents=[]
	for i in range(len(instance_0.aj_list)):
		agents.append(Agent.Agent(i,instance_0))
	if instance_0.shop_a!=0:
		agents.append(Agent.Shop_agent(i+1,instance_0))
	path='data_save/'+file_name+'/'+aj_filename+'/'
	process_file=path+'GANM_process/'+process_name
	process_file=open(process_file,'r')
	ge_popu=json.load(process_file)[-1]
	decode_ge_popu=[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in ge_popu]
	agents_ge_value=[[agents[i].value_caculate(p) for i in range(len(agents))] for p in decode_ge_popu]
	columns_n=[f'agent_value{i}' for i in range(len(agents))]
	out_excel=pd.DataFrame(agents_ge_value,columns=columns_n)
	out_excel.to_excel(path+'/'+process_name[:-5]+'/'+'lastgene_value_agents.xlsx',index=False)
def list_scater(file_name,aj_filename,process_name):
	import pandas as pd
	import matplotlib.pyplot as plt
	from mpl_toolkits.mplot3d import Axes3D
	import numpy as np
	path='data_save/'+file_name+'/'+aj_filename+'/'+process_name[:-5]+'/'
	exn=path+'/lastgene_value_agents.xlsx'
	n_scores=['0','1.1','1.2','2.1','2.2']
	sc_a=[]
	# for n_s in n_scores:
	# 	n_s_n=path+n_s+'.xlsx'
	# 	df=pd.read_excel(n_s_n)
	# 	for i in range(3):
	# 		a_c=df.ix[-1,f'agent_choice{i}']
	# 		sc_a.append(a_c)
	n_s_n=path+'0.xlsx'
	df=pd.read_excel(n_s_n)
	for i in range(3):
		a_c=df.ix[10000,f'agent_choice{i}']
		sc_a.append(np.array(a_c))
	print(sc_a)
	############################
	df=pd.read_excel(exn)
	a0_c=np.array(df.ix[:,0])
	a1_c=np.array(df.ix[:,1])
	a2_c=np.array(df.ix[:,2])
	# print(a0_c)
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter(a0_c,a1_c,a2_c)
	print(sc_a)
	ax.scatter([sc_a[0]],[sc_a[1]],[sc_a[1]],c='r')
	plt.savefig(path+'lastgene_value_agents.jpg')
	plt.show()
# def last_gene_scater(file_name,aj_filename,process_name):
# 	import json
# 	process_file='data_save/'+file_name+'/'+aj_filename+'/GANM_process/'+process_name
# 	path='data_save/'+file_name+'/'+aj_filename+'/'+process_name
# 	all_genes=json.load(process_file)
# 	last_gene=all_genes[-1]	
# 	out_excel=pd.DataFrame(count_gene,columns_n)
# 	path='data_save/'+file_name+'/'+aj_filename+'/'+process_name[0:-5]
# 	out_excel.to_excel(path+'/'+f'GANM_statistic_gen{n_g}_round{r_max}'+'.xlsx',index=False)
if __name__=='__main__':
	Main()