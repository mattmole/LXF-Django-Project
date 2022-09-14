from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Tag, Article, Author, Publisher, Publication, Edition
from .forms import SearchForm, AddTagForm
from itertools import chain
import csv


# Create your views here.

def exportTagsToCsv(request):
    tagList = Tag.objects.order_by('-tagName')
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="exportTags.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Tag Name','Tag Descriptor'])

    for tag in tagList:
        writer.writerow([tag.tagName, tag.tagDescriptor])

    return response

def addTag(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddTagForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            #ADD TO THE DATABASE
            tagName = form.cleaned_data['tagName']
            tagDescriptor = form.cleaned_data['tagDescriptor']

            if tagName != "":
                newTag = Tag(tagName = tagName)
                if tagDescriptor == "":
                    newTag.tagDescriptor = tagDescriptor
                try:
                    newTag.save()
                    message = 'Added new Tag'
                except:
                    message = 'Could not add new Tag'
                print(message)
                print(newTag)
            template = loader.get_template('Catalogue/databaseAddedMessage.html')
            context = {
                'newEntry': newTag,
                'message': message
            }
            return HttpResponse(template.render(context, request))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddTagForm()

        return render(request, 'Catalogue/addTag.html', {'form': form})

def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            searchTerm = form.cleaned_data['searchTerm']
            searchModel = form.cleaned_data['searchModel']
            fuzzySearch = form.cleaned_data['fuzzySearch']

            print(searchTerm, searchModel, fuzzySearch)

            searchResults = None
            if fuzzySearch == True:
                if searchModel == 'TAGS':
                    if searchTerm == "" or searchTerm == "*":
                        tagResults = Tag.objects.all()
                    else:
                        tagResults = Tag.objects.filter(tagName__contains = searchTerm)
                    searchResults = tagResults
                elif searchModel == 'ARTICLES':
                    if searchTerm == "" or searchTerm == "*":
                        articleResults = Article.objects.all()
                    else:
                        articleResults = Article.objects.filter(articleName__contains = searchTerm)
                    searchResults = articleResults
                elif searchModel == 'AUTHORS':
                    if searchTerm == "" or searchTerm == "*":
                        authorResults = Author.objects.all()
                    else:
                        authorResults = Author.objects.filter(authorName__contains = searchTerm)
                    searchResults = authorResults
                elif searchModel == 'PUBLICATIONS':
                    if searchTerm == "" or searchTerm == "*":
                        publicationResults = Publication.objects.all()
                    else:
                        publicationResults = Publication.objects.filter(publicationName__contains = searchTerm)
                    searchResults = publicationResults
                elif searchModel == 'PUBLISHERS':
                    if searchTerm == "" or searchTerm == "*":
                        publisherResults = Publisher.objects.all()
                    else:
                        publisherResults = Publisher.objects.filter(publisherName__contains = searchTerm)
                    searchResults = publisherResults
                elif searchModel == 'ALL':
                    if searchTerm == "" or searchTerm == "*":
                        searchResults = chain(Tag.objects.all(),
                        Article.objects.all(),
                        Author.objects.all(),
                        Publication.objects.all(),
                        Publisher.objects.all()
                        )
                    else:
                        searchResults = chain(Tag.objects.filter(tagName__contains = searchTerm),
                        Article.objects.filter(articleName__contains = searchTerm),
                        Author.objects.filter(authorName__contains = searchTerm),
                        Publication.objects.filter(publicationName__contains = searchTerm),
                        Publisher.objects.filter(publisherName__contains = searchTerm)
                        )
            else:
                if searchModel == 'TAGS':
                    tagResults = Tag.objects.filter(tagName = searchTerm)
                    searchResults = tagResults
                elif searchModel == 'ARTICLES':
                    articleResults = Article.objects.filter(articleName = searchTerm)
                    searchResults = articleResults
                elif searchModel == 'AUTHORS':
                    authorResults = Author.objects.filter(authorName = searchTerm)
                    searchResults = authorResults
                elif searchModel == 'PUBLICATIONS':
                    publicationResults = Publication.objects.filter(publicationName = searchTerm)
                    searchResults = publicationResults
                elif searchModel == 'PUBLISHERS':
                    publisherResults = Publisher.objects.filter(publisherName = searchTerm)
                    searchResults = publisherResults
                elif searchModel == 'ALL':
                    searchResults = chain(Tag.objects.filter(tagName = searchTerm),
                    Article.objects.filter(articleName = searchTerm),
                    Author.objects.filter(authorName = searchTerm),
                    Publication.objects.filter(publicationName = searchTerm),
                    Publisher.objects.filter(publisherName = searchTerm)
                    ) 
            template = loader.get_template('Catalogue/searchResults.html')
            context = {
                'searchResults': searchResults
            }
            return HttpResponse(template.render(context, request))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

        return render(request, 'Catalogue/search.html', {'form': form})

def index(request):
    template = loader.get_template('Catalogue/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
    
def returnTags(request):
    tagList = Tag.objects.order_by('-tagName')
    template = loader.get_template('Catalogue/returnTags.html')
    context = {
        'tagList': tagList,
    }
    return HttpResponse(template.render(context, request))

def returnTagById(request,tag_id):
    tag = {}
    try:
        tag = Tag.objects.get(id=tag_id)
    except:
        pass

    articlesRegisteredWithTag = {}
    try: 
        articlesRegisteredWithTag = Article.objects.filter(tag__id = tag_id)
    except:
        pass

    authorsRegisteredWithTag = {}
    try: 
        authorsRegisteredWithTag = Author.objects.filter(tag__id = tag_id)
    except:
        pass

    template = loader.get_template('Catalogue/returnTagById.html')
    context = {
        'tag': tag,
        'articlesRegisteredWithTag': articlesRegisteredWithTag,
        'authorsRegisteredWithTag': authorsRegisteredWithTag,

    }
    return HttpResponse(template.render(context, request))

def returnArticles(request):
    articleList = Article.objects.order_by('-articleName')
    template = loader.get_template('Catalogue/returnArticles.html')
    context = {
        'articleList': articleList,
    }
    return HttpResponse(template.render(context, request))

def returnArticleById(request,article_id):
    article = {}
    try:
        article = Article.objects.get(id=article_id)
    except:
        pass

    template = loader.get_template('Catalogue/returnArticleById.html')
    context = {
        'article': article,
    }
    return HttpResponse(template.render(context, request))

def returnAuthors(request):
    authorList = Author.objects.order_by('-authorName')
    template = loader.get_template('Catalogue/returnAuthors.html')
    context = {
        'authorList': authorList,
    }
    return HttpResponse(template.render(context, request))

def returnAuthorById(request,author_id):
    author = {}
    try:
        author = Author.objects.get(id=author_id)
    except:
        pass

    articles = {}
    try:
        articles = Article.objects.filter(author__id=author_id)
    except:
        pass

    template = loader.get_template('Catalogue/returnAuthorById.html')
    context = {
        'author': author,
        'articles': articles
    }
    return HttpResponse(template.render(context, request))

def returnPublishers(request):
    publisherList = Publisher.objects.order_by('-publisherName')
    template = loader.get_template('Catalogue/returnPublishers.html')
    context = {
        'publisherList': publisherList,
    }
    return HttpResponse(template.render(context, request))

def returnPublisherById(request,publisher_id):
    publisher = {}
    try:
        publisher = Publisher.objects.get(id=publisher_id)
    except:
        pass

    publications = {}
    try:
        publications = Publication.objects.filter(publisher__id=publisher_id)
    except:
        pass

    template = loader.get_template('Catalogue/returnPublisherById.html')
    context = {
        'publisher': publisher,
        'publications': publications
    }
    return HttpResponse(template.render(context, request))

def returnPublications(request):
    publicationList = Publication.objects.order_by('-publisher__publisherName')
    template = loader.get_template('Catalogue/returnPublications.html')
    context = {
        'publicationList': publicationList,
    }
    return HttpResponse(template.render(context, request))

def returnPublicationById(request,publication_id):
    publication = {}
    try:
        publication = Publication.objects.get(id=publication_id)
    except:
        pass

    articles = {}
    try:
        articles = Article.objects.filter(edition__publication__id=publication_id)
    except:
        pass

    editions = {}
    try:
        editions = Edition.objects.filter(publication__id=publication_id)
    except:
        pass

    template = loader.get_template('Catalogue/returnPublicationById.html')
    context = {
        'publication': publication,
        'articles': articles,
        'editions': editions
    }
    return HttpResponse(template.render(context, request))

def returnPublishersAndPublications(request):
    publicationList = Publication.objects.order_by('-publicationName')
    template = loader.get_template('Catalogue/returnPublishersAndPublications.html')
    context = {
        'publicationList': publicationList,
    }
    return HttpResponse(template.render(context, request))

def returnEditions(request):
    editions = Edition.objects.order_by('publication__publicationName','-publicationDate')
    template = loader.get_template('Catalogue/returnEditions.html')
    context = {
        'editions': editions,
    }
    return HttpResponse(template.render(context, request))

def returnEditionById(request,edition_id):
    edition = {}
    try:
        edition = Edition.objects.get(id=edition_id)
    except:
        pass

    articles = {}
    if 1:
        articles = Article.objects.filter(edition__id=edition_id)
        print(articles)
    #except:
    #    pass

    template = loader.get_template('Catalogue/returnEditionById.html')
    context = {
        'edition': edition,
        'articles': articles
    }
    return HttpResponse(template.render(context, request))