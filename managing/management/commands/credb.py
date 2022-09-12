from django.core.management.base import BaseCommand
from django.utils import timezone
from managing.models import Author, Publisher, Book, Comment, Reply
from django.utils.crypto import get_random_string
from authenticate.models import CustomUser as User
from random import shuffle, randint

class Command(BaseCommand):
    help = 'Displays current time'

    def __init__(self) :
        self.users_str = ["reza", "zahra", "hadi", "mohsen", "shadi", "maryam", "sadegh", "mohammad", "zeinab", "hossein"]
        
        self.authors_str = ["wiliam*shekpier", "charles*dikenz", "mark*tuain", "victor*hogo", "jin*astin", "ken*falt", "noam*chamski", "lubsang*rampa", "michele*lucier", "stiven*king"]
        
        self.publishers_str = ["motekhasesan", "negah", "cheshme", "sales", "nimazh", "ghoghnous", "soore mehr", "shaparak", "sanaa" , "sadra"]
        
        self.books_str = ["great gatsby", "george orwell", "animal farm", "joseph heler", "to kill a mockingbird", "viriginia wolf", "the catcher in the rye", "the grapes of wraph", "the sound and the fury" , "clockword orange"]
        
        self.comments_str = ["khoobe", "bad nist", "fogolade", "matnaye jazabi dare", "khosham nayoomad", "chera mojood nost ??", "key mirese dastam ??", "vase por kardan ghafase be dard mikhore", "ketabaye dihe az in nevisande mikham" , "tarahi jeld mahshar bood"]
        
        self.replies_str = ["na baba", "beshin sare jat", "harf nabashe", "khafe", "moteasefam barat", "bashe to ras migi", "baba namak", "chetor inghad bi farhangin", "ino nabayad migofti" , "oomadi o nasazi"]
        
        self.tags_str = ["romance", "beautiful","horror", "murder","sciense", "classic", "technology","epic","revolution","mystric"]
        
        self.strs = {
            "user" : self.users_str,
            "author" : self.authors_str,
            "publisher" : self.publishers_str,
            "book" : self.books_str,
            "comment" : self.comments_str,
            "reply" : self.replies_str,
            "tag" : self.tags_str,
        }
        self.users = []
        self.authors = []
        self.publishers = []
        self.books = []
        self.comments = []
        self.replies = []
        
        
    def add_arguments(self, parser):
        parser.add_argument('autoFill', type=int, help='autoFill models')
        
    def getNum(self) :
        return randint(100, 1000000)
        
    def randOf(self, aList) :
        return aList[randint(0, len(aList) -1 )]
    
    def initial(self, total) :
        for key in self.strs.keys() :
            aList = self.strs[key]
            result = [f"{x}({i})" for x in aList for i in range(0, total)]
            shuffle(result)
            self.strs[key] = result

    def choice(self, key) :
        x = self.strs[key].pop(0)
        return x


    def handle(self, *args, **kwargs):
        total = kwargs['autoFill']
        
        self.initial(total // 10)
        total = 10 * (total // 10)
        
        for i in range(total):
            user = User.objects.create_user(username=self.choice("user"),email="", national_code=self.getNum(), password="1234")
            self.users.append(user)
        
        for i in range(total):
            name = self.choice("author").split("*")
            author = Author.objects.create(name=name[0], last_name=name[1], nationality=get_random_string(5))
            self.authors.append(author)
         
        for i in range(total):
            publisher = Publisher.objects.create(name=self.choice("publisher"),register_code=self.getNum())
            
            self.publishers.append(publisher)
            

        for i in range(total):
            
            x = self.strs["tag"]
            shuffle(x)
            randnum = randint(0, len(x) - 1)
            y = ",".join(x[:randnum])
            
            
            book = Book.objects.create(title=self.choice("book"), author=self.randOf(self.authors), user=self.randOf(self.users), publisher=self.randOf(self.publishers), year_published = randint(1850, 2022), pages = self.getNum(), in_store = self.getNum(), cost=self.getNum(), tag = y)
            
            self.books.append(book)
            
        for i in range(total):
            comment = Comment.objects.create(user=self.randOf(self.users), book=self.randOf(self.books), body = self.choice("comment"), visible=True)
            
            self.comments.append(comment)
            
        for i in range(total):
            comment=self.randOf(self.comments)
            reply = Reply(user=self.randOf(self.users), comment=comment, body = self.choice("reply"), visible=True)
            x = randint(0,1)
            
            if self.replies and x:
                p = lambda _ : _.comment == comment
                sub = list(filter(p,self.replies))
                shuffle(sub)
                if sub :
                    quote = sub[randint(0, len(sub) - 1)]
                    reply.quotes = quote
                
            reply.save()
            
            self.replies.append(reply)
        