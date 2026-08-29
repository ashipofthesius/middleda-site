import io, json, pathlib
ADDRESS="114 Jefferson Street, Swainsboro, GA 30401"
PHONE="(478) 237-7846"
JSONLD={
 "@context":"https://schema.org",
 "@graph":[
  {"@type":"Person","@id":"https://middleda.org/#tripp","name":"John A. Fitzner III","alternateName":"Tripp Fitzner",
   "jobTitle":"District Attorney","worksFor":{"@id":"https://middleda.org/#office"},
   "alumniOf":[{"@type":"CollegeOrUniversity","name":"Georgia Southern University"},{"@type":"CollegeOrUniversity","name":"University of Dayton School of Law"}],
   "image":"https://middleda.org/img/tripp-fitzner-portrait.jpg","telephone":"+1-478-237-7846","url":"https://middleda.org/about.html",
   "sameAs":["https://www.facebook.com/TrippFitznerDA","https://www.instagram.com/trippfitzner"]},
  {"@type":"GovernmentOrganization","@id":"https://middleda.org/#office",
   "name":"Office of the District Attorney, Middle Judicial Circuit of Georgia",
   "url":"https://middleda.org/","areaServed":["Candler County, Georgia","Emanuel County, Georgia","Jefferson County, Georgia","Toombs County, Georgia","Washington County, Georgia"],
   "address":{"@type":"PostalAddress","streetAddress":"114 Jefferson Street","addressLocality":"Swainsboro","addressRegion":"GA","postalCode":"30401","addressCountry":"US"},
   "telephone":"+1-478-237-7846","employee":{"@id":"https://middleda.org/#tripp"}}
 ]}

def HEAD(title,desc,path):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://middleda.org/{path}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="https://middleda.org/img/tripp-fitzner-portrait.jpg">
<link rel="alternate" type="application/rss+xml" title="From the District Attorney" href="https://middleda.org/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Besley:wght@700;800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Archivo:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{json.dumps(JSONLD,separators=(",",":"))}</script>
</head>
<body>"""

def masthead(current):
    items=[("index.html","Home"),("about.html","About Tripp"),("record.html","The Record"),("circuit.html","The Circuit"),("victims.html","Victim Services"),("files.html","Files &amp; Policies"),("contact.html","Contact")]
    nav="".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==current else ""}>{t}</a></li>' for h,t in items)
    return f"""<header class="masthead"><div class="masthead-inner">
<div class="name"><a href="index.html">Tripp Fitzner</a></div>
<div class="office">District Attorney &middot; Middle Judicial Circuit of Georgia</div>
</div></header>
<nav class="site" aria-label="Main"><ul>{nav}</ul></nav>"""

FOOTER=f"""<footer><div class="foot-inner">
<div><div class="fh">Office</div>Office of the District Attorney<br>Middle Judicial Circuit of Georgia<br>{ADDRESS}<br>{PHONE}</div>
<div><div class="fh">Hours</div>Monday&ndash;Friday, 8:00 a.m.&ndash;5:00 p.m.<br>Closed weekends and state holidays</div>
<div><div class="fh">The Circuit</div>Candler &middot; Emanuel &middot; Jefferson<br>Toombs &middot; Washington<br><a href="feed.xml">RSS feed</a></div>
</div><div class="foot-legal">This site is paid for personally by Tripp Fitzner. No public funds are used.</div></footer>
</body></html>"""

def docket(no,title):
    return f'<section class="docket"><div class="cap"><h2>{title}</h2><span class="no">{no}</span></div></section>'

def page(path,title,desc,body):
    pathlib.Path(path).write_text(HEAD(title,desc,path)+masthead(path)+body+FOOTER,encoding="utf-8")
    print("built",path)
