import numpy as np
from ..utils import *
from .simpleTour import SimpleTour

class CustomTour(SimpleTour):
	""" A class for enacting custom simple tours. We travel from frame to frame
		in a certain number of steps where the next frame and number of steps
		are specifed by a generator function.
	"""

	def __init__(self, X, generator, pause=0):
		""" Constructs a CheckpointTour object.

			Inputs:
				X - A 2D numpy array of shape (n,p) representing the data to be 
					visualized

				generator - A python function that takes in 2D numpy arrays of
					size (p,d) representing the souce frame as input, and
					returns the tuple (newFrame, numSteps) where newFrame is an
					2D numpy array of size (p,d) representing the next frame to
					travel to and numSteps is the number of steps that should
					be taken to get there.


				pause - A non-negative int representing how many timesteps to
					pause for whenever a new frame is reached. Zero by default.

			Outputs:
				A CheckpointTour object
		"""

		self.X = X
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

		return generator()