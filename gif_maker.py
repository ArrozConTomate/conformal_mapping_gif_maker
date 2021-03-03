import renderizer
import logging
import numpy as np
import time
import imageio

# Initialize the logger
logger = logging.getLogger(__name__)
if not len(logger.handlers):
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s ')
    
    file_handler = logging.FileHandler('GIF_maker_log.log')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)


logger.info('--------------- New GIF ---------------')

# Set the parameters:
    
# function to be plotted
def conf_mapping(z):
    # Fancy notation: sqrt(-1) = 1j
    return((z-1j)/(z+1j)) 
    
# Parameters to compute the real and complex parts:
num_initial_lines = 100 # Number of lines to be plotted at t=0 (initial)
step_height_initial_lines = 0.1 # Distance between each lines (initial)
x_inf_lim_initial_lines = -50 # x inferior limit of the initial lines
x_sup_lim_initial_lines = 50 # x superior limiti of the initial lines
step_grid_inside_each_line = 0.01 # distance between each initial line´s points

# Parameters to create the actual .GIF file
fps = 60 # frames per second
gif_name = 'prueba.gif' # name of the .GIF file

logger.info('Plot parameters:')
logger.info('num_initial_lines: {}'.format(num_initial_lines))
logger.info('step_height_initial_lines: {}'.format(step_height_initial_lines))
logger.info('x_inf_lim_initial_lines: {}'.format(x_inf_lim_initial_lines))
logger.info('x_sup_lim_initial_lines: {}'.format(x_sup_lim_initial_lines))
logger.info('step_grid_inside_each_line: {}'.format(step_grid_inside_each_line))

    
    


logger.info('GIF parameters:')
logger.info('fps: {}'.format(fps))
logger.info('gif_name: {}'.format(gif_name))

# time_values takes the time values that will be used to create the frames of 
# the .GIF file
time_values = list(np.linspace(0, 1, 60, endpoint=True))
time_values = time_values + list(np.linspace(1, 1, 20, endpoint=True))
time_values = time_values + list(np.linspace(1, 0, 60, endpoint=True))
time_values = time_values + list(np.linspace(0, 0, 20, endpoint=True))


logger.info('Execution times:')
# Compute the plots that will build the GIF
tic = time.time()

initial_real, initial_complex, final_real, final_complex, number_of_initial_lines, steps_initial = \
renderizer.final_real_and_complex_coords(num_initial_lines,     
                                         step_height_initial_lines,
                                         x_inf_lim_initial_lines,
                                         x_sup_lim_initial_lines,
                                         step_grid_inside_each_line,
                                         conf_mapping)

toc = time.time()
logger.info('Time to compute the final values: {}'.format(toc-tic))



# Join all the plots as frames of the .GIF file

#alphas = list(np.linspace(1, 0, number_of_initial_lines)) # shadings
alphas = list(np.linspace(1, 1, number_of_initial_lines)) # shadings

tic = time.time()
kwargs_write = {'fps':1.0, 'quantizer':'nq'}
imageio.mimsave('./' + gif_name, [renderizer.plot_for_offset(initial_real,
                                                  initial_complex,
                                                  final_real,
                                                  final_complex,
                                                  number_of_initial_lines,
                                                  steps_initial,
                                                  step_height_initial_lines,
                                                  t,
                                                  alphas) for t in time_values], fps=fps)

toc = time.time()
logger.info('Time to generate the .gif file: {}'.format(toc-tic))

logging.shutdown()
