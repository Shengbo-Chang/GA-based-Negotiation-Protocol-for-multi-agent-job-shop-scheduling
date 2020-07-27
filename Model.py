#from itertools import zip
# import numpy as np
#模型：创建实例，读取实例，方案解码
# agent_types信息包含在agent jobs文件中，当agent_types==2时设置交期，读取时解析
####agent_types 编码表#################
#0：最大完工时间
#1：总（加权）完成时间(生成加权)
#2：总（加权）滞后时间（生成交期）
#3：满意度设计
######################################
from random import randint
from random import sample
from random import uniform
def loadinstance(file_name):
	# lines=[[int(j) for j in i if j.isdigit()==True] for i in lines] ##处理为数字列表
	f=open('instance/'+file_name) ##读取文件
	lines=f.readlines()
	#lines=[[int(j) for j in i.strip('\n').split(' ')] for i in lines if i[0]!='#' and len(i)>15]
	##将字符串转换为列表，并过滤掉开头的规模数，如10,10fin
	lines=[[int(j) for j in i.strip('\n').split(' ')] for i in lines if i[0]!='#']
	##包含规模数
	num_j=lines[0][0]
	num_m=lines[0][1]
	OT=[list(zip(*([iter(line)]*2))) for line in lines[1:]]
	##折叠为文档中的表形式 zip(*)解压
	#OT=[(机器，时间)]如下形式
	return num_j,num_m,OT
def agent_jobs(num_a,num_j,d_a=0):   #d_a=[1,2,3]按指定列表分配给agent
	jobs=list(range(num_j))
	a_jobs=[[] for i in range(num_a)]
	if d_a==0:
		#完全随机,不能保证agent不为空
		for j in range(num_j):
			a_i=randint(0,num_a-1)
			a_jobs[a_i].append(j)
	else:
		##d_a=[1,2,3]为agent被指定工件的数目
		for a_i in range(num_a):
			a_jobs[a_i]=random.sample(jobs,d_a[a_i])
			jobs=[i for i in d_a if i not in a_jobs[a_i]]
	return a_jobs ##a_jobs=[[],[]]
def agent_types(num_a,a_jobs,OT,type_given=[],total_types=4):
	if type_given==[]:
		a_types=[randint(0,total_types-1) for i in range(num_a)]
	else:
		a_types=type_given
	ad_types=[[t,duedate_gene(i,a_jobs[i],OT)] if t==2 else [t,weight_gene(i,a_jobs[i],OT)] \
	if t==1 else [t,Satifunc_gene(i,a_jobs[i],OT)] if t==3 else [t] for i,t in enumerate(a_types)]
	return ad_types # ad_types=[[type],[type=2,{duedates}],[type=1,{weight}]...]
def Satifunc_gene(i,a_job,OT):
	## d0<d1<d2<d3 #####
	# intvaget=random.sample(range(sum([t[1] for t in OT[j]]),2*sum([t[1] for t in OT[j]])),4).sort()
	# Satis={j:sample(range(sum([t[1] for t in OT[j]]),2*sum([t[1] for t in OT[j]])),4).sort() for j in a_job}
	Satis={}
	for j in a_job:
		Satis[j]=sample(range(sum([t[1] for t in OT[j]]),2*sum([t[1] for t in OT[j]])),4)
	return Satis
def duedate_gene(i,a_job,OT):
	##产生方式松紧均有######
	# print(a_job)
	# st=sum([t[1] for t in OT[j]])
	# due_dates={j:randint(sum([t[1] for t in OT[j]]),2*sum([t[1] for t in OT[j]])) for j in a_job}
	due_dates={}
	for j in a_job:
		due_dates[j]=[randint(sum([t[1] for t in OT[j]]),2*sum([t[1] for t in OT[j]])),uniform(0.5,2)]
	return due_dates
def weight_gene(i,a_job,OT):
	weight_finish={}
	process_time={j:sum([t[1] for t in OT[j]]) for j in a_job}
	for j in a_job:
		weight_finish[j]=process_time[j]/min(process_time.values())+uniform(-1,1)
	return weight_finish
def shop_A_gene(num_m):
	# [0机器的启动能耗，0机器的关闭能耗，0机器的运行能耗，0机器的闲置能耗]
	s_a=[[uniform(8,10),uniform(4,6),uniform(1,3),uniform(5,8)] for i in range(num_m)]
	return s_a
def aj_instance(file_name,num_a,d_a=0,num_instance=1):
#产生代理-工件归属json文件：[工件....;工件....]
#文件夹aj_instance,按实例名分类
	import os
	import datetime
	import json
	num_j,num_m,OT=loadinstance(file_name)
	path='aj_instances/'+file_name
	for _i in range(num_instance):
		a_jobs=agent_jobs(num_a,num_j,d_a)
		a_types=agent_types(num_a,a_jobs,OT)
		#######################################
		shop_a=shop_A_gene(num_m)##一些能耗参数,[[0机器的启动能耗，0机器的关闭能耗，0机器的运行能耗，0机器的闲置能耗]，....]
		# aj_dic={i:a_jobs[i] for i in range(len(a_jobs))}
		if not os.path.exists(path):
			os.makedirs(path)
		curr_time=datetime.datetime.now()
		time_str=datetime.datetime.strftime(curr_time,'%Y_%m_%d_%H_%M_%S_%f')
		output=open(path+'/'+file_name+'_ajs_instance'+time_str+'.json','w')
		json.dump([a_jobs,a_types,shop_a],output)
		# for i in range(len(a_jobs)):
		# 	for j in range(len(a_jobs[i])):
		# 		output.write(str(a_jobs[i][j]))#write函数不能写int类型的参数，所以使用str()转化
		# 		output.write('\t')#相当于Tab一下，换一个单元格
		# 	output.write('\n')#写完一行立马换行
		output.close()
def read_aj_instance(aj_instance_name):
	import json
	floder_name=aj_instance_name.split('_',1)
	aj_file=open('aj_instances/'+floder_name[0]+'/'+aj_instance_name,'r')
	aj_list=json.load(aj_file)
	return aj_list
	#读取json文件实例
def decode(e,num_j,num_m,OT):
	import pdb
	O=[0]*num_j
	M=[0]*num_m
	R=[0]*num_j
	P=[[0 for i_1 in range(num_m)] for i_2 in range(num_j)]
	F=[[0 for i_1 in range(num_m)] for i_2 in range(num_j)]
	for i in range(len(e)):
		j=e[i]
		Mi=OT[j][O[j]][0]
		Ti=OT[j][O[j]][1]
		if M[Mi]>=R[j]: 
			P[j][O[j]]=M[Mi]
		else:
			P[j][O[j]]=R[j]
		F[j][O[j]]=P[j][O[j]]+Ti
		# pdb.set_trace()
		M[Mi]=F[j][O[j]]
		R[j]=F[j][O[j]]
		O[j]=O[j]+1
	return P,F
	#解码后形式F=[[t_m1,t_m2,...],[t_m1,t_m2,...],...]
class instance:
	#创建类，包含实例中所有的信息
	def __init__(self,id,file_name,aj_instance_name,ScoreType):
		self.id=id
		self.num_j,self.num_m,self.OT=loadinstance(file_name)
		self.aj_list=read_aj_instance(aj_instance_name)[0]
		self.aj_types=read_aj_instance(aj_instance_name)[1]
		if len(read_aj_instance(aj_instance_name))>2:
			self.shop_a=read_aj_instance(aj_instance_name)[2]
		else:
			self.shop_a=0
		self.ScoreType=ScoreType
if __name__=='__main__':
	aj_instance('abz5',3)