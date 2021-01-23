from .simpleTour import SimpleTour

class PresetTour(SimpleTour):

	def __init__(self, X, framesList, stepsBetweenFrames, pause=0):

		self.X = X
		self.framesList = framesList
		self.stepsBetweenFrames = stepsBetweenFrames
		self.index = 0

		super().__init__(pause=pause)

	def nextFrame(self):

		newFrame = self.framesList[self.index]
		numSteps = self.stepsBetweenFrames

		self.index += 1
		if self.index == len(self.framesList):
			self.index = 0

		return (newFrame, numSteps)

