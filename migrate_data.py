# migrate data from json file
# 1) simple text migration
# 2) correct url alias and legacy
# 3) find category and tag or create
# 4) upload images
import os
import json

import django
import sys


print('before')

sys.path.append("~/IdeaProjects/b111")
os.environ["DJANGO_SETTINGS_MODULE"] = "b111.settings"
print(os.environ["DJANGO_SETTINGS_MODULE"])
django.setup()

from django.contrib.auth.models import User
from articles.models import Article, Category

with open('b101.json') as data_file:
    data = json.load(data_file)

print('before the copy starts')
for node in data['nodes']:
    b101 = node['node']
    print(b101['title'])
    article = Article()
    article.title = b101['title']
    article.text = b101['full_text']
    article.state = '3'
    article.category = Category.objects.last()
    article.author = User.objects.last()
    article.save()
