# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from . models import Category
from django.core.urlresolvers import reverse
# Create your tests here.
class IndexViewTests(TestCase):

    def test_index_view_with_categories(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        add_cat('test',1,1)
        add_cat('temp',1,1)
        add_cat('tmp',1,1)
        add_cat('tmp test temp',1,1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")

        num_cats =len(response.context['categories'])
        self.assertEqual(num_cats , 4)

    def add_cat(name, views, likes):
        c = Category.objects.get_or_create(name=name)[0]
        c.views = views
        c.likes = likes
        c.save()
        return c
