import numpy as np
from ..utils import *

class CheckpointTour:

	def __init__(self, X, d, axes, numSteps=0, rotSpeed=0, pause=0):


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
		self.d = d
		self.axes = axes

		self.numAxes = axes.shape[1]
		self.axesUsed = np.random.choice( range(self.numAxes), size=3, 
			replace=False)

		super().__init__(pause=pause)

	def nextFrame(self, lastFrame):

		# Perform a 1-off perturbation of the prior axes used:
		idxToReplace = np.random.randint(self.d)
		replacementValue = self.axesUsed[ idxToReplace ]
		while replacementValue in self.axesUsed:
			replacementValue = np.random.randint(self.numAxes)
		self.axesUsed[ idxToReplace ] = replacementValue

		# Calculate the frame that embeds all the used axes:
		newFrame = self.axes[:, self.axesUsed]
		newFrame, _ = qr(newFrame)

		

		if self.mode == "constTime":
			numSteps = self.numSteps
		elif self.mode == "constSpeed":
			numSteps = int(rotSpeed(lastFrame, newFrame) / self.rotSpeed)

		return (newFrame, numSteps)