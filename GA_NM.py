#[1,1,2,3,3,4,5]
import Agent
import Model
import random
from itertools import chain
from copy import copy
import numpy as np
import collections
import pdb
import Data_tracker
import save_process
def Main():
	##文件名以‘’字符串的形式输入
	#instance_id,file_name,aj_instance_name=  #################################
	# ScoreType:0-sum-total-score;1.1-sum-limited-score-10, 1.2-prod-limited-score-10; 
	# 2.1-pord-rank-to-Borda; 2.2-sum-rank-to-Borda==prod-rank-to-lexca; 2.3-prod-rank-to-kAp; 2.4-sum-rank-to-kAp
	file_name='abz5'
	aj_instance_name='abz5_aj_instance2020_06_23_14_15_45_518179.json'
	save_c=1
	ScoreType=0
	instance_0=Model.instance(1,file_name,aj_instance_name,ScoreType)
	agents=[]
	for i in range(len(instance_0.aj_list)):
		agents.append(Agent.Agent(i,instance_0))
	### 加入 Jobshop Agent #########################
	if instance_0.shop_a!=0:
		agents.append(Agent.Shop_agent(i+1,instance_0))
	################### GANM 1 ##########################################################
	print('start')
	##需要再Agent中进行设置#####
	asa_round=agents[0].saRound
	num_propose=100
	num_child=0
	r_max=10000
	agent_propose=1.1 # 1.1--SA, 1.2--SA, 1.3--GA,  1.4--Random
	B_block=[agent_propose,0,0,0] # [agent_propose=1.1(GApropose)/1.2(Random),jobshop_filter]
	P_choice,Tracker_Gene_popu=GANM(agents,num_propose,num_child,r_max,ScoreType,B_block)
	save_process.save_GANM(file_name,num_child,r_max,aj_instance_name,Tracker_Gene_popu,B_block,asa_round)
	# if save_c==1:
	# 	save_process.save_GANM(file_name,num_child,r_max,aj_instance_name,Tracker_Gene_popu)
	# else:
	# 	Tracker_num_nd,Tracker_choice,Tracker_maxSocial=Traker_get_GANM(agents,Tracker_Gene_popu[0:-1],ScoreType)
	# 	Data_tracker.GANM_best_main_1(agents,ScoreType,genes_popu,num_child,r_max,aj_instance_name,process_name,Tracker_num_nd,Tracker_choice,Tracker_maxSocial)
		# Data_tracker.statistic_gene(file_name,aj_instance_name,r_max,Tracker_Gene_popu,100)
	####################################################################################
	################### GANM 2 ##########################################################
	##### 重大问题 提案数要保证与num——parent一致，即每轮的
	# num_parent=100
	# num_child=600
	# P_choice,Tracker_Gene_popu=GANM2(agents,num_propose,num_parent,num_child,r_max)
	# Data_tracker.GANM2_best_main(agents,Tracker_Gene_popu,file_name,aj_instance_name,num_propose,num_parent,num_child,r_max)
	#####################################################################################
	print(P_choice)
def GANM(agents,num_propose,num_child,r_max,ScoreType,B_block):
	r=0
	P_popu=GANM_initial(agents,num_propose)
	#测试函数中断点###############################################
	# pdb.set_trace()##############################################
	Tracker_ps_popu=[P_popu]
	# Tracker_num_nd=[len(P_popu)]
	# Tracker_choice=[GANM_grade(agents,P_popu,ScoreType)[0]]
	# Tracker_maxSocial=[GANM_grade(agents,P_popu,ScoreType)[1]]
	while r<r_max:
		r=r+1
		C_popu=GANM_child(P_popu,num_child)
		if int(B_block[0])==1:
		 	C_popu=C_popu+GANM_Ap_child(agents,P_popu,num_propose,B_block[0])
		All_popu=C_popu+P_popu
		As_irank=GANM_ranks(All_popu,agents)
		ND_rank=GANM_NDget(As_irank)
		P_popu=[All_popu[p] for p in ND_rank]
		###########tracker start#############
		Tracker_ps_popu.append(P_popu)
		# Tracker_num_nd.append(len(P_popu))
		# Tracker_choice.append(GANM_grade(agents,P_popu,ScoreType)[0])
		# Tracker_maxSocial.append(GANM_grade(agents,P_popu,ScoreType)[1])
		###########tracker end#############
		if len(P_popu)<2:
			print('total_dominate exist')
			break
		print(r)
	p_Max_grades=GANM_grade(agents,P_popu,ScoreType)[0]
	Tracker_ps_popu.append([P_popu[p_Max_grades]])
	# Tracker_num_nd.append(1)
	# Tracker_choice.append(0)
	# Tracker_maxSocial.append(GANM_grade(agents,P_popu,ScoreType)[1])
	return P_popu[p_Max_grades],Tracker_ps_popu
def Traker_get_GANM(agents,Tracker_Gene_popu,ScoreType):
	Tracker_num_nd=[]
	Tracker_choice=[]
	Tracker_maxSocial=[]
	for i,P_popu in enumerate(Tracker_Gene_popu):
		Tracker_num_nd.append(len(P_popu))
		Tracker_choice.append(GANM_grade(agents,P_popu,ScoreType)[0])
		Tracker_maxSocial.append(GANM_grade(agents,P_popu,ScoreType)[1])
		print(i)
	return Tracker_num_nd,Tracker_choice,Tracker_maxSocial
def GANM2(agents,num_propose=100,num_parent=100,num_child=600,r_max=1000):
	P_popu=random.sample(GANM_initial(agents,num_propose),num_parent)
	P_scores=GANM2_score(P_popu,agents)
	Tracker_ps_popu=[P_popu]
	for r in range(r_max):
		C_popu=GANM2_child(P_popu,num_child,P_scores)
		# C_popu=GANM_child(P_popu,num_child)
		All_popu=P_popu+C_popu
		popu_scores=GANM2_score(All_popu,agents)
		iP_popu=GANM2_chose_tournament(popu_scores,num_parent,20)
		# pdb.set_trace()
		P_popu=[All_popu[i] for i in iP_popu]
		P_scores=[popu_scores[i] for i in iP_popu]
		Tracker_ps_popu.append(P_popu)
		print(r)
	ip_Max_score=np.argmax(popu_scores)
	print(popu_scores[ip_Max_score])
	##保存最佳结果#########################
	Tracker_ps_popu.append([P_popu[ip_Max_score] for _i in range(num_parent)])
	return All_popu[ip_Max_score],Tracker_ps_popu
def GANM2_child(P_popu,num_child,P_scores,prob_mute=0.3):##锦标赛选择法选择
	ps_child=[]
	while len(ps_child)<num_child:
		ip_selec=GANM2_chose_tournament(P_scores,2,20)
		p1=P_popu[ip_selec[0]]
		p2=P_popu[ip_selec[1]]
		c1,c2=GANM_cross(p1,p2)
		m=[random.random(),random.random()]
		if m[0]<prob_mute:
			c1=GANM_mute(c1)
		if m[1]<prob_mute:
			c2=GANM_mute(c2)
		ps_child.append(c1)
		ps_child.append(c2)
	return ps_child
def GANM2_chose_elite(popu_scores,num_parent):##采用精英保留方法#####
	i_ps=[i[0] for i in sorted(enumerate(popu_scores),reverse=True,key=lambda x:x[1])]
	i_ps=i_ps[0:num_parent]
	return i_ps
def GANM2_chose_tournament(popu_scores,num_parent,num_toura):#锦标赛
	i_ps=[]
	popu_scores_0=list(enumerate(popu_scores))
	#popu_scores_1=copy(popu_scores)
	for i in range(num_parent):
		tournament_ps=random.sample(popu_scores_0,num_toura)
		v_k=max(tournament_ps,key=lambda x:x[1])
		popu_scores_0.remove(v_k)
		i_ps.append(v_k[0])
	#[i_ps[i]=popu_scores.index(max(random.sample(popu_scores,num_toura))) for i in range(num_toura)]
	return i_ps
def GANM2_score(All_popu,agents):
	decode_ps=[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in All_popu]
	score_as=[agents[i].GANM_A_grade(decode_ps) for i in range(len(agents))]################GANM2_A_score_Cmax
	score_as=np.array(score_as)
	return score_as.sum(0).tolist()
def GANM_initial(agents,num_propose):
	Proposals=[]
	for i in range(len(agents)):
		Proposals=Proposals+agents[i].GANM_A_propose(num_propose)
	return Proposals
def GANM_Ap_child(agents,P_popu,num_propose,s_mode):
	Proposals=[]
	if s_mode==1.1:
		for i in range(len(agents)):
			Proposals=Proposals+agents[i].GANM_SA_propose(num_propose,P_popu)
	if s_mode==1.4:
		Proposals=GANM_initial(agents,num_propose)
	return Proposals
def GANM_child(P_popu,num_child,prob_mute=0.4):
	child_popu=[]
	while len(child_popu)<num_child:
		ch_cross=random.sample(list(range(len(P_popu))),2)
		p1_cross=P_popu[ch_cross[0]]
		p2_cross=P_popu[ch_cross[1]]
		c1,c2=GANM_cross(p1_cross,p2_cross)
		m=[random.random(),random.random()]
		if m[0]<prob_mute:
			c1=GANM_mute(c1)
		if m[1]<prob_mute:
			c2=GANM_mute(c2)
		child_popu.append(c1)
		child_popu.append(c2)
	return child_popu
def GANM_ranks(all_popu,agents):
	##先解码#####
	decode_ps=[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in all_popu]
	#####测试解码后的方案程序##############
	# pdb.set_trace()
	#####################################
	rank_as=[agent.GANM_A_rank(decode_ps) for agent in agents] ##得到的为对方案序号的排序，
	#需要转换为对应方案的排序号,由于GANM_NDget要求
	irank_as=[[i[0] for i in sorted(enumerate(rank_a),key=lambda x:x[1])] for rank_a in rank_as]
	##转换为对应方案的排序号
	return irank_as
def GANM_NDget(iranks):
	iranks=np.array(iranks)
	ips_nd=[]
	for i in range(iranks.shape[1]):
		#逐列判断，即按方案来判断
		irjm=iranks[:,i]-iranks.T
		# print(irjm)
		#此操作后列转行
		#一个方案不被支配，则做差，除了自身那列外其他每列存在小于0
		j_l=np.array([(irjm[_i]<0).any() for _i in range(irjm.shape[0]) if _i != i])
		if j_l.all():
			ips_nd.append(i)
	return ips_nd
def GANM_grade(agents,P_popu,ScoreType):##返回评分最大的下标
	##先解码#####
	decode_ps=[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in P_popu]
	############
	score_as=[agents[i].GANM_A_grade(decode_ps) for i in range(len(agents))]
	score_as=np.array(score_as)
	################################
	######额外的部分#################
	# print(score_as)
	# print(score_as.sum(0))
	# i_smax=np.argmax(score_as.sum(0))
	if ScoreType==0 or ScoreType==1.1 or ScoreType==2.2 or ScoreType==2.4:
		i_smax=np.argmax(score_as.sum(0))
		best_value=score_as.sum(0)[i_smax]
	if ScoreType==1.2 or ScoreType==2.1 or ScoreType==2.3:
		i_smax=np.argmax(score_as.prod(0))
		best_value=score_as.prod(0)[i_smax]
	return i_smax,best_value
# def GANM_Social_best(agents,P_popu):
# 	decode_ps=[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in P_popu]
# 	Cmax_best_as=min([sum([agents[i].Score_caculate(decode_p) for i in range(len(agents))]) for decode_p in decode_ps])
# 	return Cmax_best_as
def GANM_cross(p1,p2):
	###将agent的实例存放到列表中####
	start_end=random.sample(list(range(len(p1))),2)
	start=min(start_end)
	end=max(start_end)
	p1=copy(p1)
	p2=copy(p2)
	e1=p1[start:end+1]
	e2=p2[start:end+1]
	p1[start:end+1]=e2
	p2[start:end+1]=e1
	dic_e1=collections.Counter(e1)
	dic_e2=collections.Counter(e2)
	dif_P1=[[k]*(dic_e2[k]-dic_e1[k]) for k in dic_e2 if k not in dic_e1 or dic_e2[k]>dic_e1[k]] ##e2中比比e1中多的部分
	##即P1需要调整的部分
	dif_P2=[[k]*(dic_e1[k]-dic_e2[k]) for k in dic_e1 if k not in dic_e2 or dic_e1[k]>dic_e2[k]]
	######检测冲突并调整#####
	dif_P1=list(chain(*dif_P1))
	dif_P2=list(chain(*dif_P2))
	random.shuffle(dif_P1)
	random.shuffle(dif_P2)
	while len(dif_P1)>0:
		P1v=dif_P1.pop(0)
		P2v=dif_P2.pop(0)
		IndexP1s=[i for i,v in enumerate(p1) if v==P1v and (i<start or i>end)]
		IndexP2s=[i for i,v in enumerate(p2) if v==P2v and (i<start or i>end)]
		P1p=random.choice(IndexP1s)
		P2p=random.choice(IndexP2s)
		p1[P1p]=P2v
		p2[P2p]=P1v
	return p1,p2
def GANM_mute(c_1o):
	c_1=copy(c_1o)
	# mute_p=random.sample(list(range(len(c_1))),2)
	num_j=max(c_1)+1
	job_pos=[[] for i in range(num_j)]
	# print(len(a))
	# print(num_j)
	for i,j in enumerate(c_1):
		job_pos[j].append(i)
	mute_j=random.sample(list(range(num_j)),2)
	mute_p=[random.choice(job_pos[mute_j[0]]),random.choice(job_pos[mute_j[1]])]
	c_1[mute_p[0]],c_1[mute_p[1]]=c_1[mute_p[1]],c_1[mute_p[0]]
	return c_1
if __name__=='__main__':
	Main()