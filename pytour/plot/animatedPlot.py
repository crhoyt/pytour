import matplotlib.pyplot as plt
from matplotlib import animation




class AnimatedPlot:

    
    def __init__(self, tour, plot_kwargs={}, anim_kwargs={}):
        self.tour = tour

        proj = self.tour.currentProjection()

        fig = plt.figure( figsize=(8,6) )
        ax = fig.add_subplot(111)
        points = ax.scatter(proj[:,0], proj[:,1], **plot_kwargs)

        self.animation = animation.FuncAnimation(
            fig, self.update, fargs=(points, self.tour),
            **anim_kwargs
        )

        self.paused = False
        fig.canvas.mpl_connect('button_press_event', self.pause)

        plt.show()

    def update(self, i, points, tour):
        proj = tour.advance()
        points.set_offsets(proj)
        return points
        
    def pause(self, *args, **kwargs):
        if self.paused:
            self.animation.event_source.start()
        else:
            self.animation.event_source.stop()
        self.paused = not self.paused

    def currentFrame(self):
        return self.tour.currentFrame()