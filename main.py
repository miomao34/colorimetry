import colour
from colour.plotting import *
from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import os
import random
import numpy as np

import logic

config = logic.read_config('config.json')

window = Tk()
window.title('Colorimetry')

plot, ax = plot_chromaticity_diagram_CIE1931(standalone=False)

canvas = FigureCanvasTkAgg(plot, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=TOP, anchor=N, fill='none', expand=False)

toolbar = NavigationToolbar2Tk(canvas, window)
toolbar.update()
toolbar.pack(side=TOP, anchor=N)

frame = Frame(window)
label = Label(master=frame, text=config['filename'])
txt = Text(frame, width=34, height=3)

patch_name = 'neutral 5 (.70 D)'
patch_sd = colour.SDS_COLOURCHECKERS['ColorChecker N Ohta'][patch_name]

white = [0.31259787, 0.32870029]
x, y = white
# plt.plot(x, y, 'o-', color='white')

# Annotating the point of white.
plt.annotate('D65',
             xy=white,
             xytext=(30, 10),
             textcoords='offset points',
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=0.2'))

plt.title(config['diagram_name'])

def _get_data_file():
    file = filedialog.askopenfilename()
    if file is not None:
        curr_dir = os.getcwd()
        config['filename'] = file.replace(curr_dir, '')[1:]
        label.config(text=config['filename'])



def _run():
    x_data, y_data, z_data = logic.get_data(config)

    x, sumx = logic.get_coordinates_and_sum(x_data)
    y, sumy = logic.get_coordinates_and_sum(y_data)
    z, sumz = logic.get_coordinates_and_sum(z_data)

    # got coords
    print('x, y, z:', x, y, z)
    print('sums - x, y, z:', sumx, sumy, sumz)

    # calculatilg what coefficients we need to mix the input spectrums with to get white light
    # we go from:
    # x_mix = (k_1*m_1*x_1 + k_2*m_2*x_2 + k_3*m_3*x_3) / (k_1*m_1 + k_2*m_2 + k_3*m_3)
    # y_mix = (k_1*m_1*y_1 + k_2*m_2*y_2 + k_3*m_3*y_3) / (k_1*m_1 + k_2*m_2 + k_3*m_3)
    # to, assuming k_3 as 1:
    # k_1*m_1*(x_mix - x_1) + k_2*m_2*(x_mix - x_2) = 1*m_3*(x_3 - x_mix)
    # k_1*m_1*(y_mix - y_1) + k_2*m_2*(y_mix - y_2) = 1*m_3*(y_3 - y_mix)
    # this is a linear equation where we don't know k_1 and k_2
    
    target = [config['target_x'], config['target_y']]
    print('target:', target)

    coef_1_1 = sumx * (target[0] - x[0])
    coef_1_2 = sumy * (target[0] - y[0])
    coef_1_b = 1 * sumz * (z[0] - target[0])
    coef_2_1 = sumx * (target[1] - x[1])
    coef_2_2 = sumy * (target[1] - y[1])
    coef_2_b = 1 * sumz * (z[1] - target[1])

    a = np.array([[coef_1_1, coef_1_2], [coef_2_1, coef_2_2]])
    b = np.array([coef_1_b, coef_2_b])
    coefs = np.linalg.solve(a, b).tolist()

    print('mixing coefs, r and g:', coefs)

    final_spectrum = [coefs[0]*x_data[i] + coefs[1]*y_data[i] + z_data[i] for i in x_data.keys()]

    txt.config(state=NORMAL)
    txt.delete('1.0', END)
    txt.insert('1.0', f'{x[0]} {x[1]}\n{y[0]} {y[1]}\n{z[0]} {z[1]}')
    txt.config(state=DISABLED)
    x_numbers = [i[0] for i in [x, y, z, x]]
    y_numbers = [i[1] for i in [x, y, z, x]]

    ax.plot(x_numbers, y_numbers, color='black', linewidth=1.0)
    plt.draw()

    spt, spt_ax = plt.subplots()
    spt_ax.plot(x_data.keys(), final_spectrum)
    spt.show()

def _plot_point_window():
    plotter_window = Toplevel(window)
    Label(plotter_window, text='x [0-1]:').grid(column=1, row=1, sticky=W)
    Label(plotter_window, text='y [0-1]:').grid(column=2, row=1, sticky=W)
    x, y = Text(plotter_window, width=32, height=1), Text(plotter_window, width=32, height=1)
    x.grid(column=1, row=2, sticky=W+E)
    y.grid(column=2, row=2, sticky=W+E)
    plotter_button = Button(master=plotter_window, text="Plot", command=lambda: _plot_point(x, y, plotter_window))
    plotter_button.grid(column=2, row=3, sticky=W+E)
    plotter_window.mainloop()

def _plot_point(x, y, plotter_window):
    ax.plot(float(x.get("1.0",END)), float(y.get("1.0",END)), 'ro', color='black')
    plt.draw()
    plotter_window.quit()
    plotter_window.destroy()

def _quit():
    window.quit()
    window.destroy()


frame.pack(side=TOP, anchor=NW, fill=BOTH, expand=False)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)
frame.grid_columnconfigure(4, weight=0)

quit_button = Button(master=frame, text="Quit", command=_quit)
quit_button.grid(column=1, row=3, sticky=W)

data_file_button = Button(master=frame, text="Select data file...", command=_get_data_file)
data_file_button.grid(column=1, row=1, sticky=W+E)

label.grid(column=2, row=1)

txt.grid(column=3, row=1, rowspan=2, sticky=W+E)
txt.config(state=DISABLED)

run_button = Button(master=frame, text='RUN', command=_run)
run_button.grid(column=2, row=2, sticky=W+E)

plot_point_button = Button(master=frame, text='Plot point...', command=_plot_point_window)
plot_point_button.grid(column=1, row=2, sticky=W+E)

mainloop()