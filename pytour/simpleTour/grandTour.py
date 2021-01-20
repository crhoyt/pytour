import numpy as np
from ..utils import *

class GrandTour:

	def __init__(self, X, d, stepsBetweenFrames):

		self.X = X
		self.p = X.shape[1]
		self.stepsBetweenFrames = stepsBetweenFrames

		super().__init__()

	def nextFrame(self):

		newFrame = np.random.normal( size=(p,d) )
		newFrame, _ = np.linalg.qr(newFrame)
		numSteps = self.stepsBetweenFrames

		return (newFrame, numSteps)