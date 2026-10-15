import pathlib, re, html, email.utils, datetime
exec(open("_build.py").read())

def now_eastern():
    # The office is in Georgia; a post goes up on Georgia's clock, not
    # Greenwich's.
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("America/New_York")).replace(tzinfo=None)
    except Exception:
        return datetime.datetime.now()

def goes_live(meta):
    """When a post may appear: its date at its `time:` line (24-hour Eastern,
    e.g. `time: 18:00`), or midnight when there is no time line. 2026-10-15:
    a post dated that day went up on the site at 4 a.m. while the Facebook
    copy was scheduled for 6 p.m.; the time line keeps the two together."""
    d=datetime.date.fromisoformat(meta["date"].strip())
    t=meta.get("time","").strip()
    hh,mm=(int(x) for x in t.split(":")) if t else (0,0)
    return datetime.datetime(d.year,d.month,d.day,hh,mm)

def load_posts(include_future=False):
    """Posts not yet due are scheduled, not published: they stay in posts/
    and out of the site until their date and time arrive (2026-10-03, so one
    approval can schedule the site and the Facebook Page together)."""
    out=[]
    now=now_eastern()
    for p in sorted(pathlib.Path("posts").glob("*.html"), reverse=True):
        raw=p.read_text(encoding="utf-8")
        head,body=raw.split("---",1)
        meta=dict(l.split(":",1) for l in head.strip().splitlines())
        title=meta["title"].strip(); date=meta["date"].strip()
        if not include_future and goes_live(meta) > now:
            print("scheduled, not built yet:", p.name, "(", goes_live(meta).strftime("%Y-%m-%d %H:%M"), "Eastern )")
            continue
        slug=p.stem+".html"
        out.append({"title":title,"date":date,"body":body.strip(),"slug":"post-"+slug})
    return out

def remove_unscheduled(posts):
    """A post page whose post is no longer due (moved to a later date) comes
    down; otherwise the old page stays up at its old address. Only touches
    generated post-YYYY-MM-DD-*.html pages at the top of the site."""
    keep={po["slug"] for po in posts}
    for f in pathlib.Path(".").glob("post-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.html"):
        if f.name not in keep:
            f.unlink(); print("taken down (not due):", f.name)

def build_posts():
    posts=load_posts()
    remove_unscheduled(posts)
    for po in posts:
        d=datetime.date.fromisoformat(po["date"])
        body=f"""
{docket(d.strftime("%B %d, %Y"),html.escape(po["title"]))}
<div class="wrap prose">
{po["body"]}
<p style="margin-top:2rem"><a href="index.html">&larr; All posts</a></p>
</div>"""
        page(po["slug"],po["title"]+" — Tripp Fitzner, District Attorney",po["title"],body)
    # RSS
    items=""
    for po in posts[:20]:
        d=datetime.date.fromisoformat(po["date"])
        pub=email.utils.format_datetime(datetime.datetime(d.year,d.month,d.day,12,0,0,tzinfo=datetime.timezone(datetime.timedelta(hours=-5))))
        items+=f"""<item><title>{html.escape(po['title'])}</title><link>https://middleda.org/{po['slug']}</link><guid>https://middleda.org/{po['slug']}</guid><pubDate>{pub}</pubDate><description><![CDATA[{po['body']}]]></description></item>"""
    rss=f"""<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>From the District Attorney — Tripp Fitzner</title><link>https://middleda.org/</link><description>Updates from the Office of the District Attorney, Middle Judicial Circuit of Georgia</description>{items}</channel></rss>"""
    pathlib.Path("feed.xml").write_text(rss,encoding="utf-8")
    print("built",len(posts),"posts + feed.xml")
    return posts

if __name__=="__main__":
    build_posts()
