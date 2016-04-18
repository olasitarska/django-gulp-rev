import os

from django.test import TestCase, override_settings

import gulp_rev


class gulp_revTestCase(TestCase):
    def setUp(self):
        self.path = 'css/main.css'
        self.manifest_path = 'rev-manifest.json'
        gulp_rev._STATIC_MAPPING = None

    def test_is_debug_false(self):
        self.assertFalse(gulp_rev.is_debug())

    @override_settings(DEBUG=True)
    def test_is_debug_true(self):
        self.assertTrue(gulp_rev.is_debug())

    def test_dev_url(self):
        dev_url = gulp_rev.dev_url(self.path)
        self.assertEqual(len(self.path)+9, len(dev_url))
        self.assertIn('?', dev_url)

    @override_settings(STATIC_ROOT=os.path.dirname(os.path.realpath(__file__)))
    def test_get_mapping_default(self):
        mapping = gulp_rev._get_mapping()
        self.assertIn(self.path, mapping)

    @override_settings(DJANGO_GULP_REV_PATH=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rev-manifest.json'))
    def test_get_mapping_with_setting(self):
        mapping = gulp_rev._get_mapping()
        self.assertIn(self.path, mapping)

    @override_settings(STATIC_ROOT=os.path.dirname(os.path.realpath(__file__)))
    def test_production_url(self):
        url = gulp_rev.production_url(self.path, '/static/'+self.path)
        mapping = gulp_rev._get_mapping()
        self.assertEqual(url, '/static/'+mapping[self.path])

    @override_settings(STATIC_ROOT=os.path.dirname(os.path.realpath(__file__)))
    def test_production_url_non_existing_path(self):
        path = 'img/a.png'
        url = gulp_rev.production_url(path, '/static/'+path)
        self.assertEqual(url, '/static/'+path)

    @override_settings(STATIC_URL='/teststatic/', DEBUG=True)
    def test_static_rev_debug_true(self):
        url = gulp_rev.static_rev(self.path)
        self.assertIn('/teststatic/'+self.path+'?', url)
        self.assertEqual(len('/teststatic/'+self.path+'?')+8, len(url))

    @override_settings(STATIC_ROOT=os.path.dirname(os.path.realpath(__file__)),
        STATIC_URL='/teststatic/', DEBUG=False)
    def test_static_rev_debug_false(self):
        url = gulp_rev.static_rev(self.path)
        mapping = gulp_rev._get_mapping()
        self.assertEqual('/teststatic/'+mapping[self.path], url)

    @override_settings(DJANGO_GULP_REV_PATH='notexist.json', STATIC_URL='/teststatic/',
        DEBUG=False)
    def test_mapping_file_doesnt_exist(self):
        url = gulp_rev.static_rev(self.path)
        self.assertIn('/teststatic/'+self.path+'?', url)
        self.assertEqual(len('/teststatic/'+self.path+'?')+8, len(url))