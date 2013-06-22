from django.http import HttpResponseRedirect
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

import control_panel.urls
import securesync.urls
from kalite import settings
from feeds import RssSiteNewsFeed, AtomSiteNewsFeed


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^images/(.+)$', lambda request, path: HttpResponseRedirect('/static/images/' + path)),
    url(r'^securesync/', include(securesync.urls)),
)

urlpatterns += patterns('',
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:], 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
   
# Javascript translations
urlpatterns += patterns('',
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('ka-lite.locale')}, 'i18n_javascript_catalog'),
)

urlpatterns += patterns('central.views',
    url(r'^$', 'homepage', {}, 'homepage'), 
    url(r'^delete_admin/(?P<org_id>\w+)/(?P<user_id>\w+)/$', 'delete_admin', {}, 'delete_admin'), 
    url(r'^delete_invite/(?P<org_id>\w+)/(?P<invite_id>\w+)/$', 'delete_invite', {}, 'delete_invite'), 
    url(r'^accounts/', include('registration.urls')),
    
    # Organization
    url(r'^organization/$', 'org_management', {}, 'org_management'),
    url(r'^organization/(?P<org_id>\w+)/$', 'organization_form', {}, 'organization_form'),
    url(r'^organization/invite_action/(?P<invite_id>\w+)/$', 'org_invite_action', {}, 'org_invite_action'),

    # Zone, facility, device
    url(r'^organization/(?P<org_id>\w+)/', include(control_panel.urls)),

    url(r'^cryptologin/$', 'crypto_login', {}, 'crypto_login'), 
    url(r'^glossary/$', 'glossary', {}, 'glossary'),
    url(r'^addsubscription/$', 'add_subscription', {}, 'add_subscription'),
    url(r'^feeds/rss/$', RssSiteNewsFeed(), {}, 'rss_feed'),
    url(r'^feeds/atom/$', AtomSiteNewsFeed(), {}, 'atom_feed'),
    url(r'^faq/', include('faq.urls')),
)   
   
handler404 = 'central.views.handler_404'
handler500 = 'central.views.handler_500'

