import jieba

punctuation="。，、＇：∶；?‘’“”〝〞ˆˇ﹕︰﹔﹖﹑·¨….¸;！´？！～—ˉ｜‖＂〃｀@﹫¡¿﹏﹋﹌︴々﹟#﹩$﹠&﹪%*﹡﹢﹦﹤‐￣¯―﹨ˆ˜﹍﹎+=<­­＿_-\ˇ~﹉﹊（）〈〉‹›﹛﹜『』〖〗［］《》〔〕{}「」【】︵︷︿︹︽_﹁﹃︻︶︸﹀︺︾ˉ﹂﹄︼\n\r\t\"';:,<.>/?-_=+()*&^%$#@!`~"

stopwords=open("hit_stopwords.txt","r").read().split('\n')

def tokenization(text, remove_stopwords=True):
    for ch in punctuation:
        text=text.replace(ch,' ')
    ret=jieba.cut(text,cut_all=True)
    if remove_stopwords:
        ret=filter(lambda w:w not in stopwords,ret)
    return list(ret)