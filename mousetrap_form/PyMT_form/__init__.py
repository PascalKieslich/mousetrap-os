#-*- coding:utf-8 -*-
"""
This file is part of the Mousetrap plug-ins for OpenSesame.
"""
from libopensesame.py3compat import *

from libopensesame.widgets import form 
from libopensesame.exceptions import osexception
from openexp.mouse import mouse

# Define class for the MouseTracking form
class MT_form(form):
	
	def __init__(self, experiment,
		cols=12, rows=9, 
		spacing=0, margins=(0, 0, 0, 0),
		theme=u'gray', item=None,
		clicks=False):
		
		# Check that uniform coordinates option is activated
		if experiment.var.uniform_coordinates == 'no':
			raise osexception('To use the Mousetrap plug-ins, '
			'the option Uniform coordinates needs to be selected '
			'in the general options of the experiment.')
		
		# Timeout variable used in form class is different
		# from timeout variable used in MT_form
		super(MT_form, self).__init__(experiment,
			cols=cols, rows=rows,
			spacing=spacing, margins=margins,
			theme=theme, item=item,
			timeout=None, clicks=clicks)
	
	def _exec(self,
		logging_resolution=10,timeout=None,
		reset_mouse=True,start_unit='grid',start_coordinates=(6.0,4.5),
		click_required=True,mouse_buttons_allowed=[1,3],
		track_clicks=False,
		max_initiation_time=None,warning_widget=None):
		
		# Specify timeout settings
		if timeout != None:
			timeout = int(timeout)
			timeleft = timeout
		else:
			timeleft = logging_resolution
		
		# Calculate start coordinates (if mouse should be reset)
		if reset_mouse:
		
			# Check if start_coordinates are in allowed range
			if start_unit in ['grid', 'widget']:
				if start_coordinates[0] > len(self.cols)-1:
					raise osexception('start x coordinate exceeds number of colums - 1 (first column has value 0)')
				if  start_coordinates[1] > len(self.rows)-1:
					raise osexception('start y coordinate exceeds number of rows - 1 (first row has value 0)')
			
			# Unit: grid
			# move mouse cursor to the left upper corner of the grid position
			# (if float is given, linear interpolation is performed)
			if start_unit=='grid':
				
				start_index = self.cell_index((int(start_coordinates[0]),int(start_coordinates[1])))
				startx_mouse, starty_mouse, w, h = self.get_rect(start_index)
				
				# if form coordinates are provided as float, use linear interpolation
				# (as internal form function only accepts integers)
				if isinstance(start_coordinates[0], float):
					start_index_upper = self.cell_index((int(start_coordinates[0])+1,int(start_coordinates[1])))
					startx_upper, y, w, h = self.get_rect(start_index_upper)			
					startx_mouse += int((startx_upper-startx_mouse) * (start_coordinates[0]-int(start_coordinates[0])))
					
				if isinstance(start_coordinates[1], float):
					start_index_upper = self.cell_index((int(start_coordinates[0]),int(start_coordinates[1])+1))
					x, starty_upper, w, h = self.get_rect(start_index_upper)			
					starty_mouse += int((starty_upper-starty_mouse) * (start_coordinates[1]-int(start_coordinates[1])))

			# Unit: widget
			# move mouse cursor to the center of the widget for which starting coordinates are provided
			# (if no widget has the start coordinates for this position, mouse is centered on the position of the grid)
			elif start_unit=='widget':
				start_index = self.cell_index((int(start_coordinates[0]),int(start_coordinates[1])))
				startx_mouse, starty_mouse, w, h = self.get_rect(start_index)
				startx_mouse += w/2
				starty_mouse += h/2
			
			# Unit: pixel
			# move mouse cursor to the position specified in pixel
			elif start_unit=='pixel':
				startx_mouse = start_coordinates[0]
				starty_mouse = start_coordinates[1]
			
			else:
				raise osexception('start_unit should be one of the following: grid, widget, pixel')
			
			# Convert pixel values to integers
			startx_mouse = int(startx_mouse)
			starty_mouse = int(starty_mouse)
					
		
		# Render form
		self.render()
		
		# Initialize mouse
		self.mouse = mouse(self.experiment,visible=True)
		
		# Initialize clock
		self.clock = self.experiment._clock
		
		# Reset mouse (if specified)
		if reset_mouse:
		
			# Set mouse position
			self.mouse.set_pos((startx_mouse,starty_mouse))
			
			# Set up variables including their first values
			timestamps = [self.clock.time()]
			xpos = [startx_mouse]
			ypos = [starty_mouse]
		
		
		# Get mouse position otherwise		
		else:
		
			# Get mouse position
			position, timestamp = self.mouse.get_pos()
			
			# Set up variables including their first values
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
		while tracking and timeleft>0:
			
			# Collect mouse response
			if timeout==None:
				# (timeout corresponds to interval with which mouse coordinates are recored)
				mouse_button, xy, time = self.mouse.get_click(buttonlist=None,timeout=logging_resolution)
			else:
				# (timeout corresponds to interval with which mouse coordinates are recored,
				#  or time left - whatever is smaller)
				mouse_button, xy, time = self.mouse.get_click(buttonlist=None,timeout=min([logging_resolution,timeleft]))
			
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
					if (timestamp-timestamps[0])>max_initiation_time:
						self.set_widget(warning_widget[0],warning_widget[1],colspan=warning_widget[2],rowspan=warning_widget[3])
						self.render()
						warning_printed = True
			
			# If mouse clicks should be recorded, save them
			if track_clicks:
				if mouse_button != None:
					clicks.append(mouse_button)
					clicks_timestamps.append(timestamp)
			
			# If there was a mouse click, determine the button that was clicked
			# and if click was on a button, end tracking and finish form
			# (or check if mouse has "touched" a button even though there was no mouse click -  if no mouse click was required)
			if click_required == False or mouse_button in mouse_buttons_allowed:
				
				pos = self.xy_to_index(position)
				
				if pos != None:
					w = self.widgets[pos]
					if w != None:
						resp = self.widgets[pos].on_mouse_click(xy)
						if resp != None:
							tracking = False
			
			# Update timeleft
			if timeout != None:
				timeleft = timeout-(timestamp-timestamps[0])
			
		# Calculate response time
		resp_time = timestamps[-1]-timestamps[0]
		
		# Set form_response variable
		self.experiment.var.form_response = resp
		
		if track_clicks == False:
			return resp, resp_time, initiation_time, timestamps, xpos, ypos
		else:
			return resp, resp_time, initiation_time, timestamps, xpos, ypos, clicks, clicks_timestamps

