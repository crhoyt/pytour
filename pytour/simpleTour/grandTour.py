import numpy as np
from ..utils import *
from .simpleTour import SimpleTour

class GrandTour(SimpleTour):
	""" A class for enacting grand tours, where the tour always selects a random
		frame to travel to.
	"""

	def __init__(self, X, d, numSteps=0, rotSpeed=0, pause=0):
		""" Constructs a GrandTour object.

			Inputs:
				X - A 2D numpy array of shape (n,p) representing the data to be 
					visualized
				d - A positive int representing the dimension of the projections
					representing the frames that the tour will travel to
				numSteps - A positive int representing the number of steps that
					should be taken between two frames. If rotSpeed is zero, 
					this parameter should be ignored.
				rotSpeed - A positive float representing how fast the rotations
					should be from frame to frame. If numSteps is zero, this
					parameter should be ignored.
				pause - A non-negative int representing how many timesteps to
					pause for whenever a new frame is reached. Zero by default.

			Outputs:
				A GrandTour object
		"""


		# Check if exactly one of stepsBetweenFrames or rotSpeed
		# is nonzero.
		constTime  = (numSteps!= 0)
		constSpeed = (rotSpeed!= 0)

		if constTime and constSpeed:
			raise ValueError('PresetTour input should have exactly one of '/
				'numSteps or rotSpeed be nonzero.')
		elif not constTime and not constSpeed:
			raise ValueError('PresetTour input should have exactly one of '/
				'numSteps or rotSpeed be nonzero.')

		elif constTime:
			self.mode = "constTime"
			self.numSteps = numSteps
			self.rotSpeed = None 

		else:
			self.mode = "constSpeed"
			self.numSteps = None
			self.rotSpeed = rotSpeed


		self.X = X
		self.p = X.shape[1]
		self.d = d
		# self.stepsBetweenFrames = stepsBetweenFrames

		super().__init__(pause=pause)


	def nextFrame(self, lastFrame):
		""" A method that gives the next frame and the number of steps that
			should be taken to get there.

			Input:
				lastFrame - A 2D numpy array of size (p,d) representing the
					last frame traveled to in the path

			Output:
				newFrame - A 2D numpy array of size (p,d) representing the next
					target frame in the path
				numSteps - A positive int representing the number of steps that
					should be taken between the last frame and the given next
					frame

		"""

		# Generate a random orthogonal matrix to use as the next frame.
		newFrame = np.random.normal( size=(self.p,self.d) )
		newFrame, _ = np.linalg.qr(newFrame)
		

		# If we are moving with constant time, we just use the specified number
		# of steps.
		if self.mode == "constTime":
			numSteps = self.numSteps

		# If we are moving with constant speed, we calculate the path speed with
		# no changes, and then scale up the number of steps so that we're
		# constant.
		elif self.mode == "constSpeed":
			if lastFrame == None:
				numSteps = 0
			else:
				B, thetas, Wa = interpolateFrames(lastFrame, newFrame)
				numSteps = int(pathSpeed(B, thetas, Wa) / self.rotSpeed)


		return (newFrame, numSteps)