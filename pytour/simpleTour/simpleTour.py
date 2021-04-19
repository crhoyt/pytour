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
		self.pauseSteps = pause
		self.moveFlag = True

		self.Fz, self.moveSteps = self.nextFrame(None)
		self.checkFrame(self.Fz)
		self.createPathToNewFrame()

	def checkFrame(self, F, tol=1e-6):
		""" Checks to make sure that the frame is a legitimate orthogonal
			matrix. That is, F^T F should be the identity matrix.

			Inputs:
				F - An arbitrary (p,d) matrix
				tol - the error tolerance

			Outputs:
				If |F^T F|_2 < tol, we say that F is close enough to orthogonal
				and return nothing. Otherwise, we raise an error.
		"""

		d = F.shape[1]

		differences = F.T @ F - np.eye(d)
		error = np.linalg.norm(differences)

		if error < tol:
			return
		else:
			raise AssertionError('Provided frame for SimpleTour is not ' \
				'valid.')

	def createPathToNewFrame(self, checkFlag=True):
		""" Determines a new target frame, and determines the path used to 
			travel to it.

			Inputs:
				checkFlag - A boolean. If True, we check whether or not the
					next frame we travel to is orthogonal or not.
		"""

		# Cycle through the visited frames:
		self.Fa = self.Fz 
		self.Fz, self.moveSteps = self.nextFrame(self.Fa)
		self.t = 0

		# Check that the next frame we travel to is indeed orthogonal
		if checkFlag:
			self.checkFrame(self.Fz)

		# Determine the parameters of the walk we should take.
		self.B, self.thetas, self.Wa = interpolateFrames(self.Fa, self.Fz)
		self.XB = self.X @ self.B

	def currentProjection(self):
		""" Outputs the current projection of the tour.
		"""
		if self.moveFlag:
			tau = self.thetas * self.t / self.moveSteps
		else:
			tau = self.thetas

		return self.XB @ constructR(tau) @ self.Wa

	def currentFrame(self):
		""" Outputs the current frame of the tour.
		"""
		if self.moveFlag:
			tau = self.thetas * self.t / self.moveSteps
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
		
		# If we're moving to the next frame, ...
		if self.moveFlag:

			# ... we keep on moving towards the next frame.
			if self.t < self.moveSteps:
				self.t += 1

			# Once we reach the next frame, we either ...
			else:
				# ... move into pause mode or ...
				if self.pauseSteps > 0:
					self.t = 1
					# self.moveSteps = self.pauseSteps
					self.moveFlag = False
				# ... setup the path to the new frame.
				else:
					self.createPathToNewFrame()

		# If we're paused, ...
		else:

			# ... we wait until we've waited the time specified.
			if self.t < self.pauseSteps:
				self.t += 1

			# Afterwards, we plan our next path, and exit pause mode.
			else:
				self.createPathToNewFrame()
				self.moveFlag = True


		return self.currentProjection()





