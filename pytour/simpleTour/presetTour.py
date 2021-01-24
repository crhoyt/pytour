from .simpleTour import SimpleTour
from ..utils import *

class PresetTour(SimpleTour):

	def __init__(self, X, framesList, numSteps=0, rotSpeed=0, pause=0):

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
		self.framesList = framesList
		self.index = -1

		super().__init__(pause=pause)

	def nextFrame(self, lastFrame):

		self.index += 1
		if self.index == len(self.framesList):
			self.index = 0

		newFrame = self.framesList[self.index]

		if self.mode == "constTime":
			numSteps = self.numSteps
		elif self.mode == "constSpeed":
			numSteps = int(rotSpeed(lastFrame, newFrame) / self.rotSpeed)

		return (newFrame, numSteps)

