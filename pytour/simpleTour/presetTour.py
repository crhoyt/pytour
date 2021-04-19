from .simpleTour import SimpleTour
from ..utils import *

class PresetTour(SimpleTour):
	""" A class for enacting preset (or planned) tours, where the tour simply
		travels from frame to frame in a pre-determined list of frames. Once the
		last frame of the list is reached, the tour travels back to the start
		and repeats once again.
	"""

	def __init__(self, X, framesList, numSteps=0, rotSpeed=0, pause=0):
		""" Constructs a PresetTour object.

			Inputs:
				X - A 2D numpy array of shape (n,p) representing the data to be 
					visualized
				framesList - A list of 2D numpy arrays of shape (p,d) 
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
				A PresetTour object
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
			self.moveSteps = numSteps
			self.rotSpeed = None 

		else:
			self.mode = "constSpeed"
			self.moveSteps = None
			self.rotSpeed = rotSpeed

		self.X = X
		self.framesList = framesList
		self.stepsBetweenFrames = numSteps
		self.index = 1

		# Calculate the tuples B, thetas, Wa used in each path:
		self.numFrames = len(framesList)
		self.listOfPaths = []
		self.listOfXB = []
		for frameIndex in range(self.numFrames):
			sourceFrame = framesList[ frameIndex-1 ]
			targetFrame = framesList[ frameIndex   ]

			path = interpolateFrames(sourceFrame, targetFrame)
			self.listOfPaths += [path]

			XB = self.X @ path[0]
			self.listOfXB += [XB]

		# Setup pausing option if we want to wait on certain frames.
		self.pause = pause
		self.moveFlag = True

		self.createPathToNewFrame()


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

		return None

	def createPathToNewFrame(self):
		""" Determines a new target frame, and determines the path used to 
			travel to it.
		"""

		self.t = 0

		self.index += 1
		if self.index == self.numFrames:
			self.index = 0
		self.B, self.thetas, self.Wa = self.listOfPaths[self.index]
		self.XB = self.listOfXB[self.index]

		self.moveSteps = self.stepsBetweenFrames
		