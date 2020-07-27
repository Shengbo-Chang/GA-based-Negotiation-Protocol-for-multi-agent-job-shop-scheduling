from Model import decode
from random import randint
import random
import numpy as np
import pdb
import copy
# 代理提案目前仅按照提案数目进行模拟退火优化
# 考虑采用2*提案数目进行模拟退火搜索优化，选择提案数目解进行提交
# 产生一定的优化
class Agent:
	def __init__(self,id,_instance):
		self.id=id
		self.num_j=_instance.num_j
		self.num_m=_instance.num_m
		self.OT=_instance.OT
		try:
			self.jobs=_instance.aj_list[self.id]
			self.type=_instance.aj_types[self.id]
		except:
			self.type=10
			self.jobs=0
		self.ScoreType=_instance.ScoreType
		self.saMode=0 ##0-随机选，-1-选最差的，1-选最好的
		self.saRound=20 ##模拟退火进行的轮次
	def SF_caculate(self,F):
		##返回每个机器上的开始和结束时间##########
		e_info=self.type[1] #[[0机器的启动能耗，0机器的关闭能耗，0机器的运行能耗，0机器的闲置能耗]，....]
		sf_machines=[[[0,0] for j in range(self.num_j)] for i in range(self.num_m)]
		# OT=self.OT
		for j in range(self.num_j):
			for i in range(self.num_m):
				sf_machines[self.OT[j][i][0]][j][1]=F[j][i]
				sf_machines[self.OT[j][i][0]][j][0]=F[j][i]-self.OT[j][i][1]
		sf_machines=[sorted(sf,key=lambda x:x[0]) for sf in sf_machines]
		return sf_machines
	def Enegy_caculate(self,F):
		##华南理工大学硕士毕业论文中同等能耗计算方法
		e_info=np.array(self.type[1])
		f_machine=[0]*self.num_m
		p_machine=[0]*self.num_m
		for j in range(self.num_j):
			for i in range(self.num_m):
				m=self.OT[j][i][0]
				p_machine[m]=p_machine[m]+self.OT[j][i][1]
				if f_machine[m]<F[j][i]:
					f_machine[m]=F[j][i]
		Idle_machine=np.array(f_machine)-np.array(p_machine)
		en_cost=sum(np.array(p_machine)*e_info[:,2]+Idle_machine*e_info[:,3]+e_info[:,0]+e_info[:,1])
		return en_cost
	def Cmax_caculate(self,F): #代理计算cmax指标
		Fa=[F[i] for i in self.jobs] #取出agent的job的行
		Cmax=max(max(row) for row in Fa)
		return Cmax
	def Tardiness_caculate(self,F):
		Ta=sum([(max(F[i])-self.type[1][str(i)][0])*self.type[1][str(i)][1] if max(F[i])>self.type[1][str(i)][0] else 0 for i in self.jobs])
		return Ta
	def Finishweight_caculate(self,F):
		Fwa=sum([max(F[i])*self.type[1][str(i)] for i in self.jobs])
		return Fwa
	def Satify_caculate(self,F):
		Sa=[0 if max(F[i])<=self.type[1][str(i)][0] else (max(F[i])-self.type[1][str(i)][0])/(self.type[1][str(i)][1]-self.type[1][str(i)][0])\
		 if max(F[i])<=self.type[1][str(i)][0] else 1 if max(F[i])<self.type[1][str(i)][2] else (self.type[1][str(i)][3]-max(F[i]))/(self.type[1][str(i)][3]-self.type[1][str(i)][2])\
		  if max(F[i])<self.type[1][str(i)][3] else 0 for i in self.jobs]
		return Sa
	def value_caculate(self,F):
		if self.type[0]==0:
			value=self.Cmax_caculate(F)
		if self.type[0]==2:
			value=self.Tardiness_caculate(F)
		if self.type[0]==1:
			value=self.Finishweight_caculate(F)
		if self.type[0]==3:
			value=self.Satify_caculate(F)
		if self.type[0]==10:
			value=self.Enegy_caculate(F)
		return value
	def GANM_A_rank(self,decode_ps):#输入解码后方案
		if self.type[0]==0:
			ps_Cmax=[self.Cmax_caculate(decode_p) for decode_p in decode_ps]
			irank_ps=[i[0] for i in sorted(enumerate(ps_Cmax),key=lambda x:x[1])]
		if self.type[0]==1:
			ps_Ft=[self.Finishweight_caculate(decode_p) for decode_p in decode_ps]
			irank_ps=[i[0] for i in sorted(enumerate(ps_Ft),key=lambda x:x[1])]
		if self.type[0]==2:
			ps_Ta=[self.Tardiness_caculate(decode_p) for decode_p in decode_ps]
			irank_ps=[i[0] for i in sorted(enumerate(ps_Ta),key=lambda x:x[1])]
		if self.type[0]==3:
			ps_Sa=[self.Satify_caculate(decode_p) for decode_p in decode_ps]
			irank_ps=[i[0] for i in sorted(enumerate(ps_Sa),key=lambda x:x[1],reverse=True)]
		if self.type[0]==10:
			ps_Ec=[self.Enegy_caculate(decode_p) for decode_p in decode_ps]
			irank_ps=[i[0] for i in sorted(enumerate(ps_Ec),key=lambda x:x[1])]
		##enumerate得到（index,value)
		return irank_ps
	def GANM_A_valueTorank(self,Cha_ps):
		if self.type[0]==0:
			irank_ps=[i[0] for i in sorted(enumerate(Cha_ps),key=lambda x:x[1])]
		if self.type[0]==1:
			irank_ps=[i[0] for i in sorted(enumerate(Cha_ps),key=lambda x:x[1])]
		if self.type[0]==2:
			irank_ps=[i[0] for i in sorted(enumerate(Cha_ps),key=lambda x:x[1])]
		if self.type[0]==3:
			irank_ps=[i[0] for i in sorted(enumerate(Cha_ps),key=lambda x:x[1],reverse=True)]
		if self.type[0]==10:
			irank_ps=[i[0] for i in sorted(enumerate(Cha_ps),key=lambda x:x[1])]
		##enumerate得到（index,value)
		return irank_ps
	def GANM_A_valueToscore(self,Cha_ps,total_score=1000,ag_minmax=[]):
		if int(self.ScoreType)==0:
			if self.type[0]==3:
				to_score=Cha_ps-min(Cha_ps)
				to_sum=sum(to_score)
				score_a=total_score*to_score/to_sum
			else:
				to_score=max(Cha_ps)-Cha_ps
				to_sum=sum(to_score)
				score_a=total_score*to_score/to_sum
		if int(self.ScoreType)==1:
			if self.type[0]==3:
				if max(Cha_ps)==min(Cha_ps):
					score_a=10*Cha_ps
				else:
					score_a=10*(Cha_ps-min(Cha_ps))/(max(Cha_ps)-min(Cha_ps))
			else:
				score_a=10*(max(Cha_ps)-Cha_ps)/(max(Cha_ps)-min(Cha_ps))
		if int(self.ScoreType)==2:
			irank_ps=self.GANM_A_valueTorank(Cha_ps)
			irank_ps=[i[0] for i in sorted(enumerate(irank_ps),key=lambda x:x[1])]
				## [排序i的方案号]转换为[i方案的排序号]
			if self.ScoreType==2.1 or self.ScoreType==2.2:
				score_a=len(irank_ps)+1-np.array(irank_ps)
			if self.ScoreType==2.3 or self.ScoreType==2.4:
				score_a=np.int64(np.array(irank_ps)>len(irank_ps)/2)
		if int(self.ScoreType)==3:
			score_a=Cha_ps
		if int(self.ScoreType)==4:
			score_a=(ag_minmax[1]-Cha_ps)/(ag_minmax[1]-ag_minmax[0])
		return score_a.tolist()
	def GANM_A_grade(self,decode_ps,total_score=1000):#输入解码后方案，输出对方案的评分列表
		if self.type[0]==0:
			Cha_ps=np.array([self.Cmax_caculate(decode_ps[i]) for i in range(len(decode_ps))])
		if self.type[0]==1:
			Cha_ps=np.array([self.Finishweight_caculate(decode_ps[i]) for i in range(len(decode_ps))])	
		if self.type[0]==2:
			Cha_ps=np.array([self.Tardiness_caculate(decode_ps[i]) for i in range(len(decode_ps))])
		if self.type[0]==3:
			Cha_ps=np.array([self.Satify_caculate(decode_ps[i]) for i in range(len(decode_ps))])
		if self.type[0]==10:
			Cha_ps=np.array([self.Enegy_caculate(decode_ps[i]) for i in range(len(decode_ps))])
		######评分方法2  最大差值 ######################################
		if int(self.ScoreType)==0:
			if self.type[0]==3:
				to_score=Cha_ps-min(Cha_ps)
				to_sum=sum(to_score)
				score_a=total_score*to_score/to_sum
			else:
				to_score=max(Cha_ps)-Cha_ps
				to_sum=sum(to_score)
				score_a=total_score*to_score/to_sum
		if int(self.ScoreType)==1:
			if self.type[0]==3:
				if max(Cha_ps)==min(Cha_ps):
					score_a=10*Cha_ps
				else:
					score_a=10*(Cha_ps-min(Cha_ps))/(max(Cha_ps)-min(Cha_ps))
			else:
				score_a=10*(max(Cha_ps)-Cha_ps)/(max(Cha_ps)-min(Cha_ps))
		if int(self.ScoreType)==2:
			irank_ps=self.GANM_A_valueTorank(Cha_ps)
			irank_ps=[i[0] for i in sorted(enumerate(irank_ps),key=lambda x:x[1])]
				## [排序i的方案号]转换为[i方案的排序号]
			if self.ScoreType==2.1 or self.ScoreType==2.2:
				score_a=len(irank_ps)+1-np.array(irank_ps)
			if self.ScoreType==2.3 or self.ScoreType==2.4:
				score_a=np.int64(np.array(irank_ps)>len(irank_ps)/2)
		if int(self.ScoreType)==3:
			score_a=Cha_ps
		#####评分方法1#######################################
		# to_score=sum(Cmax_ps)/Cmax_ps
		# to_sum=sum(to_score)
		# ##按什么来分配分值更合理，值得探讨,暂时采用的分配方式为，score=sum(Cmax)/Cmax_i
		# score_a=[total_score*to_score[i]/to_sum for i in range(len(Cmax_ps))]
		####################################################
		####################################################
		#####评分方法3 满意度加权法######################
		# to_score=1-(Cmax_ps-min(Cmax_ps))/(max(Cmax_ps)-min(Cmax_ps))
		# to_sum=sum(to_score)
		# score_a=total_score*to_score/to_sum
		return score_a.tolist()
	def GANM_A_propose(self,num_propose,num_multi=3):
		Proposals=[]
		decode_ps=[]
		num_search=num_propose*num_multi
		for i in range(num_search):
			p=self.GANM_A_random_search()
			St_p,Ft_p=decode(p,self.num_m,self.num_j,self.OT)
			decode_ps.append(Ft_p)
			Proposals.append(p)
		ranks=self.GANM_A_rank(decode_ps)
		# ps_choice=ranks[0:num_propose]
		Proposals=[Proposals[i] for i in ranks[0:num_propose]]
		return Proposals
	def GANM_GA_propose(self,num_propose,P_popu):
		pass
	def GANM_SA_propose(self,num_propose,P_popu):
		# 选择个体策略：
		if num_propose>len(P_popu):
			num_propose=len(P_popu)
		num_search=2*num_propose
		l_ppopu=len(P_popu)
		# if num_search>l_ppopu:
		# 	sample_is=[random.randint(0,l_ppopu) for i in range(num_search)]
		# else:
		# 	sample_is=self.SA_sample(P_popu,num_search)
		sample_is=self.SA_sample(P_popu,num_propose)
		C_ps=[]
		# 终止条件：达到轮次，连续多轮没有优化
		r_max=self.saRound
		for i in sample_is:
			r=0
			Active_p=P_popu[i]
			decode_Ac_p=decode(Active_p,self.num_m,self.num_j,self.OT)[1]
			beta_q=0.7
			Active_p_value=self.value_caculate(decode_Ac_p)
			T=Active_p_value
			##增加预选择模块###
			while r<r_max:
				# print('Agent SA',r)
				r=r+1
				s_p=Agent.A_mute(Active_p)
				decode_s_p=decode(s_p,self.num_m,self.num_j,self.OT)[1]
				s_p_value=self.value_caculate(decode_s_p)
				if self.type[0]==3:
					print('type3 is active NOT Right')
					if s_p_value<Active_p_value:
						Active_p=s_p
					elif random.uniform(0,1)<2.7182818**((s_p_value-Active_p_value)/T):
						Active_p=s_p
				else:
					if s_p_value>Active_p_value:
						Active_p=s_p
					elif random.uniform(0,1)<2.7182818**((Active_p_value-s_p_value)/T):
						Active_p=s_p
				T=T*beta_q
			C_ps.append(Active_p)
		return C_ps
	def SA_sample(self,P_popu,num_propose):
		### 0-随机选择 ## 1-选最好的 ## -1-选最差的
		if self.saMode==0:
			ps_SA=random.sample(list(range(len(P_popu))),num_propose)
		else:
			irank_ps=self.GANM_A_valueTorank(P_popu)
			irank_ps=[i[0] for i in sorted(enumerate(irank_ps),key=lambda x:x[1])]
			if self.saMode==1:
				ps_SA=irank_ps[0:num_propose]
			elif self.saMode==-1:
				ps_SA=irank_ps[-num_propose:]
		return ps_SA
	def A_mute(o_p):
		c_1=copy.copy(o_p)
		num_j=max(c_1)+1
		job_pos=[[] for i in range(num_j)]
		for i,j in enumerate(c_1):
			job_pos[j].append(i)
		mute_j=random.sample(list(range(num_j)),2)
		mute_p=[random.choice(job_pos[mute_j[0]]),random.choice(job_pos[mute_j[1]])]
		c_1[mute_p[0]],c_1[mute_p[1]]=c_1[mute_p[1]],c_1[mute_p[0]]
		return c_1
	def GANM_A_random_search(self):
		p=[]
		Os=[i for i in range(self.num_j)]*self.num_m
		while len(Os)>0:
			l=len(Os)-1
			a=randint(0,l)
			p.append(Os.pop(a))
		return p
	def SANM_A_vote(self,decode_popu,quota):
		iquota=round(quota)
		iranks_popu=self.GANM_A_rank(decode_popu)
		return iranks_popu[0:quota]
	def GANM2_score_Cmax(self,decode_ps,total_score=100):
		Cmax_ps=np.array([self.Cmax_caculate(decode_ps[i]) for i in range(len(decode_ps))])
		to_score=max(Cmax_ps)-Cmax_ps
		to_sum=sum(to_score)
		score_a=[total_score*to_score/to_sum]
class Shop_agent(Agent):
	def __init__(self,id,_instance):
		super().__init__(id,_instance)
		self.id=id
		self.jobs=list(range(_instance.num_j))
		self.type=[10,_instance.shop_a]