## Introduction

This project is from my book [Build Blog With Wagtail CMS (second version)](https://leanpub.com/buildblogwithwagtailcms/)

Note: If you are interested in `React`, `Storybook` and `Wagtail`, you can check [wagtail-react-blog](https://github.com/AccordBox/wagtail-react-blog)

## Objective

This book will teach you how to build a modern blog with `Wagtail CMS`

By the end of this course, you will be able to:

1. Understand `Docker` and use `Docker Compose` to do development
1. Create blog models to work with Wagtail.
1. Import `Bootstrap` themes to the blog.
1. Use `PDB` and `Django shell` to debug, test code and check data in terminal.
1. Learn to use `RoutablePage` and add `Date` to the post url.
1. Build `Pagination` component and correctly handle querystring.
1. Make the blog supports wirting in `Markdown` and `Latex`.
1. Create contact page using Wagtail `FormBuilder`
1. Build menu, meta tags, sitemap, robots.txt for better SEO.
1. Build comment system based on `django-contrib-comments` which support `Generic Relations`
1. Understand how to use `Webpack` to bundle frontend assets and make it work with Django project.
1. Learn SCSS and use it to customize style in quick way.
1. Use `Tribute.js`, `Axios` to add `Mention` and `Emoji` support to the comment form.
1. Learn `Async/Await`, `Promise` and the benefits.
1. Deploy the production app to DigitalOcean

## Tech

* Python 3.8
* Django 3.1
* Wagtail 2.11
* Node 12
* Webpack 5
* jQuery 3.5.1
* Bootstrap 4.5
* Tribute.js
* Axios

## How to run on local

You need Docker and Docker Compose and you can install it here [Get Docker](https://docs.docker.com/get-docker/)

```bash
$ git clone https://github.com/AccordBox/wagtail-bootstrap-blog
$ cd wagtail-bootstrap-blog
# build and lanch app
$ docker-compose up --build
```

Now open a new terminal to import data and change password.

```bash
$ docker-compose exec web python manage.py load_initial_data
$ docker-compose exec web python manage.py changepassword admin
```

Now you can check on

* [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Demo

The demo is also online if you want to check.

* [Wagtail Blog Demo](http://wagtail-blog.accordbox.com)

## ScreenShot

![](./misc/comment.gif)

# wagteil_demo_boost
