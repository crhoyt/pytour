import numpy as np
from ..utils import *

class SimpleTour:
	""" A class for enacting simple tours, where a simple tour is simply a tour
		that moves from frame to frame using the frame interpolation algorithm
		specified in utils. 
	"""


	def __init__(self, pause=0):
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

		# Setup pausing option if we want to wait on certain frames.
		self.pause = pause
		self.moveFlag = True

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
		if self.moveFlag:
			tau = self.thetas * self.t / self.numSteps
		else:
			tau = 1
		return self.XB @ constructR(tau) @ self.Wa

	def currentFrame(self):
		""" Outputs the current frame of the tour.
		"""
		if self.moveFlag:
			tau = self.thetas * self.t / self.numSteps
		else:
			tau = 1
		return self.B @ constructR(tau) @ self.Wa


	def advance(self):
		""" Advances the tour one step towards the current target frame. If the
			current projection has reached the target frame, a target frame and
			path are created.

			Outputs:
				A 2D numpy array representing the current projection after a
				single step.
		"""

		if self.moveFlag:
			if self.t < self.numSteps:
				self.t += 1

			else:
				if self.pause > 0:
					self.t = 1
					self.numSteps = self.pause
					self.moveFlag = False
				else:
					self.createPathToNewFrame()
		else:
			if self.t < self.numSteps:
				self.t += 1
			else:
				self.createPathToNewFrame()
				self.moveFlag = True

			pass


		return self.currentProjection()





