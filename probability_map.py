import numpy as np

court_shape_0_min = -25
court_shape_0_max = 25
court_shape_1_min = -6
court_shape_1_max = 90

class Processor:
	# data.shape == (n,3)
	# data[i] = [x-coord of shot i, y-coord of shot i, outcome of shot i]
	def __init__(self, data, negligble_distance = 7):

		assert data.shape[1] == 3, 'data is incorrectly formatted. Should be (n,3) numpy array'

		self.negligble_distance = negligble_distance;
		self.decay_parameter = -negligble_distance*negligble_distance/np.log(0.01);

		self.data = data;
		print(self._point_to_bucket_label(data[:,:2].min(axis=0)))
		print(self._point_to_bucket_label(data[:,:2].max(axis=0)))
		print(data[:,:2].min(axis=0))
		print(data[:,:2].max(axis=0))

		self.bucketed_points = None;
		self.extended_bucketed_points = None;
		self.meshes = {};
		# self.mesh = None;

	#decay of two points that are of distance negligble_distance apart should be 0.01.
	def _decay(self,p1,p2):
		return np.exp(-(p1-p2).dot(p1-p2)/self.decay_parameter);
	
	#buckets should be of size negligble_distance
	def buckets(self,):
		if self.bucketed_points is not None:
			return self.bucketed_points;
		
		print('Constructing buckets of points');

		self.bucketed_points = {}
		print(court_shape_0_min//self.negligble_distance,court_shape_0_max//self.negligble_distance)
		print(court_shape_1_min//self.negligble_distance,court_shape_1_max//self.negligble_distance)
		# quit()
		for i in range(court_shape_0_min//self.negligble_distance-1,2+court_shape_0_max//self.negligble_distance):
			for j in range(court_shape_1_min//self.negligble_distance-1,2+court_shape_1_max//self.negligble_distance):
				# print(i,j)
				self.bucketed_points[(i,j)] = set();

		for i in range(self.data.shape[0]):
			label = self._point_to_bucket_label(self.data[i,:2]);
			self.bucketed_points[tuple(label)].add(tuple(self.data[i]));

		print('done')
		return self.bucketed_points;

	def extended_buckets(self,):
		if self.extended_bucketed_points is not None:
			return self.extended_bucketed_points;


		self.buckets();
		self.extended_bucketed_points = {};
		print('constructing extended buckets')

		for i in range(court_shape_0_min//self.negligble_distance,1+court_shape_0_max//self.negligble_distance):
			for j in range(court_shape_1_min//self.negligble_distance,1+court_shape_1_max//self.negligble_distance):
				cc_bucket = self.bucketed_points[(i,j)];
				ll_bucket = self.bucketed_points[(i-1,j  )];
				lu_bucket = self.bucketed_points[(i-1,j-1)];
				uu_bucket = self.bucketed_points[(i  ,j-1)];
				ur_bucket = self.bucketed_points[(i+1,j-1)];
				rr_bucket = self.bucketed_points[(i+1,j  )];
				rd_bucket = self.bucketed_points[(i+1,j+1)];
				dd_bucket = self.bucketed_points[(i  ,j+1)];
				dl_bucket = self.bucketed_points[(i-1,j+1)];

				self.extended_bucketed_points[(i,j)] = cc_bucket.union(ll_bucket).union(lu_bucket).union(uu_bucket).union(ur_bucket).union(rr_bucket).union(rd_bucket).union(dd_bucket).union(dl_bucket)

		print('done')
		return self.extended_bucketed_points;

	def probability_at_point(self,point):
		self.extended_buckets();

		if point is None:
			return

		total_successes = 0
		total_weight = 0

		label = self._point_to_bucket_label(point);

		for datum in self.extended_bucketed_points[tuple(label)]:
			weight = self._decay(point,datum[:2])
			total_successes += datum[2]*weight
			total_weight += weight

		return total_successes/total_weight;

	#default is 1 foot mesh
	def probability_mesh(self,delta=1):
		self.probability_at_point(None);

		# if self.mesh is not None:
		# 	return self.mesh
		if delta in self.meshes:
			return self.meshes[delta]

		print('making mesh')

		mesh = {};
		for i in range(court_shape_0_min,court_shape_0_max):
			print(i)
			for j in range(court_shape_1_min,court_shape_1_max):
				mesh[(i,j)] = self.probability_at_point(np.array([i,j]));

		self.meshes[delta] = mesh;
		print('done')
		return mesh;

	def _point_to_bucket_label(self,point):
		return point//self.negligble_distance;
