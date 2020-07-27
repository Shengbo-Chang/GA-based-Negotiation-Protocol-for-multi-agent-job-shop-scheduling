from random import randint
from random import sample
from model import loadinstance
#产生instance，每个代理对应一定数量的工件
def agent_jobs(num_a,num_j,d_a=0):
	jobs=list(range(num_j))
	a_jobs=[[] for i in range(num_a)]
	if d_a==0:
		#完全随机,不能保证agent不为空
		for j in range(num_j):
			a_i=randint(0,num_a)
			a_jobs[a_i].append(j)
	else:
		#按照d_a=[an1,an2,...]产生
		for a_i in range(num_a):
			a_jobs[a_i]=random.sample(d_a[a_i])
			d_a=[i for i in d_a if i not in a_jobs[a_i]]
	return a_jobs
def 