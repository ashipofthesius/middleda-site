import pathlib, re, html, email.utils, datetime
exec(open("_build.py").read())

def today_eastern():
    # The office is in Georgia; a post dated today should appear today, not
    # when it is already today in Greenwich.
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("America/New_York")).date()
    except Exception:
        return datetime.date.today()

def load_posts(include_future=False):
    """Posts dated after today are scheduled, not published: they stay in
    posts/ and out of the site until their date arrives (2026-10-03, so one
    approval can schedule the site and the Facebook Page for the same day)."""
    out=[]
    today=today_eastern()
    for p in sorted(pathlib.Path("posts").glob("*.html"), reverse=True):
        raw=p.read_text(encoding="utf-8")
        head,body=raw.split("---",1)
        meta=dict(l.split(":",1) for l in head.strip().splitlines())
        title=meta["title"].strip(); date=meta["date"].strip()
        if not include_future and datetime.date.fromisoformat(date) > today:
            print("scheduled, not built yet:", p.name, "(", date, ")")
            continue
        slug=p.stem+".html"
        out.append({"title":title,"date":date,"body":body.strip(),"slug":"post-"+slug})
    return out

def build_posts():
    posts=load_posts()
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
