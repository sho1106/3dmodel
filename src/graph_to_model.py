# -*- coding: shift_jis -*-

import model_manager
import numpy as np

np.random.seed(0)

def make_random_point(num):

	points = np.random.rand(num*3).reshape(num, 3)

	return points

def make_graph(points, th):
	pairs = []
	num = len(points)
	for pre in range(num):
		for nxt in range(pre+1, num):
			dist = np.linalg.norm(points[pre] - points[nxt])
			if dist<th:
				pairs.append([pre, nxt])
	return pairs




if __name__=="__main__":
	print("test")

	points = make_random_point(10)
	pairs = make_graph(points, 0.5)
	maker = model_manager.VRMLModelMaker()
	lines = model_manager.Lines(points.tolist(), pairs, [0, 1, 0])
	spheres = []

	for p in points:
		spheres.append(model_manager.Sphere(p.tolist(), 0.01, [1, 0, 0]))
	strs = maker.to_str_models([lines] + spheres)
	maker.dump("graph", strs)