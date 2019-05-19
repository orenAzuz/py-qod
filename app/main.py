from http.server import HTTPServer, BaseHTTPRequestHandler
import pymongo
import random
import configparser

class Quote:
    """Generic Quote"""
    def __init__(self, quote, author):
        self.quote = quote
        self.author = author
    
    def __repr__(self):
        return "\"{}\"\n\n-{}\n".format(self.quote, self.author)


class QOTD(object):
    """Quote of the Day Server"""
    
    def __init__(self, mongourl):
        myclient = pymongo.MongoClient("mongodb://{}/".format(mongourl))
        self.mydb = myclient["qoddb"]
        self.mycol = self.mydb["quotes"]
    
    def get_quote(self):
        numQuotes=self.mydb.command("dbstats")["objects"]
        n = random.randint(0,numQuotes)
        for quote in self.mycol.find({}):
            n-=1
            if (n<=0): return quote
        return None
          
        
   
    
class QuoteServer(BaseHTTPRequestHandler):
    def respond(self,code,body):
        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self):
        try:
            print("In GET")
            quote = q.get_quote()
            print ("quote is {}".format(quote))
            if quote is None:
                self.respond(404,"No quotes in DB")
            else:
                self.respond(200,"{}".format(quote))
        except:
            self.respond(500,"Internal error. Is DB OK?")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    dbHost = config['Database']['host']
    dbPort = config['Database']['port']
    print("Mongo on {}:{}".format(dbHost,dbPort))
    q = QOTD("{}:{}".format(dbHost,dbPort))
    host="0.0.0.0"
    port=8080
    print("QOTD server listening on {}:{}. Press CTRL+C to exit..\n".format(host, port))
    httpd = HTTPServer((host, port), QuoteServer)
    httpd.serve_forever()

    