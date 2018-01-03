from transitions.extensions import GraphMachine
import requests
import re

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_CNNALL(self, update):
        text = update.message.text
        return (text.lower() == 'cnn' or text.lower() == 'CNN' or text.lower() == 'Cnn')

    def is_going_to_BBCALL(self, update):
        text = update.message.text
        return (text.lower() == 'bbc' or text.lower() == 'BBC' or text.lower() == 'Bbc')
        
    def is_going_to_CNNURL(self, update):
        text = update.message.text
        return (text.lower() != 'bbc' and text.lower() != 'BBC' and text.lower() != 'Bbc' and \
                text.lower() != 'bbc10' and text.lower() != 'BBC10' and text.lower() != 'Bbc10' and \
                text.lower() != 'cnn' and text.lower() != 'CNN' and text.lower() != 'Cnn' and \
                text.lower() != 'cnn10' and text.lower() != 'CNN10' and text.lower() != 'Cnn10' and \
                text.lower() != 'freq' and text.lower() != 'Freq' and text.lower() != 'FREQ')

    def is_going_to_BBCURL(self, update):
        text = update.message.text
        return (text.lower() != 'cnn' and text.lower() != 'CNN' and text.lower() != 'Cnn' and \
                text.lower() != 'cnn10' and text.lower() != 'CNN10' and text.lower() != 'Cnn10' and \
                text.lower() != 'bbc' and text.lower() != 'BBC' and text.lower() != 'Bbc' and \
                text.lower() != 'bbc10' and text.lower() != 'BBC10' and text.lower() != 'Bbc10' and \
                text.lower() != 'freq' and text.lower() != 'Freq' and text.lower() != 'FREQ')
    
    def is_going_to_CNN10(self, update):
        text = update.message.text
        return (text.lower() == 'cnn10' or text.lower() == 'CNN10' or text.lower() == 'Cnn10')

    def is_going_to_BBC10(self, update):
        text = update.message.text
        return (text.lower() == 'bbc10' or text.lower() == 'BBC10' or text.lower() == 'Bbc10')
    
    def is_going_to_FREQ(self, update):
        text = update.message.text
        return (text.lower() == 'freq' or text.lower() == 'Freq' or text.lower() == 'FREQ')

    def on_enter_CNNALL(self, update):	
        response = requests.get("http://edition.cnn.com/")
        pattern = "uri[^,]*,\"headline\":\"[^\"]*\""
        cnn_raw = re.findall(pattern, response.text)
        cnn_concat = ""
        for i in range(len(cnn_raw)):
            cnn_raw[i] = re.findall("\"headline\":\"[^\"]*\"", cnn_raw[i])[0] 
            cnn_raw[i] = cnn_raw[i][12:]
            cnn_raw[i] = cnn_raw[i][:len(cnn_raw[i])-1]
            cnn_raw[i] = cnn_raw[i].replace('\\u003cstrong>', '')
            cnn_raw[i] = cnn_raw[i].replace('\\u003c/strong>', '') 
            cnn_concat = cnn_concat + str(i) + ') ' + cnn_raw[i] + '\n'
        reply = cnn_concat 
        update.message.reply_text(reply)

    def on_enter_BBCALL(self, update):
        response = requests.get("http://www.bbc.com/news")
        #soup = BeautifulSoup(response.text, "lxml")

        pattern = "href[^<]*<[^>]*>[^<]*</h3>"
        bbc_raw = re.findall(pattern, response.text)
        bbc_concat = ""
        for i in range(len(bbc_raw)):
            bbc_raw[i] = re.findall(">[^>]*</h3>", bbc_raw[i])[0]
            bbc_raw[i] = bbc_raw[i][1:len(bbc_raw[i])-5]
            bbc_raw[i] = bbc_raw[i].replace('&#x27;', '\'')
            bbc_concat = bbc_concat + str(i) + ') ' + bbc_raw[i] + '\n'
        reply = bbc_concat
        update.message.reply_text(reply)
        
    def on_enter_CNNURL(self, update):
        text = update.message.text
        response = requests.get("http://edition.cnn.com/")

        pattern = "uri[^,]*,\"headline\":\"[^\"]*\""
        cnn_url = re.findall(pattern, response.text)
    
        for i in range(len(cnn_url)):
            cnn_url[i] = cnn_url[i][6:]
            cnn_url[i] = re.findall("[^\"]*\"", cnn_url[i])[0] 
            cnn_url[i] = "http://edition.cnn.com" + cnn_url[i][:len(cnn_url[i])-1]
                
        if text.lower().isdigit():
            if int(text.lower()) < len(cnn_url):
                reply = cnn_url[int(text.lower())]
                #print('enter nested-if')
            else:
                reply = 'not a news index'
                #print('enter inner else')
        else:
            reply = 'not a news index'
            #print('enter else')
        update.message.reply_text(reply)
        self.go_triv(update)
        
    def on_enter_BBCURL(self, update):
        text = update.message.text
        response = requests.get("http://www.bbc.com/news")
        #soup = BeautifulSoup(response.text, "lxml")

        pattern = "href[^<]*<[^>]*>[^<]*</h3>"
        bbc_url = re.findall(pattern, response.text)

        for i in range(len(bbc_url)):
            bbc_url[i] = re.findall("[^\"]*\"", bbc_url[i][6:])[0] 
            bbc_url[i] = "http://www.bbc.com" + bbc_url[i][:len(bbc_url[i])-1]
        
        if text.lower().isdigit():
            if int(text.lower()) < len(bbc_url):
                reply = bbc_url[int(text.lower())]
                print('enter nested-if')
            else:
                reply = 'not a news index'
                print('enter inner else')
        else:
            reply = 'not a news index'
            print('enter else')
        update.message.reply_text(reply)
        self.go_triv(update)
        
    def on_enter_CNN10(self, update):	
        response = requests.get("http://edition.cnn.com/")
        pattern = "uri[^,]*,\"headline\":\"[^\"]*\""
        cnn_raw = re.findall(pattern, response.text)
        cnn_concat = ""
        for i in (range(len(cnn_raw)) if len(cnn_raw) < 10 else range(10)):
            cnn_raw[i] = re.findall("\"headline\":\"[^\"]*\"", cnn_raw[i])[0] 
            cnn_raw[i] = cnn_raw[i][12:]
            cnn_raw[i] = cnn_raw[i][:len(cnn_raw[i])-1]
            cnn_raw[i] = cnn_raw[i].replace('\\u003cstrong>', '')
            cnn_raw[i] = cnn_raw[i].replace('\\u003c/strong>', '') 
            cnn_concat = cnn_concat + str(i) + ') ' + cnn_raw[i] + '\n'
        reply = cnn_concat 
        update.message.reply_text(reply)

    def on_enter_BBC10(self, update):
        response = requests.get("http://www.bbc.com/news")
        #soup = BeautifulSoup(response.text, "lxml")

        pattern = "href[^<]*<[^>]*>[^<]*</h3>"
        bbc_raw = re.findall(pattern, response.text)
        bbc_concat = ""
        for i in (range(len(bbc_raw)) if len(bbc_raw) < 10 else range(10)):
            bbc_raw[i] = re.findall(">[^>]*</h3>", bbc_raw[i])[0]
            bbc_raw[i] = bbc_raw[i][1:len(bbc_raw[i])-5]
            bbc_raw[i] = bbc_raw[i].replace('&#x27;', '\'')
            bbc_concat = bbc_concat + str(i) + ') ' + bbc_raw[i] + '\n'
            reply = bbc_concat
        update.message.reply_text(reply)
    
    def on_enter_FREQ(self, update):
        response = requests.get("http://edition.cnn.com/")
        pattern = "uri[^,]*,\"headline\":\"[^\"]*\""
        cnn_raw = re.findall(pattern, response.text)
        cnn_concat = ""
        for i in range(len(cnn_raw)):
            cnn_raw[i] = re.findall("\"headline\":\"[^\"]*\"", cnn_raw[i])[0] 
            cnn_raw[i] = cnn_raw[i][12:]
            cnn_raw[i] = cnn_raw[i][:len(cnn_raw[i])-1]
            cnn_raw[i] = cnn_raw[i].replace('\\u003cstrong>', '')
            cnn_raw[i] = cnn_raw[i].replace('\\u003c/strong>', '') 
            cnn_concat = cnn_concat + cnn_raw[i] + ' '


        response = requests.get("http://www.bbc.com/news")

        pattern = "href[^<]*<[^>]*>[^<]*</h3>"
        bbc_raw = re.findall(pattern, response.text)
        bbc_concat = ""
        for i in range(len(bbc_raw)):
            bbc_raw[i] = re.findall(">[^>]*</h3>", bbc_raw[i])[0]
            bbc_raw[i] = bbc_raw[i][1:len(bbc_raw[i])-5]
            bbc_raw[i] = bbc_raw[i].replace('&#x27;', '\'')
            bbc_concat = bbc_concat + bbc_raw[i] + ' '

        both_concat = cnn_concat + ' ' + bbc_concat
        
        tokenizer = RegexpTokenizer(r'\w+')
        
        mostcommon = list();
        for concat in [both_concat, cnn_concat, bbc_concat]:
            word_tokens = tokenizer.tokenize(concat)
            stopword_list = stopwords.words('english')
            stopword_list.insert(0,"The")
            stop_words = set(stopword_list)
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            filtered_sentence = []
         
            for w in word_tokens:
                if w not in stop_words:
                    filtered_sentence.append(w)
            fdist = FreqDist(filtered_sentence)
            mostcommon.append(fdist.most_common(10))
    
        reply = 'Overall Freq Words:\n'
        for i in range(10):
            reply = reply + mostcommon[0][i][0]
            if i < 9:
                reply = reply + ', '
        reply = reply + '\n\nCNN Freq Words:\n'
        for i in range(10):
            reply = reply + mostcommon[1][i][0]
            if i < 9:
                reply = reply + ', '
        reply = reply + '\n\nBBC Freq Words:\n'
        for i in range(10):
            reply = reply + mostcommon[2][i][0]
            if i < 9:
                reply = reply + ', '
        update.message.reply_text(reply)
        self.go_start(update)
    
    def on_exit_START(self, update):
        print('Leaving START')

    def on_exit_CNNALL(self, update):
        print('Leaving CNNALL') 

    def on_exit_BBCALL(self, update):
        print('Leaving BBCALL')
    
    def on_exit_CNNURL(self, update):
        print('Leaving CNNURL') 

    def on_exit_BBCURL(self, update):
        print('Leaving BBCURL')
        
    def on_exit_CNN10(self, update):
        print('Leaving CNN10') 

    def on_exit_BBC10(self, update):
        print('Leaving BBC10')
        
    def on_exit_FREQ(self, update):
        print('Leaving FREQ')