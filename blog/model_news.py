import datetime

from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.formats import date_format
from django.utils.dateformat import DateFormat
from django.http import Http404
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from django.template.defaultfilters import slugify as django_slugify
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search import index
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from wagtailmetadata.models import MetadataPageMixin
from .blocks import OldBodyBlock
from wagtail.admin.edit_handlers import HelpPanel

from wagtail.contrib.table_block.blocks import TableBlock



class BlogNewsPage(RoutablePageMixin, Page):
    description = models.CharField(max_length=255, blank=True,verbose_name='Описание')

    content_panels = Page.content_panels + [FieldPanel("description", classname="full")]
    tags = models.ForeignKey(
        'blog.Tag',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Предыдущая связанная новость'
    )

    content_panels = Page.content_panels + [
            FieldPanel("tags",classname='full'),
    ]
    subpage_types = ['PostPage', 'BlogPostPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # https://docs.djangoproject.com/en/3.1/topics/pagination/#using-paginator-in-a-view-function
        paginator = Paginator(self.posts, 2)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.object_list.none()

        context["posts"] = posts
        return context

    def get_posts(self):
        q = BlogPostPage.objects.descendant_of(self).live().order_by("-post_date")
        print(q.count())
        print(q[0].full_url)

        return q

    @route(r"^(\d{4})/$")
    @route(r"^(\d{4})/(\d{2})/$")
    @route(r"^(\d{4})/(\d{2})/(\d{2})/$")
    def post_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.search_type = 'date'
        self.search_term = year
        self.posts = self.get_posts().filter(post_date__year=year)
        if month:
            df = DateFormat(datetime.date(int(year), int(month), 1))
            self.search_term = df.format('F Y')
            self.posts = self.posts.filter(post_date__month=month)
        if day:
            self.search_term = date_format(datetime.date(int(year), int(month), int(day)))
            self.posts = self.posts.filter(post_date__day=day)
        return self.render(request)

    @route(r"^(\d{4})/(\d{2})/(\d{2})/(.+)/$")
    def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
        post_page = self.get_posts().filter(slug=slug).first()
        if not post_page:
            raise Http404
        # here we render another page, so we call the serve method of the page instance
        return post_page.serve(request)

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = 'tag'
        self.search_term = tag
        self.posts = self.get_posts().filter(tags__slug=tag)
        return self.render(request)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.search_type = 'category'
        self.search_term = category
        self.posts = self.get_posts().filter(categories__blog_category__slug=category)
        return self.render(request)

    @route(r"^search/$")
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get("q", None)
        self.posts = self.get_posts()
        if search_query:
            self.search_term = search_query
            self.search_type = 'search'
            self.posts = self.posts.search(search_query)
        return self.render(request)

    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return self.render(request)

    def get_sitemap_urls(self, request=None):
        output = []
        posts = self.get_posts()
        for post in posts:
            post_date = post.post_date
            url = self.get_full_url(request) + self.reverse_subpage(
                'post_by_date_slug',
                args=(
                    post_date.year,
                    '{0:02}'.format(post_date.month),
                    '{0:02}'.format(post_date.day),
                    post.slug,
                )
            )

            output.append({
                'location': url,
                'lastmod': post.last_published_at
            })

        return output

    class Meta:
        verbose_name = "Лента новостей"


class BlogPostPage(RoutablePageMixin, Page):
    template = "blog/blog_news.html"

    header_image = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name='Изображения в заголовке'
    )
    post_date = models.DateTimeField(
        verbose_name="Время создания",help_text='Время отображаемое на сайте', default=datetime.datetime.today
    )

    body = StreamField(OldBodyBlock(), blank=True, verbose_name='Контент на странице')

    is_recl_0 = models.BooleanField(verbose_name='Не выводится в Яндекс.новостях', default=False)
    is_recl_1 = models.BooleanField(verbose_name='Не выводить на главной', default=False)
    is_recl_2 = models.BooleanField(verbose_name='Не выводить в индексе', default=False)
    is_recl_3 = models.BooleanField(verbose_name='Не дублировать', default=False)
    

    tags = ClusterTaggableManager(through="blog.PostPage2Tag", blank=True)
    related_page = ParentalKey("BlogPostPage", related_name="++",null=True,blank=True,on_delete=models.SET_NULL, verbose_name='Предыдущая связанная новость')
    # related_page = models.ForeignKey(
    #     'wagtailcore.Page',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='+',
        
    # )

    content_panels = Page.content_panels + [
        ImageChooserPanel("header_image"),
        FieldPanel("tags",classname='full'),
        PageChooserPanel('related_page', 'blog.BlogPostPage'),
        StreamFieldPanel("body"),
    ]

    settings_panels = [
        FieldPanel("post_date"),
        MultiFieldPanel([
        FieldPanel('is_recl_0'),
        FieldPanel('is_recl_1'),
        FieldPanel('is_recl_2'),
        FieldPanel('is_recl_3'),

    ], 'Найстройки отображения'),
     ] + Page.settings_panels 
    
    @cached_property
    def blog_page(self):
        return self.get_parent().specific

    @cached_property
    def canonical_url(self):
        # we should import here to avoid circular import
        from blog.templatetags.blogapp_tags import post_page_date_slug_url

        blog_page = self.blog_page
        return post_page_date_slug_url(self, blog_page)

    def get_sitemap_urls(self, request=None):
        return []

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Новость"

class PostPage2Tag(TaggedItemBase):
    content_object = ParentalKey("BlogPostPage", related_name="post_tags")

    @classmethod
    def tag_model(cls):
        from blog.models import Tag
        return Tag
