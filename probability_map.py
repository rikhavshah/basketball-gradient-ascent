import numpy as np

court_shape_0_min = -50
court_shape_0_max = 50
court_shape_1_min = -6
court_shape_1_max = 90

class Processor:
	# data.shape == (n,3)
	# data[i] = [x-coord of shot i, y-coord of shot i, outcome of shot i]
	def __init__(self, data, negligble_distance = 7):

		assert data.shape[1] == 3, 'data is incorrectly formatted. Should be (n,3) numpy array'

		self.data = data;

		self.negligble_distance = negligble_distance;
		self.decay_parameter = -negligble_distance*negligble_distance/np.log(0.01);

		self.bucketed_points = None;
		self.extended_bucketed_points = None;
		self.meshes = {};
		# self.mesh = None;

	#decay of two points that are of distance negligble_distance apart should be 0.01.
	def _decay(p1,p2):
		return np.exp(-(p1-p2).dot(p1-p2)/self.decay_parameter);
	
	#buckets should be of size negligble_distance
	def buckets():
		if self.bucketed_points is not None:
			return self.bucketed_points;
		
		print('Constructing buckets of points');

		self.bucketed_points = {}
		for i in range(court_shape_0_min//self.negligble_distance,court_shape_0_max//self.negligble_distance):
			for j in range(court_shape_1_min//self.negligble_distance,court_shape_1_max//self.negligble_distance):
				self.bucketed_points((i,j)) = set();

		for i in range(data.shape[0]):
			label = _point_to_bucket_label(data[i,:2]);
			self.bucketed_points[tuple(label)].add(data[i]);

		return self.bucketed_points;

	def extended_buckets():
		if self.extended_bucketed_points is not None:
			return self.extended_bucketed_points;


		self.buckets();
		self.extended_bucketed_points = {};
		print('constructing extended buckets')

		for label in self.bucketed_points:
			cc_bucket = self.bucketed_points[tuple(label)];
			ll_bucket = self.bucketed_points[(label[0]-1,label[1]  )];
			lu_bucket = self.bucketed_points[(label[0]-1,label[1]-1)];
			uu_bucket = self.bucketed_points[(label[0]  ,label[1]-1)];
			ur_bucket = self.bucketed_points[(label[0]+1,label[1]-1)];
			rr_bucket = self.bucketed_points[(label[0]+1,label[1]  )];
			rd_bucket = self.bucketed_points[(label[0]+1,label[1]+1)];
			dd_bucket = self.bucketed_points[(label[0]  ,label[1]+1)];
			dl_bucket = self.bucketed_points[(label[0]-1,label[1]+1)];

			self.extended_bucketed_points[tuple(label)] = cc_bucket.union(ll_bucket).union(lu_bucket).union(uu_bucket).union(ur_bucket).union(rr_bucket).union(rd_bucket).union(dd_bucket).union(dl_bucket)

	def probability_at_point(point):
		self.extended_buckets();

		if point is None:
			return

		total_successes = 0
		total_weight = 0
		for datum in self.extended_bucketed_points:
			weight = self._decay(point,datum[:2])
			total_successes += datum[2]*weight
			total_weight += weight

		return total_successes/total_weight;

	#default is 1 foot mesh
	def probability_mesh(delta=1):
		probability_at_point(None);
		# if self.mesh is not None:
		# 	return self.mesh
		if delta in self.meshes:
			return self.meshes[delta]

		mesh = {};
		for i in range(court_shape_0_min,court_shape_0_max):
			for j in range(court_shape_1_min,court_shape_1_max):
				mesh[(i,j)] = probability_at_point(np.array([i,j]));

		self.meshes[delta] = mesh;
		return mesh;

	def _point_to_bucket_label(point):
		return point//self.negligble_distance;
