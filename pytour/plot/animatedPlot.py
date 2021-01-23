import matplotlib.pyplot as plt
from matplotlib import animation

class AnimatedPlot:

    def __init__(self, tour, plot_kwargs={}, anim_kwargs={}):
        self.tour = tour

        
        # Setup the initial plot:
        proj = self.tour.currentProjection()
        self.fig = plt.figure( figsize=(8,6) )
        self.ax = self.fig.add_subplot(111)
        self.sc = self.ax.scatter(proj[:,0], proj[:,1], **plot_kwargs)

        
        # Create animation:
        self.animation = animation.FuncAnimation(
            self.fig, self.update, **anim_kwargs
        )
        
        
        # Create annotation utility:
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),
            textcoords="offset points", bbox=dict(fc="w"),
            arrowprops=dict(arrowstyle="->"))
        
        self.annot.set_visible(False)
        self.fig.canvas.mpl_connect('motion_notify_event', self.hover)

        
        # Create pause utility:
        self.paused = False
        self.fig.canvas.mpl_connect('button_press_event', self.pause)

        plt.show()

    def update(self, i):
        proj = self.tour.advance()
        self.sc.set_offsets(proj)
        return self.sc

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            cont, ind = self.sc.contains(event)
            if cont:
                pos = self.sc.get_offsets()[ind["ind"][0]]
                self.annot.xy = pos
                text = str( ind["ind"][0] )
                self.annot.set_text(text)
                self.annot.set_visible(True)
                self.fig.canvas.draw()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw()

    def pause(self, *args, **kwargs):
        if self.paused:
            self.animation.event_source.start()
        else:
            self.animation.event_source.stop()
        self.paused = not self.paused

    def currentFrame(self):
        return self.tour.currentFrame()