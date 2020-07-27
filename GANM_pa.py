import GA_NM
import Agent
import Model
import numpy as np
from itertools import chain
def Main(file_name,aj_instance_name):
	instance_0=Model.instance(1,file_name,aj_instance_name)
	agents=[]
	for i in range(len(instance_0.aj_list)):
		agents.append(Agent.Agent(i,instance_0))
	re_p=GA_p(agents)
	print(re_p)
def GA_p(agents,num_exchange_round=10,num_rounds=10,num_parent=50):
	AsP_popu=[agents[i].GANM_A_propose_Cmax(num_parent,num_multi=3) for i in range(len(agents))]
	for _i in range(num_rounds):
		for i in range(len(agents)):
			AsP_popu[i]=GA_agent(agents[i],AsP_popu[i],num_exchange_round,num_parent)
		AsP_popu=Apopu_exchange(agents,AsP_popu)
		print('kakkakkakakakkakakakka',_i)
	return AsP_popu
def GA_agent(agent,P_popu,num_exchange_round,num_parent):
	for r in range(num_exchange_round):
		decode_ps=[Model.decode(p,agent.num_j,agent.num_m,agent.OT)[1] for p in P_popu]
		P_scores=agent.GANM_A_grade_Cmax(decode_ps)
		num_child=50
		C_popu=GA_NM.GANM2_child(P_popu,num_child,P_scores,prob_mute=0.3)
		All_popu=P_popu+C_popu
		All_decode_ps=[Model.decode(p,agent.num_j,agent.num_m,agent.OT)[1] for p in All_popu]
		popu_scores=agent.GANM_A_grade_Cmax(All_decode_ps)
		iP_popu=GA_NM.GANM2_chose_tournament(popu_scores,num_parent,10)
		P_popu=[All_popu[i] for i in iP_popu]
		print(r)
	return P_popu
def Apopu_exchange(agents,AsP_popu,np_exchange=5):
	decode_AsP_popu=[[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in A_popu] for A_popu in AsP_popu]
	Apopu_i=[[_i[0] for _i in sorted(enumerate(agents[i].GANM_A_grade_Cmax(decode_AsP_popu[i])),reverse=True,key=lambda x:x[1])] for i in range(len(decode_AsP_popu))]
	Apopu_ie=[a_p[:np_exchange] for a_p in Apopu_i]
	As_popu=[[AsP_popu[i][_i] for _i in Apopu_ie[i]] for i in range(len(Apopu_ie))]
	AsP_popu=[AsP_popu[i]+list(chain(*(As_popu[:i]+As_popu[i+1:]))) for i in range(len(AsP_popu))]
	return AsP_popu
if __name__=='__main__':
	Main('abz5','abz5_aj_instance2020_02_04_13_15_34_492996.json')