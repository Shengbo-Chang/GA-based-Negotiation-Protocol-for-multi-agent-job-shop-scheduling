# p_a=[[[[0000,...,0009],...,[0090,...,0099]],...,[]],...,[[9900,...,9909],...,[9990,...,9999]]]
# 采用4维方式更好理解,缩小规模,但是无法体现不同机器之间的差别
# 以上错误
# 采用二维矩阵表达 p_a=[](nj^2*nj^2)
import numpy as np
def main(num_j,num_m):
	initial_mat=np.zeros((num_j*num_j*num_m,num_j*num_j*num_m))
def weight_update():
	pass