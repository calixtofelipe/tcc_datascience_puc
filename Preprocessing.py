class PreProcessing():
    def __init__(self, dataset):
        self.dataset = dataset
        
    def putCharBtw(self, x, letra, sep):
        rex = re.compile('[0-9]'+letra)
        if rex.search(x)==None:
            return x
        else:
            inicio = (rex.search(x).start())+1
            newString = x[:inicio]+sep+x[inicio:]
            return newString    
    

    def replaceWord(self, text, antiga, nova):
        text = [nova if t == antiga else t for t in text.split()]
        return ' '.join(text)

    
    def clean_text(self,text):
        """
            text: a string

            return: modified initial string
        """
        text = text.lower() # padroniza o texto para minusculo
        # text = unidecode(text) # retira acentuação do texto

        text = self.replaceWord(text,'d', ' ')  # substitui o "d" quando sozinho por espaço.
        text = self.replaceWord(text, 'n', ' ') # substitui o "n" quando sozinho por espaço.
        text = self.replaceWord(text,'c', ' ') # substitui o "c" quando sozinho por espaço.
        text = self.replaceWord(text, 'pcte', 'pct') # padroniza o pcte como pct
        text = self.replaceWord(text,'pt', 'pct') # padroniza o pt como pct
        text = text.replace(r'c/',' com ') # padroniza o "c/" para "com"
        text = text.replace(r"\.c/",' com ') # padroniza o ".c/" para "com"
        text = text.replace(r'-c/',' com ') # padroniza o "-c/" para "com"
        text = text.replace(' s/',' sem ') # padroniza o "s/" para "sem"
        text = text.replace(r'\.s/',' sem ') # padroniza o ".s/" para "sem"
        text = text.replace(r'-s/',' sem ') # padroniza o "-s/" para "sem"
        text = text.replace(' p/',' para ') # padroniza o "p/" para "para"
        text = text.replace(r'\.p/',' para ') # padroniza o ".p/" para "para"
        text = text.replace(r'-p/',' para ') # padroniza o "-p/" para "para"
        text = self.replaceWord(text,'unid', 'un') # padroniza o "unid" para "un"
        text = self.putCharBtw(text,'ml',' ')  #inclui um espaço entre a palavra e a unidade, para que a unidade tenha um token.
        text = self.putCharBtw(text,'kg',' ') #inclui um espaço entre a palavra e a unidade, para que a unidade tenha um token.
        text = self.putCharBtw(text,'g',' ') #inclui um espaço entre a palavra e a unidade, para que a unidade tenha um token.
        text = self.putCharBtw(text,'gr',' ') #inclui um espaço entre a palavra e a unidade, para que a unidade tenha um token.
        text = self.putCharBtw(text,'cm',' ') #inclui um espaço entre a palavra e a unidade, para que a unidade tenha um token.
        text = self.putCharBtw(text,'l',' ') #inclui um espaço entre a palavra e a unidade, para que a unidade tenha um token.
        text = self.putCharBtw(text,'mm',' ') #inclui um espaço entre a palavra e a unidade, para que a unidade tenha um token.
        text = self.putCharBtw(text,'mt',' ') #inclui um espaço entre a palavra e a unidade, para que a unidade tenha um token.
        text = self.putCharBtw(text,'un',' ') #inclui um espaço entre a palavra e a unidade, para que a unidade tenha um token.
        
        REPLACE_BY_SPACE_RE = re.compile('\[/(){}\[\]\|@,;.+-')
        text = REPLACE_BY_SPACE_RE.sub(' ', text) #substitui simbolos por expaço
        
        BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_-]')
        text = BAD_SYMBOLS_RE.sub('', text) # qualquer simbolo fora do alfabeto é retirado e substituido por nada.
       
        text = text.replace('  ',' ') #se tiver mais de um espaco em branco é substituido por somente 1 espaço em branco
        text = text.replace('  ',' ') #se tiver mais de um espaco em branco é substituido por somente 1 espaço em branco
        return text

    def processar(self):
        dataset_processed = self.dataset.copy()
        dataset_processed['nome_produto_processed'] = dataset_processed['nome_produto'].apply(self.clean_text).copy()
        return dataset_processed