import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
def excel_scater(file_name,aj_filename,excel_name):
	exn='data_save/'+file_name+'/'+aj_filename+'/'+excel_name
	df=pd.read_excel(exn)
	a0_c=np.array(df.ix[:,0])
	a1_c=np.array(df.ix[:,1])
	a2_c=np.array(df.ix[:,2])
	# print(a0_c)
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter(a0_c,a1_c,a2_c)
	plt.savefig(f'{exn[-6:-5]}.jpg')
	plt.show()
def last_gene_scater(file_name,aj_filename,process_name):
	import json
	process_file='data_save/'+file_name+'/'+aj_filename+'/GANM_process/'+process_name
	r_max=len(Gene_popu)
	last_genes=Gene_popu
	# columns_n=list(range(len(last_genes[0][0])))
	# out_excel=pd.DataFrame(count_gene,columns_n)
	# path='data_save/'+file_name+'/'+aj_filename+'/'+process_name[0:-5]
	# out_excel.to_excel(path+'/'+f'GANM_statistic_gen{n_g}_round{r_max}'+'.xlsx',index=False)
print(2)
excel_scater('abz5','abz5_aj_instance2020_06_23_14_15_45_518179.json','r_10000_c_1002020_06_29_22_15_54_215131/0.xlsx')