import numpy as np
from ..utils import *

class SimpleTour:
	""" A class for enacting simple tours, where a simple tour is simply a tour
		that moves from frame to frame using the frame interpolation algorithm
		specified in utils. 
	"""


	def __init__(self):
		""" Constructs a SimpleTour object given a generator function that
			specifies the next frame to travel to and the number of steps to
			take. Should not be called explicitly.
		"""

		if not hasattr(self, 'nextFrame'):
			raise RuntimeError('SimpleTour instance has no specified '\
				'nextFrame method.')
		if not hasattr(self, 'X'):
			raise RuntimeError('SimpleTour instance has no specified '\
				'X property.')

		self.Fz, self.numSteps = self.nextFrame()
		self.checkFrame(self.Fz)
		self.createPathToNewFrame()

	def checkFrame(self, F, tol=1e-6):
		""" Checks to make sure that the frame is a legitimate orthogonal
			matrix. That is, F^T F should be the identity matrix.

			Inputs:
				F - An arbitrary (p,d) matrix

			Outputs:
				If F^T F is close to identity, nothing. Otherwise, an error is
				raised.
		"""

		d = F.shape[1]

		differences = F.T @ F - np.eye(d)
		error = np.linalg.norm(differences)

		if error < tol:
			return
		else:
			raise AssertionError('Provided frame for SimpleTour is not ' \
				'valid.')

	def createPathToNewFrame(self):
		""" Determines a new target frame, and determines the path used to 
			travel to it.
		"""
		self.Fa = self.Fz 
		self.Fz, self.numSteps = self.nextFrame()
		self.t = 0

		self.checkFrame(self.Fz)

		self.B, self.thetas, self.Wa = interpolateFrames(self.Fa, self.Fz)
		self.XB = self.X @ self.B

	def currentProjection(self):
		""" Outputs the current projection of the tour.
		"""
		tau = self.thetas * self.t / self.numSteps
		return self.XB @ constructR(tau) @ self.Wa

	def advance(self):
		""" Advances the tour one step towards the current target frame. If the
			current projection has reached the target frame, a target frame and
			path are created.

			Outputs:
				A 2D numpy array representing the current projection after a
				single step.
		"""
		self.t += 1
		if self.t == self.numSteps:
			self.createPathToNewFrame()
		return self.currentProjection()





