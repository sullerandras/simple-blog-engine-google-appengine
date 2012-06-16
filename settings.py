# set this to "/blog", if you want to publish the blog engine on the http://<your domain>/blog url.
# it is useful if you want to use one domain for several services, like "/wiki", "/blog", "/todo", etc.
BASE = '/blog'

# the application's public URLs
URLS = {
    'index': BASE + '/',
    'new_blog_entry': BASE + '/new',
    'edit_blog_entry': BASE + '/edit',
}