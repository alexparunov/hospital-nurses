#!/usr/bin/python3
import matplotlib.pyplot as plt


# 0, 0.1,....,1.0
grasp_alpha = [i/10 for i in range(0,11)]

# time in secs it took to find solution
grasp_time =      [481, 589, 608, 378, 181, 133, 141, 155, 183, 187, 175]
grasp_objective = [1379, 1640, 1726, 1492, 1467, 1631, 2107, 2268, 2714, 2675, 2759]


# Those values and results are coming from parameters.py file named as param0,param1,...param{index_of_array}
# ILP results
number_instances = [17, 18, 20, 30, 48, 66, 72, 80, 92, 110, 115, 138, 144, 168, 184, 207, 220]
ilp_objective =    [11, 18, 11, 21, 47, 62, 49, 55, 64, 76, 106, 96, 100, 145, 122, 131, 154]
ilp_time =         [0.72, 0.8, 2.57, 1.17, 5.72, 3.21, 23.89, 6.4, 6.82, 17.78, 4.58, 17.75, 16.34, 9.51, 57.83, 65.69, 52.08]


def plot_grasp_vs_alpha(grasp_alpha, grasp_time, grasp_objective):
	fig, ax = plt.subplots()
	ax.plot(grasp_alpha, grasp_objective,'r--', label="Objective Function Value")
	ax.plot(grasp_alpha, grasp_time, '.b-', label="Execution Time")
	plt.xlabel("alpha")

	legend = ax.legend(loc=0, shadow=True)
	frame = legend.get_frame()
	frame.set_facecolor('0.90')
	plt.show()

def main():
	plot_grasp_vs_alpha(grasp_alpha, grasp_time, grasp_objective)

if __name__ == "__main__":
	main()