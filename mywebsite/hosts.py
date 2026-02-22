from django_hosts import patterns, host

host_patterns = patterns(
    "",
    host(r"", "home.urls", name="home"),
    host(r"about", "about.urls", name="about"),
    host(r"blog", "blog.urls", name="blog"),
    host(r"ticket", "ticket.urls", name="ticket"),
)