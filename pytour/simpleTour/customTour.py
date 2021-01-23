import numpy as np
from ..utils import *

class CheckpointTour:

	def __init__(self, X, generator, pause=0):
		self.X = X
		super().__init__(pause=pause)

	def nextFrame(self):

		return generator()