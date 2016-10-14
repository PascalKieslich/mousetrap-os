#-*- coding:utf-8 -*-
"""
This file is part of the Mousetrap plug-ins for OpenSesame.
"""
from libopensesame.py3compat import *
from libopensesame import item, widgets
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.exceptions import osexception
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'mousetrap_form', category=u'plugins')

# Import class for mouse button label conversion
from libopensesame.mouse_response import mouse_response_mixin

# Import mouse-tracking form
from PyMT_form import MT_form

# Define class for mouse-tracking plugin
# Note that parts if this code are take from the code of the form_base plug-in
class mousetrap_form(item.item, mouse_response_mixin):

	"""Tracks mouse movements in custom form defined using OpenSesame script"""

	initial_view = u'controls'
	#initial_view = u'split'
	description = u'Tracks mouse movements in custom form defined using OpenSesame script'

	def reset(self):

		"""
		desc:
			Initialize plug-in.
		"""
		
		self.item_type = u'mousetrap_form'
		
		# Set default values for variables (not displayed in controls)
		self.var.spacing = 0
		self.var.focus_widget = None
		self.var.only_render = u'no'
		self.var.margins = u'0;0;0;0'
		self.var.start_unit = u'grid'

		# Set default values for variables
		self.var._theme = u'plain'
		self.var.logging_resolution = 10
		self.var.timeout = u'infinite'
		self.var.correct_button = u''
		self.var.update_feedback = u'no'
		self.var.reset_mouse = u'no'
		self.var.click_required = u'yes'
		self.var.mouse_buttons_allowed = u'left_button;right_button'
		self.var.check_initiation_time = u'no'
		self.var.max_initiation_time = 1000
		self.var.skip_item = u'no'
		self.var.save_trajectories = u'yes'

		# Set default values for col and row
		# so their ratio corresponds to ratio of screen resolutions
		h = self.var.__parent__.height
		w = self.var.__parent__.width

		if float(w)/h == 4.0/3:
			cols = 12
			rows = 9
		elif float(w)/h == 16.0/9:
			cols = 16
			rows = 9
		elif float(w)/h == 16.0/10:
			cols = 16
			rows = 10
		else:
			cols = 16
			rows = 9

		self.var.cols = str(cols)
		self.var.rows = str(rows)
		self.var.warning_message = 'widget '+str(cols/2-2)+' '+str(rows/2-1+rows%2)+' 4 1 label text="Please start moving"'

		# Adapt start coordinates so that they correspond
		# to the center of the button in the form_text_display item
		h_start = (float(h)-2*50-2*10)/6*5.5+70
		self.var.start_coordinates = str(float(cols)/2)+';'+str(round(h_start/float(h) * float(rows),2))

		# Set internal variables
		self._cols = None
		self._rows = None
		self._timeout = None
		self._correct_button = None
		self._start_coordinates = None
		self._mouse_buttons_allowed=None
		self._max_initiation_time = None
		self._warning_message = None
		self._start_unit = None
		self._warning_widget = None

		self._widgets = []
		self._variables = []


	def parse_line(self, line):

		"""
		Allows for arbitrary line parsing, for item-specific requirements.

		Arguments:
		line	--	A single definition line.
		"""

		# taken from form_base.py

		cmd, arglist, kwdict = self.syntax.parse_cmd(line)
		if cmd != u'widget':
			return
		if len(arglist) != 5:
			raise osexception(_(u'Invalid widget specification: %s' % line))
		self._widgets.append((arglist, kwdict))
		if u'var' in kwdict:
			self._variables.append(kwdict[u'var'])

	def to_string(self):

		"""
		Parse the widgets back into a definition string

		Returns:
		A definition string
		"""

		# taken from form_base.py

		s = item.item.to_string(self, self.item_type)
		for arglist, kwdict in self._widgets:
			s += u'\t%s\n' % self.syntax.create_cmd(u'widget', arglist, kwdict)
		s += u'\n'
		return s


	def clean_input(self,text):

		"""Replace unnecessary characters with whitespace"""

		text= text.replace(',', ' ')
		text= text.replace(';', ' ')
		text= text.replace('(', ' ')
		text= text.replace(')', ' ')
		return(text)


	def prepare(self):

		"""Prepares the item."""

		item.item.prepare(self)

		if self.var.skip_item == u'no':

			# Get values for internal variables (to allow the use of OpenSesame variables)
			self._cols = self.var.cols
			self._rows = self.var.rows
			self._correct_button = self.var.correct_button
			self._start_coordinates = self.var.start_coordinates
			self._mouse_buttons_allowed=self.var.mouse_buttons_allowed

			# Prepare the form
			try:
				cols = [float(i) for i in unicode(self._cols).split(';')]
				rows = [float(i) for i in unicode(self._rows).split(';')]
				margins = [float(i) for i in unicode(self.var.margins).split(';')]
			except:
				raise osexception(
					_(u'cols, rows, and margins should be numeric values separated by a semi-colon'))

			# Modification of original form:
			# if cols and rows only have one value, then treat this as the number of cols/rows
			if len(cols)==1:
				cols = int(cols[0])
			if len(rows)==1:
				rows = int(rows[0])

			# Initialize form
			self._form = MT_form(self.experiment, cols=cols, rows=rows, \
				margins=margins, spacing=self.var.spacing, theme=self.var._theme, item=self)

			# Prepare the widgets
			self.focus_widget = None
			for arglist, orig_kwdict in self._widgets:
				kwdict = orig_kwdict.copy()
				# Evaluate all values
				arglist = [self.syntax.eval_text(arg) for arg in arglist]
				for key, val in kwdict.items():
					kwdict[key] = self.syntax.eval_text(val, var=self.var)
				# Translate paths into full file names
				if u'path' in kwdict:
					kwdict[u'path'] = self.experiment.pool[kwdict[u'path']]
				# Process focus keyword
				focus = False
				if u'focus' in kwdict:
					if kwdict[u'focus'] == u'yes':
						focus = True
					del kwdict[u'focus']
				# Parse arguments
				_type = arglist[4]
				try:
					col = int(arglist[0])
					row = int(arglist[1])
					colspan = int(arglist[2])
					rowspan = int(arglist[3])
				except:
					raise osexception(
						_(u'In a form widget col, row, colspan, and rowspan should be integer'))
				# Create the widget and add it to the form
				try:
					_w = getattr(widgets, _type)(self._form, **kwdict)
				except Exception as e:
					raise osexception(
						u'Failed to create widget "%s": %s' % (_type, e))
				self._form.set_widget(_w, (col, row), colspan=colspan,
					rowspan=rowspan)
				# Add as focus widget
				if focus:
					if self.focus_widget is not None:
						raise osexception(
							_(u'You can only specify one focus widget'))
					self.focus_widget = _w


			# Create list with allowed mouse buttons as integers
			if self.var.click_required == u'yes':
				# Convert to string first (in case that only one integer is provided)
				self._mouse_buttons_allowed = str(self._mouse_buttons_allowed)
				self._mouse_buttons_allowed= self.clean_input(self._mouse_buttons_allowed)
				self._mouse_buttons_allowed=self._mouse_buttons_allowed.split()
				self._mouse_buttons_allowed= [self.button_code(i) for i in self._mouse_buttons_allowed]


			# Prepare start_coordinates
			if self.var.reset_mouse == u'yes':

				self._start_unit = self.var.start_unit

				# Clean input for start_coordinates
				self._start_coordinates= self.clean_input(self._start_coordinates)

				# Create start_coordinate tuple
				if '.' in self._start_coordinates:
					self._start_coordinates= self._start_coordinates.split()
					self._start_coordinates= tuple([float(i) for i in self._start_coordinates])
				else:
					self._start_coordinates= self._start_coordinates.split()
					self._start_coordinates= tuple([int(i) for i in self._start_coordinates])

			# Prepare initiation time warning
			if self.var.check_initiation_time == u'yes':
				self._max_initiation_time = int(self.var.max_initiation_time)

				try:
					cmd, arglist, kwdict = self.syntax.parse_cmd(self.var.warning_message)

					# Evaluate all values
					arglist = [self.syntax.eval_text(arg) for arg in arglist]
					for key, val in kwdict.items():
						kwdict[key] = self.syntax.eval_text(val, var=self.var)
					# Translate paths into full file names
					if u'path' in kwdict:
						kwdict[u'path'] = self.experiment.pool[kwdict[u'path']]
					# Create the widget
					_type = arglist[4]
					_w  = getattr(widgets, _type)(self._form, **kwdict)
					self._warning_widget=[_w,(int(arglist[0]),int(arglist[1])),int(arglist[2]),int(arglist[3])]

				except:
					raise osexception(u'Failed to create widget for warning message.\
					Please check again the syntax and test it, e.g.,\
					by directly inserting the widget in the OpenSesame script first.')


	def run(self):

		"""Runs the item."""

		if self.var.skip_item == u'no':

			# Prepare timeout
			self._timeout = self.var.timeout
			if self._timeout == 'infinite':
				self._timeout = None
			else:
				try:
					self._timeout = int(self._timeout)
				except:
					raise osexception(u'Timeout specified incorrectly. It should either be an integer or "infinite".')

			self.set_item_onset()

			if self.var.only_render == u'yes':
				self._form.render()
			else:

				# Execute form
				button_clicked, response_time, initiation_time, timestamps, xpos, ypos = self._form._exec(
					logging_resolution=self.var.logging_resolution,
					timeout=self._timeout,
					reset_mouse=self.var.reset_mouse==u'yes',
					start_unit=self._start_unit,start_coordinates=self._start_coordinates,
					click_required = self.var.click_required==u'yes',
					mouse_buttons_allowed=self._mouse_buttons_allowed,
					max_initiation_time=self._max_initiation_time,
					warning_widget = self._warning_widget
					)

				# Set response variables as OpenSesame variables
				self.experiment.response = button_clicked
				self.experiment.response_time = response_time
				self.experiment.var.set('response_%s'% self.name,button_clicked)
				self.experiment.var.set('response_time_%s'% self.name,response_time)
				self.experiment.var.set('initiation_time',initiation_time)
				self.experiment.var.set('initiation_time_%s'% self.name,initiation_time)

				# Save trajectory data
				if self.var.save_trajectories ==u'yes':
					self.experiment.var.set('timestamps_%s'% self.name,timestamps)
					self.experiment.var.set('xpos_%s'% self.name,xpos)
					self.experiment.var.set('ypos_%s'% self.name,ypos)

				# Determine if response was correct and set corresponding variable
				if self.var.correct_button ==u'':
					correct = None
					self.experiment.var.correct = u'undefined'
				else:
					if button_clicked == self._correct_button:
						correct = 1
					else:
						correct = 0
					self.experiment.var.set('correct_button_%s'% self.name,self._correct_button)
					self.experiment.var.correct = correct
				self.experiment.var.set('correct_%s'% self.name,self.experiment.var.correct)


				# Response bookkeeping (optional)
				if self.var.update_feedback == u'yes':
					self.set_response(response=button_clicked,response_time=response_time,correct=correct)


	def var_info(self):

		"""
		desc:
			Add response variables to var info list.

		returns:
			desc:	A list of (var_name, description) tuples.
			type:	list
		"""

		l = item.item.var_info(self)

		if self.var.skip_item == u'no':

			for var in self._variables:
				l.append( (var, u'[Response variable]') )

			response_variables = [
				'response','response_%s'% self.name,
				'response_time','response_time_%s'% self.name,
				'initiation_time','initiation_time_%s'% self.name,
				'correct','correct_%s'% self.name,
				'correct_button_%s'% self.name]

			if self.var.update_feedback == u'yes':
				response_variables.extend([
					'acc','accuracy',
					'avg_rt','average_response_time'])

			if self.save_trajectories ==u'yes':
				response_variables.extend(['timestamps_%s'% self.name,
										   'xpos_%s'% self.name,
										   'ypos_%s'% self.name])

			for var in response_variables:
				l.append( (var, u'[Response variable]') )

		return l



class qtmousetrap_form(mousetrap_form, qtautoplugin):

	def __init__(self, name, experiment, script=None):

		mousetrap_form.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)
		self.custom_interactions()

	def apply_edit_changes(self):

		"""Applies the controls."""

		if not qtautoplugin.apply_edit_changes(self) or self.lock:
			return False
		self.custom_interactions()
		return True

	def edit_widget(self):

		"""Refreshes the controls."""

		if self.lock:
			return
		self.lock = True
		w = qtautoplugin.edit_widget(self)
		self.custom_interactions()
		self.lock = False
		return w

	def custom_interactions(self):

		"""Activates the relevant controls and adjusts tooltips."""

		present_form = self.var.skip_item == u'no'

		self.cols_widget.setEnabled(present_form)
		self.rows_widget.setEnabled(present_form)
		self.theme_widget.setEnabled(present_form)
		self.logging_resolution_widget.setEnabled(present_form)
		self.timeout_widget.setEnabled(present_form)
		self.correct_button_widget.setEnabled(present_form)
		self.update_feedback_widget.setEnabled(present_form)

		reset_mouse = self.var.reset_mouse == u'yes'
		self.reset_mouse_widget.setEnabled(present_form)
		self.start_coordinates_widget.setEnabled(present_form and reset_mouse)

		click_required = self.var.click_required == u'yes'
		self.click_required_widget.setEnabled(present_form)
		self.mouse_buttons_allowed_widget.setEnabled(present_form and click_required)

		check_initiation_time= self.var.check_initiation_time == u'yes'
		self.check_initiation_time_widget.setEnabled(present_form)
		self.max_initiation_time_widget.setEnabled(present_form and check_initiation_time)
		self.warning_message_widget.setEnabled(present_form and check_initiation_time)
		self.save_trajectories_widget.setEnabled(present_form)
