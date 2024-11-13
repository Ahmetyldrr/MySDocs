***Soru:*** 6.3 Built-in class-based views API
Class-based views API reference. For introductory material, see the Class-based views topic guide.
6.3.1 Base views
The following three classes provide much of the functionality needed to create Django views. You may think of them
as parent views, which can be used by themselves or inherited from. They may not provide all the capabilities required
for projects, in which case there are Mixins and Generic class-based views.
Many of Django’s built-in class-based views inherit from other class-based views or various mixins. Because this
inheritance chain is very important, the ancestor classes are documented under the section title of Ancestors (MRO).
MRO is an acronym for Method Resolution Order.
View
class django.views.generic.base.View
The master class-based base view. All other class-based views inherit from this base class. It isn’t strictly a
generic view and thus can also be imported from django.views.
Method Flowchart
1. setup()
2. dispatch()
3. http_method_not_allowed()
4. options()
Example views.py:
from django.http import HttpResponse
from django.views import View
class MyView(View):
(continues on next page)
666 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
(continued from previous page)
def get(self, request, *args, **kwargs):
return HttpResponse('Hello, World!')
Example urls.py:
from django.urls import path
from myapp.views import MyView
urlpatterns = [
path('mine/', MyView.as_view(), name='my-view'),
]
Attributes
http_method_names
The list of HTTP method names that this view will accept.
Default:
['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
Methods
classmethod as_view(**initkwargs)
Returns a callable view that takes a request and returns a response:
response = MyView.as_view()(request)
The returned view has view_class and view_initkwargs attributes.
When the view is called during the request/response cycle, the setup() method assigns the
HttpRequest to the view’s request attribute, and any positional and/or keyword arguments captured
from the URL pattern to the args and kwargs attributes, respectively. Then dispatch() is
called.
setup(request, *args, **kwargs)
Initializes view instance attributes: self.request, self.args, and self.kwargs prior to
dispatch().
Overriding this method allows mixins to setup instance attributes for reuse in child classes. When overriding
this method, you must call super().
dispatch(request, *args, **kwargs)
The view part of the view – the method that accepts a request argument plus arguments, and returns a
HTTP response.
The default implementation will inspect the HTTP method and attempt to delegate to a method that
matches the HTTP method; a GET will be delegated to get(), a POST to post(), and so on.
By default, a HEAD request will be delegated to get(). If you need to handle HEAD requests in a different
way than GET, you can override the head() method. See Supporting other HTTP methods for an
example.
http_method_not_allowed(request, *args, **kwargs)
If the view was called with a HTTP method it doesn’t support, this method is called instead.
The default implementation returns HttpResponseNotAllowed with a list of allowed methods in
plain text.
6.3. Built-in class-based views API 667
Django Documentation, Release 3.0.15.dev
options(request, *args, **kwargs)
Handles responding to requests for the OPTIONS HTTP verb. Returns a response with the Allow header
containing a list of the view’s allowed HTTP method names.
TemplateView
class django.views.generic.base.TemplateView
Renders a given template, with the context containing parameters captured in the URL.
Ancestors (MRO)
This view inherits methods and attributes from the following views:
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.base.ContextMixin
• django.views.generic.base.View
Method Flowchart
1. setup()
2. dispatch()
3. http_method_not_allowed()
4. get_context_data()
Example views.py:
from django.views.generic.base import TemplateView
from articles.models import Article
class HomePageView(TemplateView):
template_name = "home.html"
def get_context_data(self, **kwargs):
context = super().get_context_data(**kwargs)
context['latest_articles'] = Article.objects.all()[:5]
return context
Example urls.py:
from django.urls import path
from myapp.views import HomePageView
urlpatterns = [
path('', HomePageView.as_view(), name='home'),
]
Context
• Populated (through ContextMixin) with the keyword arguments captured from the URL pattern that
served the view.
• You can also add context using the extra_context keyword argument for as_view().
668 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
RedirectView
class django.views.generic.base.RedirectView
Redirects to a given URL.
The given URL may contain dictionary-style string formatting, which will be interpolated against the parameters
captured in the URL. Because keyword interpolation is always done (even if no arguments are passed in), any
"%" characters in the URL must be written as "%%" so that Python will convert them to a single percent sign
on output.
If the given URL is None, Django will return an HttpResponseGone (410).
Ancestors (MRO)
This view inherits methods and attributes from the following view:
• django.views.generic.base.View
Method Flowchart
1. setup()
2. dispatch()
3. http_method_not_allowed()
4. get_redirect_url()
Example views.py:
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from articles.models import Article
class ArticleCounterRedirectView(RedirectView):
permanent = False
query_string = True
pattern_name = 'article-detail'
def get_redirect_url(self, *args, **kwargs):
article = get_object_or_404(Article, pk=kwargs['pk'])
article.update_counter()
return super().get_redirect_url(*args, **kwargs)
Example urls.py:
from django.urls import path
from django.views.generic.base import RedirectView
from article.views import ArticleCounterRedirectView, ArticleDetail
urlpatterns = [
path('counter/<int:pk>/', ArticleCounterRedirectView.as_view(), name='article-
˓→counter'),
path('details/<int:pk>/', ArticleDetail.as_view(), name='article-detail'),
path('go-to-django/', RedirectView.as_view(url='https://djangoproject.com'),
˓→name='go-to-django'),
]
Attributes
6.3. Built-in class-based views API 669
Django Documentation, Release 3.0.15.dev
url
The URL to redirect to, as a string. Or None to raise a 410 (Gone) HTTP error.
pattern_name
The name of the URL pattern to redirect to. Reversing will be done using the same args and kwargs as are
passed in for this view.
permanent
Whether the redirect should be permanent. The only difference here is the HTTP status code returned. If
True, then the redirect will use status code 301. If False, then the redirect will use status code 302. By
default, permanent is False.
query_string
Whether to pass along the GET query string to the new location. If True, then the query string is appended
to the URL. If False, then the query string is discarded. By default, query_string is False.
Methods
get_redirect_url(*args, **kwargs)
Constructs the target URL for redirection.
The args and kwargs arguments are positional and/or keyword arguments captured from the URL pattern,
respectively.
The default implementation uses url as a starting string and performs expansion of % named parameters
in that string using the named groups captured in the URL.
If url is not set, get_redirect_url() tries to reverse the pattern_name using what was captured
in the URL (both named and unnamed groups are used).
If requested by query_string, it will also append the query string to the generated URL. Subclasses
may implement any behavior they wish, as long as the method returns a redirect-ready URL string.
6.3.2 Generic display views
The two following generic class-based views are designed to display data. On many projects they are typically the
most commonly used views.
DetailView
class django.views.generic.detail.DetailView
While this view is executing, self.object will contain the object that the view is operating upon.
Ancestors (MRO)
This view inherits methods and attributes from the following views:
• django.views.generic.detail.SingleObjectTemplateResponseMixin
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.detail.BaseDetailView
• django.views.generic.detail.SingleObjectMixin
• django.views.generic.base.View
Method Flowchart
1. setup()
2. dispatch()
670 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
3. http_method_not_allowed()
4. get_template_names()
5. get_slug_field()
6. get_queryset()
7. get_object()
8. get_context_object_name()
9. get_context_data()
10. get()
11. render_to_response()
Example myapp/views.py:
from django.utils import timezone
from django.views.generic.detail import DetailView
from articles.models import Article
class ArticleDetailView(DetailView):
model = Article
def get_context_data(self, **kwargs):
context = super().get_context_data(**kwargs)
context['now'] = timezone.now()
return context
Example myapp/urls.py:
from django.urls import path
from article.views import ArticleDetailView
urlpatterns = [
path('<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
]
Example myapp/article_detail.html:
<h1>{{ object.headline }}</h1>
<p>{{ object.content }}</p>
<p>Reporter: {{ object.reporter }}</p>
<p>Published: {{ object.pub_date|date }}</p>
<p>Date: {{ now|date }}</p>
ListView
class django.views.generic.list.ListView
A page representing a list of objects.
While this view is executing, self.object_list will contain the list of objects (usually, but not necessarily
a queryset) that the view is operating upon.
Ancestors (MRO)
6.3. Built-in class-based views API 671
Django Documentation, Release 3.0.15.dev
This view inherits methods and attributes from the following views:
• django.views.generic.list.MultipleObjectTemplateResponseMixin
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.list.BaseListView
• django.views.generic.list.MultipleObjectMixin
• django.views.generic.base.View
Method Flowchart
1. setup()
2. dispatch()
3. http_method_not_allowed()
4. get_template_names()
5. get_queryset()
6. get_context_object_name()
7. get_context_data()
8. get()
9. render_to_response()
Example views.py:
from django.utils import timezone
from django.views.generic.list import ListView
from articles.models import Article
class ArticleListView(ListView):
model = Article
paginate_by = 100 # if pagination is desired
def get_context_data(self, **kwargs):
context = super().get_context_data(**kwargs)
context['now'] = timezone.now()
return context
Example myapp/urls.py:
from django.urls import path
from article.views import ArticleListView
urlpatterns = [
path('', ArticleListView.as_view(), name='article-list'),
]
Example myapp/article_list.html:
<h1>Articles</h1>
<ul>
{% for article in object_list %}
(continues on next page)
672 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
(continued from previous page)
<li>{{ article.pub_date|date }} - {{ article.headline }}</li>
{% empty %}
<li>No articles yet.</li>
{% endfor %}
</ul>
If you’re using pagination, you can adapt the example template from the pagination docs. Change instances of
contacts in that example template to page_obj.
class django.views.generic.list.BaseListView
A base view for displaying a list of objects. It is not intended to be used directly, but rather as a parent class of
the django.views.generic.list.ListView or other views representing lists of objects.
Ancestors (MRO)
This view inherits methods and attributes from the following views:
• django.views.generic.list.MultipleObjectMixin
• django.views.generic.base.View
Methods
get(request, *args, **kwargs)
Adds object_list to the context. If allow_empty is True then display an empty list. If
allow_empty is False then raise a 404 error.
6.3.3 Generic editing views
The following views are described on this page and provide a foundation for editing content:
• django.views.generic.edit.FormView
• django.views.generic.edit.CreateView
• django.views.generic.edit.UpdateView
• django.views.generic.edit.DeleteView
See also:
The messages framework contains SuccessMessageMixin, which facilitates presenting messages about successful
form submissions.
Note: Some of the examples on this page assume that an Author model has been defined as follows in myapp/
models.py:
from django.db import models
from django.urls import reverse
class Author(models.Model):
name = models.CharField(max_length=200)
def get_absolute_url(self):
return reverse('author-detail', kwargs={'pk': self.pk})
6.3. Built-in class-based views API 673
Django Documentation, Release 3.0.15.dev
FormView
class django.views.generic.edit.FormView
A view that displays a form. On error, redisplays the form with validation errors; on success, redirects to a new
URL.
Ancestors (MRO)
This view inherits methods and attributes from the following views:
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.edit.BaseFormView
• django.views.generic.edit.FormMixin
• django.views.generic.edit.ProcessFormView
• django.views.generic.base.View
Example myapp/forms.py:
from django import forms
class ContactForm(forms.Form):
name = forms.CharField()
message = forms.CharField(widget=forms.Textarea)
def send_email(self):
# send email using the self.cleaned_data dictionary
pass
Example myapp/views.py:
from myapp.forms import ContactForm
from django.views.generic.edit import FormView
class ContactView(FormView):
template_name = 'contact.html'
form_class = ContactForm
success_url = '/thanks/'
def form_valid(self, form):
# This method is called when valid form data has been POSTed.
# It should return an HttpResponse.
form.send_email()
return super().form_valid(form)
Example myapp/contact.html:
<form method="post">{% csrf_token %}
{{ form.as_p }}
<input type="submit" value="Send message">
</form>
CreateView
class django.views.generic.edit.CreateView
A view that displays a form for creating an object, redisplaying the form with validation errors (if there are any)
and saving the object.
674 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
Ancestors (MRO)
This view inherits methods and attributes from the following views:
• django.views.generic.detail.SingleObjectTemplateResponseMixin
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.edit.BaseCreateView
• django.views.generic.edit.ModelFormMixin
• django.views.generic.edit.FormMixin
• django.views.generic.detail.SingleObjectMixin
• django.views.generic.edit.ProcessFormView
• django.views.generic.base.View
Attributes
template_name_suffix
The CreateView page displayed to a GET request uses a template_name_suffix of '_form'.
For example, changing this attribute to '_create_form' for a view creating objects for the example
Author model would cause the default template_name to be 'myapp/author_create_form.
html'.
object
When using CreateView you have access to self.object, which is the object being created. If the
object hasn’t been created yet, the value will be None.
Example myapp/views.py:
from django.views.generic.edit import CreateView
from myapp.models import Author
class AuthorCreate(CreateView):
model = Author
fields = ['name']
Example myapp/author_form.html:
<form method="post">{% csrf_token %}
{{ form.as_p }}
<input type="submit" value="Save">
</form>
UpdateView
class django.views.generic.edit.UpdateView
A view that displays a form for editing an existing object, redisplaying the form with validation errors (if there
are any) and saving changes to the object. This uses a form automatically generated from the object’s model
class (unless a form class is manually specified).
Ancestors (MRO)
This view inherits methods and attributes from the following views:
• django.views.generic.detail.SingleObjectTemplateResponseMixin
• django.views.generic.base.TemplateResponseMixin
6.3. Built-in class-based views API 675
Django Documentation, Release 3.0.15.dev
• django.views.generic.edit.BaseUpdateView
• django.views.generic.edit.ModelFormMixin
• django.views.generic.edit.FormMixin
• django.views.generic.detail.SingleObjectMixin
• django.views.generic.edit.ProcessFormView
• django.views.generic.base.View
Attributes
template_name_suffix
The UpdateView page displayed to a GET request uses a template_name_suffix of '_form'.
For example, changing this attribute to '_update_form' for a view updating objects for the example
Author model would cause the default template_name to be 'myapp/author_update_form.
html'.
object
When using UpdateView you have access to self.object, which is the object being updated.
Example myapp/views.py:
from django.views.generic.edit import UpdateView
from myapp.models import Author
class AuthorUpdate(UpdateView):
model = Author
fields = ['name']
template_name_suffix = '_update_form'
Example myapp/author_update_form.html:
<form method="post">{% csrf_token %}
{{ form.as_p }}
<input type="submit" value="Update">
</form>
DeleteView
class django.views.generic.edit.DeleteView
A view that displays a confirmation page and deletes an existing object. The given object will only be deleted
if the request method is POST. If this view is fetched via GET, it will display a confirmation page that should
contain a form that POSTs to the same URL.
Ancestors (MRO)
This view inherits methods and attributes from the following views:
• django.views.generic.detail.SingleObjectTemplateResponseMixin
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.edit.BaseDeleteView
• django.views.generic.edit.DeletionMixin
• django.views.generic.detail.BaseDetailView
• django.views.generic.detail.SingleObjectMixin
676 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
• django.views.generic.base.View
Attributes
template_name_suffix
The DeleteView page displayed to a GET request uses a template_name_suffix of
'_confirm_delete'. For example, changing this attribute to '_check_delete' for a view deleting
objects for the example Author model would cause the default template_name to be 'myapp/
author_check_delete.html'.
Example myapp/views.py:
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from myapp.models import Author
class AuthorDelete(DeleteView):
model = Author
success_url = reverse_lazy('author-list')
Example myapp/author_confirm_delete.html:
<form method="post">{% csrf_token %}
<p>Are you sure you want to delete "{{ object }}"?</p>
<input type="submit" value="Confirm">
</form>
6.3.4 Generic date views
Date-based generic views, provided in django.views.generic.dates, are views for displaying drilldown
pages for date-based data.
Note: Some of the examples on this page assume that an Article model has been defined as follows in myapp/
models.py:
from django.db import models
from django.urls import reverse
class Article(models.Model):
title = models.CharField(max_length=200)
pub_date = models.DateField()
def get_absolute_url(self):
return reverse('article-detail', kwargs={'pk': self.pk})
ArchiveIndexView
class ArchiveIndexView
A top-level index page showing the “latest” objects, by date. Objects with a date in the future are not included
unless you set allow_future to True.
Ancestors (MRO)
• django.views.generic.list.MultipleObjectTemplateResponseMixin
6.3. Built-in class-based views API 677
Django Documentation, Release 3.0.15.dev
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.dates.BaseArchiveIndexView
• django.views.generic.dates.BaseDateListView
• django.views.generic.list.MultipleObjectMixin
• django.views.generic.dates.DateMixin
• django.views.generic.base.View
Context
In addition to the context provided by django.views.generic.list.MultipleObjectMixin (via
django.views.generic.dates.BaseDateListView), the template’s context will be:
• date_list: A QuerySet object containing all years that have objects available according to
queryset, represented as datetime.datetime objects, in descending order.
Notes
• Uses a default context_object_name of latest.
• Uses a default template_name_suffix of _archive.
• Defaults to providing date_list by year, but this can be altered to month or day using the attribute
date_list_period. This also applies to all subclass views.
Example myapp/urls.py:
from django.urls import path
from django.views.generic.dates import ArchiveIndexView
from myapp.models import Article
urlpatterns = [
path('archive/',
ArchiveIndexView.as_view(model=Article, date_field="pub_date"),
name="article_archive"),
]
Example myapp/article_archive.html:
<ul>
{% for article in latest %}
<li>{{ article.pub_date }}: {{ article.title }}</li>
{% endfor %}
</ul>
This will output all articles.
YearArchiveView
class YearArchiveView
A yearly archive page showing all available months in a given year. Objects with a date in the future are not
displayed unless you set allow_future to True.
Ancestors (MRO)
• django.views.generic.list.MultipleObjectTemplateResponseMixin
• django.views.generic.base.TemplateResponseMixin
678 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
• django.views.generic.dates.BaseYearArchiveView
• django.views.generic.dates.YearMixin
• django.views.generic.dates.BaseDateListView
• django.views.generic.list.MultipleObjectMixin
• django.views.generic.dates.DateMixin
• django.views.generic.base.View
make_object_list
A boolean specifying whether to retrieve the full list of objects for this year and pass those to the template.
If True, the list of objects will be made available to the context. If False, the None queryset will be
used as the object list. By default, this is False.
get_make_object_list()
Determine if an object list will be returned as part of the context. Returns make_object_list by
default.
Context
In addition to the context provided by django.views.generic.list.MultipleObjectMixin (via
django.views.generic.dates.BaseDateListView), the template’s context will be:
• date_list: A QuerySet object containing all months that have objects available according to
queryset, represented as datetime.datetime objects, in ascending order.
• year: A date object representing the given year.
• next_year: A date object representing the first day of the next year, according to allow_empty
and allow_future.
• previous_year: A date object representing the first day of the previous year, according to
allow_empty and allow_future.
Notes
• Uses a default template_name_suffix of _archive_year.
Example myapp/views.py:
from django.views.generic.dates import YearArchiveView
from myapp.models import Article
class ArticleYearArchiveView(YearArchiveView):
queryset = Article.objects.all()
date_field = "pub_date"
make_object_list = True
allow_future = True
Example myapp/urls.py:
from django.urls import path
from myapp.views import ArticleYearArchiveView
urlpatterns = [
path('<int:year>/',
ArticleYearArchiveView.as_view(),
(continues on next page)
6.3. Built-in class-based views API 679
Django Documentation, Release 3.0.15.dev
(continued from previous page)
name="article_year_archive"),
]
Example myapp/article_archive_year.html:
<ul>
{% for date in date_list %}
<li>{{ date|date }}</li>
{% endfor %}
</ul>
<div>
<h1>All Articles for {{ year|date:"Y" }}</h1>
{% for obj in object_list %}
<p>
{{ obj.title }} - {{ obj.pub_date|date:"F j, Y" }}
</p>
{% endfor %}
</div>
MonthArchiveView
class MonthArchiveView
A monthly archive page showing all objects in a given month. Objects with a date in the future are not displayed
unless you set allow_future to True.
Ancestors (MRO)
• django.views.generic.list.MultipleObjectTemplateResponseMixin
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.dates.BaseMonthArchiveView
• django.views.generic.dates.YearMixin
• django.views.generic.dates.MonthMixin
• django.views.generic.dates.BaseDateListView
• django.views.generic.list.MultipleObjectMixin
• django.views.generic.dates.DateMixin
• django.views.generic.base.View
Context
In addition to the context provided by MultipleObjectMixin (via BaseDateListView), the template’s
context will be:
• date_list: A QuerySet object containing all days that have objects available in the given month,
according to queryset, represented as datetime.datetime objects, in ascending order.
• month: A date object representing the given month.
• next_month: A date object representing the first day of the next month, according to allow_empty
and allow_future.
• previous_month: A date object representing the first day of the previous month, according to
allow_empty and allow_future.
680 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
Notes
• Uses a default template_name_suffix of _archive_month.
Example myapp/views.py:
from django.views.generic.dates import MonthArchiveView
from myapp.models import Article
class ArticleMonthArchiveView(MonthArchiveView):
queryset = Article.objects.all()
date_field = "pub_date"
allow_future = True
Example myapp/urls.py:
from django.urls import path
from myapp.views import ArticleMonthArchiveView
urlpatterns = [
# Example: /2012/08/
path('<int:year>/<int:month>/',
ArticleMonthArchiveView.as_view(month_format='%m'),
name="archive_month_numeric"),
# Example: /2012/aug/
path('<int:year>/<str:month>/',
ArticleMonthArchiveView.as_view(),
name="archive_month"),
]
Example myapp/article_archive_month.html:
<ul>
{% for article in object_list %}
<li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
{% endfor %}
</ul>
<p>
{% if previous_month %}
Previous Month: {{ previous_month|date:"F Y" }}
{% endif %}
{% if next_month %}
Next Month: {{ next_month|date:"F Y" }}
{% endif %}
</p>
WeekArchiveView
class WeekArchiveView
A weekly archive page showing all objects in a given week. Objects with a date in the future are not displayed
unless you set allow_future to True.
Ancestors (MRO)
• django.views.generic.list.MultipleObjectTemplateResponseMixin
6.3. Built-in class-based views API 681
Django Documentation, Release 3.0.15.dev
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.dates.BaseWeekArchiveView
• django.views.generic.dates.YearMixin
• django.views.generic.dates.WeekMixin
• django.views.generic.dates.BaseDateListView
• django.views.generic.list.MultipleObjectMixin
• django.views.generic.dates.DateMixin
• django.views.generic.base.View
Context
In addition to the context provided by MultipleObjectMixin (via BaseDateListView), the template’s
context will be:
• week: A date object representing the first day of the given week.
• next_week: A date object representing the first day of the next week, according to allow_empty
and allow_future.
• previous_week: A date object representing the first day of the previous week, according to
allow_empty and allow_future.
Notes
• Uses a default template_name_suffix of _archive_week.
• The week_format attribute is a strptime() format string used to parse the week number. The
following values are supported:
– '%U': Based on the United States week system where the week begins on Sunday. This is the default
value.
– '%W': Similar to '%U', except it assumes that the week begins on Monday. This is not the same as
the ISO 8601 week number.
Example myapp/views.py:
from django.views.generic.dates import WeekArchiveView
from myapp.models import Article
class ArticleWeekArchiveView(WeekArchiveView):
queryset = Article.objects.all()
date_field = "pub_date"
week_format = "%W"
allow_future = True
Example myapp/urls.py:
from django.urls import path
from myapp.views import ArticleWeekArchiveView
urlpatterns = [
# Example: /2012/week/23/
path('<int:year>/week/<int:week>/',
ArticleWeekArchiveView.as_view(),
(continues on next page)
682 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
(continued from previous page)
name="archive_week"),
]
Example myapp/article_archive_week.html:
<h1>Week {{ week|date:'W' }}</h1>
<ul>
{% for article in object_list %}
<li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
{% endfor %}
</ul>
<p>
{% if previous_week %}
Previous Week: {{ previous_week|date:"W" }} of year {{ previous_week|date:
˓→"Y" }}
{% endif %}
{% if previous_week and next_week %}--{% endif %}
{% if next_week %}
Next week: {{ next_week|date:"W" }} of year {{ next_week|date:"Y" }}
{% endif %}
</p>
In this example, you are outputting the week number. Keep in mind that week numbers computed by the date
template filter with the 'W' format character are not always the same as those computed by strftime()
and strptime() with the '%W' format string. For year 2015, for example, week numbers output by
date are higher by one compared to those output by strftime(). There isn’t an equivalent for the
'%U' strftime() format string in date. Therefore, you should avoid using date to generate URLs for
WeekArchiveView.
DayArchiveView
class DayArchiveView
A day archive page showing all objects in a given day. Days in the future throw a 404 error, regardless of
whether any objects exist for future days, unless you set allow_future to True.
Ancestors (MRO)
• django.views.generic.list.MultipleObjectTemplateResponseMixin
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.dates.BaseDayArchiveView
• django.views.generic.dates.YearMixin
• django.views.generic.dates.MonthMixin
• django.views.generic.dates.DayMixin
• django.views.generic.dates.BaseDateListView
• django.views.generic.list.MultipleObjectMixin
• django.views.generic.dates.DateMixin
• django.views.generic.base.View
6.3. Built-in class-based views API 683
Django Documentation, Release 3.0.15.dev
Context
In addition to the context provided by MultipleObjectMixin (via BaseDateListView), the template’s
context will be:
• day: A date object representing the given day.
• next_day: A date object representing the next day, according to allow_empty and
allow_future.
• previous_day: A date object representing the previous day, according to allow_empty and
allow_future.
• next_month: A date object representing the first day of the next month, according to allow_empty
and allow_future.
• previous_month: A date object representing the first day of the previous month, according to
allow_empty and allow_future.
Notes
• Uses a default template_name_suffix of _archive_day.
Example myapp/views.py:
from django.views.generic.dates import DayArchiveView
from myapp.models import Article
class ArticleDayArchiveView(DayArchiveView):
queryset = Article.objects.all()
date_field = "pub_date"
allow_future = True
Example myapp/urls.py:
from django.urls import path
from myapp.views import ArticleDayArchiveView
urlpatterns = [
# Example: /2012/nov/10/
path('<int:year>/<str:month>/<int:day>/',
ArticleDayArchiveView.as_view(),
name="archive_day"),
]
Example myapp/article_archive_day.html:
<h1>{{ day }}</h1>
<ul>
{% for article in object_list %}
<li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
{% endfor %}
</ul>
<p>
{% if previous_day %}
Previous Day: {{ previous_day }}
{% endif %}
(continues on next page)
684 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
(continued from previous page)
{% if previous_day and next_day %}--{% endif %}
{% if next_day %}
Next Day: {{ next_day }}
{% endif %}
</p>
TodayArchiveView
class TodayArchiveView
A day archive page showing all objects for today. This is exactly the same as django.views.generic.
dates.DayArchiveView, except today’s date is used instead of the year/month/day arguments.
Ancestors (MRO)
• django.views.generic.list.MultipleObjectTemplateResponseMixin
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.dates.BaseTodayArchiveView
• django.views.generic.dates.BaseDayArchiveView
• django.views.generic.dates.YearMixin
• django.views.generic.dates.MonthMixin
• django.views.generic.dates.DayMixin
• django.views.generic.dates.BaseDateListView
• django.views.generic.list.MultipleObjectMixin
• django.views.generic.dates.DateMixin
• django.views.generic.base.View
Notes
• Uses a default template_name_suffix of _archive_today.
Example myapp/views.py:
from django.views.generic.dates import TodayArchiveView
from myapp.models import Article
class ArticleTodayArchiveView(TodayArchiveView):
queryset = Article.objects.all()
date_field = "pub_date"
allow_future = True
Example myapp/urls.py:
from django.urls import path
from myapp.views import ArticleTodayArchiveView
urlpatterns = [
path('today/',
ArticleTodayArchiveView.as_view(),
(continues on next page)
6.3. Built-in class-based views API 685
Django Documentation, Release 3.0.15.dev
(continued from previous page)
name="archive_today"),
]
Where is the example template for TodayArchiveView?
This view uses by default the same template as the DayArchiveView, which is in the previous example. If
you need a different template, set the template_name attribute to be the name of the new template.
DateDetailView
class DateDetailView
A page representing an individual object. If the object has a date value in the future, the view will throw a 404
error by default, unless you set allow_future to True.
Ancestors (MRO)
• django.views.generic.detail.SingleObjectTemplateResponseMixin
• django.views.generic.base.TemplateResponseMixin
• django.views.generic.dates.BaseDateDetailView
• django.views.generic.dates.YearMixin
• django.views.generic.dates.MonthMixin
• django.views.generic.dates.DayMixin
• django.views.generic.dates.DateMixin
• django.views.generic.detail.BaseDetailView
• django.views.generic.detail.SingleObjectMixin
• django.views.generic.base.View
Context
• Includes the single object associated with the model specified in the DateDetailView.
Notes
• Uses a default template_name_suffix of _detail.
Example myapp/urls.py:
from django.urls import path
from django.views.generic.dates import DateDetailView
urlpatterns = [
path('<int:year>/<str:month>/<int:day>/<int:pk>/',
DateDetailView.as_view(model=Article, date_field="pub_date"),
name="archive_date_detail"),
]
Example myapp/article_detail.html:
<h1>{{ object.title }}</h1>
686 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
Note: All of the generic views listed above have matching Base views that only differ in
that they do not include the MultipleObjectTemplateResponseMixin (for the archive views) or
SingleObjectTemplateResponseMixin (for the DateDetailView):
class BaseArchiveIndexView
class BaseYearArchiveView
class BaseMonthArchiveView
class BaseWeekArchiveView
class BaseDayArchiveView
class BaseTodayArchiveView
class BaseDateDetailView
6.3.5 Class-based views mixins
Class-based views API reference. For introductory material, see Using mixins with class-based views.
Simple mixins
ContextMixin
class django.views.generic.base.ContextMixin
Attributes
extra_context
A dictionary to include in the context. This is a convenient way of specifying some context in
as_view(). Example usage:
from django.views.generic import TemplateView
TemplateView.as_view(extra_context={'title': 'Custom Title'})
Methods
get_context_data(**kwargs)
Returns a dictionary representing the template context. The keyword arguments provided will make up the
returned context. Example usage:
def get_context_data(self, **kwargs):
context = super().get_context_data(**kwargs)
context['number'] = random.randrange(1, 100)
return context
The template context of all class-based generic views include a view variable that points to the View
instance.
Use alters_data where appropriate
Note that having the view instance in the template context may expose potentially hazardous methods
to template authors. To prevent methods like this from being called in the template, set
6.3. Built-in class-based views API 687
Django Documentation, Release 3.0.15.dev
alters_data=True on those methods. For more information, read the documentation on rendering a
template context.
TemplateResponseMixin
class django.views.generic.base.TemplateResponseMixin
Provides a mechanism to construct a TemplateResponse, given suitable context. The template to use is
configurable and can be further customized by subclasses.
Attributes
template_name
The full name of a template to use as defined by a string. Not defining a template_name will raise a
django.core.exceptions.ImproperlyConfigured exception.
template_engine
The NAME of a template engine to use for loading the template. template_engine is passed as the
using keyword argument to response_class. Default is None, which tells Django to search for the
template in all configured engines.
response_class
The response class to be returned by render_to_response method. Default is
TemplateResponse. The template and context of TemplateResponse instances can be
altered later (e.g. in template response middleware).
If you need custom template loading or custom context object instantiation, create a
TemplateResponse subclass and assign it to response_class.
content_type
The content type to use for the response. content_type is passed as a keyword argument to
response_class. Default is None – meaning that Django uses 'text/html'.
Methods
render_to_response(context, **response_kwargs)
Returns a self.response_class instance.
If any keyword arguments are provided, they will be passed to the constructor of the response class.
Calls get_template_names() to obtain the list of template names that will be searched looking for
an existent template.
get_template_names()
Returns a list of template names to search for when rendering the template. The first template that is found
will be used.
If template_name is specified, the default implementation will return a list containing
template_name (if it is specified).
Single object mixins
SingleObjectMixin
class django.views.generic.detail.SingleObjectMixin
Provides a mechanism for looking up an object associated with the current HTTP request.
Methods and Attributes
688 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
model
The model that this view will display data for. Specifying model = Foo is effectively the same as
specifying queryset = Foo.objects.all(), where objects stands for Foo’s default manager.
queryset
A QuerySet that represents the objects. If provided, the value of queryset supersedes the value
provided for model.
Warning: queryset is a class attribute with a mutable value so care must be taken when using it
directly. Before using it, either call its all() method or retrieve it with get_queryset() which
takes care of the cloning behind the scenes.
slug_field
The name of the field on the model that contains the slug. By default, slug_field is 'slug'.
slug_url_kwarg
The name of the URLConf keyword argument that contains the slug. By default, slug_url_kwarg is
'slug'.
pk_url_kwarg
The name of the URLConf keyword argument that contains the primary key. By default, pk_url_kwarg
is 'pk'.
context_object_name
Designates the name of the variable to use in the context.
query_pk_and_slug
If True, causes get_object() to perform its lookup using both the primary key and the slug. Defaults
to False.
This attribute can help mitigate insecure direct object reference attacks. When applications allow access to
individual objects by a sequential primary key, an attacker could brute-force guess all URLs; thereby
obtaining a list of all objects in the application. If users with access to individual objects should be
prevented from obtaining this list, setting query_pk_and_slug to True will help prevent the guessing
of URLs as each URL will require two correct, non-sequential arguments. Using a unique slug may serve
the same purpose, but this scheme allows you to have non-unique slugs.
get_object(queryset=None)
Returns the single object that this view will display. If queryset is provided, that queryset will be
used as the source of objects; otherwise, get_queryset() will be used. get_object() looks
for a pk_url_kwarg argument in the arguments to the view; if this argument is found, this method
performs a primary-key based lookup using that value. If this argument is not found, it looks for a
slug_url_kwarg argument, and performs a slug lookup using the slug_field.
When query_pk_and_slug is True, get_object() will perform its lookup using both the primary
key and the slug.
get_queryset()
Returns the queryset that will be used to retrieve the object that this view will display. By default,
get_queryset() returns the value of the queryset attribute if it is set, otherwise it constructs a
QuerySet by calling the all() method on the model attribute’s default manager.
get_context_object_name(obj)
Return the context variable name that will be used to contain the data that this view is manipulating. If
context_object_name is not set, the context name will be constructed from the model_name of
the model that the queryset is composed from. For example, the model Article would have context
object named 'article'.
6.3. Built-in class-based views API 689
Django Documentation, Release 3.0.15.dev
get_context_data(**kwargs)
Returns context data for displaying the object.
The base implementation of this method requires that the self.object attribute be set by the view
(even if None). Be sure to do this if you are using this mixin without one of the built-in views that does
so.
It returns a dictionary with these contents:
• object: The object that this view is displaying (self.object).
• context_object_name: self.object will also be stored under the name returned by
get_context_object_name(), which defaults to the lowercased version of the model name.
Context variables override values from template context processors
Any variables from get_context_data() take precedence over context variables from context
processors. For example, if your view sets the model attribute to User, the default context
object name of user would override the user variable from the django.contrib.auth.
context_processors.auth() context processor. Use get_context_object_name() to
avoid a clash.
get_slug_field()
Returns the name of a slug field to be used to look up by slug. By default this returns the value of
slug_field.
SingleObjectTemplateResponseMixin
class django.views.generic.detail.SingleObjectTemplateResponseMixin
A mixin class that performs template-based response rendering for views that operate upon a single object
instance. Requires that the view it is mixed with provides self.object, the object instance that the view is
operating on. self.object will usually be, but is not required to be, an instance of a Django model. It may
be None if the view is in the process of constructing a new instance.
Extends
• TemplateResponseMixin
Methods and Attributes
template_name_field
The field on the current object instance that can be used to determine the name of a candidate template.
If either template_name_field itself or the value of the template_name_field on the current
object instance is None, the object will not be used for a candidate template name.
template_name_suffix
The suffix to append to the auto-generated candidate template name. Default suffix is _detail.
get_template_names()
Returns a list of candidate template names. Returns the following list:
• the value of template_name on the view (if provided)
• the contents of the template_name_field field on the object instance that the view is operating
upon (if available)
• <app_label>/<model_name><template_name_suffix>.html
690 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
Multiple object mixins
MultipleObjectMixin
class django.views.generic.list.MultipleObjectMixin
A mixin that can be used to display a list of objects.
If paginate_by is specified, Django will paginate the results returned by this. You can specify the page
number in the URL in one of two ways:
• Use the page parameter in the URLconf. For example, this is what your URLconf might look like:
path('objects/page<int:page>/', PaginatedView.as_view()),
• Pass the page number via the page query-string parameter. For example, a URL would look like this:
/objects/?page=3
These values and lists are 1-based, not 0-based, so the first page would be represented as page 1.
For more on pagination, read the pagination documentation.
As a special case, you are also permitted to use last as a value for page:
/objects/?page=last
This allows you to access the final page of results without first having to determine how many pages there are.
Note that page must be either a valid page number or the value last; any other value for page will result in
a 404 error.
Extends
• django.views.generic.base.ContextMixin
Methods and Attributes
allow_empty
A boolean specifying whether to display the page if no objects are available. If this is False and no
objects are available, the view will raise a 404 instead of displaying an empty page. By default, this is
True.
model
The model that this view will display data for. Specifying model = Foo is effectively the same as
specifying queryset = Foo.objects.all(), where objects stands for Foo’s default manager.
queryset
A QuerySet that represents the objects. If provided, the value of queryset supersedes the value
provided for model.
Warning: queryset is a class attribute with a mutable value so care must be taken when using it
directly. Before using it, either call its all() method or retrieve it with get_queryset() which
takes care of the cloning behind the scenes.
ordering
A string or list of strings specifying the ordering to apply to the queryset. Valid values are the same as
those for order_by().
6.3. Built-in class-based views API 691
Django Documentation, Release 3.0.15.dev
paginate_by
An integer specifying how many objects should be displayed per page. If this is given, the view will
paginate objects with paginate_by objects per page. The view will expect either a page query string
parameter (via request.GET) or a page variable specified in the URLconf.
paginate_orphans
An integer specifying the number of “overflow” objects the last page can contain. This extends the
paginate_by limit on the last page by up to paginate_orphans, in order to keep the last page
from having a very small number of objects.
page_kwarg
A string specifying the name to use for the page parameter. The view will expect this parameter to be
available either as a query string parameter (via request.GET) or as a kwarg variable specified in the
URLconf. Defaults to page.
paginator_class
The paginator class to be used for pagination. By default, django.core.paginator.Paginator
is used. If the custom paginator class doesn’t have the same constructor interface as django.core.
paginator.Paginator, you will also need to provide an implementation for get_paginator().
context_object_name
Designates the name of the variable to use in the context.
get_queryset()
Get the list of items for this view. This must be an iterable and may be a queryset (in which querysetspecific
behavior will be enabled).
get_ordering()
Returns a string (or iterable of strings) that defines the ordering that will be applied to the queryset.
Returns ordering by default.
paginate_queryset(queryset, page_size)
Returns a 4-tuple containing (paginator, page, object_list, is_paginated).
Constructed by paginating queryset into pages of size page_size. If the request contains a page
argument, either as a captured URL argument or as a GET argument, object_list will correspond to
the objects from that page.
get_paginate_by(queryset)
Returns the number of items to paginate by, or None for no pagination. By default this returns the value
of paginate_by.
get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)
Returns an instance of the paginator to use for this view. By default, instantiates an instance of
paginator_class.
get_paginate_orphans()
An integer specifying the number of “overflow” objects the last page can contain. By default this returns
the value of paginate_orphans.
get_allow_empty()
Return a boolean specifying whether to display the page if no objects are available. If this method returns
False and no objects are available, the view will raise a 404 instead of displaying an empty page. By
default, this is True.
get_context_object_name(object_list)
Return the context variable name that will be used to contain the list of data that this view is manipulating.
If object_list is a queryset of Django objects and context_object_name is not set, the context
name will be the model_name of the model that the queryset is composed from, with postfix '_list'
appended. For example, the model Article would have a context object named article_list.
692 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
get_context_data(**kwargs)
Returns context data for displaying the list of objects.
Context
• object_list: The list of objects that this view is displaying. If context_object_name is specified,
that variable will also be set in the context, with the same value as object_list.
• is_paginated: A boolean representing whether the results are paginated. Specifically, this is set to
False if no page size has been specified, or if the available objects do not span multiple pages.
• paginator: An instance of django.core.paginator.Paginator. If the page is not paginated,
this context variable will be None.
• page_obj: An instance of django.core.paginator.Page. If the page is not paginated, this
context variable will be None.
MultipleObjectTemplateResponseMixin
class django.views.generic.list.MultipleObjectTemplateResponseMixin
A mixin class that performs template-based response rendering for views that operate upon a list of object
instances. Requires that the view it is mixed with provides self.object_list, the list of object instances
that the view is operating on. self.object_list may be, but is not required to be, a QuerySet.
Extends
• TemplateResponseMixin
Methods and Attributes
template_name_suffix
The suffix to append to the auto-generated candidate template name. Default suffix is _list.
get_template_names()
Returns a list of candidate template names. Returns the following list:
• the value of template_name on the view (if provided)
• <app_label>/<model_name><template_name_suffix>.html
Editing mixins
The following mixins are used to construct Django’s editing views:
• django.views.generic.edit.FormMixin
• django.views.generic.edit.ModelFormMixin
• django.views.generic.edit.ProcessFormView
• django.views.generic.edit.DeletionMixin
Note: Examples of how these are combined into editing views can be found at the documentation on Generic editing
views.
6.3. Built-in class-based views API 693
Django Documentation, Release 3.0.15.dev
FormMixin
class django.views.generic.edit.FormMixin
A mixin class that provides facilities for creating and displaying forms.
Mixins
• django.views.generic.base.ContextMixin
Methods and Attributes
initial
A dictionary containing initial data for the form.
form_class
The form class to instantiate.
success_url
The URL to redirect to when the form is successfully processed.
prefix
The prefix for the generated form.
get_initial()
Retrieve initial data for the form. By default, returns a copy of initial.
get_form_class()
Retrieve the form class to instantiate. By default form_class.
get_form(form_class=None)
Instantiate an instance of form_class using get_form_kwargs(). If form_class isn’t provided
get_form_class() will be used.
get_form_kwargs()
Build the keyword arguments required to instantiate the form.
The initial argument is set to get_initial(). If the request is a POST or PUT, the request data
(request.POST and request.FILES) will also be provided.
get_prefix()
Determine the prefix for the generated form. Returns prefix by default.
get_success_url()
Determine the URL to redirect to when the form is successfully validated. Returns success_url by
default.
form_valid(form)
Redirects to get_success_url().
form_invalid(form)
Renders a response, providing the invalid form as context.
get_context_data(**kwargs)
Calls get_form() and adds the result to the context data with the name ‘form’.
ModelFormMixin
class django.views.generic.edit.ModelFormMixin
A form mixin that works on ModelForms, rather than a standalone form.
Since this is a subclass of SingleObjectMixin, instances of this mixin have access to the model and
queryset attributes, describing the type of object that the ModelForm is manipulating.
694 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
If you specify both the fields and form_class attributes, an ImproperlyConfigured exception will
be raised.
Mixins
• django.views.generic.edit.FormMixin
• django.views.generic.detail.SingleObjectMixin
Methods and Attributes
model
A model class. Can be explicitly provided, otherwise will be determined by examining self.object
or queryset.
fields
A list of names of fields. This is interpreted the same way as the Meta.fields attribute of ModelForm.
This is a required attribute if you are generating the form class automatically (e.g. using model). Omitting
this attribute will result in an ImproperlyConfigured exception.
success_url
The URL to redirect to when the form is successfully processed.
success_url may contain dictionary string formatting, which will be interpolated against the object’s
field attributes. For example, you could use success_url="/polls/{slug}/" to redirect to a URL
composed out of the slug field on a model.
get_form_class()
Retrieve the form class to instantiate. If form_class is provided, that class will be used. Otherwise,
a ModelForm will be instantiated using the model associated with the queryset, or with the model,
depending on which attribute is provided.
get_form_kwargs()
Add the current instance (self.object) to the standard get_form_kwargs().
get_success_url()
Determine the URL to redirect to when the form is successfully validated. Returns django.views.
generic.edit.ModelFormMixin.success_url if it is provided; otherwise, attempts to use the
get_absolute_url() of the object.
form_valid(form)
Saves the form instance, sets the current object for the view, and redirects to get_success_url().
form_invalid(form)
Renders a response, providing the invalid form as context.
ProcessFormView
class django.views.generic.edit.ProcessFormView
A mixin that provides basic HTTP GET and POST workflow.
Note: This is named ‘ProcessFormView’ and inherits directly from django.views.generic.base.
View, but breaks if used independently, so it is more of a mixin.
Extends
• django.views.generic.base.View
Methods and Attributes
6.3. Built-in class-based views API 695
Django Documentation, Release 3.0.15.dev
get(request, *args, **kwargs)
Renders a response using a context created with get_context_data().
post(request, *args, **kwargs)
Constructs a form, checks the form for validity, and handles it accordingly.
put(*args, **kwargs)
The PUT action is also handled and passes all parameters through to post().
DeletionMixin
class django.views.generic.edit.DeletionMixin
Enables handling of the DELETE http action.
Methods and Attributes
success_url
The url to redirect to when the nominated object has been successfully deleted.
success_url may contain dictionary string formatting, which will be interpolated against the object’s
field attributes. For example, you could use success_url="/parent/{parent_id}/" to redirect
to a URL composed out of the parent_id field on a model.
delete(request, *args, **kwargs)
Retrieves the target object and calls its delete() method, then redirects to the success URL.
get_success_url()
Returns the url to redirect to when the nominated object has been successfully deleted. Returns
success_url by default.
Date-based mixins
Note: All the date formatting attributes in these mixins use strftime() format characters. Do not try to use the
format characters from the now template tag as they are not compatible.
YearMixin
class YearMixin
A mixin that can be used to retrieve and provide parsing information for a year component of a date.
Methods and Attributes
year_format
The strftime() format to use when parsing the year. By default, this is '%Y'.
year
Optional The value for the year, as a string. By default, set to None, which means the year will be
determined using other means.
get_year_format()
Returns the strftime() format to use when parsing the year. Returns year_format by default.
get_year()
Returns the year for which this view will display data, as a string. Tries the following sources, in order:
• The value of the YearMixin.year attribute.
696 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
• The value of the year argument captured in the URL pattern.
• The value of the year GET query argument.
Raises a 404 if no valid year specification can be found.
get_next_year(date)
Returns a date object containing the first day of the year after the date provided. This function can
also return None or raise an Http404 exception, depending on the values of allow_empty and
allow_future.
get_previous_year(date)
Returns a date object containing the first day of the year before the date provided. This function can
also return None or raise an Http404 exception, depending on the values of allow_empty and
allow_future.
MonthMixin
class MonthMixin
A mixin that can be used to retrieve and provide parsing information for a month component of a date.
Methods and Attributes
month_format
The strftime() format to use when parsing the month. By default, this is '%b'.
month
Optional The value for the month, as a string. By default, set to None, which means the month will be
determined using other means.
get_month_format()
Returns the strftime() format to use when parsing the month. Returns month_format by default.
get_month()
Returns the month for which this view will display data, as a string. Tries the following sources, in order:
• The value of the MonthMixin.month attribute.
• The value of the month argument captured in the URL pattern.
• The value of the month GET query argument.
Raises a 404 if no valid month specification can be found.
get_next_month(date)
Returns a date object containing the first day of the month after the date provided. This function can
also return None or raise an Http404 exception, depending on the values of allow_empty and
allow_future.
get_previous_month(date)
Returns a date object containing the first day of the month before the date provided. This function can
also return None or raise an Http404 exception, depending on the values of allow_empty and
allow_future.
DayMixin
class DayMixin
A mixin that can be used to retrieve and provide parsing information for a day component of a date.
Methods and Attributes
6.3. Built-in class-based views API 697
Django Documentation, Release 3.0.15.dev
day_format
The strftime() format to use when parsing the day. By default, this is '%d'.
day
Optional The value for the day, as a string. By default, set to None, which means the day will be determined
using other means.
get_day_format()
Returns the strftime() format to use when parsing the day. Returns day_format by default.
get_day()
Returns the day for which this view will display data, as a string. Tries the following sources, in order:
• The value of the DayMixin.day attribute.
• The value of the day argument captured in the URL pattern.
• The value of the day GET query argument.
Raises a 404 if no valid day specification can be found.
get_next_day(date)
Returns a date object containing the next valid day after the date provided. This function can also return
None or raise an Http404 exception, depending on the values of allow_empty and allow_future.
get_previous_day(date)
Returns a date object containing the previous valid day. This function can also return None or raise an
Http404 exception, depending on the values of allow_empty and allow_future.
WeekMixin
class WeekMixin
A mixin that can be used to retrieve and provide parsing information for a week component of a date.
Methods and Attributes
week_format
The strftime() format to use when parsing the week. By default, this is '%U', which means the week
starts on Sunday. Set it to '%W' if your week starts on Monday.
week
Optional The value for the week, as a string. By default, set to None, which means the week will be
determined using other means.
get_week_format()
Returns the strftime() format to use when parsing the week. Returns week_format by default.
get_week()
Returns the week for which this view will display data, as a string. Tries the following sources, in order:
• The value of the WeekMixin.week attribute.
• The value of the week argument captured in the URL pattern
• The value of the week GET query argument.
Raises a 404 if no valid week specification can be found.
get_next_week(date)
Returns a date object containing the first day of the week after the date provided. This function can
also return None or raise an Http404 exception, depending on the values of allow_empty and
allow_future.
698 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
get_prev_week(date)
Returns a date object containing the first day of the week before the date provided. This function can
also return None or raise an Http404 exception, depending on the values of allow_empty and
allow_future.
DateMixin
class DateMixin
A mixin class providing common behavior for all date-based views.
Methods and Attributes
date_field
The name of the DateField or DateTimeField in the QuerySet’s model that the date-based
archive should use to determine the list of objects to display on the page.
When time zone support is enabled and date_field is a DateTimeField, dates are assumed to be
in the current time zone. Otherwise, the queryset could include objects from the previous or the next day
in the end user’s time zone.
Warning: In this situation, if you have implemented per-user time zone selection, the same URL may
show a different set of objects, depending on the end user’s time zone. To avoid this, you should use a
DateField as the date_field attribute.
allow_future
A boolean specifying whether to include “future” objects on this page, where “future” means objects in
which the field specified in date_field is greater than the current date/time. By default, this is False.
get_date_field()
Returns the name of the field that contains the date data that this view will operate on. Returns
date_field by default.
get_allow_future()
Determine whether to include “future” objects on this page, where “future” means objects in which the
field specified in date_field is greater than the current date/time. Returns allow_future by default.
BaseDateListView
class BaseDateListView
A base class that provides common behavior for all date-based views. There won’t normally be a reason to
instantiate BaseDateListView; instantiate one of the subclasses instead.
While this view (and its subclasses) are executing, self.object_list will contain the list of objects that
the view is operating upon, and self.date_list will contain the list of dates for which data is available.
Mixins
• DateMixin
• MultipleObjectMixin
Methods and Attributes
allow_empty
A boolean specifying whether to display the page if no objects are available. If this is True and no objects
are available, the view will display an empty page instead of raising a 404.
6.3. Built-in class-based views API 699
Django Documentation, Release 3.0.15.dev
This is identical to django.views.generic.list.MultipleObjectMixin.allow_empty,
except for the default value, which is False.
date_list_period
Optional A string defining the aggregation period for date_list. It must be one of 'year' (default),
'month', or 'day'.
get_dated_items()
Returns a 3-tuple containing (date_list, object_list, extra_context).
date_list is the list of dates for which data is available. object_list is the list of objects.
extra_context is a dictionary of context data that will be added to any context data provided by
the MultipleObjectMixin.
get_dated_queryset(**lookup)
Returns a queryset, filtered using the query arguments defined by lookup. Enforces any restrictions on
the queryset, such as allow_empty and allow_future.
get_date_list_period()
Returns the aggregation period for date_list. Returns date_list_period by default.
get_date_list(queryset, date_type=None, ordering=’ASC’)
Returns the list of dates of type date_type for which queryset contains entries. For example,
get_date_list(qs, 'year') will return the list of years for which qs has entries. If date_type
isn’t provided, the result of get_date_list_period() is used. date_type and ordering are
passed to QuerySet.dates().
6.3.6 Class-based generic views - flattened index
This index provides an alternate organization of the reference documentation for class-based views. For each view, the
effective attributes and methods from the class tree are represented under that view. For the reference documentation
organized by the class which defines the behavior, see Class-based views.
See also:
Classy Class-Based Views provides a nice interface to navigate the class hierarchy of the built-in class-based views.
Simple generic views
View
class View
Attributes (with optional accessor):
• http_method_names
Methods
• as_view()
• dispatch()
• head()
• http_method_not_allowed()
• setup()
700 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
TemplateView
class TemplateView
Attributes (with optional accessor):
• content_type
• extra_context
• http_method_names
• response_class [render_to_response()]
• template_engine
• template_name [get_template_names()]
Methods
• as_view()
• dispatch()
• get()
• get_context_data()
• head()
• http_method_not_allowed()
• render_to_response()
• setup()
RedirectView
class RedirectView
Attributes (with optional accessor):
• http_method_names
• pattern_name
• permanent
• query_string
• url [get_redirect_url()]
Methods
• as_view()
• delete()
• dispatch()
• get()
• head()
• http_method_not_allowed()
• options()
6.3. Built-in class-based views API 701
Django Documentation, Release 3.0.15.dev
• post()
• put()
• setup()
Detail Views
DetailView
class DetailView
Attributes (with optional accessor):
• content_type
• context_object_name [get_context_object_name()]
• extra_context
• http_method_names
• model
• pk_url_kwarg
• query_pk_and_slug
• queryset [get_queryset()]
• response_class [render_to_response()]
• slug_field [get_slug_field()]
• slug_url_kwarg
• template_engine
• template_name [get_template_names()]
• template_name_field
• template_name_suffix
Methods
• as_view()
• dispatch()
• get()
• get_context_data()
• get_object()
• head()
• http_method_not_allowed()
• render_to_response()
• setup()
702 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
List Views
ListView
class ListView
Attributes (with optional accessor):
• allow_empty [get_allow_empty()]
• content_type
• context_object_name [get_context_object_name()]
• extra_context
• http_method_names
• model
• ordering [get_ordering()]
• paginate_by [get_paginate_by()]
• paginate_orphans [get_paginate_orphans()]
• paginator_class
• queryset [get_queryset()]
• response_class [render_to_response()]
• template_engine
• template_name [get_template_names()]
• template_name_suffix
Methods
• as_view()
• dispatch()
• get()
• get_context_data()
• get_paginator()
• head()
• http_method_not_allowed()
• paginate_queryset()
• render_to_response()
• setup()
Editing views
FormView
class FormView
6.3. Built-in class-based views API 703
Django Documentation, Release 3.0.15.dev
Attributes (with optional accessor):
• content_type
• extra_context
• form_class [get_form_class()]
• http_method_names
• initial [get_initial()]
• prefix [get_prefix()]
• response_class [render_to_response()]
• success_url [get_success_url()]
• template_engine
• template_name [get_template_names()]
Methods
• as_view()
• dispatch()
• form_invalid()
• form_valid()
• get()
• get_context_data()
• get_form()
• get_form_kwargs()
• http_method_not_allowed()
• post()
• put()
• setup()
CreateView
class CreateView
Attributes (with optional accessor):
• content_type
• context_object_name [get_context_object_name()]
• extra_context
• fields
• form_class [get_form_class()]
• http_method_names
• initial [get_initial()]
• model
704 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
• pk_url_kwarg
• prefix [get_prefix()]
• query_pk_and_slug
• queryset [get_queryset()]
• response_class [render_to_response()]
• slug_field [get_slug_field()]
• slug_url_kwarg
• success_url [get_success_url()]
• template_engine
• template_name [get_template_names()]
• template_name_field
• template_name_suffix
Methods
• as_view()
• dispatch()
• form_invalid()
• form_valid()
• get()
• get_context_data()
• get_form()
• get_form_kwargs()
• get_object()
• head()
• http_method_not_allowed()
• post()
• put()
• render_to_response()
• setup()
UpdateView
class UpdateView
Attributes (with optional accessor):
• content_type
• context_object_name [get_context_object_name()]
• extra_context
• fields
6.3. Built-in class-based views API 705
Django Documentation, Release 3.0.15.dev
• form_class [get_form_class()]
• http_method_names
• initial [get_initial()]
• model
• pk_url_kwarg
• prefix [get_prefix()]
• query_pk_and_slug
• queryset [get_queryset()]
• response_class [render_to_response()]
• slug_field [get_slug_field()]
• slug_url_kwarg
• success_url [get_success_url()]
• template_engine
• template_name [get_template_names()]
• template_name_field
• template_name_suffix
Methods
• as_view()
• dispatch()
• form_invalid()
• form_valid()
• get()
• get_context_data()
• get_form()
• get_form_kwargs()
• get_object()
• head()
• http_method_not_allowed()
• post()
• put()
• render_to_response()
• setup()
706 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
DeleteView
class DeleteView
Attributes (with optional accessor):
• content_type
• context_object_name [get_context_object_name()]
• extra_context
• http_method_names
• model
• pk_url_kwarg
• query_pk_and_slug
• queryset [get_queryset()]
• response_class [render_to_response()]
• slug_field [get_slug_field()]
• slug_url_kwarg
• success_url [get_success_url()]
• template_engine
• template_name [get_template_names()]
• template_name_field
• template_name_suffix
Methods
• as_view()
• delete()
• dispatch()
• get()
• get_context_data()
• get_object()
• head()
• http_method_not_allowed()
• post()
• render_to_response()
• setup()
Date-based views
ArchiveIndexView
class ArchiveIndexView
6.3. Built-in class-based views API 707
Django Documentation, Release 3.0.15.dev
Attributes (with optional accessor):
• allow_empty [get_allow_empty()]
• allow_future [get_allow_future()]
• content_type
• context_object_name [get_context_object_name()]
• date_field [get_date_field()]
• extra_context
• http_method_names
• model
• ordering [get_ordering()]
• paginate_by [get_paginate_by()]
• paginate_orphans [get_paginate_orphans()]
• paginator_class
• queryset [get_queryset()]
• response_class [render_to_response()]
• template_engine
• template_name [get_template_names()]
• template_name_suffix
Methods
• as_view()
• dispatch()
• get()
• get_context_data()
• get_date_list()
• get_dated_items()
• get_dated_queryset()
• get_paginator()
• head()
• http_method_not_allowed()
• paginate_queryset()
• render_to_response()
• setup()
708 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
YearArchiveView
class YearArchiveView
Attributes (with optional accessor):
• allow_empty [get_allow_empty()]
• allow_future [get_allow_future()]
• content_type
• context_object_name [get_context_object_name()]
• date_field [get_date_field()]
• extra_context
• http_method_names
• make_object_list [get_make_object_list()]
• model
• ordering [get_ordering()]
• paginate_by [get_paginate_by()]
• paginate_orphans [get_paginate_orphans()]
• paginator_class
• queryset [get_queryset()]
• response_class [render_to_response()]
• template_engine
• template_name [get_template_names()]
• template_name_suffix
• year [get_year()]
• year_format [get_year_format()]
Methods
• as_view()
• dispatch()
• get()
• get_context_data()
• get_date_list()
• get_dated_items()
• get_dated_queryset()
• get_paginator()
• head()
• http_method_not_allowed()
• paginate_queryset()
• render_to_response()
6.3. Built-in class-based views API 709
Django Documentation, Release 3.0.15.dev
• setup()
MonthArchiveView
class MonthArchiveView
Attributes (with optional accessor):
• allow_empty [get_allow_empty()]
• allow_future [get_allow_future()]
• content_type
• context_object_name [get_context_object_name()]
• date_field [get_date_field()]
• extra_context
• http_method_names
• model
• month [get_month()]
• month_format [get_month_format()]
• ordering [get_ordering()]
• paginate_by [get_paginate_by()]
• paginate_orphans [get_paginate_orphans()]
• paginator_class
• queryset [get_queryset()]
• response_class [render_to_response()]
• template_engine
• template_name [get_template_names()]
• template_name_suffix
• year [get_year()]
• year_format [get_year_format()]
Methods
• as_view()
• dispatch()
• get()
• get_context_data()
• get_date_list()
• get_dated_items()
• get_dated_queryset()
• get_next_month()
• get_paginator()
710 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
• get_previous_month()
• head()
• http_method_not_allowed()
• paginate_queryset()
• render_to_response()
• setup()
WeekArchiveView
class WeekArchiveView
Attributes (with optional accessor):
• allow_empty [get_allow_empty()]
• allow_future [get_allow_future()]
• content_type
• context_object_name [get_context_object_name()]
• date_field [get_date_field()]
• extra_context
• http_method_names
• model
• ordering [get_ordering()]
• paginate_by [get_paginate_by()]
• paginate_orphans [get_paginate_orphans()]
• paginator_class
• queryset [get_queryset()]
• response_class [render_to_response()]
• template_engine
• template_name [get_template_names()]
• template_name_suffix
• week [get_week()]
• week_format [get_week_format()]
• year [get_year()]
• year_format [get_year_format()]
Methods
• as_view()
• dispatch()
• get()
• get_context_data()
6.3. Built-in class-based views API 711
Django Documentation, Release 3.0.15.dev
• get_date_list()
• get_dated_items()
• get_dated_queryset()
• get_paginator()
• head()
• http_method_not_allowed()
• paginate_queryset()
• render_to_response()
• setup()
DayArchiveView
class DayArchiveView
Attributes (with optional accessor):
• allow_empty [get_allow_empty()]
• allow_future [get_allow_future()]
• content_type
• context_object_name [get_context_object_name()]
• date_field [get_date_field()]
• day [get_day()]
• day_format [get_day_format()]
• extra_context
• http_method_names
• model
• month [get_month()]
• month_format [get_month_format()]
• ordering [get_ordering()]
• paginate_by [get_paginate_by()]
• paginate_orphans [get_paginate_orphans()]
• paginator_class
• queryset [get_queryset()]
• response_class [render_to_response()]
• template_engine
• template_name [get_template_names()]
• template_name_suffix
• year [get_year()]
• year_format [get_year_format()]
712 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
Methods
• as_view()
• dispatch()
• get()
• get_context_data()
• get_date_list()
• get_dated_items()
• get_dated_queryset()
• get_next_day()
• get_next_month()
• get_paginator()
• get_previous_day()
• get_previous_month()
• head()
• http_method_not_allowed()
• paginate_queryset()
• render_to_response()
• setup()
TodayArchiveView
class TodayArchiveView
Attributes (with optional accessor):
• allow_empty [get_allow_empty()]
• allow_future [get_allow_future()]
• content_type
• context_object_name [get_context_object_name()]
• date_field [get_date_field()]
• day [get_day()]
• day_format [get_day_format()]
• extra_context
• http_method_names
• model
• month [get_month()]
• month_format [get_month_format()]
• ordering [get_ordering()]
• paginate_by [get_paginate_by()]
6.3. Built-in class-based views API 713
Django Documentation, Release 3.0.15.dev
• paginate_orphans [get_paginate_orphans()]
• paginator_class
• queryset [get_queryset()]
• response_class [render_to_response()]
• template_engine
• template_name [get_template_names()]
• template_name_suffix
• year [get_year()]
• year_format [get_year_format()]
Methods
• as_view()
• dispatch()
• get()
• get_context_data()
• get_date_list()
• get_dated_items()
• get_dated_queryset()
• get_next_day()
• get_next_month()
• get_paginator()
• get_previous_day()
• get_previous_month()
• head()
• http_method_not_allowed()
• paginate_queryset()
• render_to_response()
• setup()
DateDetailView
class DateDetailView
Attributes (with optional accessor):
• allow_future [get_allow_future()]
• content_type
• context_object_name [get_context_object_name()]
• date_field [get_date_field()]
• day [get_day()]
714 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
• day_format [get_day_format()]
• extra_context
• http_method_names
• model
• month [get_month()]
• month_format [get_month_format()]
• pk_url_kwarg
• query_pk_and_slug
• queryset [get_queryset()]
• response_class [render_to_response()]
• slug_field [get_slug_field()]
• slug_url_kwarg
• template_engine
• template_name [get_template_names()]
• template_name_field
• template_name_suffix
• year [get_year()]
• year_format [get_year_format()]
Methods
• as_view()
• dispatch()
• get()
• get_context_data()
• get_next_day()
• get_next_month()
• get_object()
• get_previous_day()
• get_previous_month()
• head()
• http_method_not_allowed()
• render_to_response()
• setup()
6.3. Built-in class-based views API 715
Django Documentation, Release 3.0.15.dev
6.3.7 Specification
Each request served by a class-based view has an independent state; therefore, it is safe to store state variables on the
instance (i.e., self.foo = 3 is a thread-safe operation).
A class-based view is deployed into a URL pattern using the as_view() classmethod:
urlpatterns = [
path('view/', MyView.as_view(size=42)),
]
Thread safety with view arguments
Arguments passed to a view are shared between every instance of a view. This means that you shouldn’t use a list,
dictionary, or any other mutable object as an argument to a view. If you do and the shared object is modified, the
actions of one user visiting your view could have an effect on subsequent users visiting the same view.
Arguments passed into as_view() will be assigned onto the instance that is used to service a request. Using the
previous example, this means that every request on MyView is able to use self.size. Arguments must correspond
to attributes that already exist on the class (return True on a hasattr check).
6.3.8 Base vs Generic views
Base class-based views can be thought of as parent views, which can be used by themselves or inherited from. They
may not provide all the capabilities required for projects, in which case there are Mixins which extend what base views
can do.
Django’s generic views are built off of those base views, and were developed as a shortcut for common usage patterns
such as displaying the details of an object. They take certain common idioms and patterns found in view development
and abstract them so that you can quickly write common views of data without having to repeat yourself.
Most generic views require the queryset key, which is a QuerySet instance; see Making queries for more information
about QuerySet objects.   bana django döümanında anlatılan bu konuyu aşağıdaki parçaya bağlı kalarak uzunca anlatırı mıxın , tüm konuşarı anlar

**Cevap:** Django'nun class-based views (sınıf tabanlı görünümler) API'si, web projelerinde yaygın olarak kullanılan çeşitli işlemleri gerçekleştirmek için hazır sınıflar sunar. Bu sınıflar, programcılara daha modüler ve tekrar kullanılabilir yapı taşları sağlayarak, projelerin bakımı ve geliştirilmesini kolaylaştırır. Class-based views (CBV) API, belirli işlevleri gerçekleştirmek için birden fazla sınıf ve mixin (karışım) sunar. Django'nun dahili CBV'leri temelde ikiye ayrılır: **Base Views** (Temel Görünümler) ve **Generic Class-based Views** (Genel Sınıf Tabanlı Görünümler).

### 1. Temel Sınıf Tabanlı Görünümler (Base Views)
Temel class-based views, bir projenin çeşitli bölümlerinde kullanılabilecek altyapı sağlar. Bu sınıflar, inheritance (kalıtım) yoluyla genişletilebilir ve projenin belirli ihtiyaçlarına göre özelleştirilebilir.

#### `View` Sınıfı
`View` sınıfı, Django'nun tüm class-based views'lerinin temelini oluşturur. Bir Django görünümünün nasıl çalıştığını tanımlar ve HTTP isteklerine nasıl yanıt verileceğini belirler. Bu sınıf, bir HTTP isteği alındığında çalışacak bir **method dispatching** (yöntem yönlendirme) mekanizmasına sahiptir.

- **Method Flowchart**:  
  1. `setup()`  
  2. `dispatch()`  
  3. `http_method_not_allowed()`  
  4. `options()`

##### Örnek `views.py`
```python
from django.http import HttpResponse
from django.views import View

class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
```

##### Örnek `urls.py`
```python
from django.urls import path
from myapp.views import MyView

urlpatterns = [
    path('mine/', MyView.as_view(), name='my-view'),
]
```

#### Önemli Yöntemler
1. **`setup()`**: İsteği (`request`) alır ve görünümün (`view`) temel değişkenlerini ayarlar.
2. **`dispatch()`**: İsteğin türüne göre (GET, POST, vb.) uygun yöntemi (`get()`, `post()`, vb.) çalıştırır.
3. **`http_method_not_allowed()`**: İzin verilmeyen bir HTTP metodu kullanıldığında çağrılır ve 405 yanıtı döner.
4. **`options()`**: OPTIONS HTTP isteği için yanıt verir ve desteklenen HTTP yöntemlerini belirtir.

#### `TemplateView`
`TemplateView` sınıfı, bir template (şablon) kullanarak HTTP isteğine yanıt verir. Genellikle sabit bir sayfa sunmak için kullanılır (örneğin, anasayfa). Şablon adı ve ek bağlam verileri görünüm sınıfında tanımlanır.

##### Örnek `views.py`
```python
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context
```

##### Örnek `urls.py`
```python
from django.urls import path
from myapp.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
```

#### `RedirectView`
`RedirectView`, bir URL'ye yönlendirme yapmak için kullanılır. Bu yönlendirme sabit bir URL'ye olabileceği gibi dinamik olarak da belirlenebilir. Örneğin, URL parametreleri kullanılarak hedef URL dinamik hale getirilebilir.

##### Örnek `views.py`
```python
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from articles.models import Article

class ArticleCounterRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        article.update_counter()
        return super().get_redirect_url(*args, **kwargs)
```

##### Örnek `urls.py`
```python
from django.urls import path
from myapp.views import ArticleCounterRedirectView

urlpatterns = [
    path('counter/<int:pk>/', ArticleCounterRedirectView.as_view(), name='article-counter'),
]
```

### 2. Genel Sınıf Tabanlı Görünümler (Generic Class-based Views)
Django'nun generic views (genel görünümleri), verilerin görüntülenmesi ve düzenlenmesi gibi yaygın işlemler için kullanılır. Bu görünümler, CRUD (Create, Read, Update, Delete) işlemleri gibi yaygın görevler için özelleştirilmiş işlevsellik sağlar.

#### `DetailView`
`DetailView`, bir modelin detaylarını görüntülemek için kullanılır. Görünüm işlevini gerçekleştirirken `self.object` nesnesi, üzerinde işlem yapılan objeyi içerir.

##### Örnek `views.py`
```python
from django.views.generic.detail import DetailView
from articles.models import Article

class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
```

##### Örnek `urls.py`
```python
from django.urls import path
from myapp.views import ArticleDetailView

urlpatterns = [
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
]
```

#### `ListView`
`ListView`, bir modelin nesnelerinin listesini göstermek için kullanılır. Bu görünümde, `self.object_list` nesnesi, işlem yapılan nesnelerin listesini içerir.

##### Örnek `views.py`
```python
from django.views.generic.list import ListView
from articles.models import Article

class ArticleListView(ListView):
    model = Article
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
```

##### Örnek `urls.py`
```python
from django.urls import path
from myapp.views import ArticleListView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
]
```

### 3. Düzenleme Görünümleri (Editing Views)
Django'nun generic editing views sınıfları, veri ekleme, güncelleme ve silme işlemlerini kolaylaştırır. **`CreateView`**, **`UpdateView`** ve **`DeleteView`** gibi sınıflar, veri tabanındaki nesneler üzerinde CRUD işlemleri yapmayı sağlar.

#### `CreateView`
Bir modelin yeni bir örneğini oluşturmak için kullanılır. Form gönderimi başarılı olduğunda, form verilerini kaydeder ve belirlenen bir URL'ye yönlendirir.

##### Örnek `views.py`
```python
from django.views.generic.edit import CreateView
from myapp.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['name']
```

##### Örnek `urls.py`
```python
from django.urls import path
from myapp.views import AuthorCreate

urlpatterns = [
    path('author/add/', AuthorCreate.as_view(), name='author-add'),
]
```

#### `UpdateView`
Bir model nesnesini güncellemek için kullanılır. Mevcut bir nesne seçilip formda düzenlenebilir ve güncellenen bilgiler kaydedilebilir.

##### Örnek `views.py`
```python
from django.views.generic.edit import UpdateView
from myapp.models import Author

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']
    template_name_suffix = '_update_form'
```

##### Örnek `urls.py`
```python
from django.urls import path
from myapp.views import AuthorUpdate

urlpatterns = [
    path('author/<int:pk>/edit/', AuthorUpdate.as_view(), name='author-edit'),
]
```

#### `DeleteView`
Bir model nesnesini silmek için kullanılır. GET isteği ile silme onayı sayfası gösterilir, POST isteği ile silme işlemi gerçekleştirilir.

##### Örnek `views.py`
```python
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from myapp.models import Author

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')
```

##### Örnek `urls.py`
```python
from django.urls import path
from myapp.views import AuthorDelete

urlpatterns = [
    path('author/<int:pk>/delete/', AuthorDelete.as_view(), name='author-delete'),
]
```

### 4. Tarih Bazlı Görünümler (Date-based Views)
Tarih bazlı görünümler, veri modellerindeki tarih alanlarına göre listeleme ve ayrıntılı gösterim gibi işlemleri kolaylaştırır. Bu sınıflar, makaleler veya blog gönderileri gibi tarih bazlı içeriklerin yönetimi için kullanışlıdır.

#### `ArchiveIndexView`
Bu görün

**Cevap:** üm, en son içerikleri tarih sırasına göre listelemek için kullanılır.

#### `YearArchiveView`, `MonthArchiveView`, `WeekArchiveView`, `DayArchiveView`
Bu görünümler, belirli bir yıl, ay, hafta veya güne ait içerikleri listelemek için kullanılır.

#### `DateDetailView`
Belirli bir tarihteki tekil bir nesneyi göstermek için kullanılır.

---

Bu şekilde Django'nun class-based views yapısı, geliştiricilere hazır fonksiyonlar sunarak projeleri hızlı ve verimli bir şekilde inşa etmeyi sağlar. Görünümler modülerdir ve inheritance (kalıtım) yapısıyla genişletilebilir, ayrıca mixin yapılarıyla işlevsellik daha da esnek hale getirilebilir.

***Soru:*** Konuyu biraz daha açıklar mısın sana attığım kaynaklardan faydalan ve onun aynısını açıkal

**Cevap:** Django’nun **class-based views** (sınıf tabanlı görünümler) API’si, web uygulamalarındaki çeşitli işlemleri gerçekleştirmek için kullanılabilen, modüler ve genişletilebilir görünümler sunar. Bu görünümler, genellikle veri görüntüleme, veri düzenleme gibi sık yapılan işlemleri soyutlayarak geliştiricilere hızlı bir şekilde işlevsel kod yazma imkanı verir. 

Class-based views (CBV) API’sinde temel iki yaklaşım vardır: **Base views** ve **Generic views**. Base views, en temel işlevleri sağlayan sınıflardır, bu sınıflar doğrudan kullanılabilir veya genişletilebilir. Generic views ise, sık kullanılan işlemler (detay görüntüleme, listeleme, oluşturma, düzenleme, silme) için önceden hazırlanmış CBV'lerdir. Generic views, daha karmaşık projelerde işlerin hızlanmasına yardımcı olur. 

#### 1. **Base Views (Temel Görünümler)**
Django’nun class-based views mimarisi, basit işlevlerden daha karmaşık işlevlere kadar birçok yapıyı destekler. Temel sınıflar, bu yapıların çekirdeğini oluşturur. Django’nun en temel CBV sınıfı `View` sınıfıdır. Diğer tüm class-based views bu sınıftan türetilir.

- **`View` Sınıfı**:
    - `View` sınıfı, tüm CBV'lerin temelini oluşturan ana sınıftır. Diğer tüm CBV'ler bu sınıfı genişleterek kendi işlevselliklerini ekler. Örneğin, bir HTTP isteği alındığında, `dispatch()` yöntemi bu isteğin türünü (GET, POST gibi) analiz eder ve uygun metodu (`get()`, `post()`) çağırır.

**Method Flowchart (Yöntem Akış Şeması)**:
1. `setup()`: İstek geldiğinde görünümün temel değişkenlerini (örneğin `request`, `args`, `kwargs`) ayarlar.
2. `dispatch()`: HTTP isteğinin türüne göre ilgili yöntemi çağırır. GET isteği varsa `get()` metodunu çağırır, POST isteği varsa `post()` metodunu çağırır vb.
3. `http_method_not_allowed()`: Eğer HTTP isteği desteklenmeyen bir metotla yapılırsa (örneğin PATCH desteklenmiyorsa ama PATCH isteği yapılırsa), bu yöntem çalışır ve 405 yanıtı (HTTP Method Not Allowed) döner.
4. `options()`: Bu yöntem, OPTIONS HTTP isteğini işler ve hangi HTTP yöntemlerinin desteklendiği hakkında bilgi verir.

##### Örnek `views.py` Kullanımı:
```python
from django.http import HttpResponse
from django.views import View

class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
```

##### Örnek `urls.py` Kullanımı:
```python
from django.urls import path
from myapp.views import MyView

urlpatterns = [
    path('mine/', MyView.as_view(), name='my-view'),
]
```

- **`http_method_names`**: `View` sınıfı, varsayılan olarak şu HTTP yöntemlerini kabul eder: `['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']`. Bir görünümde bu listede olmayan bir HTTP metodu kullanılırsa, `http_method_not_allowed()` çağrılır.

- **`as_view(**initkwargs)`**: Bu sınıf metodu, görünümü çağrılabilir hale getirir. Örneğin, bir `request` aldığında, `MyView.as_view()` metodunu çağırabilir ve istek üzerine yanıt verir. Bu metot, URL desenlerinde kullanılmak üzere `MyView` gibi sınıfların `view` olarak çağrılabilmesine olanak tanır.

---

#### 2. **TemplateView**
`TemplateView`, bir template'i (şablonu) render eden bir CBV'dir. Genellikle statik sayfalar veya ek veri gerektirmeyen basit sayfalar için kullanılır. Sadece bir şablon dosyası belirlenir ve bu şablon render edilir.

**Method Flowchart (Yöntem Akış Şeması)**:
1. `setup()`
2. `dispatch()`
3. `get_context_data()`: Görünümde kullanılacak bağlamı (context) oluşturur ve bu bağlamı şablona gönderir.
4. `render_to_response()`: Belirlenen şablonu render eder ve kullanıcıya geri döner.

##### Örnek `views.py` Kullanımı:
```python
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context
```

##### Örnek `urls.py` Kullanımı:
```python
from django.urls import path
from myapp.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
```

---

#### 3. **RedirectView**
`RedirectView`, bir URL'ye yönlendirme yapmak için kullanılır. Sabit bir URL'ye veya URL parametrelerine göre dinamik bir URL'ye yönlendirme yapabilir.

- **`get_redirect_url()`**: Hedef URL'yi oluşturur. Bu URL statik olabilir ya da URL parametreleri kullanarak dinamik olarak oluşturulabilir.

##### Örnek `views.py` Kullanımı:
```python
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from articles.models import Article

class ArticleCounterRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        article.update_counter()
        return super().get_redirect_url(*args, **kwargs)
```

##### Örnek `urls.py` Kullanımı:
```python
from django.urls import path
from myapp.views import ArticleCounterRedirectView

urlpatterns = [
    path('counter/<int:pk>/', ArticleCounterRedirectView.as_view(), name='article-counter'),
]
```

---

#### 4. **Generic Class-based Views**
Django’nun generic class-based views'leri, verilerin görüntülenmesi ve düzenlenmesi gibi yaygın işlemler için kullanılır. Bu CBV'ler, CRUD işlemleri (Create, Read, Update, Delete) gibi yaygın kullanım senaryolarına yönelik önceden tanımlanmış işlevsellik sunar.

##### **`DetailView`**
`DetailView`, bir model nesnesinin detaylarını görüntülemek için kullanılır. Bu görünüm işlevini gerçekleştirirken `self.object` nesnesi, üzerinde işlem yapılan objeyi içerir.

##### Örnek `views.py` Kullanımı:
```python
from django.views.generic.detail import DetailView
from articles.models import Article

class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
```

##### Örnek `urls.py` Kullanımı:
```python
from django.urls import path
from myapp.views import ArticleDetailView

urlpatterns = [
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
]
```

##### **`ListView`**
`ListView`, bir modelin nesnelerinin listesini görüntülemek için kullanılır. Bu görünüm işlevini gerçekleştirirken `self.object_list` nesnesi, işlem yapılan nesnelerin listesini içerir.

##### Örnek `views.py` Kullanımı:
```python
from django.views.generic.list import ListView
from articles.models import Article

class ArticleListView(ListView):
    model = Article
    paginate_by = 100  # Sayfalama yapmak isterseniz

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
```

##### Örnek `urls.py` Kullanımı:
```python
from django.urls import path
from myapp.views import ArticleListView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
]
```

---

#### 5. **Generic Editing Views**
Veri ekleme, güncelleme ve silme işlemleri için Django, generic editing views sağlar. Bu sınıflar sayesinde form işlemleri kolaylıkla yapılabilir. Örneğin, `CreateView` yeni bir model nesnesi oluşturmak için, `UpdateView` ise mevcut bir nesneyi düzenlemek için kullanılır.

##### **`CreateView`**
Bir modelin yeni bir örneğini oluşturmak için kullanılır. Form gönderildiğinde veriler kaydedilir ve bir başarı URL’sine yönlendirilir.

##### Örnek `views.py` Kullanımı:
```python
from django.views.generic.edit import CreateView
from myapp.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['name']
```

##### Örnek `urls.py` Kullanımı:
```python
from django.urls import

**Cevap:** path
from myapp.views import AuthorCreate

urlpatterns = [
    path('author/add/', AuthorCreate.as_view(), name='author-add'),
]
```

##### **`UpdateView`**
Mevcut bir model nesnesini güncellemek için kullanılır. Kullanıcı, formda güncelleme yaptıktan sonra bu değişiklikler kaydedilir.

##### Örnek `views.py` Kullanımı:
```python
from django.views.generic.edit import UpdateView
from myapp.models import Author

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']
    template_name_suffix = '_update_form'
```

##### Örnek `urls.py` Kullanımı:
```python
from django.urls import path
from myapp.views import AuthorUpdate

urlpatterns = [
    path('author/<int:pk>/edit/', AuthorUpdate.as_view(), name='author-edit'),
]
```

##### **`DeleteView`**
Bir model nesnesini silmek için kullanılır. GET isteği ile onay sayfası gösterilir, POST isteği ile silme işlemi yapılır.

##### Örnek `views.py` Kullanımı:
```python
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from myapp.models import Author

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')
```

##### Örnek `urls.py` Kullanımı:
```python
from django.urls import path
from myapp.views import AuthorDelete

urlpatterns = [
    path('author/<int:pk>/delete/', AuthorDelete.as_view(), name='author-delete'),
]
```

---

Bu yapıların tümü, Django’nun class-based views API’sinin sunduğu esneklik ve işlevsellik ile projelerde verimli ve modüler kod yazmayı mümkün kılar.

***Soru:*** peki normal views lerle ne gibi farklılıkları vardır hangi durumda kullanılmaz tüm işlemlerde kullanılur mı

**Cevap:** Django’da **class-based views** (CBV) ve **function-based views** (FBV) iki farklı yaklaşımı temsil eder. Her iki yöntem de projelerde kullanılır, ancak bazı durumlarda bir yöntem diğerine göre daha uygun olabilir. CBV'ler, view fonksiyonlarını sınıf bazlı hale getirerek tekrar kullanılabilirliği, genişletilebilirliği ve modülerliği artırır. Öte yandan, FBV'ler daha basit ve anlaşılır bir yapı sunar. Her iki yaklaşımın da kendine özgü avantajları ve kullanım durumları vardır.

### Class-based Views (CBV) ve Function-based Views (FBV) Arasındaki Farklılıklar

1. **Modülerlik ve Tekrar Kullanılabilirlik**:
   - **CBV**'ler modüler ve tekrar kullanılabilir yapıdadır. Aynı işlevleri farklı CBV'ler arasında paylaşmak, miras alma (inheritance) veya mixin kullanımı ile mümkündür. Bu durum, aynı kodu tekrar yazma ihtiyacını azaltır ve DRY (Don't Repeat Yourself) ilkesine uyar.
   - **FBV**'lerde ise her bir görünüm için işlevler ayrı ayrı yazılır. Fonksiyonlar tekrar kullanılabilir, ancak CBV'deki gibi miras alma veya mixin gibi olanaklar yoktur. Fonksiyonlar daha izole ve belirli işlemler için yazılır.

2. **Basitlik**:
   - **FBV**'ler genellikle daha basit ve doğrudandır. Küçük projelerde veya tek bir işlevi olan görünümlerde FBV'ler daha anlaşılır ve hızlı bir çözüm sunar. Tek bir HTTP isteğine yanıt veren basit bir görünüm için bir fonksiyon yazmak genellikle yeterlidir.
   - **CBV**'ler ise daha fazla yapı ve kurulum gerektirir. CBV'lerde birçok şey sınıflar ve yöntemler etrafında döner, bu nedenle basit işlemler için fazla karmaşık gelebilir. Ancak daha karmaşık projelerde CBV'ler daha iyi ölçeklenir.

3. **Kod Tekrarı ve Genişletilebilirlik**:
   - **CBV**'ler miras alma ve mixin kullanımı sayesinde daha genişletilebilir bir yapı sunar. Bir sınıfı farklı görünümler arasında paylaşarak veya mixin'lerle işlevsellik ekleyerek çok fazla kod tekrarı yapılmadan genişletme sağlanabilir. Örneğin, hem liste hem de detay görünümü sunan benzer bir model için CBV'ler oldukça faydalıdır.
   - **FBV**'lerde işlevselliği genişletmek daha fazla kod yazmayı gerektirebilir. Bir işlevi genişletmek veya tekrar kullanmak için manuel olarak kod yazmanız gerekebilir.

4. **Durum Yönetimi ve Durum Saklama**:
   - **CBV**'lerde her bir request (istek) ayrı bir sınıf örneği (instance) tarafından yönetilir. Sınıf içinde belirli bir durum (state) saklanabilir ve bu durum, isteğin tüm yaşam döngüsü boyunca kullanılabilir. Örneğin, bir formun doğrulanması ve hataların yönetimi CBV'lerde daha düzenli şekilde yapılabilir.
   - **FBV**'ler ise durum saklama işlevine sahip değildir. Eğer bir fonksiyonda belirli bir durumda veri tutmanız gerekiyorsa, bu veriyi manuel olarak yönetmek zorunda kalabilirsiniz.

5. **Karmaşık İşlemler**:
   - **CBV**'ler özellikle CRUD (Create, Read, Update, Delete) işlemleri için ideal olarak yapılandırılmıştır. `DetailView`, `ListView`, `CreateView`, `UpdateView`, `DeleteView` gibi hazır sınıflar, veri tabanındaki nesneler üzerinde işlem yapmayı son derece kolaylaştırır. Bu sınıflar sayesinde minimal kodla nesneler üzerinde karmaşık işlemler yapılabilir.
   - **FBV**'ler ise karmaşık işlemler için daha fazla manuel kod yazmayı gerektirir. CRUD işlemlerini FBV ile gerçekleştirmek elbette mümkündür, ancak her işlemi kendiniz kodlamanız gerekir.

---

### Hangi Durumlarda Class-based Views (CBV) Kullanılmamalıdır?

CBV’ler, her duruma uygun olmayabilir. Aşağıdaki durumlarda FBV kullanmak daha uygun olabilir:

1. **Basit veya Tek Adımlı İşlemler**:
   Eğer sadece tek bir HTTP isteğiyle (örneğin basit bir GET isteği ile) işlem yapmanız gerekiyorsa, **FBV**'ler genellikle daha hızlı ve doğrudan bir çözüm sunar. Basit bir görünüm fonksiyonu, bir sınıf yapısına göre daha kısa ve anlaşılır olabilir. Örneğin, statik bir HTML sayfası sunarken CBV yerine FBV kullanmak daha kolay olabilir.

   **FBV Örneği:**
   ```python
   from django.http import HttpResponse

   def my_view(request):
       return HttpResponse('Hello, World!')
   ```

2. **Özel Mantık Gerektiren Görünümler**:
   Bazı durumlarda, CBV'lerin sunduğu yapı fazlasıyla esnek olmayabilir. Eğer görünüm, çok özel bir mantık içeriyorsa ve bu mantığın CBV'lerdeki yerleşik akışla uyumsuz olduğunu düşünüyorsanız, **FBV** kullanmak daha uygun olabilir. Çünkü FBV'de tüm kontrol sizdedir ve işleyişi daha basitçe yönetebilirsiniz.

3. **Zaman Yönetimi veya Performans Sorunları**:
   CBV'ler her ne kadar modülerlik sağlasa da, bazı durumlarda gereksiz yere fazla yapı ve soyutlama ekleyebilir. Özellikle küçük ve basit projelerde CBV'ler gereksiz bir karmaşıklık katmanı oluşturabilir. Bu durumlarda **FBV** daha hızlı ve basit bir çözüm olabilir.

### Tüm İşlemlerde CBV Kullanılabilir Mi?

Evet, **CBV’ler** hemen hemen tüm işlemler için kullanılabilir, çünkü Django'nun class-based views yapısı çok esnektir ve çoğu senaryoyu kapsayacak kadar genişletilebilir. Özellikle:

- **Veri Listeleme ve Detay Görüntüleme** işlemlerinde `ListView` ve `DetailView` CBV'leri kullanılabilir.
- **Veri Ekleme, Güncelleme ve Silme** işlemlerinde `CreateView`, `UpdateView` ve `DeleteView` gibi CBV'ler mükemmel şekilde iş görür.
- **Tarih Tabanlı Görüntüleme** işlemlerinde `ArchiveIndexView`, `YearArchiveView`, `MonthArchiveView` gibi CBV'ler kullanılarak tarih tabanlı arşivler kolayca yönetilebilir.

Ancak CBV'ler, iş mantığının fazlasıyla özel olduğu veya basit işlemler için gereğinden fazla yapı gerektirdiği durumlarda tercih edilmeyebilir.

---

### Sonuç

**CBV**'ler, genişletilebilirlik, modülerlik ve kod tekrarı yapmama gibi avantajlar sunarken, **FBV**'ler daha basit, doğrudan ve hızlı çözümler sunar. İki yapı arasında tercih yapmak tamamen projenizin karmaşıklığına ve ihtiyaçlarına bağlıdır:

- Eğer proje karmaşık ve genişletilebilir olmalıysa, **CBV**'ler en iyi seçimdir.
- Eğer proje küçük ve basitse veya görünüm çok özelleşmiş bir mantık içeriyorsa, **FBV** kullanmak daha mantıklı olabilir.

Her iki yaklaşımı da projede bir arada kullanmak mümkündür, bu yüzden en uygun çözümü sağlamak için hangisinin daha iyi olduğuna proje bazında karar vermek önemlidir.

***Soru:*** 6.4 Clickjacking Protection
The clickjacking middleware and decorators provide easy-to-use protection against clickjacking. This type of attack
occurs when a malicious site tricks a user into clicking on a concealed element of another site which they have loaded
in a hidden frame or iframe.
6.4.1 An example of clickjacking
Suppose an online store has a page where a logged in user can click “Buy Now” to purchase an item. A user has
chosen to stay logged into the store all the time for convenience. An attacker site might create an “I Like Ponies”
button on one of their own pages, and load the store’s page in a transparent iframe such that the “Buy Now” button
is invisibly overlaid on the “I Like Ponies” button. If the user visits the attacker’s site, clicking “I Like Ponies” will
cause an inadvertent click on the “Buy Now” button and an unknowing purchase of the item.
716 Chapter 6. API Reference
Django Documentation, Release 3.0.15.dev
6.4.2 Preventing clickjacking
Modern browsers honor the X-Frame-Options HTTP header that indicates whether or not a resource is allowed to load
within a frame or iframe. If the response contains the header with a value of SAMEORIGIN then the browser will only
load the resource in a frame if the request originated from the same site. If the header is set to DENY then the browser
will block the resource from loading in a frame no matter which site made the request.
Django provides a few ways to include this header in responses from your site:
1. A middleware that sets the header in all responses.
2. A set of view decorators that can be used to override the middleware or to only set the header for certain views.
The X-Frame-Options HTTP header will only be set by the middleware or view decorators if it is not already
present in the response.
6.4.3 How to use it
Setting X-Frame-Options for all responses
To set the same X-Frame-Options value for all responses in your site, put 'django.middleware.
clickjacking.XFrameOptionsMiddleware' to MIDDLEWARE:
MIDDLEWARE = [
...
'django.middleware.clickjacking.XFrameOptionsMiddleware',
...
]
This middleware is enabled in the settings file generated by startproject.
By default, the middleware will set the X-Frame-Options header to DENY for every outgoing HttpResponse.
If you want any other value for this header instead, set the X_FRAME_OPTIONS setting:
X_FRAME_OPTIONS = 'SAMEORIGIN'
The default value of the X_FRAME_OPTIONS setting was changed from SAMEORIGIN to DENY.
When using the middleware there may be some views where you do not want the X-Frame-Options header set.
For those cases, you can use a view decorator that tells the middleware not to set the header:
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def ok_to_load_in_a_frame(request):
return HttpResponse("This page is safe to load in a frame on any site.")
Note: If you want to submit a form or access a session cookie within a frame or iframe, you may need to modify the
CSRF_COOKIE_SAMESITE or SESSION_COOKIE_SAMESITE settings.
Setting X-Frame-Options per view
To set the X-Frame-Options header on a per view basis, Django provides these decorators:
6.4. Clickjacking Protection 717
Django Documentation, Release 3.0.15.dev
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
@xframe_options_deny
def view_one(request):
return HttpResponse("I won't display in any frame!")
@xframe_options_sameorigin
def view_two(request):
return HttpResponse("Display in a frame if it's from the same origin as me.")
Note that you can use the decorators in conjunction with the middleware. Use of a decorator overrides the middleware.
6.4.4 Limitations
The X-Frame-Options header will only protect against clickjacking in a modern browser. Older browsers will
quietly ignore the header and need other clickjacking prevention techniques.
Browsers that support X-Frame-Options
• Internet Explorer 8+
• Edge
• Firefox 3.6.9+
• Opera 10.5+
• Safari 4+
• Chrome 4.1+
See also
A complete list of browsers supporting X-Frame-Options.  bana bu konuyu ayrıntılı açıklar mısın

**Cevap:** ### Clickjacking Protection Nedir?

**Clickjacking** (tıklama hırsızlığı), bir saldırganın, kullanıcının farkında olmadan bir web sitesindeki gizli bir öğeye tıklamasını sağladığı bir tür güvenlik saldırısıdır. Bu saldırı, genellikle bir web sayfasının içeriğinin başka bir web sitesinin bir iframe içinde yüklenmesiyle gerçekleştirilir. Kullanıcı, saldırganın web sitesinde görünen bir düğmeye tıkladığını düşünürken, aslında başka bir web sitesindeki gizli bir düğmeye (örneğin bir "Buy Now" düğmesine) tıklamış olur.

### 1. Clickjacking'e Bir Örnek

Örneğin, bir çevrimiçi mağazada kullanıcıların bir ürünü satın almak için "Buy Now" (Satın Al) düğmesine tıklayabileceği bir sayfa olduğunu düşünün. Kullanıcı, bu siteye sürekli giriş yapmış durumda. Bir saldırgan, kendi web sitesinde görünüşte masum bir "I Like Ponies" (Ponileri Seviyorum) düğmesi oluşturabilir ve mağazanın "Buy Now" düğmesinin bulunduğu sayfasını şeffaf bir iframe içinde bu düğmenin üstüne yerleştirebilir. Kullanıcı, saldırganın sitesinde "I Like Ponies" düğmesine tıkladığında, aslında mağazanın "Buy Now" düğmesine tıklayarak ürünü satın almış olur. Bu durumda, kullanıcı farkında olmadan bir işlem yapmış olur.

### 2. Clickjacking'i Önlemek

Modern web tarayıcıları, **X-Frame-Options** adında bir HTTP başlığını destekler. Bu başlık, bir kaynağın bir çerçeve veya iframe içinde yüklenip yüklenemeyeceğini belirtir. Bu başlık iki farklı değer alabilir:

- **`SAMEORIGIN`**: Kaynak sadece isteğin aynı site (aynı domain) üzerinden geldiği durumlarda bir çerçeve içinde yüklenebilir.
- **`DENY`**: Kaynak hiçbir durumda bir çerçeve veya iframe içinde yüklenemez.

Django, sitenizdeki yanıtlar için bu başlığı kolayca eklemenizi sağlayan birkaç yöntem sunar:
1. **Middleware**: Tüm yanıtlar için bu başlığı ayarlar.
2. **View Decorators**: Middleware’i geçersiz kılmak veya yalnızca belirli görünümler için başlığı ayarlamak için kullanılabilir.

Eğer yanıt zaten **X-Frame-Options** başlığı içeriyorsa, Django'nun middleware'i veya dekoratörleri bu başlığı değiştirmez.

### 3. Nasıl Kullanılır?

#### Tüm Yanıtlar İçin X-Frame-Options Ayarlama

Sitenizdeki tüm yanıtlar için aynı **X-Frame-Options** değerini ayarlamak için, `MIDDLEWARE` ayarınıza **`XFrameOptionsMiddleware`** eklemeniz yeterlidir:

```python
MIDDLEWARE = [
    ...
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ...
]
```

Bu middleware, varsayılan olarak her çıkan yanıt için **X-Frame-Options** başlığını **`DENY`** olarak ayarlar. Yani, hiçbir sayfanız başka bir sitede iframe içinde yüklenemez. Eğer farklı bir değer ayarlamak isterseniz (örneğin, sadece aynı kökene sahip istekler için iframe içinde yüklenebilir olmasını istiyorsanız), **`X_FRAME_OPTIONS`** ayarını değiştirebilirsiniz:

```python
X_FRAME_OPTIONS = 'SAMEORIGIN'
```

#### Belirli Görünümlerde X-Frame-Options Başlığını Kaldırma

Eğer bazı görünümler için **X-Frame-Options** başlığının ayarlanmasını istemiyorsanız, **`xframe_options_exempt`** adlı bir view dekoratörünü kullanabilirsiniz:

```python
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def ok_to_load_in_a_frame(request):
    return HttpResponse("Bu sayfa herhangi bir sitede iframe içinde yüklenebilir.")
```

Bu dekoratör, middleware tarafından varsayılan olarak eklenen **X-Frame-Options** başlığını, bu belirli görünümde kaldırır. Böylece bu sayfa başka sitelerde bir iframe içinde yüklenebilir hale gelir.

**Not**: Eğer bir formu bir iframe içinde göndermek veya bir oturum çerezine (session cookie) erişmek istiyorsanız, **CSRF_COOKIE_SAMESITE** veya **SESSION_COOKIE_SAMESITE** ayarlarını değiştirmeniz gerekebilir. Bu ayarlar, çerezlerin aynı site politikalarına göre yönetilmesini sağlar.

#### Belirli Görünümler İçin X-Frame-Options Başlığını Ayarlama

Her bir görünüm için ayrı ayrı **X-Frame-Options** başlığını ayarlamak isterseniz, Django size iki farklı dekoratör sunar:

- **`xframe_options_deny`**: Bu dekoratör, yanıtın hiçbir iframe içinde yüklenmemesini sağlar.
- **`xframe_options_sameorigin`**: Bu dekoratör, yalnızca yanıtın aynı kökene sahip istekler için iframe içinde yüklenmesine izin verir.

##### Örnek Kullanım:
```python
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin

@xframe_options_deny
def view_one(request):
    return HttpResponse("Bu sayfa hiçbir çerçeve içinde görüntülenemez.")

@xframe_options_sameorigin
def view_two(request):
    return HttpResponse("Bu sayfa sadece aynı kökene sahip istekler için iframe içinde görüntülenebilir.")
```

Bu dekoratörler middleware ile birlikte kullanılabilir. Eğer bir görünümde hem middleware hem de dekoratör kullanılırsa, dekoratör middleware'i geçersiz kılar.

### 4. Clickjacking Korumasının Sınırları

**X-Frame-Options** başlığı, yalnızca modern tarayıcılar tarafından desteklenir. Eski tarayıcılar bu başlığı görmezden gelebilir ve bu tür tarayıcılarda clickjacking saldırılarına karşı korunma sağlanmaz. Modern tarayıcılar, bu başlığı destekleyerek iframe yüklemelerini kontrol eder.

**X-Frame-Options** başlığını destekleyen tarayıcılar şunlardır:
- Internet Explorer 8+
- Edge
- Firefox 3.6.9+
- Opera 10.5+
- Safari 4+
- Chrome 4.1+

Ancak, eski tarayıcılar (özellikle Internet Explorer'ın daha eski sürümleri) bu başlığı desteklemez. Bu nedenle, clickjacking'e karşı tam koruma sağlamak için ek önlemler gerekebilir. Örneğin, JavaScript tabanlı önlemler veya UI overlay (görsel örtü) teknikleri kullanılabilir.

### Sonuç

Django’nun clickjacking koruma mekanizmaları, sitenizi iframe içinde izinsiz yüklenmeye karşı korumak için güçlü bir çözüm sunar. **X-Frame-Options** başlığını kullanarak, sayfalarınızın sadece belirli durumlarda iframe içinde yüklenmesine izin verebilir veya tamamen engelleyebilirsiniz. Middleware ve dekoratörler sayesinde bu korumayı esnek bir şekilde uygulayabilirsiniz. Ancak unutmayın ki bu koruma sadece modern tarayıcılarda etkilidir; eski tarayıcılar için ek güvenlik önlemleri alınmalıdır.