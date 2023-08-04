from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import numpy as np
import matplotlib.pyplot as plt


class NMRApp(App):

    def build(self):
        return MainLayout()


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.xvalues = np.linspace(0, 20, 1001)
        self.yvalues = 1 / (((self.xvalues - 5) ** 2) * 25 + 0.5)

        plt.figure(facecolor='#F1F6F9')
        plt.plot(self.xvalues, self.yvalues,
                 linewidth=1, color='#212A3E')
        plotXLabel = plt.xlabel('δ, ppm')
        plt.gca().invert_xaxis()
        plt.yticks([])  # delete y axis ticks
        plt.tight_layout()  # reduce graph margins

        ax = plt.gca()
        axisColor = '#a0a0a0'
        labelColor = '#0f0f0f'
        ax.spines['bottom'].set_color(axisColor)
        ax.spines['top'].set_color(axisColor)
        ax.spines['right'].set_color(axisColor)
        ax.spines['left'].set_color(axisColor)
        plotXLabel.set_color(labelColor)
        plt.tick_params(axis='x', colors=labelColor)

        graph = self.ids.graphLayout.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def on_open_button_released(self):
        print('open')


NMRApp().run()

'''
self.graphWidget = Graph(#xmin=float(np.max(xvalues)), xmax=float(np.min(xvalues)),
                         xmin=float(np.min(xvalues)), xmax=float(np.max(xvalues)),
                         ymin=float(np.min(yvalues)), ymax=float(np.max(yvalues)),
                         border_color=[0.75, 0.75, 0.75, 1],
                         x_grid_label=True,
                         x_ticks_major=2,
                         xlabel='ppm')
self.ids.graphLayout.add_widget(self.graphWidget)
self.plot = LinePlot(color=[0, 0, 0.6, 1], line_width=2)
self.plot.points = [(xvalues[i], yvalues[i]) for i in range(xvalues.size)]
self.graphWidget.add_plot(self.plot)
'''
