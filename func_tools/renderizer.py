import matplotlib.pyplot as plt
import numpy as np
import imageio
import time
import logging


# Initialize the logger

logger = logging.getLogger(__name__)
if not len(logger.handlers):
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s ')
    
    file_handler = logging.FileHandler('GIF_maker_log.log')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    logger.propagate = False
    
# Define the functions that will be used

# Same function as np.linspace but takes step as input instead of number of 
# elements
def linspace(start, stop, step=1.):
  """
    Like np.linspace but uses step instead of num
    This is inclusive to stop, so if start=1, stop=3, step=0.5
    Output is: array([1., 1.5, 2., 2.5, 3.])
  """
  return np.linspace(start, stop, int((stop - start) / step + 1))

def final_real_and_complex_coords(num_initial_lines,
                                  step_height_initial_lines,
                                  x_inf_lim_initial_lines,
                                  x_sup_lim_initial_lines,
                                  step_grid_inside_each_line,
                                  conf_mapping,
                                  upper_half_complex_plane=1):
    
    if upper_half_complex_plane:
        logger.info('Initial domain: upper-half complex plane')
        heights = []
        
        i = 0
        while len(heights) <= num_initial_lines:
            x = i*step_height_initial_lines
            heights.append(x)
            i += 1
            
        number_of_initial_lines = len(heights)
        X = linspace(x_inf_lim_initial_lines, x_sup_lim_initial_lines, step_grid_inside_each_line)
        steps_initial = len(X)
        
        heigth_complex_lines = heights
        
        for i in range(number_of_initial_lines+1):
            if i != 1:
                heigth_complex_lines.append(i)
                
                
        t = np.linspace(0, 1, number_of_initial_lines)
        
        
        initial_real = np.zeros([number_of_initial_lines, steps_initial])
        initial_complex = np.zeros([number_of_initial_lines, steps_initial])
        
        final_real = np.zeros([number_of_initial_lines, steps_initial])
        final_complex = np.zeros([number_of_initial_lines, steps_initial])
        
        #X = linspace(-6, 6, 0.01)
        for i in range(number_of_initial_lines):
            for ii in range(steps_initial):
                x = X[ii]
                
                initial_real[i, ii] = x
                initial_complex[i, ii] = heigth_complex_lines[i]
        
        for i in range(number_of_initial_lines):
            for ii in range(steps_initial):
                z = complex(initial_real[i, ii], initial_complex[i, ii])
                
                f_z = conf_mapping(z)
                
                final_real[i, ii] = np.real(f_z)
                final_complex[i, ii] = np.imag(f_z)
                
    else:
        logger.info('Initial domain: upper-half complex plane')
        heights = []
        
        i = 0
        while len(heights) <= num_initial_lines/2:
            x = i*step_height_initial_lines
            heights.append(x)
            i += 1
            
        i = 0
        while len(heights) <= num_initial_lines:
            x = i*step_height_initial_lines
            heights.append(x)
            i -= 1
            
        number_of_initial_lines = len(heights)
        X = linspace(x_inf_lim_initial_lines, x_sup_lim_initial_lines, step_grid_inside_each_line)
        steps_initial = len(X)
        
        heigth_complex_lines = heights
        
        for i in range(number_of_initial_lines+1):
            if i != 1:
                heigth_complex_lines.append(i)
                
                
        t = np.linspace(0, 1, number_of_initial_lines)
        
        
        initial_real = np.zeros([number_of_initial_lines, steps_initial])
        initial_complex = np.zeros([number_of_initial_lines, steps_initial])
        
        final_real = np.zeros([number_of_initial_lines, steps_initial])
        final_complex = np.zeros([number_of_initial_lines, steps_initial])
        
        #X = linspace(-6, 6, 0.01)
        for i in range(number_of_initial_lines):
            for ii in range(steps_initial):
                x = X[ii]
                
                initial_real[i, ii] = x
                initial_complex[i, ii] = heigth_complex_lines[i]
        
        for i in range(number_of_initial_lines):
            for ii in range(steps_initial):
                z = complex(initial_real[i, ii], initial_complex[i, ii])
                
                f_z = conf_mapping(z)
                
                final_real[i, ii] = np.real(f_z)
                final_complex[i, ii] = np.imag(f_z)
            
    return(initial_real, initial_complex, final_real, final_complex, number_of_initial_lines, steps_initial)



# This function takes the values of the initial and final real and complex 
# parts of the dots to be plotted (and other optional args) and creates the 
# frames of the .GIF file
def plot_for_offset(initial_real, initial_complex, final_real, final_complex,
                    number_of_initial_lines, steps_initial, step_height_initial_lines, t, alphas,
                    color_hor='b', color_ver='r', x_inf_lim_plot=-1.1,
                    x_sup_lim_plot=1.1, y_inf_lim_plot=-1.1,
                    y_sup_lim_plot=1.1):
    
    plot_real = initial_real * (1-t) + final_real * t
    plot_complex = initial_complex * (1-t) + final_complex * t
    

    
    
    
    # Data for plotting
    fig, ax = plt.subplots(figsize=(5, 5))
    
    #alphas = list(np.linspace(1, 0, number_of_initial_lines))
    
    for i in range(number_of_initial_lines):
        X = []
        Y = []
        for ii in range(steps_initial):
            X.append(plot_real[i, ii])
            Y.append(plot_complex[i, ii])
        ax.plot(X, Y, color=color_hor, alpha=alphas[i])
    
    j=0
    for ii in range(steps_initial):
        X = []
        Y = []
        if j%10==0:
        #if initial_real[0, ii]%step_height_initial_lines<=0.00005:
            for i in range(number_of_initial_lines):
                X.append(plot_real[i, ii])
                Y.append(plot_complex[i, ii])
            ax.plot(X, Y, color=color_ver, alpha=alphas[i])
        j += 1
    
    # IMPORTANT ANIMATION CODE HERE
    # Used to keep the limits constant
    ax.set_xlim(x_inf_lim_plot, x_sup_lim_plot)
    ax.set_ylim(y_inf_lim_plot, y_sup_lim_plot)

    # Used to return the plot as an image rray
    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    
    return image
