from __future__ import print_function
import webapp2
from BeautifulSoup import BeautifulSoup
import jinja2
import json
import urllib2
import urllib
import re
import sys
import os
import logging
import cgi



from google.appengine.api import urlfetch

from google.appengine.ext import db

#Jinja template
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        #self._render_text = self.content.replace('\n', '<br>')
        self.write(self.render_str(template,**kw))

#function to check valid user input
def valid_ISBN(isbn): 
    if isbn.isdigit():
        if len(isbn) == 13:
            return False
    return True




def book_details():
    global isbn
    indiaplaza_base_url ="http://www.indiaplaza.com/books/" +str(isbn) + ".htm"
    try:
        a = urlfetch.fetch(url = indiaplaza_base_url,deadline = 10).content
    except:
        return('not available')
    b = BeautifulSoup(a)
    #logging.info(b)
    try:
        c = b.findAll("span", "greyFont")
        l = b.find("a", "greyFont")
        q = b.findAll("a", "skuAuthorName")
        e = b.find("span", "boldFont")
        i = b.findAll("img", id="imgpfd")
        #d = b.findAll("div", "inContent")
        #x = str(d[0])
        #s = x.encode("ascii", "ignore")
    except:
        return ('not available')
    #return(e.string,q[0].string)
    #return ("%s" %e.string)
    try:
        return (e.string,q[0].string,c[6].string,c[3].string,l.string,c[0].string,i[0]["src"])
    except:
        return ('not available')
        #return (' ',q[0].string,' ',c[3].string,l.string,c[0].string,i[0]["src"])


def flipkart_price_info():
    global isbn
    flipkartbase_url = "http://www.flipkart.com/search.php?query="
    flipkarturl = flipkartbase_url + str(isbn)
    try:
        #a = urllib2.urlopen(flipkarturl).read()
         a = urlfetch.fetch(url = flipkarturl,deadline = 60).content
    except:
        return ('not available')
    flipkartsoup = BeautifulSoup(a)
    try:
        #z = flipkartsoup.find_all('meta')[4]['content']
        z = flipkartsoup.findAll('meta')
        v = str(z[4])
        #c = z.split('.')
        #x = str(flipkartsoup.find("div", "shipping-details"))
        #a = re.compile('\d\-\d\s*\w*\s*\w*\.')
        f = re.compile('Rs\.\s*\d*')
        match = re.search(f,v)
        s = match.start()
        e = match.end()
    except:
        return ('not available')
        #"Delivered in %s" %x[s:e]
    #return(c[0],'%s %s' %(c[1],c[2]))
    try:
        return(v[s:e])
    except:
        return ('not available')


def Indiaplaza_price_info():
    global isbn
    Indiaplazaurl = "http://www.indiaplaza.com/books/" + str(isbn) + ".htm"
    try:
        b = urlfetch.fetch(url=Indiaplazaurl,deadline = 60).content
        #b = urllib2.urlopen(Indiaplazaurl).read()
        #b = a.content
        #if a.status_code == 200:
    except:
        return ('not available')
    Indiaplazasoup = BeautifulSoup(b)
    try:
        x = Indiaplazasoup.find("span", "blueFont")
        k = Indiaplazasoup.find("div", "fdpSave")
        a = x.string
        c = k.string
    except:
        return ('not available')
    try:
        return ("%s %s" %(a,c))
    except:
        return ('not available')        



def infibeam_price_info():
    global isbn
    infibeam_base_url = "http://www.infibeam.com/Books/search?q="
    infibeam_url = infibeam_base_url + str(isbn)
    try:
        a = urllib2.urlopen(url = infibeam_url).read()
    except:
        return ('not available')
    infibeam_soup = BeautifulSoup(a)
    try:
        #m = infibeam_soup.find_all("span", "textlight")[1]
        x = infibeam_soup.find("span", "infiPrice amount price")
        #n = infibeam_soup.find_all("span", "textlight")[2]
        k = infibeam_soup.find("span", "yousave")
        l = infibeam_soup.find("span", "yousaveper")
    except:
        return ('not available')
    try:
        return("our price %s you save %s" %(x.string,k.string))
    except:
        return ('not available')


def rediff_price_info():
    global isbn
    rediff_base_url = "http://books.rediff.com/book/ISBN:"
    rediff_url = rediff_base_url + str(isbn)
    try:
        a = urlfetch.fetch(url = rediff_url).content
    except:
        return ('not available')
    rediff_soup = BeautifulSoup(a)
    try:
        #z = rediff_soup.find("font", id="book-pric")
        c = re.compile('font\s*id\=\"book\-pric\"\>\<b\>\w{2}\.\d+')
        match = re.search(c,a)
        s = match.start()
        e = match.end()
    except:
        return ('not available')
    #if z == None:
        #return ('Item not found')
        #return
    #return (z.string)
    try:
        return (a[s+23:e])
    except:
        return ('not available')


def nbc_India_price_info():
    global isbn
    nbc_India_base_url = "http://www.nbcindia.com/Search-books.asp?q="
    nbc_India_url = nbc_India_base_url + str(isbn)
    try:
         a = urlfetch.fetch(url = nbc_India_url,deadline = 10).content
    except:
        return ('not available')
    nbc_India = BeautifulSoup(a)
    try:
        z = nbc_India.find("span", "red")
        x = str(nbc_India.find("div", "fictiong-grid-content-2"))
    except:
        return ('not available')
    #if z == None:
        #print('Item not found')
        #return
    #print("NbcIndia Books",end="\t")
    #print(a[440:555])
    try:
        if z:
            return (z.string)
    except:
        if x:
            a = re.compile('Rs\s*\d+')
            c = re.search(a,x)
            s = c.start()
            e = c.end()
            return (x[s:e])
        return ('not available')


def bookadda_price_info():
    global isbn
    bookadda_base_url = "http://www.bookadda.com/search/"
    bookadda_url = bookadda_base_url + str(isbn)
    try:
         a =  urlfetch.fetch(url = bookadda_url,deadline = 10).content
    except:
        return ('not available')
    bookadda_soup = BeautifulSoup(a)
    try:
        #d = bookadda_soup.find_all("meta")[1]["content"]
        c = re.compile('our\s*price\s*\d+\,?\d+')
        match = re.search(c,a)
        s = match.start()
        e = match.end()
    except:
        return ('not available')
    #v = d.split('.')
    #return ("%s %s %s" %(v[0],v[1],v[2]))
    try:
        return (a[s:e])
    except:
        return ('not available')


def uread_price_info():
    global isbn
    uread_base_url = "http://www.uread.com/book/isbnnetin/"
    uread_url = uread_base_url + str(isbn)
    try:
        a = urlfetch.fetch(url = uread_url,deadline = 10).content
    except:
        return ('not availablee')
    uread_soup = BeautifulSoup(a)
    try:
        d = str(uread_soup.find("label", id="ctl00_phBody_ProductDetail_lblourPrice"))
        #c = re.compile('Our\s*Price\:\s*\<span\>\s*\<span\s*style\s*\=\"font\-family\:rupee\"\>R\<\/span\>\d+')
        #match = re.search(c,a)
        #s = match.start()
        #e = match.end()
        #b = a[s:e]
    except:
        return ('not availableee')
    try:
        v = d.split('>')
        g = v[4]
        b = re.compile("\d+\,?\d*")
        match = re.search(b,g)
        s = match.start()
        e = match.end()
    except:
        return ('not availableeee')
    try:
        return ("%s %s" %(v[1][:10],g[s:e]))
    except:
        return ('not available')


def homeshop18_price_info():
    global isbn
    homeshop18_base_url = "http://www.homeshop18.com/search/books/"
    homeshop18_url = homeshop18_base_url + str(isbn)
    try:
        a = urlfetch.fetch(url = homeshop18_url,deadline = 10).content
    except:
        return ('not available')
    c = BeautifulSoup(a)
    try:
        v = c.find("span", "our_price")
        #k = c.find_all("div", "listView_discount")[1]
        #y = c.find("div", "pdp_details_deliveryTime")
        #y = re.compile('\w*\s*\w{2}\s*\d\-\d\s*\w+\s*$')
        #match = re.search(y,a)
        #s = match.start()
        #e = match.end()
    except:
        return ('not available')
    try:
        return("%s" %v.string)
    except:
        return ('not available')


class DisplayPrice(Handler):
    def get(self,isbn):
        kw = {}
        kw['ISBN']=isbn
        kw['book_details']=book_details()
        kw['flipkart_info'] = flipkart_price_info()
        kw['Indiaplaza_info'] = Indiaplaza_price_info()
        kw['infibeam_info'] = infibeam_price_info()
        kw['rediff_info'] = rediff_price_info()
        kw['nbcIndia_info'] = nbc_India_price_info()
        kw['bookadda_info'] = bookadda_price_info()
        kw['uread_info'] = uread_price_info()
        kw['homeshop18_info'] = homeshop18_price_info()

        self.render('displayprice.html', **kw )
        


class MainHandler(Handler):
    def get(self):
        self.render("price.html",ISBN="enter ISBN")


    def post(self): 
        global isbn 
        isbn = self.request.get('ISBN')
        params = dict(invalid_isbn=isbn)
       
                  
                  
        if valid_ISBN(isbn):
            params['error'] = "that's not a valid ISBN."
            self.render('price.html',**params)
        else:
            self.redirect('/ISBN/%s' % str(isbn))



app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/ISBN/([0-9]+)',DisplayPrice)], debug=True)
