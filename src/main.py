from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.lang import Builder

import numpy as np
import matplotlib.pyplot as plt

Builder.load_file('mainScreen.kv')
Builder.load_file('fileChooser.kv')

class NMRApp(App):

    def build(self):
        return MainLayout()


class MainLayout(BoxLayout):
    vert_line1 = plt.axvline(x=1, color='r')
    vert_line2 = plt.axvline(x=2, color='r')
    touch_down = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.xvalues = np.linspace(0, 20, 1001)
        self.yvalues = 1 / (((self.xvalues - 5) ** 2) * 25 + 0.5)

        self.plot_figure = plt.figure(facecolor='#F1F6F9')
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

        self.vert_line1 = plt.axvline(x=1, color='r')
        self.vert_line2 = plt.axvline(x=2, color='b')
        self.vert_line1.set_visible(False)
        self.vert_line2.set_visible(False)

        graph = self.ids.graphLayout.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        cid = self.plot_figure.canvas.mpl_connect('button_press_event', self.graph_touch_down)
        self.cidpress = self.plot_figure.canvas.mpl_connect('button_press_event', self.graph_touch_down)
        self.cidrelease = self.plot_figure.canvas.mpl_connect('button_release_event', self.graph_touch_up)
        self.cidmotion = self.plot_figure.canvas.mpl_connect('motion_notify_event', self.graph_touch_motion)
        
    def on_open_button_released(self):
        print('open')
        content = FileChooseLayout(open=self.process_file, cancel=self.dismiss_popup)
        self._popup = Popup(title="Open fid file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def on_save_button_released(self):
        print('save')

    def on_info_button_released(self):
        print('info')

    def on_zoom_in_button_pressed(self):
        print(self.ids.zoomInButton.state)

    def on_zoom_out_button_released(self):
        plt.gca().autoscale()
        self.plot_figure.canvas.draw()
        self.plot_figure.canvas.flush_events()

    def dismiss_popup(self):
        self._popup.dismiss()

    def process_file(self, filename):
        print(f'file {filename} is processed')
        self.dismiss_popup()

    def graph_touch_down(self, event):
        self.touch_down = True
        print('touch down', event)
        current_x = event.xdata
        if current_x:
            self.vert_line1.set_xdata(current_x)
            self.vert_line2.set_xdata(current_x)
            self.vert_line1.set_visible(True)
            self.vert_line2.set_visible(True)
            self.plot_figure.canvas.draw()
            self.plot_figure.canvas.flush_events()

    def graph_touch_up(self, event):
        self.touch_down = False
        print('touch up', event)
        self.vert_line1.set_visible(False)
        self.vert_line2.set_visible(False)
        new_borders = self.vert_line1.get_xdata()[0], self.vert_line2.get_xdata()[0]
        plt.gca().set_xlim(left=max(new_borders), right=min(new_borders))
        self.plot_figure.canvas.draw()
        self.plot_figure.canvas.flush_events()

    def graph_touch_motion(self, event):
        if self.touch_down:
            current_x = event.xdata
            if current_x:
                self.vert_line2.set_xdata(current_x)
                self.plot_figure.canvas.draw()
                self.plot_figure.canvas.flush_events()


class FileChooseLayout(BoxLayout):
    open = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('aaa')


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
