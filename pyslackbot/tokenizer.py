'''
khaiii: https://github.com/kakao/khaiii
한글 형태소 품사: http://kkma.snu.ac.kr/documents/?doc=postag
'''
from collections.abc import Iterable
from khaiii import KhaiiiApi


class Tokenizer:
    def __init__(self):
        self.api = KhaiiiApi()

    def tokenize(self, text):
        tokens = []
        for token in self.api.analyze(text):
            #print(token, type(token))
            tokens.append(token)
        return tuple(tokens)

    def check(self, text, words, check_func):
        if not check_func or not hasattr(check_func, '__call__'):
            return False
        nouns = self.get_nouns(text)
        if check_func([x for x in words if x in nouns]):
            return True
        return False

    def check_all(self, text, words):
        return self.check(text, words, check_func=all)

    def check_any(self, text, words):
        return self.check(text, words, check_func=any)

    def get_verbs(self, text, tags=['VV', 'XSV']):
        tokens = []
        for word in self.tokenize(text):
            for morph in word.morphs:
                if morph.tag in tags:
                    tokens.append(morph.lex)
        return tuple(tokens)

    def get_nouns(self, text, tags=['NNG', 'NNP']):
        tokens = []
        for word in self.tokenize(text):
            for morph in word.morphs:
                if morph.tag in tags:
                    tokens.append(morph.lex)
        return tuple(tokens)


def test():
    import sys
    t = Tokenizer()
    # assert t.check_all('훈민정음 스물 여덟자는 각각 그 모양을 본떠서 만들었다.', '훈민정음 모양'.split()) == True
    # assert t.check_all('훈민정음 스물 여덟자는 각각 그 모양을 본떠서 만들었다.', '한글 모양'.split()) == False
    # assert t.check_all('훈민정음 스물 여덟자는 각각 그 모양을 본떠서 만들었다.', '본뜨다'.split()) == True
    # assert t.check_any('훈민정음 스물 여덟자는 각각 그 모양을 본떠서 만들었다.', '한글 훈민정음 나랏말'.split()) == True
    text = ' -'.join(sys.argv[1:]) if len(sys.argv) > 1 else ''
    nouns = (('감자', 'potato'), ('고구마', 'sweet potato'))
    verbs = (('감자', 'potato'), ('고구마', 'sweet potato'))

    verbs = ()

    omitted_tags = (
        'SS',   # space
    )

    if text:
        for word in t.tokenize(text):
            for morph in word.morphs:
                if morph.tag in omitted_tags:
                    continue
                print(morph.lex, morph.tag)

        # for word in t.tokenize(text):
        #     print([(x.lex, x.tag) for x in word.morphs])
        #     #print(word, type(word))
        #     #print(dir(word))
        #     #print([x for x in word
    
if __name__ == '__main__':
    test()

    # def check_nouns(tokens, *args):
    #     #def get_nouns(self, text, tags=['NNG', 'NNP']):
    #     #tokens = []
    #     for word in self.tokenize(text):
    #         for morph in word.morphs:
    #             if morph.tag in tags:
    #                 tokens.append(morph.lex)
    #     return tuple(tokens)

    #     for token in tokens:
    #         for morph in token.morphs:

    #     input_nouns = t.


    #     for word_or_words in args:
    #         words = []
    #         if isinstance(word_or_words, str):
    #             words.append(word_or_words)
    #         elif isinstance(word_or_words, Iterable):
    #             words.extend(word_or_words)
            
    #         if any([word  for word in words if )

    # if not check_noun(tokens, ('NNG:토마토', 'NNP:도마도', 'SL:tomato'), ('', '', '')):
    #     return


    #     check_all())

    # if bla(text, ['NNG:토마토 and ', 'NP': '뭐', 'VCP': '이'}):
    #     return '토마토란 blabla 입니다.'
