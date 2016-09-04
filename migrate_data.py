# migrate data from json file
# 1) simple text migration
# 2) correct url alias and legacy
# 3) find category and tag or create
# 4) upload images
import os
import django
import sys
import json
import urllib.request

from datetime import datetime

from django.core.files import File
from django.utils.timezone import get_default_timezone


sys.path.append("~/IdeaProjects/b111")
os.environ["DJANGO_SETTINGS_MODULE"] = "b111.settings"
django.setup()

from django.contrib.auth.models import User
from articles.models import Article, Category

with open('b101.json') as data_file:
    data = json.load(data_file)


def get_date(string):
    date = datetime.strptime(string, '%d/%m/%Y - %H:%M')
    return date.replace(tzinfo=get_default_timezone())


def is_legacy(full_alias):
    prefix = full_alias.split('/', 2)[1]
    if prefix == 'lenta':
        return True
    if prefix == 'article':
        return False
    raise RuntimeError('unknown url prefix')


def strip_slug(full_alias):
    return full_alias.split('/', 2)[2]

for node in data['nodes']:
    b101 = node['node']
    article = Article()
    article.title = b101['title']
    article.legacy = is_legacy(b101['alias'])
    article.slug = strip_slug(b101['alias'])
    article.text = b101['full_text']
    article.preview_text = b101['body_1']
    article.category = Category.objects.last()
    article.author = User.objects.last()
    article.published_date = get_date(b101['created'])
    article.state = '3'
    article.save()

    url = b101['field_image']['src']
    filename = url.split('/')[-1]
    resource = urllib.request.urlopen(url)
    output = open(filename, "wb")
    output.write(resource.read())
    output.close()

    with open(filename, 'rb') as image:
        article.teaser_image.save('test_teaser.jpg', File(image), save=True)

    os.remove(filename)
