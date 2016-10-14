#-*- coding:utf-8 -*-
"""
This file is part of the Mousetrap plug-ins for OpenSesame.
"""
from libopensesame.py3compat import *
from libopensesame import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.exceptions import osexception
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'mousetrap_response', category=u'plugins')

# Import class for mouse button label conversion
from libopensesame.mouse_response import mouse_response_mixin

# Import mouse-tracking response
from PyMT_response import MT_response


# Define class for mouse-tracking plugin
class mousetrap_response(item.item, mouse_response_mixin):

	initial_view = u'controls'
	description = u'Tracks mouse movements'

	def reset(self):

		"""
		desc:
			Initialize plug-in.
		"""


		# Set default values for variables
		self.var.logging_resolution = 10
		self.var.timeout = u'infinite'
		self.var.boundaries = u'upper=no lower=no left=no right=no'
		self.var.correct_button = u''
		self.var.update_feedback = u'no'
		self.var.reset_mouse = u'no'
		self.var.click_required = u'yes'
		self.var.mouse_buttons_allowed = u'left_button;right_button'
		self.var.check_initiation_time = u'no'
		self.var.max_initiation_time = 1000
		self.var.warning_message = u'draw textline text="Please start moving" x=0 y=0 sketchpad=example'
		self.var.number_of_buttons = 1
		self.var.button1 = u'x=-100 y=-100 w=200 h=200 name=example'
		self.var.button2 = u''
		self.var.button3 = u''
		self.var.button4 = u''
		self.var.skip_item = u'no'
		self.var.save_trajectories = u'yes'

		# Adapt start coordinates so that they correspond
		# to the center of the button in the form_text_display item
		h = self.var.__parent__.height
		h_start = (float(h)-2*50-2*10)/6*5.5+70
		self.var.start_coordinates = '0;'+str(int(h_start-h/2))

		# Set internal variables
		self._timeout = None
		self._boundaries = {'upper':None,'lower':None,'left':None,'right':None}
		self._correct_button = None
		self._start_coordinates = None
		self._mouse_buttons_allowed=None
		self._max_initiation_time = None
		self._warning_message = None
		self._warning_textline = None


	def clean_input(self,text):

		"""Replace unnecessary characters with whitespace"""

		text= text.replace(',', ' ')
		text= text.replace(';', ' ')
		text= text.replace('(', ' ')
		text= text.replace(')', ' ')
		return(text)


	def prepare_button(self,text,button):

		"""Creates dictionary based on the button definition."""


		cmd, arglist, kwdict = self.syntax.parse_cmd(button+' '+text)

		try:
			button_dict = {kwdict['name']:tuple([kwdict['x'],kwdict['y'],kwdict['w'],kwdict['h']])}
		except:
			raise osexception(button+' is not specified correctly.')

		return button_dict


	def prepare(self):

		"""Prepares the item."""

		item.item.prepare(self)

		if self.var.skip_item == u'no':

			# Get values for internal variables (to allow the use of OpenSesame variables)
			self._correct_button = self.var.correct_button
			self._start_coordinates = self.var.start_coordinates
			self._mouse_buttons_allowed=self.var.mouse_buttons_allowed
			self._warning_message = self.var.warning_message

			# Prepare boundaries
			cmd, args, boundaries_dict = self.syntax.parse_cmd('Boundaries '+self.var.boundaries)
			try:
				for boundary in boundaries_dict:
					if boundaries_dict[boundary] != 'no':
						self._boundaries[boundary] = int(boundaries_dict[boundary])
			except:
				raise osexception('Boundaries are not specified correctly.')

			# Create list with allowed mouse buttons as integers
			if self.var.click_required == u'yes':
				# Convert to string first (in case that only one integer is provided)
				self._mouse_buttons_allowed = str(self._mouse_buttons_allowed)
				self._mouse_buttons_allowed = self.clean_input(self._mouse_buttons_allowed)
				self._mouse_buttons_allowed = self._mouse_buttons_allowed.split()
				self._mouse_buttons_allowed = [self.button_code(i) for i in self._mouse_buttons_allowed]

			# Create start_coordinate tuple
			if self.reset_mouse == u'yes':
				self._start_coordinates = self.clean_input(self._start_coordinates)
				self._start_coordinates = self._start_coordinates.split()
				self._start_coordinates = tuple([int(i) for i in self._start_coordinates])

			# Prepare initiation time warning
			if self.var.check_initiation_time == u'yes':

				self._max_initiation_time = int(self.var.max_initiation_time)

				try:
					cmd, arglist, kwdict = self.syntax.parse_cmd(self._warning_message)
					if arglist[0] != 'textline':
						raise
					if 'sketchpad' in kwdict:
						warning_canvas = kwdict['sketchpad']
						del kwdict['sketchpad']
					for i in kwdict:
						if kwdict[i] in ['yes','no']:
							kwdict[i]=kwdict[i]=='yes'
					self._warning_textline = [warning_canvas,kwdict]
				except:
					raise osexception(u'Failed to create warning message.\
					Please check again the input.')


			# Prepare buttons
			if self.var.number_of_buttons==0:
				self._buttons = None
			else:
				self._buttons = {}

			if self.var.number_of_buttons>=1:
				self._buttons.update(self.prepare_button(self.var.button1,'Button1'))

			if self.var.number_of_buttons>=2:
				self._buttons.update(self.prepare_button(self.var.button2,'Button2'))

			if self.var.number_of_buttons>=3:
				self._buttons.update(self.prepare_button(self.var.button3,'Button3'))

			if self.var.number_of_buttons>=4:
				self._buttons.update(self.prepare_button(self.var.button4,'Button4'))


			# Initialize MT_response object
			self.MT_response = MT_response(self.experiment,buttons=self._buttons)


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

			# Execute MT_response object
			self.set_item_onset()
			button_clicked, response_time, initiation_time, timestamps, xpos, ypos = self.MT_response._exec(
				logging_resolution=self.var.logging_resolution,
				timeout=self._timeout,
				boundaries=self._boundaries,
				reset_mouse=self.var.reset_mouse==u'yes',
				start_coordinates=self._start_coordinates,
				click_required = self.var.click_required==u'yes',
				mouse_buttons_allowed=self._mouse_buttons_allowed,
				max_initiation_time=self._max_initiation_time,
				warning_textline = self._warning_textline
				)


			# Set response variables as OpenSesame variables
			self.experiment.var.response = button_clicked
			self.experiment.var.response_time = response_time
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

		"""Add response variables to var info list."""

		l = item.item.var_info(self)

		if self.var.skip_item == u'no':

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




class qtmousetrap_response(mousetrap_response, qtautoplugin):

	def __init__(self, name, experiment, script=None):

		mousetrap_response.__init__(self, name, experiment, script)
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

		self.logging_resolution_widget.setEnabled(present_form)
		self.timeout_widget.setEnabled(present_form)
		self.boundaries_widget.setEnabled(present_form)
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

		number_of_buttons = self.var.number_of_buttons
		self.number_of_buttons_widget.setEnabled(present_form)
		self.button1_widget.setEnabled(present_form and number_of_buttons>=1)
		self.button2_widget.setEnabled(present_form and number_of_buttons>=2)
		self.button3_widget.setEnabled(present_form and number_of_buttons>=3)
		self.button4_widget.setEnabled(present_form and number_of_buttons>=4)

		self.save_trajectories_widget.setEnabled(present_form)
