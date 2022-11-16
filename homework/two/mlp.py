from tqdm import tqdm
import math
import numpy as np



identity  = lambda x: x
one       = lambda x: np.ones_like(x)
sigmoid   = lambda x: 1/(1 + np.exp(-x))
sig_deriv = lambda x: (y := sigmoid(x)) * (1 - y)
relu	  = lambda x: np.maximum(0, x)
heavyside = lambda x: (x > 0).astype(np.float64)
mse       = lambda y, t: 0.5 * (y - t)**2
diff      = lambda y, t: y - t



class Function:
	def __init__(self, activation, derivative):
		self.activation = activation
		self.derivative = derivative
	
	def __call__(self, *x):
		return self.activation(*x)



Identity = Function(identity, one)
ReLU	 = Function(relu, heavyside)
Sigmoid  = Function(sigmoid, sig_deriv)
MSE      = Function(mse, diff)



class Affine:
	def __init__(self, n_units:int, n_inputs:int=None, 
				 activation:Function=ReLU, lmd:float=1e-1):
		self.n_units = n_units
		self.activation = activation
		self.lmd = lmd
		self.Δ_b = 0
		self.Δ_W = 0
		if n_inputs is None:
			self.is_built = False
		else:
			self.build(n_inputs)


	def build(self, n_inputs:int):
		self.n_inputs = n_inputs
		limit = math.sqrt(6 / (self.n_inputs + self.n_units))
		self.W = np.random.uniform(-limit, limit, size=(self.n_inputs, self.n_units))
		self.b = np.zeros(shape=(1, self.n_units))
		self.is_built = True
	
	
	def __call__(self, x:np.ndarray, backward:bool=False):
		if not self.is_built:
			self.build(x.shape[1])
		if not backward:
			self.x = x.copy()
			self.z = np.einsum('ij,bi->bj', self.W, x) + self.b
			self.a = self.activation(self.z)
			return self.a
		else:
			Δ = x * self.activation.derivative(self.z)
			Δ_b = np.mean(Δ, axis=0)[None,...]
			Δ_W = np.einsum('bi,bj->bji', Δ, self.x)
			Δ_W = np.mean(np.einsum('bi,bj->bji', Δ, self.x), axis=0)
			self.Δ_W = (1 - self.lmd) * self.Δ_W + self.lmd * Δ_W
			self.Δ_b = (1 - self.lmd) * self.Δ_b + self.lmd * Δ_b
			return np.einsum('bj,ij->bi', Δ, self.W)



class MLP:
	def __init__(self, sizes, activations, loss:Function, lmd:float):
		self.sizes = sizes
		self.loss = loss
		self.layers = [Affine(i, j, a, lmd) for i, j, a in zip(sizes[1:], sizes[:-1], activations)]
	
	def __call__(self, x):
		for layer in self:
			x = layer(x)
		return x
	
	def __iter__(self):
		return iter(self.layers)
	
	def __getitem__(self, key):
		return self.layers[key]
	
	def train(self, x:np.ndarray, t:np.ndarray, eta:float, epochs:int, batchsize:int):
		N = x.shape[0]
		idx = np.arange(N)
		with tqdm(total=epochs) as bar:
			history = {'loss': [], 'grad': []}
			for epoch in range(epochs):
				grad = 0
				bar.set_description('Training')
				np.random.shuffle(idx)
				for batch, (x_batch, t_batch) in enumerate((x[idx[i*batchsize:(i+1)*batchsize],:], 
														    t[idx[i*batchsize:(i+1)*batchsize],:]) \
														  for i in range(N//batchsize)):
					y = self(x_batch)
					loss = self.loss(y, t_batch)
					history['loss'].append(np.mean(loss))
					Δ = self.loss.derivative(y, t_batch)# * self[-1].activation.derivative(self[-1].z)
					# BACKPROPAGATION
					for i, layer in enumerate(self.layers[::-1]):
						Δ = layer(Δ, backward=True)
						layer.W -= eta * layer.Δ_W
						layer.b -= eta * layer.Δ_b
						grad += np.sum(layer.Δ_W**2) + np.sum(layer.Δ_b**2)
					history['grad'].append(math.sqrt(grad))
					bar.set_postfix({'Loss': history['loss'][-1], 'Δ': history['grad'][-1]})
				bar.update(1)
		return history


if __name__ == '__main__':
	test = np.ones((2, 10))
