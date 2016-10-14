#-*- coding:utf-8 -*-
"""
This file is part of the Mousetrap plug-ins for OpenSesame.
"""

from libopensesame.py3compat import *

from libopensesame.exceptions import osexception
from openexp.mouse import mouse

# Define class for the MouseTracking response
class MT_response(object):
	"""Python class for collecting mouse-tracking data in OpenSesame."""
	
	def __init__(self, experiment, buttons=None):
		
		"""Initialize MT_response object.
		
		Initialize MT_response object to track mouse movements and collect 
		clicks on virtual 'buttons', which are areas at defined screen
		coordinates.
		
		Args:
		    experiment: The current experiment instance. 
		        In an OpenSesame script, this is usually the self.experiment
		        variable.
		    buttons: A dictionary defining the response buttons. 
		        Each key corresponds to the name that will be returned by the
		        _exec method if the user responds using the button (either by
		        clicking it or by moving the cursor into the associated area).
		        Each value contains four integers that define the button area:
		        The left  x- and top  y-coordinate and the width and height of
		        the button (as used in the canvas.rect function).
		"""
		
		
		# Check that uniform coordinates option is activated
		if experiment.var.uniform_coordinates == 'no':
			raise osexception('To use the Mousetrap plug-ins, '
				'the option Uniform coordinates needs to be selected '
				'in the general options of the experiment.')
		
		self.experiment = experiment
		
		# Prepare buttons
		if buttons == None:
			self.buttons = None
		else:
			self.buttons = {}
			for button in buttons:
				vals = buttons[button]
				
				# Allow for negative width/height values
				if vals[2] >= 0:
					xleft = vals[0]
					xright = xleft+vals[2]
				else:
					xright = vals[0]
					xleft = xright+vals[2]
				
				if vals[3] >= 0:
					yleft = vals[1]
					yright = yleft+vals[3]
				else:
					yright = vals[1]
					yleft = yright+vals[3]
					
				self.buttons[button]=(xleft,yleft,xright,yright)

	def _exec(self,
		logging_resolution=10, timeout=None,
		boundaries={'upper':None,'lower':None,'left':None,'right':None},
		reset_mouse=True, start_coordinates=(0,0),
		click_required=True, mouse_buttons_allowed=[1, 3],
		track_clicks=False,
		max_initiation_time=None, warning_textline=None):
	    
		"""Executes MT_response object and returns results.

    	Executes the MT_response object and returns the response, response time,
		and mouse-tracking data.

	    Args:
	        logging_resolution (int): Time interval (in ms) between recordings 
				of the mouse position.
			timeout (int): Response timeout (in ms). Use None (default) if there
				is no timeout.
			boundaries (dict): Contains optional vertical and horizontal 
				boundaries. Tracking stops if the cursor moves beyond one of 
				these.
			reset_mouse (bool): Reset mouse position when tracking starts.
			start_coordinates (tuple): The x- and y- coordinates (in sketchpad 
				metric) the cursor should be reset to.
			click_required (bool): Click required to indicate response. If False, 
				a response can be indicated just by entering the area of one 
				of the buttons with the mouse.
			mouse_buttons_allowed (list): The (physical) mouse buttons that 
				can be used to click one of the buttons.
			track_clicks (bool): Enable separate tracking of mouse clicks. 
				If True, the physical mouse button that was clicked will be 
				returned along with a corresponding timestamp as a separate 
				list.
			max_initiation_time (int): If specified, a custom warning message 
				will be displayed if no mouse movement was initiated after the 
				specified time limit (in ms).
			warning_textline (list): Custom warning message to be displayed. List
				containing the name of the currently displayed canvas/sketchpad 
				as the first element and input for the canvas.text function as 
				the second argument.
	    
		Returns:
			resp (str): The name (key) of the buttton that was clicked.
			resp_time (int): Response time (in ms).
			initiation_time (int): Time (in ms) until a movement was initiated.
			timestamps (list): Timestamps (in ms) for each recorded position.
			xpos (list): x-positions for each recorded position.
			ypos (list): y-positions for each recorded position.
			clicks (list): (Physical) mouse button for each mouse click. 
				Only returned if track_clicks is True.
			clicks_timestamps (list): Timestamp (in ms) for each mouse click. 
				Only returned if track_clicks is True.
	    """	
		
		# Initialize mouse
		self.mouse = mouse(self.experiment, visible=True)
		
		# Initialize clock
		self.clock = self.experiment._clock
		
		# Specify timeout settings
		if timeout != None:
			timeout = int(timeout)
			timeleft = timeout
		else:
			timeleft = logging_resolution
		
		# Check if any boundary values are specified
		check_boundaries = any(val!=None for val in boundaries.values())
			
		# Check if timeout or boundaries are specified in case there are no buttons
		if self.buttons == None:
			if timeout == None and check_boundaries == False:
				raise osexception('As no buttons are specified, either a timeout or boundaries have to be specified.')
		
		# Prepare boundaries if boundary values are specified
		if check_boundaries:
		
			check_boundaries_x = False
			if any(boundaries[label] != None for label in ['left', 'right']):
				check_boundaries_x = True
				boundaries_x = [-float('Inf'), float('Inf')]
				if boundaries['left'] != None:
					boundaries_x[0] = int(boundaries['left'])
				if boundaries['right'] != None:
					boundaries_x[1] = int(boundaries['right'])
				
			check_boundaries_y = False
			if any(boundaries[label] != None for label in ['upper', 'lower']):
				check_boundaries_y = True
				boundaries_y = [-float('Inf'), float('Inf')]
				# As OpenSesame's screen coordinates increase when mouse moves toward the bottom of the screen
				# assign the value of 'upper' boundary as the lower value (and vice versa)
				if boundaries['upper'] != None:
					boundaries_y[0] = int(boundaries['upper'])
				if boundaries['lower'] != None:
					boundaries_y[1] = int(boundaries['lower'])
		
		# Reset mouse (if specified)
		if reset_mouse:
			# Move mouse cursor to the position specified in pixel
			startx_mouse = int(start_coordinates[0])
			starty_mouse = int(start_coordinates[1])
						
			# Set mouse position
			self.mouse.set_pos((startx_mouse, starty_mouse))
			
			# Set up variables including their first values
			timestamps = [self.clock.time()]
			xpos = [startx_mouse]
			ypos = [starty_mouse]
		
		# Get mouse position otherwise
		else:
			# Set up variables including their first values
			position, timestamp = self.mouse.get_pos()
			timestamps = [timestamp]
			xpos = [position[0]]
			ypos = [position[1]]
			
		# Show mouse
		self.mouse.show_cursor(show=True)
		
		# Set tracking variables
		tracking = True
		mouse_on_start = True
		warning_printed = False
		resp = None
		initiation_time = None
		
		if track_clicks:
			clicks = []
			clicks_timestamps = []
		
		# Start tracking
		while tracking and timeleft > 0:
			
			# Collect mouse response
			if timeout==None:
				# (timeout corresponds to interval with which mouse coordinates are recorded)
				mouse_button, xy, time = self.mouse.get_click(buttonlist=None, timeout=logging_resolution)
			else:
				# (timeout corresponds to interval with which mouse coordinates are recorded,
				#  or time left - whatever is smaller)
				mouse_button, xy, time = self.mouse.get_click(buttonlist=None, timeout=min([logging_resolution, timeleft]))
			
			# Retrieve and save mouse coordinates and timestamp using get_pos if there was no click
			# (as get_click returns None for xy if there was no mouse click)
			if xy != None:
				position = xy
				timestamp = time
			else:
				position, timestamp = self.mouse.get_pos()
			
			# Append values
			timestamps.append(timestamp)
			xpos.append(position[0])
			ypos.append(position[1])
				
			# Check if mouse has left the starting position, and, if so, determine initiation time
			if mouse_on_start == True:
				mouse_on_start = (position[0] == xpos[0]) and (position[1] == ypos[0])
				if mouse_on_start == False:
					# difference between last (not current) timestamp and timestamp at start
					initiation_time = timestamps[-2]-timestamps[0]

			
			# If mouse is still on starting position and initiation time is exceeded, show warning
			if max_initiation_time != None:
				if mouse_on_start == True and warning_printed == False:
					if (timestamp-timestamps[0]) > max_initiation_time:
						warning_canvas = self.experiment.items[warning_textline[0]].canvas
						warning_canvas.text(**warning_textline[1])
						warning_canvas.show()
						warning_printed = True
			
			# If mouse clicks should be recorded, save them
			if track_clicks:
				if mouse_button != None:
					clicks.append(mouse_button)
					clicks_timestamps.append(timestamp)
			
			# If boundaries should be checked, determine if mouse position is outside the boundaries
			if check_boundaries:
				if check_boundaries_x:
					if position[0] < boundaries_x[0] or position[0] > boundaries_x[1]:
						tracking = False
				if check_boundaries_y:
					if position[1] < boundaries_y[0] or position[1] > boundaries_y[1]:
						tracking = False
			
			# If there was a mouse click, determine if the click was in the range of one of the "buttons"
			# (or check if mouse has "touched" a button even though there was no mouse click -  if no mouse click was required)
			if click_required == False or mouse_button in mouse_buttons_allowed:
				if self.buttons != None:
					if position != None:
						resp = None
						for button in self.buttons:
							vals = self.buttons[button]
							if position[0] >= vals[0] and position[0] <= vals[2] and position[1] >= vals[1] and position[1] <= vals[3]:
								resp = button
						if resp != None:
							tracking = False
							
			# Update timeleft
			if timeout != None:
				timeleft = timeout-(timestamp-timestamps[0])

			
		# Calculate response time
		resp_time = timestamps[-1] - timestamps[0]
		
		if track_clicks == False:
			return resp, resp_time, initiation_time, timestamps, xpos, ypos
		else:
			return resp, resp_time, initiation_time, timestamps, xpos, ypos, clicks, clicks_timestamps
