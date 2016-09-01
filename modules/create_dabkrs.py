from pydal import DAL, Field
import re
dsl_pattern=re.compile("(?m)^\n([^ ].*?)\n (.*?)\n (.*?)$")
dabkrs=DAL(uri='sqlite://dabkrs.sqlite')

slovar = dabkrs.define_table('slovar',
                             Field('slovo','string',unique=True,label="Слово"),
                             Field('pinyin',label="Пиньин"),
                             Field('perevod',"text",label="Перевод"),
                             Field('dlina','integer',compute=lambda row:len(row.slovo),label="Длина"),
                             Field('sostav','list:reference slovar'),
                             Field('links','list:reference slovar'),
                             )
#slovar.truncate()
#dabkrs.executesql('CREATE INDEX IF NOT EXISTS slovoidx ON dabkrs (slovo);')
#dabkrs.executesql('CREATE INDEX IF NOT EXISTS pinyinidx ON dabkrs (pinyin);')
#dabkrs.executesql('CREATE INDEX IF NOT EXISTS perevodidx ON dabkrs (perevod);')
file='dabkrs_160829'
#file='dabkrs_test.dsl'
with open(file,mode='r',encoding='utf-8') as f:
    n=len(f.readlines())
    f.close()

with open(file,mode='r',encoding='utf-8') as f:
    i,j=0,0
    #файл большой, поэтому читаем его блоками по 10000 строк
    nbl=10000
    block=[f.readline()]
    while block[-1]:
        block=[block[-1]]
        [block.append(f.readline()) for i in range(nbl)]
        i+=nbl
        #блок должен заканчиваться на строке "\n" либо на символе конца файла, проверяем и читаем дальше, пока не найдем эту строку
        while block[-1]!="\n" and block[-1]!="":
            block.append(f.readline())
        for slovo,pinyin,perevod in dsl_pattern.findall("".join(block)):
            try:
                slovar.insert(slovo=slovo,pinyin=pinyin,perevod=perevod)
                j+=1
            except:
                print(slovo,perevod)
        if j%10000==0:dabkrs.commit()
        print(round(i/n*100,2)," %",j,end="\r")
    f.close()
    dabkrs.commit()