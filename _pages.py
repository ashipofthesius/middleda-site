import datetime, html
exec(open("_build.py").read())
exec(open("_posts.py").read().split('if __name__')[0])

# ---------- HOME: blog front ----------
posts=load_posts()

def _excerpt(body, words=34):
    """The first paragraph with words in it (the first <p> is often the
    picture), cut at a word boundary."""
    import re
    for para in re.findall(r"<p[^>]*>(.*?)</p>", body, flags=re.S):
        text=re.sub(r"<[^>]+>","",para).strip()
        if text:
            w=text.split()
            return html.escape(" ".join(w[:words]))+("&hellip;" if len(w)>words else "")
    return ""

def _thumb(body):
    import re
    m=re.search(r'<img[^>]*src="([^"]+)"[^>]*?(?:alt="([^"]*)")?[^>]*>', body)
    if not m: return ""
    alt=re.search(r'alt="([^"]*)"', m.group(0))
    return f'<a class="entry-pic" href="{{slug}}" tabindex="-1" aria-hidden="true"><img src="{m.group(1)}" alt="{alt.group(1) if alt else ""}" loading="lazy"></a>'

def post_row(po):
    """One post in a list: small picture, date, title, a few lines, the link.
    2026-10-15: the home page used each post's first paragraph as its
    preview, which for the photo posts was the full-size picture, so the
    front page was one long scroll of pictures."""
    d=datetime.date.fromisoformat(po["date"])
    pic=_thumb(po["body"]).replace("{slug}",po["slug"])
    return f"""<article class="entry{' has-pic' if pic else ''}">{pic}<div class="entry-text">
<div class="entry-date">{d.strftime("%B %d, %Y").replace(" 0"," ")}</div>
<h3 class="entry-title"><a href="{po['slug']}">{html.escape(po['title'])}</a></h3>
<p class="entry-excerpt">{_excerpt(po["body"])}</p>
<a class="entry-more" href="{po['slug']}">Read the post &rarr;</a></div></article>"""

HOME_COUNT=5
cards="".join(post_row(po) for po in posts[:HOME_COUNT])
if len(posts)>HOME_COUNT:
    cards+=f'<p class="entry-all"><a href="blog.html">All {len(posts)} posts &rarr;</a></p>'
elif posts:
    cards+='<p class="entry-all"><a href="blog.html">All posts &rarr;</a></p>'

# ---------- BLOG: every post, ten to a page ----------
PER_PAGE=10
pages_n=max(1,-(-len(posts)//PER_PAGE))
def blog_path(n): return "blog.html" if n==1 else f"blog-{n}.html"
for n in range(1,pages_n+1):
    chunk=posts[(n-1)*PER_PAGE:n*PER_PAGE]
    nav=""
    if pages_n>1:
        newer=f'<a href="{blog_path(n-1)}">&larr; Newer posts</a>' if n>1 else "<span></span>"
        older=f'<a href="{blog_path(n+1)}">Older posts &rarr;</a>' if n<pages_n else "<span></span>"
        nav=f'<nav class="entry-pages" aria-label="More posts">{newer}<span class="entry-pageno">Page {n} of {pages_n}</span>{older}</nav>'
    body=f"""
{docket("The Blog" if n==1 else f"Page {n}","From the District Attorney")}
<div class="wrap entries">
{"".join(post_row(po) for po in chunk) or '<p>No posts yet.</p>'}
{nav}
<p class="entry-all"><a href="index.html">&larr; Home</a></p>
</div>"""
    page(blog_path(n),"From the District Attorney"+("" if n==1 else f", page {n}")+" — Tripp Fitzner",
         "Posts from Tripp Fitzner, District Attorney of the Middle Judicial Circuit of Georgia.",body)
# a page left over from a time when there were more posts comes down
import pathlib as _pl
for f in _pl.Path(".").glob("blog-[0-9]*.html"):
    if int(f.stem.split("-")[1])>pages_n: f.unlink()

home=f"""
<div class="hero" style="padding-bottom:1.6rem">
<div class="kicker">The State's Lawyer for Five Counties</div>
<h1>Murder, rape, and crimes against children get tried here, not talked about.</h1>
<div class="counties"><span>Candler</span><span>Emanuel</span><span>Jefferson</span><span>Toombs</span><span>Washington</span></div>
</div>

{docket("The Blog","From the District Attorney")}
<div class="wrap entries">
{cards}
<p style="margin-top:2rem"><a href="https://www.facebook.com/TrippFitznerDA" style="display:inline-block;background:var(--navy);color:#fff;text-decoration:none;font-family:'Archivo',Arial,sans-serif;font-size:.85rem;letter-spacing:.18em;text-transform:uppercase;padding:.85rem 1.6rem;border:1px solid var(--ink);box-shadow:4px 4px 0 var(--garnet)"><svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor" style="vertical-align:-2px;margin-right:.6rem"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.09 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.7 4.53-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.51c-1.49 0-1.96.93-1.96 1.89v2.26h3.33l-.53 3.49h-2.8V24C19.61 23.09 24 18.1 24 12.07z"/></svg>Follow on Facebook</a>&nbsp;&nbsp;<a href="feed.xml" style="font-family:'Archivo',Arial,sans-serif;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)">or subscribe by RSS</a></p>
</div>

<div class="numbers"><div class="numbers-inner">
<div><div class="n">5,811</div><div class="l">Cases closed, 2020&ndash;2025</div></div>
<div><div class="n">2,910</div><div class="l">Convictions, 2020&ndash;2025</div></div>
<div><div class="n">6,261</div><div class="l">Cases worked by the DA personally</div></div>
<div><div class="n">$1M+</div><div class="l">In grants won for victims and the circuit</div></div>
<div class="src">From the office's closed-case disposition logs, public record. Details on <a href="record.html" style="color:#fff">The Record</a>.</div>
</div></div>

{docket("No. 1","The Mission")}
<div class="wrap prose">
<p class="lede">The mission of the Office of the District Attorney of the Middle Judicial Circuit is to keep our communities safe and to protect the constitutional rights of all citizens, including the accused, through the prompt, fair, and efficient prosecution of criminal offenses with integrity, honor, and the highest degree of professionalism.</p>
</div>
"""
page("index.html","Tripp Fitzner — District Attorney, Middle Judicial Circuit of Georgia",
 "Tripp Fitzner is the District Attorney for the Middle Judicial Circuit of Georgia: Candler, Emanuel, Jefferson, Toombs, and Washington counties.",home)

# ---------- ABOUT ----------
about=f"""
{docket("No. 1","About Tripp")}
<div class="wrap" style="display:grid;grid-template-columns:minmax(260px,340px) 1fr;gap:2.4rem;align-items:start">
<figure style="margin:0"><img src="img/tripp-fitzner-portrait.jpg" alt="District Attorney Tripp Fitzner" style="border:1px solid var(--ink);box-shadow:6px 6px 0 var(--garnet)" width="340" height="433">
<figcaption style="font-family:'Archivo',Arial,sans-serif;font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-top:.6rem">District Attorney Tripp Fitzner</figcaption></figure>
<div class="prose">
<p class="lede">I've spent most of my career putting child molesters, rapists, and murderers in prison, and I asked for the job.</p>
<p>Before the voters of this circuit elected me District Attorney in 2020, I was the Chief Assistant here, and before that I was a child abuse prosecutor. When you've sat with a child who has to describe the worst thing that ever happened to them in a room full of strangers, you don't forget which side of the courtroom you belong on. I never have.</p>
<p>Swainsboro has been home for more than twenty-five years. My wife Jennifer teaches school. I have four sons, two grown and making their own way, and two boys we're raising here now. We're members of our church here in Swainsboro, where I've served as a deacon. My faith isn't a line on a website. It's the reason I believe the strong owe something to the weak, and it's what gets me up in the morning to do this work.</p>

<h3>The road here</h3>
<p>My family is from Sylvania. I went to school at Darlington, a boarding school in Rome, Georgia, where a debate coach told me something that stuck: an athlete can only run so fast, but there's no limit on how often or how well you can persuade people. I took an accounting degree at Georgia Southern because it was practical, earned my law degree at the University of Dayton, and worked briefly as an accountant. I hated every day of it. So I went to a courtroom, and I never left.</p>
<p>I started prosecuting in 2000 as this circuit's first full-time juvenile court prosecutor, and became the first prosecutor here to handle all crimes against children. From 2005 to 2008 I served as District Court Administrator for the Eighth Judicial Administrative District, the administrative arm of the superior courts across twenty-seven counties. In 2009 I came back to the courtroom as Chief Assistant District Attorney, where I carried child victim prosecution, felony cases in Candler and Emanuel counties, the office's budget, and the building of our victim advocate program.</p>

<h3>The work</h3>
<ul class="plain">
<li><strong>Trial work.</strong> Lead prosecutor in murder and child victim cases across all five counties, including cases that drew statewide and national attention.</li>
<li><strong>Appellate work.</strong> This office also represents the State when convictions are appealed. Every conviction of this tenure that has been reviewed on appeal has been upheld.</li>
<li><strong>Victim advocacy.</strong> Built the office's victim advocate program from zero positions to four, all grant-funded, including the circuit's first bilingual advocate, so language is never a barrier to justice. More than a million dollars in grants won for victims and the circuit, including equipment for courthouses and even the public defender's office.</li>
<li><strong>Stewardship.</strong> Prepared every budget this office has presented to the counties of the circuit since 2009.</li>
<li><strong>Teaching.</strong> National trial advocacy instructor for the National District Attorneys Association, and search-and-seizure trainer for law enforcement agencies across the circuit.</li>
<li><strong>The profession.</strong> Elected by the lawyers of this circuit to four terms on the State Bar of Georgia's Board of Governors.</li>
</ul>

<h3>Recognition</h3>
<p>In March 2026, the Attorney General of the United States personally recognized this office's work on a multi-agency child sex-trafficking investigation that began in Emanuel County and put four defendants in federal prison for crimes against five child victims. The Georgia Senate has commended the office's work alongside the Emanuel County Sheriff's Office.</p>
</div>
</div>
"""
page("about.html","About Tripp Fitzner — District Attorney","Career prosecutor. Child abuse prosecutor, Chief Assistant, and since 2021 the elected District Attorney of the Middle Judicial Circuit of Georgia.",about)
