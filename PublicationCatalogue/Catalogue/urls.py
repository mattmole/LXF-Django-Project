from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('tags/', views.returnTags,name='tagList'),
    path('tags/<int:tag_id>/', views.returnTagById, name='tag'),
    path('articles/', views.returnArticles, name='articleList'),
    path('articles/<int:article_id>/', views.returnArticleById, name='article'),
    path('authors/', views.returnAuthors, name='authorList'),
    path('authors/<int:author_id>/', views.returnAuthorById, name='author'),
    path('publishers/', views.returnPublishers, name='publisherList'),
    path('publishers/<int:publisher_id>/', views.returnPublisherById, name='publisher'),
    path('publications/', views.returnPublications, name='publicationList'),
    path('publications/<int:publication_id>/', views.returnPublicationById, name='publication'),
    path('editions/', views.returnEditions, name='editionList'),
    path('editions/<int:edition_id>/', views.returnEditionById, name='edition'),
    path('pubs/', views.returnPublishersAndPublications, name='publicationAndPublishersList'),
    path('search/', views.search, name='search'),
    path('addTag/', views.addTag, name='addTag'),
    path('exportTags/', views.exportTagsToCsv, name='exportTagsToCsv')
]
