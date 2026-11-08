import re, io, base64
from PIL import Image
A='/var/lib/freelancer/projects/40747122/author/'
src=open(A+'src/chloe.html',encoding='utf-8').read()
L=src.split('\n')
def idx(pred): return next(i for i,l in enumerate(L) if pred(l))
style_end=idx(lambda l:l.strip()=='</style>')
main_start=idx(lambda l:l.strip()=='<main>')
news_start=idx(lambda l:'<!-- NEWSLETTER' in l)
main_end=idx(lambda l:l.strip()=='</main>')
head='\n'.join(L[:style_end])
head=head.replace('<title>Chloe Hart | Dark &amp; Sports Romance Author</title>','<title>Out of My League | Chloe Hart</title>')
extra=open(A+'src/book_extra.css',encoding='utf-8').read()
top='\n'.join(L[style_end:main_start+1])          # </style> ... header ... <main>
# header / strip links go to the homepage sections
top=re.sub(r'href="#(books|about|new|book-1|love)"',r'href="/#\1"',top)
tail='\n'.join(L[news_start:])                     # newsletter, instagram, </main>, footer, script
tail=re.sub(r'href="#(books|about|new|book-1)"',r'href="/#\1"',tail)
main=open(A+'src/book1_main.html',encoding='utf-8').read()
# newsletter = what's live: MailerLite form with Email only
tail=tail.replace('        <input type="text" name="first_name" placeholder="First name" aria-label="First name" autocomplete="given-name">\n','')
tail=tail.replace('>Count me in</button>','>Subscribe</button>')
tail=re.sub(r'\s*<div class="news-small">.*?</div>','',tail,flags=re.S)
extra+="\n.news-form{grid-template-columns:1fr auto}\n@media (max-width:760px){.news-form{grid-template-columns:1fr}}\n"
out=head+'\n'+extra+'\n'+top+'\n'+main+'\n'+tail
def uri(f):
    im=Image.open(A+'img/'+f).convert('RGB'); b=io.BytesIO(); im.save(b,'WEBP',quality=86,method=6)
    return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
IG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'
out=out.replace('__B1__',uri('b1.jpg')).replace('__B2__',uri('b2.jpg')).replace('__B3__',uri('b3.jpg')).replace('__IG__',IG).replace('__PERSON__','')
assert '__B' not in out
open(A+'chloe_hart_book1_out_of_my_league.html','w',encoding='utf-8').write(out)
print(len(out))
