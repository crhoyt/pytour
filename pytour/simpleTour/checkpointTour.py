import numpy as np
from ..utils import *

class CheckpointTour:

	def __init__(self, X, d, axes, stepsBetweenFrames, pause=0):

		self.X = X
		self.d = d
		self.axes = axes
		self.stepsBetweenFrames = stepsBetweenFrames

		self.numAxes = axes.shape[1]
		self.axesUsed = np.random.choice( range(self.numAxes), size=3, 
			replace=False)

		super().__init__(pause=pause)

	def nextFrame(self):

		# Perform a 1-off perturbation of the prior axes used:
		idxToReplace = np.random.randint(self.d)
		replacementValue = self.axesUsed[ idxToReplace ]
		while replacementValue in self.axesUsed:
			replacementValue = np.random.randint(self.numAxes)
		self.axesUsed[ idxToReplace ] = replacementValue

		# Calculate the frame that embeds all the used axes:
		newFrame = self.axes[:, self.axesUsed]
		newFrame, _ = qr(newFrame)

		

		numSteps = self.stepsBetweenFrames

		return (newFrame, numSteps)