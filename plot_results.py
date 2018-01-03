#!/usr/bin/python3

# 0, 0.1,....,1.0
grasp_alpha = [i/10 for i in range(0,11)]

# time in secs it took to find solution
grasp_time =      [481, 589, 608, 378, 181, 133, 141, 155, 183, 187, 175]
grasp_objective = [1379, 1640, 1726, 1492, 1467, 1631, 2107, 2268, 2714, 2675, 2759]

def plot_grasp_vs_alpha(grasp_alpha, grasp_time, grasp_objective):
	pass

def main():
	plot_grasp_vs_alpha(grasp_alpha, grasp_time, grasp_objective)

if __name__ == "__main__":
	main()