import numpy as np
from ..utils import *

class GrandTour:

	def __init__(self, X, d, numSteps=0, rotSpeed=0, pause=0):


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

		super().__init__(pause=pause)

	def nextFrame(self, lastFrame):

		newFrame = np.random.normal( size=(p,d) )
		newFrame, _ = np.linalg.qr(newFrame)
		
		numSteps = self.stepsBetweenFrames

		if self.mode == "constTime":
			numSteps = self.numSteps
		elif self.mode == "constSpeed":
			numSteps = int(rotSpeed(lastFrame, newFrame) / self.rotSpeed)

		return (newFrame, numSteps)