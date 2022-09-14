from traceback import StackSummary
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

class Publisher(models.Model):
    publisherName = models.CharField("Publisher's Name", max_length=200)

    def __str__(self):
        return self.publisherName

    def modelType(self):
        return self.__class__.__name__

class Publication(models.Model):
    typeChoices = [('NEWSPAPER', 'Newspaper'),('MAGAZINE', 'Magazine')]
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, blank=True)
    publicationName = models.CharField("Publication's Name", max_length=200)
    publicationNotes = models.CharField("Notes", max_length=200, blank=True)
    publicationType = models.CharField("Publication Type", max_length=200, choices = typeChoices)

    def __str__ (self):
        return self.publicationName 

    def modelType(self):
        return self.__class__.__name__

class Edition(models.Model):
    editionName = models.CharField("Name of Edition", max_length = 200)
    publicationDate = models.DateField("Publication Date", blank=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.publication.publicationName + ": " + self.editionName

    def modelType(self):
        return self.__class__.__name__
        
class Tag(models.Model):
    tagName = models.CharField("Tag", max_length = 20)
    tagDescriptor = models.CharField("Description", max_length = 200, blank=True)

    def __str__(self):
        return self.tagName

    def modelType(self):
        return self.__class__.__name__

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('tagName'),
                name='tagNameUnique',
            ),
        ]

class Author(models.Model):
    authorName = models.CharField("Author's Name", max_length = 200)
    notes = models.CharField("Notes", max_length = 200, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.authorName

    def modelType(self):
        return self.__class__.__name__

class Article(models.Model):
    articleName = models.CharField("Article Name", max_length = 200)
    keywords = models.TextField("Keywords", max_length = 2000)
    notes = models.TextField("Notes", max_length = 2000, blank=True)
    summary = models.CharField("Summary",max_length = 500, blank=True)
    edition = models.ManyToManyField(Edition, blank=True)
    author = models.ManyToManyField(Author, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.articleName

    def modelType(self):
        return self.__class__.__name__