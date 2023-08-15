import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import os
import colorsys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

first_time = 1
relaunch = 0


def myRGBColor(iterations,exp,const,scale):
    color = iterations**exp
    rgb = colorsys.hsv_to_rgb(const+scale*color, 1-0.6*color,0.9)
    return tuple(round(i*255) for i in rgb)

def sandColor(distance):
    color = int(float(color_scale_entry.get())*20*(distance*255))
    rgb = colorsys.hsv_to_rgb(float(color_entry.get()),float(color_const_entry.get()),color)
    return (int(rgb[0]),int(rgb[1]),int(rgb[2]))

def mouse_event(event):
    x_pointer = min_x+event.xdata*(x_range/width)
    y_pointer =(max_y-event.ydata*(y_range/height))
    
    x_min_entry.delete(0,END)
    x_max_entry.delete(0,END)
    y_max_entry.delete(0,END)
    
    x_min_entry.insert(0,str(x_pointer-x_range/10))
    x_max_entry.insert(0,str(x_pointer+x_range/10))
    y_max_entry.insert(0,str(y_pointer+y_range/10))
    # print(x_pointer,y_pointer)
    draw_mandelbort()


def reset_params():
    x_min_entry.delete(0,END)
    x_max_entry.delete(0,END)
    y_max_entry.delete(0,END)
    width_entry.delete(0,END)
    color_entry.delete(0,END)
    color_const_entry.delete(0,END)
    color_scale_entry.delete(0,END)
    
    x_min_entry.insert(0,"-3.0")
    x_max_entry.insert(0,"2.0")
    y_max_entry.insert(0,"1.9")
    width_entry.insert(0, "600")
    color_entry.insert(END, "0.2")
    color_const_entry.insert(END, "0.27")
    color_scale_entry.insert(END, "1.0")


    draw_mandelbort()
    

fig, ax = plt.subplots()
fig.suptitle("Fractal Visualizer ")
plt.subplots_adjust(left = 0, right = 1)

def draw_mandelbort():
    global fig,ax,min_x,max_x,max_y,x_range,y_range,height,width,canvas,first_time,plot1,img,relaunch
    precision = int(precision_entry.get())
    width = int(width_entry.get())
    aspect_ratio = float(aspect_ratio_entry.get())
    height = int(width/aspect_ratio)

    min_x = float(x_min_entry.get())
    max_x = float(x_max_entry.get())
    max_y = float(y_max_entry.get())

    x_range = (max_x-min_x)
    y_range = x_range/aspect_ratio
    
    
    img = Image.new('RGB', (width,height),color = 'black')
    pixels = img.load()



    for col_no in range(width):
        for row_no in range(height):
            x = min_x+col_no*(x_range/width)
            y = -(max_y-row_no*(y_range/height))

            z0 = complex(0.0,0.0)
            c = complex(x,y)
            for i in range(precision):
                '''# Mandelbrot Set
                z0 = z0**2+c
                '''
                # Burning Ship Fractal 
                z_inside = complex(abs(z0.real),abs(z0.imag))
                z0 = (z_inside)**2+complex(x,y)
                

                '''# Multibrot set
                z0 = z0**15 + complex(x,y)
                '''
                
                if(abs(z0)>2.0):
                    distance = (i+1) / 501
                    if(cmode_value.get()=="RGB"):
                        rgb = myRGBColor(distance, float(color_entry.get()), float(color_const_entry.get()), float(color_scale_entry.get()))
                        pixels[col_no,row_no] = rgb
                    elif(cmode_value.get()=="HSV"):
                        sand = sandColor(distance)
                        pixels[col_no,row_no] = sand
                        
                    break
    ax.clear()
    ax.imshow(img)
    ax.set_axis_off()
    cid = fig.canvas.mpl_connect('button_press_event',mouse_event)
    
    if first_time == 1:
        first_time=0
        plt.ion()
        canvas = FigureCanvasTkAgg(fig,master=root)
        canvas.get_tk_widget().place(x=500,y=80)
        toolbar = NavigationToolbar2Tk(canvas,root)
        toolbar.update()

    else:
        pass
    



def open_photo():
    img.save('mb.png')
    os.system('mb.png')


    
root=Tk()
root.geometry('1500x880')
root.title("Fractal Visualizer : Sandeep Bhardwaj")

label = Label(root, text="Fractal Visualizer - By Sandeep Bhardwaj", bd="3", font=("Times New Roman",16))
label.place(x=10,y=10)

precision_label = Label(root, text="Precision ")
precision_label.place(x=10,y=100)

precision_entry = Entry(root)
precision_entry.insert(END, "20")
precision_entry.place(x=200,y=100)

width_label = Label(root, text="Width")
width_label.place(x=10,y=140)

width_entry = Entry(root)
width_entry.insert(END, "600")
width_entry.place(x=200,y=140)

ar_label = Label(root, text="Aspect-ratio(w/h) ")
ar_label.place(x=10,y=180)

aspect_ratio_entry = Entry(root)
aspect_ratio_entry.insert(END, "1.7777")
aspect_ratio_entry.place(x=200,y=180)

x_min_label = Label(root, text="Minimum X ")
x_min_label.place(x=10,y=220)

x_min_entry = Entry(root)
x_min_entry.insert(END, "-3.0")
x_min_entry.place(x=200,y=220)

x_max_label = Label(root, text="Maximum X ")
x_max_label.place(x=10,y=260)

x_max_entry = Entry(root)
x_max_entry.insert(END, "2.0")
x_max_entry.place(x=200,y=260)


y_max_label = Label(root, text="Maximum Y ")
y_max_label.place(x=10,y=300)

y_max_entry = Entry(root)
y_max_entry.insert(END, "1.9")
y_max_entry.place(x=200,y=300)

color_label = Label(root, text="Color Exponent/Hue")
color_label.place(x=10,y=340)

color_entry = Entry(root)
color_entry.insert(END, "0.2")
color_entry.place(x=200,y=340)

color_const_label = Label(root, text="Contrast/Saturation ")
color_const_label.place(x=10,y=380)

color_const_entry = Entry(root)
color_const_entry.insert(END, "0.27")
color_const_entry.place(x=200,y=380)

color_scale_label = Label(root, text="Color Scale ")
color_scale_label.place(x=10,y=420)

color_scale_entry = Entry(root)
color_scale_entry.insert(END, "1.0")
color_scale_entry.place(x=200,y=420)

color_mode_label = Label(root, text="Color Mode ")
color_mode_label.place(x=10,y=470)

cmode_value = StringVar()
options = ["RGB","HSV"]
cmode_value.set("RGB")

color_mode_dd = OptionMenu(root,cmode_value,*options)
color_mode_dd.place(x=200,y=470)

draw_button = Button(root, text=" Draw Fractal ", width = "20", height = "1", command=draw_mandelbort)
draw_button.place(x=20,y=550)


open_photo_button = Button(root, text=" Open Photo in App ", width = "20", height = "1", command=open_photo)
open_photo_button.place(x=270,y=550)

reset_params_button = Button(root, text=" Reset View  ", width = "20", height = "1", command=reset_params)
reset_params_button.place(x=20,y=630)

draw_mandelbort()

root.mainloop()
