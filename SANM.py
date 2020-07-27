import random
import Model
import copy
import Agent
import pdb
import Data_tracker
def Main(file_name,aj_instance_name):
	ScoreType=0
	instance_0=Model.instance(1,file_name,aj_instance_name,ScoreType)
	agents=[]
	for i in range(len(instance_0.aj_list)):
		agents.append(Agent.Agent(i,instance_0))
	num_child=200
	r_max=5000
	quota=500
	P_choice,tracker_active_ps=SANM(agents,num_child,r_max,quota)##一般quota设为num_child的一半
	Data_tracker.SANM_active_main(agents,file_name,aj_instance_name,tracker_active_ps,num_child,r_max,quota)
	print(P_choice)
def SANM(agents,num_child=1000,r_max=1000,quota=500):
	r=0
	Active_p=SANM_initial(agents)
	beta_q=(1/quota)**(1/(r_max-1))
	tracker_active_ps=[Active_p]
	##增加预选择模块###
	for r in range(r_max):
		C_popu=SANM_child(Active_p,num_child)
		iagents_chose=SANM_chose(agents,C_popu,quota)
		#print(iagents_chose)
		ia_p=SANM_active_d(iagents_chose)
		Active_p=C_popu[ia_p]
		tracker_active_ps.append(Active_p)
		#print(ia_p)
		quota=quota*beta_q
		if quota<1:
			quota=1
		print(r)
		# print(quota)
		#print(Active_p)
	return Active_p,tracker_active_ps
def SANM_initial(agents):
	protocol=agents[0].GANM_A_random_search()
	return protocol
def SANM_child(a_p,num_child):
	c_popu=[a_p]
	while len(c_popu)<num_child:
		c_p=SANM_mute(a_p)
		c_popu.append(c_p)
	# print(c_popu)
	# pdb.set_trace()
	return c_popu
def SANM_chose(agents,c_popu,quota):
	iagents_chose=[]
	iquota=round(quota)
	decode_popu=[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in c_popu]
	for i in range(len(agents)):
		ias_chose=agents[i].SANM_A_vote(decode_popu,iquota)
		iagents_chose.append(ias_chose)
	return iagents_chose
def SANM_active_d(iagents_chose):
	common_ps=SANM_common_d(iagents_chose)
	active_d=0
	if len(common_ps)!=0:
		active_d=random.choice(common_ps)
	return active_d
def SANM_common_d(iagents_chose):
	# common_ps=[s=s&set(iagents_chose[i+1]) for i in range(len(iagents_chose))]
	common_ps=set(iagents_chose[0])
	i=1
	while i<len(iagents_chose)-1:
		i=i+1
		common_ps=common_ps&set(iagents_chose[i])
	return list(common_ps)
def SANM_mute(o_p,exchange_mode=1):
	c_1=copy.copy(o_p)
	num_j=max(c_1)
	a=[[] for i in range(num_j)]
	job_pos=[a[j].append(i) for i,j in enumerate(c_1)]
	if exchange_mode==0:
		mute_j=random.sample(list(range(num_j)),2)
		mute_p=[random.choice(job_pos[mute_j[0]]),random.choice(job_pos[mute_j[1]])]
		c_1[mute_p[0]],c_1[mute_p[1]]=c_1[mute_p[1]],c_1[mute_p[0]]
	else:
		##按正态分布选择####
		num_mute=int(abs(random.normalvariate(2,1)))
		if num_mute==0:
			num_mute=num_mute+1
		for i in range(num_mute):
			mute_j=random.sample(list(range(num_j)),2)
			mute_p=[random.choice(job_pos[mute_j[0]]),random.choice(job_pos[mute_j[1]])]
			c_1[mute_p[0]],c_1[mute_p[1]]=c_1[mute_p[1]],c_1[mute_p[0]]
	return c_1
if __name__=='__main__':
	Main('abz5','abz5_aj_instance2020_06_23_14_15_45_518179.json')