import colour
from colour.plotting import *
from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import os

import logic

# config = logic.read_config()
config = logic.read_config('config.json')

window = Tk()
window.title('Colorimetry')
# window.geometry('350x200')

plot, _ = plot_chromaticity_diagram_CIE1931(standalone=False)
# annotations = []
# figure = None

canvas = FigureCanvasTkAgg(plot, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=TOP, anchor=N, fill='none', expand=False)

toolbar = NavigationToolbar2Tk(canvas, window)
toolbar.update()
toolbar.pack(side=TOP, anchor=N)
# canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=1)

frame = Frame(window)
label = Label(master=frame, text=config['filename'])
txt = Text(frame, width=30, height=3)

patch_name = 'neutral 5 (.70 D)'
patch_sd = colour.SDS_COLOURCHECKERS['ColorChecker N Ohta'][patch_name]

xy = [0.31259787, 0.32870029]
x, y = xy
# plt.plot(x, y, 'o-', color='white')

# Annotating the plot.
plt.annotate(patch_sd.name.title(),
             xy=xy,
             xytext=(-50, 30),
             textcoords='offset points',
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=-0.2'))

plt.title(config['diagram_name'])

def _get_data_file():
    file = filedialog.askopenfilename()
    if file is not None:
        curr_dir = os.getcwd()
        config['filename'] = file.replace(curr_dir, '')[1:]
        label.config(text=config['filename'])



def _run():
    # config['filename'] = 'data_corr.csv'
    x, y, z = logic.get_data(config)
    # sum_x = 0
    # for val in x.values():
    #     sum_x += val
    # sum_y = 0
    # for val in y.values():
    #     sum_y += val
    # sum_z = 0
    # for val in z.values():
    #     sum_z += val
    # print('****', sum_x, sum_y, sum_z, '****')
    x, sumx = logic.get_coordinates_manual(x)
    y, sumy = logic.get_coordinates_manual(y)
    z, sumz = logic.get_coordinates_manual(z)

    print('****', sumx, sumy, sumz, '****')
    print(x, y, z)
    # x=0.782, y=0.704451
    wh=[z[0]+0.245047*x[0]+0.0134472*y[0], z[1]+0.245047*x[1]+0.0134472*y[1]]
    fr=[0.292936*x[0]+0.155379*y[0]+0.551685*z[0], 0.292936*x[1]+0.155379*y[1]+0.551685*z[1]]
    test=[(z[0]/z[1] + 0.782*x[0]/x[1] + 0.704451*y[0]/y[1]) / (1/z[1] + 0.782 / x[1] + 0.704451 / y[1]),
        (1 + 0.782 + 0.704451) / (1/z[1] + 0.782/x[1] + 0.704451/y[1])]
    # test2 = [(z[0]/z[1] + 0.245047*x[0]/x[1] + 0.0134472*y[0]/y[1]) / (1/z[1] + 0.245047 / x[1] + 0.0134472 / y[1]),
    #     (1 + 0.245047 + 0.0134472) / (1/z[1] + 0.245047/x[1] + 0.0134472/y[1])]
    print('true:', xy)
    print('blu1:', wh)
    print('form:', fr)
    print('test:', test)
    ########

    # xy = [0.31259787, 0.32870029]
    # x_ch = [x[0] - z[0], x[1] - z[1]]
    # y_ch = [y[0] - z[0], y[1] - z[1]]
    
    # print('****', x_ch, y_ch, '****')

    ########

    txt.config(state=NORMAL)
    txt.delete('1.0', END)
    txt.insert('1.0', f'{x[0]} {x[1]}\n{y[0]} {y[1]}\n{z[0]} {z[1]}')
    txt.config(state=DISABLED)
    x_numbers = [i[0] for i in [x, y, z, x]]
    y_numbers = [i[1] for i in [x, y, z, x]]


    plt.plot(x_numbers, y_numbers, color='black', linewidth=1.0)
    # plt.annotate('Red', x)
    # plt.annotate('Green', y)
    # plt.annotate('Blue', z)

    plt.draw()


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
# data_file_button.pack(side=TOP, anchor=NW)
data_file_button.grid(column=1, row=1, sticky=W+E)

# label.pack(side=TOP, anchor=N)
label.grid(column=2, row=1)

txt.grid(column=3, row=1, rowspan=2, sticky=W+E)
txt.config(state=DISABLED)

run_button = Button(master=frame, text='RUN', command=_run)
run_button.grid(column=2, row=2, sticky=W+E)

# table_file_button = Button(master=window, text="Select table file...", command=_get_table_file)
# table_file_button.grid(column=0, row=2)

mainloop()