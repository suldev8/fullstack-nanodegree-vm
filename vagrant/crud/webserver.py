from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Base

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
sessionDB = sessionmaker(bind=engine)
session = sessionDB()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant).all()
                output =  ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Create new restaurant</a>"
                for restaurant in restaurants:
                    output += "<h1>{}</h1>".format(restaurant.name)
                    output += "<a href='restaurants/%s/edit'>edit</a></br>" % restaurant.id
                    output += "<a href='restaurants/%s/delete'>delete</a>" % restaurant.id
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '''<h1> new restaurant </h1>
                <form method='POST' action='/restaurants/new' enctype='multipart/form-data'>
                <input type='text' name='newRestaurant'/>
                <input type='submit' name='Submit' />
                </form>
                '''
                output += "</body> </html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/edit"):
                restaurantID = self.path.split('/')[2]
                restaurantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
                if restaurantQuery:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += '''<h1> New name for %s</h1>
                    <form method='POST' action='restaurants/%s/edit' enctype='multipart/form-data'>
                    <input type='text' name='newRestaurantName'/>
                    <input type='submit' value='Rename' />
                    </form>
                    '''% (restaurantQuery.name, restaurantID)
                    output += "</body> </html>"
                    print output
                    self.wfile.write(output)
                    return
                
            if self.path.endswith("/delete"):
                restaurantID = self.path.split('/')[2]
                restaurantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
                if restaurantQuery:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += '''<h1> Are sure you want to delte {}?</h1>
                    <form method='POST' action='restaurants/{}/delete' enctype='multipart/form-data'>
                    <input type='submit' value='remove' />
                    </form>
                    '''.format(restaurantQuery.name, restaurantID)
                    output += "</body> </html>"
                    print output
                    self.wfile.write(output)
                    return
        except IOError:
            self.send_error(404, "file NO Found %s" % self.path)
    
    def do_POST(self):
        try:
            if self.path.endswith('/resataurants/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('newRestaurant')
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                self.send_response(301)
                self.send_header('location', '/restaurants')
                self.end_headers()
           
            if self.path.endswith('edit'):
                restaurantID = self.path.split('/')[2]
                restaurantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
                if restaurantQuery:
                    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields=cgi.parse_multipart(self.rfile,pdict)
                        messagecontent = fields.get('newRestaurantName')
                        restaurantQuery.name = messagecontent[0]
                        session.add(restaurantQuery)
                        session.commit()
                    self.send_response(301)
                    self.send_header('location', '/restaurants')
                    self.end_headers()
            
            if self.path.endswith('delete'):
                restaurantID = self.path.split('/')[2]
                restaurantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
                if restaurantQuery:
                    session.delete(restaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('location', '/restaurants')
                    self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print 'C^ enter, stopping web server...'
        server.socket.close()

if __name__ == "__main__":
    main()