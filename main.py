#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
from google.appengine.api import users
import webapp2

MAIN_PAGE_HTML = """\
<html>
    <body>
	<center>
	<header class="main-header" role="banner">
  <img src= "/img/1500x1500.jpg" style="width:500px;height:100px" />
</header>
	<form action="/order" method="post">
	    <h1> Trustworthy Travel Agency </h1></br>
        <div>
        <label for="name">Name:</label>
        <input type="text" id="name" name="user_name" />
        </div>
        <div>
        <label for="mail">E-mail:</label>
        <input type="email" id="mail" name="user_mail" /><br>
		<input type="checkbox" name="Member" value="true">Member?<br>
        </div></br></br>
		
  <select name="Packages">
  
  <div>
  <label for="package">Select A Package: </label>
  </div>
  <option disabled selected value><center> </center></option>
  <option value="UK">UK, France, Germany: $3000/pax </option>
  <option value="HK">HK, Japan, Korea: $2500/pax </option>
  <option value="USA">USA-LA, SF, Las Vegas: $2800/pax </option>
  <option value="TH">Thailand, Vietnam, Cambodia: $1200/pax </option>
</select></br></br>

<input type="radio" name="group1" value="Cathay Pacific" checked><img src = "/img/cathay_pacific.jpg" style="width:100px;height:64px">
<input type="radio" name="group1" value="Emirates"><img src = "/img/emirates.jpg" style="width:100px;height:64px"><br>
<input type="radio" name="group1" value="SG"><img src = "/img/sg.jpg" style="width:100px;height:64px">
<input type="radio" name="group1" value="Thai"><img src = "/img/thai_airways.jpg" style="width:100px;height:64px"><br></br>
</div>

   <div>
        <label for="Adult">Enter Number of Adults:</label>
        <input type="number" name="quantity1" min="1" value="1" />
        </div>
    <div>
        <label for="Children">Enter Number of Children:</label>
        <input type="number" name="quantity2" min="0" value="0"/>
        </div>
		
	    <div><input type="Submit" value="Submit"></input></div>
	</form>
    </body>
</html>
"""


ORDER_PAGE_HTML = """\
<html>
    <head>
    <style>
    div.transbox {
  margin: 0.1px;
  background-color: #ffffff;
  border: 1px solid black;
  opacity: 1.0;
  filter: alpha(opacity=0); /* For IE8 and earlier */
}

div.transbox p {
  margin: 0.1%;
  font-weight: bold;
  color: #000000;
}
</style>
    </head>
    <body>

    <h2><b>ORDER INFORMATION</b></h2>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

class Guestbook(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body><b><h2>ORDER INFORMATION</h2></b><pre><textarea name="emailtext" rows="30" cols="70" >Name: ')
        self.response.write(cgi.escape(self.request.get('user_name')))
        self.response.write('\nEmail: ')
        self.response.write(cgi.escape(self.request.get('user_mail')))
        self.response.write('\n\nYour Order')
        self.response.write('\n==========\n\n')
        self.response.write('Your selected package is ')
        if self.request.get('Packages')=="UK":
            pcost=3000
            self.response.write('UK, France, Germany: $3000/pax')
        if self.request.get('Packages')=="HK":
            pcost=2500
            self.response.write('HK, Japan, Korea: $2500/pax')
        if self.request.get('Packages')=="USA":
            pcost=2800
            self.response.write('USA-LA, SF, Las Vegas: $2800/pax')
        if self.request.get('Packages')=="TH":
            pcost=1200
            self.response.write('Thailand, Vietnam, Cambodia: $1200/pax')
        self.response.write('\nNumber of adult(s) = ')
        self.response.write(cgi.escape(self.request.get('quantity1')))
        self.response.write('\nNumber of child(ren) = ')
        self.response.write(cgi.escape(self.request.get('quantity2')))
        if self.request.get('member')=='yes':
            self.response.write('\nWith member discount')
        self.response.write('\nNumber of free package = ')
        freepackage=int(cgi.escape(self.request.get('quantity1')))/5
        adult=int(self.request.get('quantity1'))-freepackage
        self.response.write(freepackage)
        self.response.write('\n\nChosen airline: ')
        if self.request.get('group1')=="Cathay Pacific":
            self.response.write('Cathay Pacific at no extra cost')
            ascost=0
        if self.request.get('group1')=="Emirates":
            self.response.write('Emirates at extra $200/pax')
            ascost=200
        if self.request.get('group1')=="SG":
            self.response.write('Singapore Airlines at extra $250/pax')
            ascost=250
        if self.request.get('group1')=="Thai":
            self.response.write('Thai Airways at extra $100/pax')
            ascost=100
        self.response.write('\n\nYour totalCost\n')
        self.response.write('==============\n\n')
        self.response.write('Adult Cost = $')
        acost=adult*pcost
        self.response.write(acost)
        self.response.write('\nChild Cost = $')
        ccost=float(int(cgi.escape(self.request.get('quantity2')))*pcost*0.7)
        self.response.write(ccost)
        self.response.write('\nAirline Surcharge = $')
        excost=(adult+int(cgi.escape(self.request.get('quantity2'))))*ascost
        self.response.write(excost)
        self.response.write('\nTotal Cost = $')
        tcost=int(acost)+int(ccost)+int(excost)
        exmsg=''
        if cgi.escape(self.request.get('Member'))=='true':
            tcost=tcost*0.97
            exmsg=' (With 3% member discount)'
        self.response.write(tcost)
        self.response.write(exmsg)
        self.response.write('\n\n\n\n\n\n')
        self.response.write('</textarea></pre><br><a href="/">Home</a></body></html>')

		
app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/order', Guestbook)
], debug=True)
