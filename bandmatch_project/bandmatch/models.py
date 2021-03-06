from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.template.defaultfilters import slugify

import ast

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)



class Player(models.Model):
	user = models.OneToOneField(User)

#	name = models.CharField(max_length = 128) 	#Forename/surname or just name?
#	email = models.EmailField(max_length = 254)
	contact_info = models.TextField(blank = True)
	description = models.TextField(blank = True)
	#Preferences can be included in your own description?
	PRIVACY_CHOICES = [('1', 'on'),('0', 'off')]
	privacy = models.IntegerField(default=1, choices = PRIVACY_CHOICES)
	demo = models.FileField(upload_to = 'player_demos', blank = True) #How to have multiple (from 0 to n) demos? 
	instruments = ListField(blank = True)
	#instrument = models.CharField(max_length = 128, default = 'None') #Need to have this as a list of strings
	location = models.CharField(max_length = 256, default = 'Nowhere')
	image = models.ImageField(upload_to ='profile_images', blank = True)

	GENDER_CHOICES = [('unknown', 'do not wish to specify'), ('m', 'male'),('f', 'female')]

	gender = models.CharField(max_length = 25, choices = GENDER_CHOICES, default = 'unknown')
	
	def __unicode__(self):
		return self.user.username
	





class Message(models.Model):
	title = models.CharField(max_length = 128) #May need to be changed
	content = models.TextField()
	sender = models.ForeignKey('Player', related_name='sender')
#	The relationship is yet to be defined, so need to use the name, not the object
#	---> Use 'Player' rather than Player
#	See https://docs.djangoproject.com/en/1.7/ref/models/fields/#lazy-relationships
	recipients = models.ManyToManyField('Player') 
	date = models.DateTimeField(auto_now_add=True) #Change to dateTimeField

	def __unicode__(self):
		return self.title + ': ' + self.content


#Possible to gather "when a member joined the band" - data easily.
# See https://docs.djangoproject.com/en/1.7/ref/models/fields/#django.db.models.ManyToManyField.through

class Band(models.Model):
	#Genres as a separate field for easier queries?
	name = models.CharField(max_length = 128)
	demo = models.FileField(upload_to = 'band_demos', blank = True)
	location = models.CharField(max_length = 256)
	description = models.TextField()
	image = models.ImageField(upload_to = 'band_images', blank = True)
	members = models.ManyToManyField('Player')
	slug = models.SlugField(unique=True) #With this we can't have bands with same names.

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Band, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name



class Advert(models.Model):

#	What need to happen is:
#	When a band gets deleted - all it's adverts are deleted also!

	band = models.ForeignKey(Band) #Cascade deletion?
	title = models.CharField(max_length = 128)
	content = models.TextField()
	date = models.DateField(auto_now_add=True) #date is set when the object is created, cannot be edited
	looking_for = models.CharField(max_length = 256) #Need to have this as a list??

	def __unicode__(self):
		return self.title


class Reply(models.Model):

	advert = models.ForeignKey('Advert')
	replier = models.ForeignKey('Player')
	content = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.content

	



admin.site.register(Advert)
admin.site.register(Message)
admin.site.register(Reply)
