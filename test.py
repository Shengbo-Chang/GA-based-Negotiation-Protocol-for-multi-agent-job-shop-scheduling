# from Model import read_aj_instance
# import datetime
# l=read_aj_instance('abz5_aj_instance2020_02_04_13_15_34_492996.json')
# print(l)
# curr_time=datetime.datetime.now()
# time_str=datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
# print(time_str)
# def b():
# 	i=7
# 	print(i)
# def a():
# 	for i in range(5):
# 		b()
# 		print(i)
# a()
###测试a是否在能改
# class a:
# 	def __init__(self,id):
# 		self.id=id

# a_s=[0]
# a_s[0]=a(1)
# print(a_s[0])
# a_s[0].id=2
# print(a_s[0])
###################
# Os=[i for i in range(3)]*5
# Os[1]=9
# print(Os)
#####################变量在a中改了
# def a(p):
# 	return p
# def b():
# 	p=2
# 	a(1)
# 	print(p)
# print([a(i) for i in range(5)])
############################
#列表传进函数会不会改变
# def a():
# 	return 1,2
# print(a()[0])
# a=[1,2,3,4,5]
# for i in range(len(a)):
# 	a.pop(i)
# 	print(i)
# a=[[1,2,3,4,5],[7,8,9,10]]
# b=[[i+1 for i in j] for j in a]
# print(b)
#######################
# import numpy as np
# a=np.array([[1,2,3,4],[5,6,7,8]])
# print(a[:,1])
# for i in range(5):
# 	a=[i for i in range(4)]
# 	print(i)
# 	print(a)
######测试GANM_NDget函数,应输出[1,2,3]#########
# from GA_NM import GANM_NDget 
# ar=[[1,4,3,2,0],[2,3,1,0,4]]
# ar=[[i[0] for i in sorted(enumerate(rank_a),key=lambda x:x[1])] for rank_a in ar] ####先转换
# print(ar)
# n=GANM_NDget(ar)
# print(n)
##########################
#####测试GANM_cross函数######################
# from GA_NM import GANM_cross
# import random
# a=[1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]
# b=[1,1,2,2,3,3,4,4,1,1,2,2,3,3,4,4]
# random.shuffle(a)
# random.shuffle(b)
# c,d=GANM_cross(a,b)
# print(a,b)
# print(d,c)
#####测试GANM_mute函数#########################
# from GA_NM import GANM_mute
# a=[1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]
# d=GANM_mute(a)
# print(d)
###############################################################################1111111
#运行函数
import GA_NM
GA_NM.Main('abz5','abz5_aj_instance2020_02_04_13_15_34_492996.json')
# import SANM
# SANM.Main('abz5','abz5_aj_instance2020_02_04_13_15_34_492996.json')
#####测试 Model.decode函数#####################在GANM中设置断点
#输入如下代码##########################################
# Model.decode(P_popu[0],agents[0].num_j,agents[0].num_m,agents[0].OT)
#####测试 Agent.Cmax_caculate()函数#################
# agents[0].Cmax_caculate(Model.decode(P_popu[0],agents[0].num_j,agents[0].num_m,agents[0].OT)[1])
###################################################################
#测试 Agent.GANM_A_random_search()函数##################
# agents[0].GANM_A_random_search()
#测试 Agent.GANM_A_propose_Cmax(10)####################
# agents[0].GANM_A_propose_Cmax(10)
#测试 Agent GANM_A_grade_Cmax##############
# decode_ps=[Model.decode(p,agents[0].num_j,agents[0].num_m,agents[0].OT)[1] for p in P_popu]
# agents[0].GANM_A_grade_Cmax(decode_ps[0:2])
# agents[0].Cmax_caculate(decode_ps[0])
#测试 Agent GANM_A_rank_Cmax#########################
# agents[0].GANM_A_rank_Cmax(decode_ps[0:2])
#测试 GA_NM GANM_grade(agents,P_popu)#####################
# GANM_grade(agents,all_popu[0:5])
##################################################################################1111111
#SANM
###测试 SANM_common_d################
# import SANM
# # s=SANM.SANM_active_d([[1,2,3],[3,2,1],[4,2,1]])
# # print(s)
# ## 测试 SANM_mute
# # s=SANM.SANM_mute([1,2,3,4,5,6,7])
# # print(s)
# ## 测试 MAIN#####
# SANM.main('abz5','abz5_aj_instance2020_02_04_13_15_34_492996.json')