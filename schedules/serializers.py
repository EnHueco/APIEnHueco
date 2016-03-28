__author__ = 'Diego'
from rest_framework import serializers
import schedules.models as models


class GapSerializer(serializers.ModelSerializer) :
	class Meta :
		model = models.Gap
		# read_only_fields = ('created_on', 'updated_on')

	def __init__ (self, *args, **kwargs) :
		# Don't pass the 'fields' arg up to the superclass
		exclude = kwargs.pop('exclude', None)

		# Instantiate the superclass normally
		super(GapSerializer, self).__init__(*args, **kwargs)

		if exclude is not None :
			# Drop any fields that are specified in the `excluded` argument.
			excluded = set(exclude)
			for field_name in excluded :
				self.fields.pop(field_name)

	def to_representation (self, instance) :
		repr = super(GapSerializer, self).to_representation(instance)

		if instance.user != None :
			if not instance.user.shares_event_names : repr['name'] = ''
			if not instance.user.shares_event_locations : repr['location'] = ''

		return repr

class ImmediateEventSerializer(serializers.ModelSerializer) :
	class Meta:
		model = models.ImmediateEvent
		read_only = ('updated_on',)

class ImmediateEventSerializerNoUser(serializers.ModelSerializer) :
    class Meta:
        exclude = ('user',)
        read_only = ('updated_on',)


