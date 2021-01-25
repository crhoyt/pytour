import matplotlib.pyplot as plt
from matplotlib import animation

class AnimatedPlot:
    """ A plot utility that takes in a specified tour, and creates an
        interactive matplotlib.pyplot figure that explores the data.
    """

    def __init__(self, tour, plot_kwargs={}, anim_kwargs={}):
        """ Constructs the Animated Plot object.

            Inputs:
                tour - A tour object (PresetTour, CustomTour, ect)
                plot_kwargs - A dict specifying the arguments passed onto the
                    plotting utility.
                anim_kwargs - A dict specifying the arguments passed onto theh
                    animaiton utility.
        """

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
        """ Update the plot and tour by one timestep.

            Inputs:
                i - A positive integer representing the current time (unused)

            Output:
                A handle to the updated scatterplot.
        """
        proj = self.tour.advance()
        self.sc.set_offsets(proj)
        return self.sc

    def hover(self, event):
        """ Update the annotation given the specified event

            Inputs:
                event - a matplotlib.pyplot event specifying an action made by 
                    the user.

            Output:
                No output given, but the annotation is changed accordingly.
        """
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
        """ Pauses or unpauses the animation when called.

            Inputs:
                *args - positional arguments (unused)
                **kwargs - keyword arguments (unused)

            Output:
                No output given, but the animation is paused if it was playing,
                and plays if was paused.
        """
        if self.paused:
            self.animation.event_source.start()
        else:
            self.animation.event_source.stop()
        self.paused = not self.paused

    def currentFrame(self):
        """ Return the current frame of the tour.

            Inputs:
                None

            Outputs:
                A 2D numpy array of size (p,d) representing the current frame
                visualized in the tour.
        """
        return self.tour.currentFrame()