

'''
Задание для студентов МИИГАиК - Вариант 1 (2024г)

Используя любой скриптовый язык (напр Python, Ruby, Javascript, Perl) написать скрипт, извлекающий новости (отдельно заголовок, анотацию, авторов) из веб-страницы новостного агенства, но не используя RSS. 
Требуется написать такой скрипт, который будучи запущен на на определенное время (например 4 часа) автоматически выделит и отобразит/запишет в лог все статьи, которые будут опубликованы за этот период (т.е. только новые), 
при этом выводить нужно новости содержащие упоминания Республиканской и Демократической партий США.
'''

# read-news-11.py

import datetime, requests, time

# 1. Constants

proxies_asDict = {'http': 'http://localhost:9080', 'http://https': 'localhost:9080'}
##print("1. N_17: ", "proxies_asDict=", proxies_asDict )

# 2. Types

# 2.1. Один заголовок-новости-NewsHdlin, как Dictionary/Словарь
# one NewsHdlin: structure
# { 'agency' : 'abbrev',   # NewsAgency/Агентство-новостей
#   'newsHdlin' : 'text',  # NewsHeadline/ЗаголовокНовости
#   'newsAnnot' : 'text',  # NewsAnnotation/АннотацияНовости
#   'newsAuthor' : 'text', # NewsAuthor/АвторНовости
#   'newsURL' : 'text',    # News URL
#   'match1' : boolean,    # Match2_1criteria/Соответствие_1критерию
#   'match2' : boolean,    # Match2_2criteria/Соответствие_2критерию
#   'datetime' : datetime  # DateTime/ДатаВремя
#   }

# one NewsHdlin: example
# [ 'lenta', "Стало известно о запрете американским дипломатам посещать инаугурацию", "2Стало известно о запрете американским дипломатам посещать инаугурацию", "", False, False, datetime.datetime.today() ]

# 2.2. Список-заголовков-новостей, состоящий из заголовок-новости-NewsHdlin, как List/Список из элементов Dictionary/Словарь

# Списков Список-заголовков-новостей несколько:
# - Список-заголовков-новостей нефильтрованный, только что прочитанный с HTML-страничка NewsAgency/Агентство-новостей, удаляемый
# List1NewsHdlin_Unflt_asList: example
# [   { 'lenta', "Успехи физических наук", "2Успехи физических наук", "", False, False, datetime.datetime.today() }
#   , { 'lenta', "Повышены зарплаты академикам", "2Повышены зарплаты академикам", "", False, False, datetime.datetime.today() }
#   , { 'lenta', "Провал демократической партии США", "2Провал демократической партии США", "", True, False, datetime.datetime.today() }
#   , { 'lenta', "Запрет атрибутики Победы в Германии", "2Запрет атрибутики Победы в Германии", "", False, False, datetime.datetime.today() }
#   , { 'lenta', "Назван новый фаворит на пост главного тренера «Баварии»", "2Назван новый фаворит на пост главного тренера «Баварии»", "", False, False, datetime.datetime.today() }
#   , { 'lenta', "набор очков республиканской партией США", "2набор очков республиканской партией США", "", False, True, datetime.datetime.today() }
#   , { 'lenta', "Победы химических наук", "2Победы химических наук", "", False, False, datetime.datetime.today() }
# ] 

# List1NewsHdlin_Unflt_asList: example
# [   { 'cbsnews', "failure of the US Democratic Party", "2failure of the US Democratic Party", "", True, False, datetime.datetime.today() }
#   , { 'cbsnews', "improving the position of the Republican Party of the USA", "2improving the position of the Republican Party of the USA", "", False, True, datetime.datetime.today() }
#   , { 'nytimes', "Trump and R.N.C. Announce $141 Million Haul in May", "2Trump and R.N.C. Announce $141 Million Haul in May", "", False, True, datetime.datetime.today() }
#   , { 'nytimes', "Biden Goes After Trump’s Felon Status at Connecticut Fund-Raiser", "2Biden Goes After Trump’s Felon Status at Connecticut Fund-Raiser", "", False, True, datetime.datetime.today() }
# ]

# - Список-заголовков-новостей отфильтрованный, содержит только те заголовок-новости-NewsHdlin, которые соответствуют Match2_1criteria/Соответствие_1критерию или Match2_2criteria/Соответствие_2критерию, удаляемый, unsorted
# List2NewsHdlin_Flt_asList: example
# [   { 'lenta', "Провал демократической партии США", "2Провал демократической партии США", "", True, False, datetime.datetime.today() }
#   , { 'lenta', "набор очков республиканской партией США", "2набор очков республиканской партией США", "", False, True, datetime.datetime.today() }
#   , { 'cbsnews', "failure of the US Democratic Party", "2failure of the US Democratic Party", "", True, False, datetime.datetime.today() }
#   , { 'cbsnews', "improving the position of the Republican Party of the USA", "2improving the position of the Republican Party of the USA", "", False, True, datetime.datetime.today() }
# ] 

# 3. Переменные глобальные сгруппированные

# 3.1. Переменные для Крутилка-RotatingBarProgressor

RotatBarPrg_patt = ' -/|\\'
RotatBarPrg_currPos = 0
RotatBarPrg_NinLine = 0
RotatBarPrg_NinLineMax = 10

# 4. Функции

# 4.1. Функция ищёт указанный атрибут/параметр в строке и считываеь его как integer
#      Attrib_find_n_read(strOrig, strAttrib)

def Attrib_find_n_read ( prm_strOrig, prm_strAttrib ):
    ##print("4.1. N_71: ", "prm_strOrig=str({Fstr1})str".format(Fstr1=prm_strOrig))
    ##print("4.1. N_72: ", "prm_strAttrib=str({Fstr1})str".format(Fstr1=prm_strAttrib))
    res073 = (-1)
    index074 = prm_strOrig.find(prm_strAttrib)
    ##print("4.1. N_75: ", "index074=", index074 )
    if index074 != -1:
        # found
        str078 = prm_strOrig[ (index074+len(prm_strAttrib)) :]  # со следующего символа после окончания "атрибут/параметр", по конец строки включительно
        ##print("4.1. N_79: ", "str078=str({Fstr1})str".format(Fstr1=str078))
        num080_asStr = ""
        for ch1 in str078:
            if ch1.isdigit():
                num080_asStr = num080_asStr + ch1
            else:
                break
        res073 = int(num080_asStr)
    # а если не нашли, то остаётся (-1)

    ##print("4.1. N_89: ", "res073=", res073 )
    return res073
# end of def Attrib_find_n_read



# 4.2. Функция проверяет строки на ключевые слова,
#      относящиеся к Democratic Party / Демократическая партия
#      Chk4DemocrParty( oneNewsHdlin1_newsHdlin, oneNewsHdlin1_newsAnnot )

def Chk4DemocrParty ( prm_str1, prm_str2 ):
    # Constants
    keywords_asList = ['Democrat', 'Демократ', 'Biden', 'Байден']

    resChk4 = False
    prm_str3 = prm_str1 + ' ' + prm_str2
    ##print("4.2. N_105: ", "prm_str3=", prm_str3 )
    for keyword103 in keywords_asList:
        if int(prm_str3.find(keyword103)) >= 0:
            resChk4 = True
            break
    ##print("4.2. N_110: ", "resChk4=", resChk4 )
    return resChk4



# 4.3. Функция проверяет строки на ключевые слова,
#      относящиеся к Republican Party / Республиканская партия
#      Chk4DemocrParty( oneNewsHdlin1_newsHdlin, oneNewsHdlin1_newsAnnot )

def Chk4RepublParty ( prm_str1, prm_str2 ):
    # Constants
    keywords_asList = ['Republic', 'Республикан', 'Trump', 'Трамп']

    resChk4 = False
    prm_str3 = prm_str1 + ' ' + prm_str2
    ##print("4.3. N_125: ", "prm_str3=", prm_str3 )
    for keyword120 in keywords_asList:
        if int(prm_str3.find(keyword120)) >= 0:
            resChk4 = True
            break
    ##print("4.3. N_130: ", "resChk4=", resChk4 )
    return resChk4



# 4.4. Функция выделяет из HTML-страничка все HTML-заголовки новостей
#      и дополняет их в List2NewsHdlin_Flt_asList и в лог/протокол
#      Mk_CBSNews_List2NewsHdlin( prm_pageNews1 )

def Mk_CBSNews_List2NewsHdlin( prm_pageNews1 ):
    # Constants
    whitespaceChars_asStr = ' \f\n\r\t\v'
    tag_AnchorSta = '<a '
    tag_anyFin = '>'
    tag_H4Fin = '</h4>'
    tag_H4Sta = '<h4 '
    tag_href = 'href='
    tag_P_Fin = '</p>'
    tag_P_Sta = '<p '

    str_pageNews1 = prm_pageNews1[:] # создаём копию путём full_selection/полной_вырезки
    isNewsHdlin_present = True  # чтобы не было предупреждения "Переменная не инициализирована"
    while len(str_pageNews1) > 0:
        # 4.4.1. Инициализации

        isNewsHdlin_present = True  # чтобы не было предупреждения "Переменная не инициализирована"
        oneNewsHdlin1_asDict = {}  # create an empty dictionary
        oneNewsHdlin1_agency = 'cbsnews'
        oneNewsHdlin1_newsHdlin = ''
        oneNewsHdlin1_newsAnnot = ''
        oneNewsHdlin1_newsAuthor = ''
        oneNewsHdlin1_newsURL = ''
        oneNewsHdlin1_match1 = False
        oneNewsHdlin1_match2 = False
        oneNewsHdlin1_asDatetime = datetime.datetime.today()
        #                          library |class_exemplar|method

        # 4.4.2. Ищем начало тэга H3 (HTML-заголовок-новости)
        #        и запоминаем начало строки. Это может понадобиться...

        index170 = int(str_pageNews1.find(tag_H4Sta))
        ##print("4.4.2. N_171: ", "index170=", index170 )
        if index170 < 0:
            break  # Заголовки новостей кончились

        # HTML-страничка содержит (в HTML-заголовок-новости) тэги-неправильно-вложенные:
        #       <a ><h4 >___</h4></a><p >___</p> ...itemprop="name">___</span>

        str178beforeH3 = str_pageNews1[ : index170 ]  # с начала строки до тэга "tag_H4Sta"_невключительно. Это понадобится...
        ##print("4.4.2. N_179: ", "str178beforeH3=str({Fstr1})str".format(Fstr1=str178beforeH3[ -512 : ]) )
        str_pageNews1 = str_pageNews1[ (index170+len(tag_H4Sta)) : ]  # со следующего символа после окончания "tag_H4Sta", по конец строки включительно
        ##print("4.4.2. N_181: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

        # Пропускаем всю-первую-часть-тэга tag_H4Sta
        index184 = int(str_pageNews1.find(tag_anyFin))
        ##print("4.4.2. N_185: ", "index184=", index184 )
        str_pageNews1 = str_pageNews1[ (index184+len(tag_anyFin)) : ]  # со следующего символа после окончания "tag_anyFin", по конец строки включительно
        ##print("4.4.2. N_187: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

        # 4.4.3. Обрабатываем тэг Anchor (в HTML-заголовок-новости), сохранённый в str178beforeH3

        # Ищем начало тэга Anchor (в HTML-заголовок-новости)
        index192 = int(str178beforeH3.rfind(tag_AnchorSta))
        ##print("4.4.3. N_193: ", "index185=", index192 )
        ###if index192 >= 3105:
        ###    print("4.4.3. N_195: ", "str178beforeH3=str({Fstr1})str".format(Fstr1=str178beforeH3[ -512 : ]) )

        str197anchor = str178beforeH3[ index192 : ]  # с начала тэга "tag_AnchorSta", по конец строки включительно
        ##print("3.5.4. N_198: ", "str197anchor=str({Fstr1})str".format(Fstr1=str197anchor) )

        # 4.4.3.1. Заполняем oneNewsHdlin1_newsURL

        # Начало тэга href
        index203 = int(str197anchor.find(tag_href))
        ##print("4.4.3.1. N_204: ", "index203=", index203 )
        str205href = str197anchor[ (index203 + len(tag_href)) : ]  # со следующего символа после окончания "tag_href", по конец строки включительно
        ##print("4.4.3.1. N_206: ", "str205href=str({Fstr1})str".format(Fstr1=str205href) )

        # Пропускаем первый символ
        char209 = str205href[0]
        if char209 == '"':
            str205href = str205href[1:]

        # News URL заканчивается по пробелу либо по двойной кавычке
        str214href = ""
        while len(str205href) > 0 and not (str205href[0] == '"' or str205href[0] == ' '):
            str214href = str214href + str205href[0]
            str205href = str205href[1:]
        oneNewsHdlin1_newsURL = str214href
        ##print("4.4.3.1. N_219: ", "oneNewsHdlin1_newsURL=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsURL) )
        isNewsHdlin_present = (len(oneNewsHdlin1_newsURL) > 0)
        ##print("4.4.3.1. N_221: ", "isNewsHdlin_present=", isNewsHdlin_present)
        ###if not isNewsHdlin_present:
        ###    print("4.4.3.1. N_223: ", "isNewsHdlin_present=", isNewsHdlin_present)

        # 4.4.3.2. Заполняем oneNewsHdlin1_newsHdlin

        if isNewsHdlin_present:
            index228 = int(str_pageNews1.find(tag_H4Fin))
            ##print("4.4.3.2. N_229: ", "index228=", index228 )
            str230NewsHdlin = str_pageNews1[: index228]  # с начала строки до "tag_H4Fin"_невключительно
            ##print("4.4.3.2. N_231: ", "str230NewsHdlin=str({Fstr1})str".format(Fstr1=str230NewsHdlin) )
            str_pageNews1 = str_pageNews1[ (index228 + len(tag_H4Fin)) : ]  # со следующего символа после окончания "tag_H4Fin", по конец строки включительно
            ##print("4.4.4.2. N_233: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # 4.4.4.3. Translate whitespace characters to blanks/spaces
            str236table = str230NewsHdlin.maketrans('\f\n\r\t\v', '     ')  # Define a mapping table
            #                                        -----5----    --5--
            str230NewsHdlin = str230NewsHdlin.translate(str.maketrans(str236table))

            # Remove heading/trailing whitespace characters
            str230NewsHdlin = str230NewsHdlin.lstrip(whitespaceChars_asStr)
            str230NewsHdlin = str230NewsHdlin.rstrip(whitespaceChars_asStr)
            ##print("4.4.3.3. N_243: ", "str230NewsHdlin=str({Fstr1})str".format(Fstr1=str230NewsHdlin) )

            oneNewsHdlin1_newsHdlin = str230NewsHdlin
            ##print("4.4.3.3. N_246: ", "oneNewsHdlin1_newsHdlin=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsHdlin) )
        # end of if isNewsHdlin_present:

        # 4.4.3.3. Заполняем oneNewsHdlin1_newsAnnot

        if isNewsHdlin_present:
            # Начало тэга p
            index253 = int(str_pageNews1.find(tag_P_Sta))
            ##print("4.4.3.3. N_254: ", "index253=", index253 )
            str_pageNews1 = str_pageNews1[ (index253 + len(tag_P_Sta)) : ]  # со следующего символа после окончания "tag_P_Sta", по конец строки включительно
            ##print("4.4.3.3. N_256: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # Окончание первой части тэга p
            index259 = int(str_pageNews1.find(tag_anyFin))
            ##print("4.4.3.3. N_260: ", "index259=", index259 )
            str_pageNews1 = str_pageNews1[ (index259 + len(tag_anyFin)) : ]  # со следующего символа после окончания "tag_anyFin", по конец строки включительно
            ##print("4.4.3.3. N_262: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # Окончание всего тэга p
            index265 = int(str_pageNews1.find(tag_P_Fin))
            ##print("4.4.4.3. N_266: ", "index265=", index265 )
            str267newsAnnot = str_pageNews1[: index265]  # с начала строки до "tag_P_Fin"_невключительно
            ##print("4.4.4.3. N_268: ", "str267newsAnnot=str({Fstr1})str".format(Fstr1=str267newsAnnot) )
            str_pageNews1 = str_pageNews1[ (index265 + len(tag_P_Fin)) : ]  # со следующего символа после окончания "tag_P_Fin", по конец строки включительно
            ##print("4.4.4.3. N_270: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # Translate whitespace characters to blanks/spaces
            str273table = str267newsAnnot.maketrans('\f\n\r\t\v', '     ')  # Define a mapping table
            #                                        -----5----    --5--
            str267newsAnnot = str267newsAnnot.translate(str.maketrans(str273table))

            # Remove heading/trailing whitespace characters
            str267newsAnnot = str267newsAnnot.lstrip(whitespaceChars_asStr)
            str267newsAnnot = str267newsAnnot.rstrip(whitespaceChars_asStr)
            ##print("4.4.3.3. N_280: ", "str267newsAnnot=str({Fstr1})str".format(Fstr1=str267newsAnnot) )

            oneNewsHdlin1_newsAnnot = str267newsAnnot
            ##print("4.4.3.3. N_283: ", "oneNewsHdlin1_newsAnnot=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsAnnot) )
        # end of if isNewsHdlin_present:

        # 4.4.4. Заполняем oneNewsHdlin1_asDict

        if isNewsHdlin_present:
            oneNewsHdlin1_asDict['agency'] = oneNewsHdlin1_agency
            oneNewsHdlin1_asDict['newsHdlin'] = oneNewsHdlin1_newsHdlin
            oneNewsHdlin1_asDict['newsAnnot'] = oneNewsHdlin1_newsAnnot
            oneNewsHdlin1_asDict['newsAuthor'] = oneNewsHdlin1_newsAuthor
            oneNewsHdlin1_asDict['newsURL'] = oneNewsHdlin1_newsURL
            oneNewsHdlin1_asDict['match1'] = Chk4DemocrParty( oneNewsHdlin1_newsHdlin, oneNewsHdlin1_newsAnnot )  # Democratic Party
            oneNewsHdlin1_asDict['match2'] = Chk4RepublParty( oneNewsHdlin1_newsHdlin, oneNewsHdlin1_newsAnnot )  # Republican Party
            oneNewsHdlin1_asDict['datetime'] = oneNewsHdlin1_asDatetime
            ##print("4.4.4. N_297: ", "type=", type(oneNewsHdlin1_asDict), "; oneNewsHdlin1_asDict=", oneNewsHdlin1_asDict )

            # 4.4.5. Дополняем List1NewsHdlin_Unflt_asList и List2NewsHdlin_Flt_asList

            NewsHdlin_Add( oneNewsHdlin1_asDict )
            ##print("4.4.5. N_302: ", "len(str_pageNews1)=", len(str_pageNews1) )
            ###if len(List1NewsHdlin_Unflt_asList) == 132:  # 132 - номер действительно последней новости на HTML-страничка
            ###    print("3.5.4. N_304: ", "len(str_pageNews1)=", len(str_pageNews1) )
        # end of if isNewsHdlin_present:

    # end of while len(str_pageNews1) > 0:
    ##print("4.4. N_308: ", "; len(List1NewsHdlin_Unflt_asList)=", len(List1NewsHdlin_Unflt_asList) )
    ##print("4.4. N_309: ", "type=", type(List1NewsHdlin_Unflt_asList), "; List1NewsHdlin_Unflt_asList=", List1NewsHdlin_Unflt_asList )
    ##str310 = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S+03')
    ##print("4.4. N_311: ", str310, "; len(List2NewsHdlin_Flt_asList)=", len(List2NewsHdlin_Flt_asList), flush=True )
    str322 = datetime.datetime.today().minute
    RotatBarProgrs_Step()
    RotatBarProgrs_Print2( str322, len(List2NewsHdlin_Flt_asList) )
# end of def Mk_CBSNews_List2NewsHdlin( prm_pageNews1 ):



# 4.5. Функция выделяет из HTML-страничка все HTML-заголовки новостей
#      и дополняет их в List2NewsHdlin_Flt_asList и в лог/протокол
#      Mk_NYTimes_List2NewsHdlin( prm_pageNews1 )

def Mk_NYTimes_List2NewsHdlin( prm_pageNews1 ):
    # Constants
    tag_AnchorSta = '<a '
    tag_AnchorFin = '</a>'
    tag_anyStart = '<'
    tag_anyFin = '>'
    tag_H3Sta = '<h3 '
    tag_href = 'href='
    tag_P_Sta = '<p '
    tag_P_Fin = '</p>'

    andBetweenAuthorsSkipped = False
    partOf_HTML_Newspage = 0

    str_pageNews1 = prm_pageNews1[:] # создаём копию путём full_selection/полной_вырезки
    while len(str_pageNews1) > 0:
        # 4.5.0. Инициализации

        oneNewsHdlin1_asDict = {}  # create an empty dictionary
        oneNewsHdlin1_agency = 'nytimes'
        oneNewsHdlin1_newsHdlin = ''
        oneNewsHdlin1_newsAnnot = ''
        oneNewsHdlin1_newsAuthor = ''
        oneNewsHdlin1_newsURL = ''
        oneNewsHdlin1_match1 = False
        oneNewsHdlin1_match2 = False
        oneNewsHdlin1_asDatetime = datetime.datetime.today()
        #                          library |class_exemplar|method
        andBetweenAuthorsSkipped = False

        # 4.5.1. Ищем начало тэга H3 (HTML-заголовок-новости)
        #        и запоминаем начало строки. Это может понадобиться...

        index165 = int(str_pageNews1.find(tag_H3Sta))
        ##print("4.5.1. N_353: ", "index165=", index165 )
        if index165 < 0:
            break  # Заголовки новостей кончились

        str170beforeH3 = str_pageNews1[ : index165 ]  # с начала строки до тэга "tag_H3Sta"_невключительно. Это может понадобиться...
        ##print("4.5.1. N_358: ", "str170beforeH3=str({Fstr1})str".format(Fstr1=str170beforeH3[ -512 : ]) )
        str_pageNews1 = str_pageNews1[ (index165+len(tag_H3Sta)) : ]  # со следующего символа после окончания "tag_H3Sta", по конец строки включительно
        ##print("4.5.1. N_360: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

        # HTML-страничка может содержать (в HTML-заголовок-новости) тэги-правильно-вложенные:
        #       <h3 ><a >___</a></h3><p >___</p> ...itemprop="name">___</span>
        # а может содержать (в HTML-заголовок-новости) и тэги-неправильно-вложенные:
        #       <a ><h3 >___</h3></a><p >___</p> ...itemprop="name">___</span>

        # 4.5.2. Распознавание вида вложения тэгов

        # Пропускаем всю-первую-часть-тэга tag_H3Sta
        index183 = int(str_pageNews1.find(tag_anyFin))
        ##print("4.5.2. N_371: ", "index183=", index183 )
        str_pageNews1 = str_pageNews1[ (index183+len(tag_anyFin)) : ]  # со следующего символа после окончания "tag_anyFin", по конец строки включительно
        ##print("4.5.2. N_373: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

        # Проверяем следующие символы/тэг
        str189 = str_pageNews1[ : len(tag_AnchorSta) ]
        ##print("4.5.2. N_377: ", "str189=str({Fstr1})str".format(Fstr1=str189) )
        if str189 == tag_AnchorSta:
            # тэги-правильно-вложенные: <h3 ><a >___</a></h3><p >___</p> ...itemprop="name">___</span>
            ##print("4.5.2. N_380: ", '<h3 ><a >___</a></h3><p >___</p> ...itemprop="name">___</span>' )

            if partOf_HTML_Newspage < 1:
                partOf_HTML_Newspage = 1  # Первая часть новостей на HTML-страничка
            ##print("4.5.2. N_384: ", "partOf_HTML_Newspage=", partOf_HTML_Newspage )

            # 4.5.3. Обрабатываем тэг Anchor (в HTML-заголовок-новости)

            # 4.5.3.1. Ищем начало тэга Anchor (в HTML-заголовок-новости)
            index202 = int(str_pageNews1.find(tag_AnchorSta))
            ##print("4.5.3.1. N_390: ", "index202=", index202 )
            str_pageNews1 = str_pageNews1[ (index202+len(tag_AnchorSta)) : ]  # со следующего символа после окончания "tag_AnchorSta", по конец строки включительно
            ##print("4.5.3.1. N_392: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # 4.5.3.2. Ищем окончание тэга Anchor (в HTML-заголовок-новости)
            index208 = int(str_pageNews1.find(tag_AnchorFin))
            ##print("4.5.3.2. N_396: ", "index208=", index208 )
            str210anchor = str_pageNews1[ 0 : index208 ]  # тэг "tag_AnchorFin" не включаем
            ##print("4.5.3.2. N_398: ", "str210anchor=str({Fstr1})str".format(Fstr1=str210anchor) )
            str_pageNews1 = str_pageNews1[ (index208+len(tag_AnchorFin)) : ]  # со следующего символа после окончания "tag_AnchorFin", по конец строки включительно
            ##print("4.5.3.2. N_400: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # 4.5.3.3. Заполняем oneNewsHdlin1_newsURL

            # Начало тэга href
            index218 = int(str210anchor.find(tag_href))
            ##print("4.5.3.3. N_406: ", "index218=", index218 )
            str220href_NewsHdlin = str210anchor[ (index218+len(tag_href)) : ]  # со следующего символа после окончания "tag_href", по конец строки включительно
            ##print("4.5.3.3. N_408: ", "str220href_NewsHdlin=str({Fstr1})str".format(Fstr1=str220href_NewsHdlin) )

            # Пропускаем первый символ
            char224 = str220href_NewsHdlin[0]
            if char224 == '"':
                str220href_NewsHdlin = str220href_NewsHdlin[1:]

            # News URL заканчивается по пробелу либо по двойной кавычке
            str229href = ""
            while len(str220href_NewsHdlin) > 0 and not (str220href_NewsHdlin[0] == '"' or str220href_NewsHdlin[0] == ' '):
                str229href = str229href + str220href_NewsHdlin[0]
                str220href_NewsHdlin = str220href_NewsHdlin[1:]
            if len(str220href_NewsHdlin) > 0 and (str220href_NewsHdlin[0] == '"' or str220href_NewsHdlin[0] == ' '):
                str220href_NewsHdlin = str220href_NewsHdlin[1:]
            oneNewsHdlin1_newsURL = str229href
            ##print("4.5.3.3. N_423: ", "oneNewsHdlin1_newsURL=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsURL) )
            # str220href_NewsHdlin содержит лишний символ tag_anyFin  и далее заголовок-новости oneNewsHdlin1_newsHdlin
            ##print("4.5.3.3. N_425: ", "str220href_NewsHdlin=str({Fstr1})str".format(Fstr1=str220href_NewsHdlin) )

            # 4.5.3.4. Заполняем oneNewsHdlin1_newsHdlin

            # Окончание первой части тэга anchor
            index243 = int(str220href_NewsHdlin.find(tag_anyFin))
            ##print("4.5.3.4. N_431: ", "index243=", index243 )
            str220href_NewsHdlin = str220href_NewsHdlin[ (index243+len(tag_anyFin)) : ]  # со следующего символа после окончания "tag_anyFin", по конец строки включительно
            ##print("4.5.3.4. N_433: ", "str220href_NewsHdlin=str({Fstr1})str".format(Fstr1=str220href_NewsHdlin) )

            oneNewsHdlin1_newsHdlin = str220href_NewsHdlin
            ##print("4.5.2.3.4. N_436: ", "oneNewsHdlin1_newsHdlin=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsHdlin))

            # 4.5.3.5. Заполняем oneNewsHdlin1_newsAnnot

            #  Начало тэга p
            index254 = int(str_pageNews1.find(tag_P_Sta))
            ##print("4.5.3.5. N_442: ", "index254=", index254 )
            str_pageNews1 = str_pageNews1[ (index254+len(tag_P_Sta)) : ]  # со следующего символа после окончания "tag_P_Sta", по конец строки включительно
            ##print("4.5.3.5. N_444: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # Окончание первой части тэга p
            index260 = int(str_pageNews1.find(tag_anyFin))
            ##print("4.5.3.5. N_448: ", "index260=", index260 )
            str_pageNews1 = str_pageNews1[ (index260+len(tag_anyFin)) : ]  # со следующего символа после окончания "tag_anyFin", по конец строки включительно
            ##print("4.5.3.5. N_450: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # Окончание всего тэга p
            index266 = int(str_pageNews1.find(tag_P_Fin))
            ##print("4.5.3.5. N_454: ", "index266=", index266 )
            str268newsAnnot = str_pageNews1[ : index266 ]  # с начала строки до "tag_P_Fin"_невключительно
            ##print("4.5.3.5. N_456: ", "str268newsAnnot=str({Fstr1})str".format(Fstr1=str268newsAnnot) )
            str_pageNews1 = str_pageNews1[ (index266+len(tag_P_Fin)) : ]  # со следующего символа после окончания "tag_P_Fin", по конец строки включительно
            ##print("4.5.3.5. N_458: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # Translate whitespace characters to blanks/spaces
            str274table = str268newsAnnot.maketrans('\f\n\r\t\v', '     ')  # Define a mapping table
            #                                        -----5----    --5--
            str276newsAnnot = str268newsAnnot.translate(str.maketrans(str274table) )
            ##print("4.5.3.5. N_464: ", "str276newsAnnot=str({Fstr1})str".format(Fstr1=str276newsAnnot) )

            oneNewsHdlin1_newsAnnot = str276newsAnnot
            ##print("4.5.3.5. N_467: ", "oneNewsHdlin1_newsAnnot=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsAnnot))

            # 4.5.3.6. Заполняем oneNewsHdlin1_newsAuthor

            # Constants
            patt_itemprop_name = 'itemprop="name"'

            #  Авторов может быть несколько, поэтому выделяем длинную подстроку для анализа
            #  от itemprop="name"> и возможно itemprop="name">  до </p>_невключительно
            oneNewsHdlin1_newsAuthor = ""

            #  Начало невыделенный-список-newsAuthor
            index292 = int(str_pageNews1.find(patt_itemprop_name))
            ##print("4.5.3.6. N_480: ", "index292=", index292 )
            if index292 >= 0:
                str_pageNews1 = str_pageNews1[ index292 :]  # с первого символа "patt_itemprop_name", по конец строки включительно
                ##print("4.5.3.6. N_483: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

                # Окончание невыделенный-список-newsAuthor
                index299 = int(str_pageNews1.find(tag_P_Fin))
                ##print("4.5.3.6. N_487: ", "index299=", index299 )
                str301newsAuthor = str_pageNews1[ : index299 ]  # до первого символа "tag_P_Fin"_невключительно
                ##print("4.5.3.6. N_489: ", "str301newsAuthor=str({Fstr1})str".format(Fstr1=str301newsAuthor) )
                str_pageNews1 = str_pageNews1[ (index299+len(tag_P_Fin)) : ]  # со следующего символа после окончания "tag_P_Fin", по конец строки включительно
                ##print("4.5.3.6. N_491: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

                # Выделение всех newsAuthor из невыделенный-список-newsAuthor
                while int(str301newsAuthor.find(patt_itemprop_name)) >= 0:
                    #  Начало образца-для-newsAuthor
                    index309 = int(str301newsAuthor.find(patt_itemprop_name))
                    ##print("4.5.3.6. N_497: ", "index309=", index309 )
                    str301newsAuthor = str301newsAuthor[ (index309+len(patt_itemprop_name)) : ]  # со следующего символа после окончания "patt_itemprop_name", по конец строки включительно
                    ##print("4.5.3.6. N_499: ", "str301newsAuthor=str({Fstr1})str".format(Fstr1=str301newsAuthor) )

                    # Окончание тэга перед newsAuthor
                    index315 = int(str301newsAuthor.find(tag_anyFin))
                    ##print("4.5.3.6. N_503: ", "index315=", index315 )
                    str301newsAuthor = str301newsAuthor[ (index315+len(tag_anyFin)) : ]  # со следующего символа после окончания "tag_anyFin", по конец строки включительно
                    ##print("4.5.3.6. N_505: ", "str301newsAuthor=str({Fstr1})str".format(Fstr1=str301newsAuthor) )

                    # newsAuthor заканчивается по tag_anyStart
                    if len(oneNewsHdlin1_newsAuthor) > 0:
                        oneNewsHdlin1_newsAuthor = oneNewsHdlin1_newsAuthor + " and "
                    while len(str301newsAuthor) > 0 and str301newsAuthor[0] != tag_anyStart:
                        oneNewsHdlin1_newsAuthor = oneNewsHdlin1_newsAuthor + str301newsAuthor[0]
                        str301newsAuthor = str301newsAuthor[1:]
                    ##print("4.5.3.6. N_513: ", "oneNewsHdlin1_newsAuthor=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsAuthor) )
                    ##print("4.5.3.6. N_514: ", "str301newsAuthor=str({Fstr1})str".format(Fstr1=str301newsAuthor) )
                # end of while int(str301newsAuthor.find(patt_itemprop_name)) >= 0:
            # end of if index292 >= 0:
            ##print("4.5.3.6. N_517: ", "oneNewsHdlin1_newsAuthor=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsAuthor) )

        # end of if str189 == tag_AnchorSta:

        if str189 != tag_AnchorSta:
            # тэги-неправильно-вложенные: <a ><h3 >___</h3></a><p >___</p> ...itemprop="name">___</span>
            ##print("4.5.4. N_522: ", '<a ><h3 >___</h3></a><p >___</p> ...itemprop="name">___</span>' )
            ##print("4.5.4. N_523: ", "str170beforeH3=str({Fstr1})str".format(Fstr1=str170beforeH3[ -512 : ]))

            if partOf_HTML_Newspage < 2:
                partOf_HTML_Newspage = 2  # Вторая часть новостей на HTML-страничка
            ##print("4.5.4. N_527: ", "partOf_HTML_Newspage=", partOf_HTML_Newspage )

            # 4.5.4. Обрабатываем тэг Anchor (в HTML-заголовок-новости), сохранённый в str170beforeH3

            # Ищем начало тэга Anchor (в HTML-заголовок-новости)
            index345 = int(str170beforeH3.rfind(tag_AnchorSta))
            ##print("4.5.4. N_533: ", "index345=", index345 )
            ###if index345 >= 3105:
            ###    print("4.5.4. N_535: ", "str170beforeH3=str({Fstr1})str".format(Fstr1=str170beforeH3) )

            str350anchor = str170beforeH3[ index345 : ]  # с начала тэга "tag_AnchorSta", по конец строки включительно
            ##print("4.5.4. N_538: ", "str350anchor=str({Fstr1})str".format(Fstr1=str350anchor) )

            # 4.5.4.1. Заполняем oneNewsHdlin1_newsURL

            # Начало тэга href
            index356 = int(str350anchor.find(tag_href))
            ##print("4.5.4.1. N_544: ", "index356=", index356 )
            str358href= str350anchor[ (index356+len(tag_href)) : ]  # со следующего символа после окончания "tag_href", по конец строки включительно
            ##print("4.5.4.1. N_546: ", "str358href=str({Fstr1})str".format(Fstr1=str358href) )

            # Пропускаем первый символ
            char362 = str358href[0]
            if char362 == '"':
                str358href = str358href[1:]

            # News URL заканчивается по пробелу либо по двойной кавычке
            str367href = ""
            while len(str358href) > 0 and not (str358href[0] == '"' or str358href[0] == ' '):
                str367href = str367href + str358href[0]
                str358href = str358href[1:]
            oneNewsHdlin1_newsURL = str367href
            ##print("4.5.4.1. N_559: ", "oneNewsHdlin1_newsURL=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsURL) )

            # 4.5.4.2. Заполняем oneNewsHdlin1_newsHdlin

            # Constants
            patt_newsAnnot = '</a><p'
            tag_H3Fin = '</h3>'

            index380 = int(str_pageNews1.find(tag_H3Fin))
            ##print("4.5.4.2. N_568: ", "index380=", index380 )
            str382NewsHdlin = str_pageNews1[ : index380 ]  # с начала строки до "tag_anyFin"_невключительно
            ##print("4.5.4.2. N_570: ", "str382NewsHdlin=str({Fstr1})str".format(Fstr1=str382NewsHdlin) )
            str_pageNews1 = str_pageNews1[ (index380+len(tag_H3Fin)) : ]  # со следующего символа после окончания "tag_H3Fin", по конец строки включительно
            ##print("4.5.4.2. N_572: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            oneNewsHdlin1_newsHdlin = str382NewsHdlin
            ##print("4.5.4.2. N_575: ", "oneNewsHdlin1_newsHdlin=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsHdlin))

            # 4.5.4.3. Или заполняем oneNewsHdlin1_newsAnnot, или нету oneNewsHdlin1_newsAnnot и это блок меню

            #  Распознавание последовательности тэгов в str_pageNews1
            ##print("4.5.4.3. N_580: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )
            # Проверка на '</a><p'
            str395 = str_pageNews1[: len(patt_newsAnnot)]  # с начала строки по len(patt_newsAnnot)_включительно
            if str395 != patt_newsAnnot:
                partOf_HTML_Newspage = 3  # Третья часть на HTML-страничка - это не новости, а меню
                str_pageNews1 = ""
                break

            #  Начало тэга p
            index402 = int(str_pageNews1.find(tag_P_Sta))
            ##print("4.5.4.3. N_590: ", "index402=", index402 )
            str_pageNews1 = str_pageNews1[ (index402+len(tag_P_Sta)) : ]  # со следующего символа после окончания "tag_P_Sta", по конец строки включительно
            ##print("4.5.4.3. N_592: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # Окончание первой части тэга p
            index408 = int(str_pageNews1.find(tag_anyFin))
            ##print("4.5.4.3. N_596: ", "index408=", index408 )
            str_pageNews1 = str_pageNews1[ (index408+len(tag_anyFin)) : ]  # со следующего символа после окончания "tag_anyFin", по конец строки включительно
            ##print("4.5.4.3. N_598: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # Окончание всего тэга p
            index414 = int(str_pageNews1.find(tag_P_Fin))
            ##print("4.5.4.3. N_602: ", "index414=", index414 )
            str416newsAnnot = str_pageNews1[ : index414 ]  # с начала строки до "tag_P_Fin"_невключительно
            ##print("4.5.4.3. N_604: ", "str416newsAnnot=str({Fstr1})str".format(Fstr1=str416newsAnnot) )
            str_pageNews1 = str_pageNews1[ (index414+len(tag_P_Fin)) : ]  # со следующего символа после окончания "tag_P_Fin", по конец строки включительно
            ##print("4.5.4.3. N_606: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # 4.5.4.4. Translate whitespace characters to blanks/spaces

            str422table = str416newsAnnot.maketrans('\f\n\r\t\v', '     ')  # Define a mapping table
            #                                        -----5----    --5--
            str416newsAnnot = str416newsAnnot.translate(str.maketrans(str422table) )
            ##print("4.5.4.4. N_612: ", "str424newsAnnot=str({Fstr1})str".format(Fstr1=str424newsAnnot) )

            oneNewsHdlin1_newsAnnot = str416newsAnnot
            ##print("4.5.4.4. N_615: ", "oneNewsHdlin1_newsAnnot=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsAnnot))

            # 4.5.4.5. Заполняем oneNewsHdlin1_newsAuthor

            #  Авторов может быть несколько, поэтому выделяем длинную подстроку для анализа
            #  от <p до </p>_невключительно и проверяем на 'By '
            oneNewsHdlin1_newsAuthor = ""

            #  Начало невыделенный-список-newsAuthor
            index437 = int(str_pageNews1.find(tag_P_Sta))
            ##print("4.5.4.5. N_625: ", "index437=", index437 )
            str_pageNews1 = str_pageNews1[ (index437+len(tag_P_Sta)) : ]  # со следующего символа после окончания "tag_P_Sta", по конец строки включительно
            ##print("4.5.4.5. N_627: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )
            index441 = int(str_pageNews1.find(tag_anyFin))
            ##print("4.5.4.5. N_629: ", "index441=", index441 )
            str_pageNews1 = str_pageNews1[ (index441+len(tag_anyFin)) : ]  # со следующего символа после окончания "tag_anyFin", по конец строки включительно
            ##print("4.5.4.5. N_631: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # Окончание невыделенный-список-newsAuthor
            index447 = int(str_pageNews1.find(tag_P_Fin))
            ##print("4.5.4.5. N_635: ", "index447=", index447 )
            str449newsAuthor = str_pageNews1[ : index447 ]  # до первого символа "tag_P_Fin"_невключительно
            ##print("4.5.4.5. N_637: ", "str449newsAuthor=str({Fstr1})str".format(Fstr1=str449newsAuthor) )
            str_pageNews1 = str_pageNews1[ (index447+len(tag_P_Fin)) : ]  # со следующего символа после окончания "tag_P_Fin", по конец строки включительно
            ##print("4.5.4.5. N_639: ", "str_pageNews1=str({Fstr1})str".format(Fstr1=str_pageNews1[:512]) )

            # Выделение всех newsAuthor из невыделенный-список-newsAuthor

            # Constants
            patt_By = 'By '
            tag_SpanSta1 = '<span'
            tag_SpanFin = '</span>'
            whitespaceChars_asStr = ' \f\n\r\t\v'

            index462 = int(str449newsAuthor.find(patt_By))
            ##print("4.5.4.5. N_650: ", "index432=", index462 )
            if index462 >= 0:
                str449newsAuthor = str449newsAuthor[ (index462+len(patt_By)) : ]  # со следующего символа после окончания "patt_By", по конец строки включительно
                ##print("4.5.4.5. N_653: ", "str449newsAuthor=str({Fstr1})str".format(Fstr1=str449newsAuthor))
                while len(str449newsAuthor) > 0:
                    #  Начало образца-для-newsAuthor
                    index469 = int(str449newsAuthor.find(tag_SpanSta1))
                    ##print("4.5.4.5. N_657: ", "index469=", index469 )
                    if index469 >= 0:
                        str449newsAuthor = str449newsAuthor[ (index469+len(tag_SpanSta1)) : ]  # со следующего символа после окончания "tag_SpanSta1", по конец строки включительно
                        ##print("4.5.4.5. N_660: ", "str449newsAuthor=str({Fstr1})str".format(Fstr1=str449newsAuthor) )

                        # Окончание тэга перед newsAuthor
                        index476 = int(str449newsAuthor.find(tag_anyFin))
                        ##print("4.5.4.5. N_664: ", "index445=", index476 )
                        str449newsAuthor = str449newsAuthor[ (index476+len(tag_anyFin)) : ]  # со следующего символа после окончания "tag_anyFin", по конец строки включительно
                        ##print("4.5.4.5. N_666: ", "str449newsAuthor=str({Fstr1})str".format(Fstr1=str449newsAuthor) )
                    # end of if index469 >= 0:

                    # Пропускаем начальные whitespace characters ' \f\n\r\t\v'
                    str449newsAuthor = str449newsAuthor.lstrip(whitespaceChars_asStr)
                    ##print("4.5.4.5. N_671: ", "str449newsAuthor=str({Fstr1})str".format(Fstr1=str449newsAuthor) )

                    if len(oneNewsHdlin1_newsAuthor) > 0:
                        if andBetweenAuthorsSkipped:
                            pass  # не-автор 'and' был пропущен на предыдушем проходе
                        else:
                            oneNewsHdlin1_newsAuthor = oneNewsHdlin1_newsAuthor + ' and '

                    # newsAuthor заканчивается по tag_anyStart
                    str493newsAuthor = ""
                    while len(str449newsAuthor) > 0 and str449newsAuthor[0] != tag_anyStart:
                        str493newsAuthor = str493newsAuthor + str449newsAuthor[0]
                        str449newsAuthor = str449newsAuthor[1:]
                    ##print("4.5.4.5. N_684: ", "str493newsAuthor=str({Fstr1})str".format(Fstr1=str493newsAuthor) )
                    ##print("4.5.4.5. N_685: ", "str449newsAuthor=str({Fstr1})str".format(Fstr1=str449newsAuthor) )

                    # Удаляем хвостовые whitespace characters ' \f\n\r\t\v'
                    str493newsAuthor = str493newsAuthor.rstrip(whitespaceChars_asStr)
                    ##print("4.5.4.5. N_689: ", "str493newsAuthor=str({Fstr1})str".format(Fstr1=str493newsAuthor) )

                    # Проверка на 'and' - нет такого автора
                    if str493newsAuthor == 'and':
                        andBetweenAuthorsSkipped = True
                        str493newsAuthor = ''

                    oneNewsHdlin1_newsAuthor = oneNewsHdlin1_newsAuthor + str493newsAuthor
                    ##print("4.5.4.5. N_697: ", "oneNewsHdlin1_newsAuthor=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsAuthor) )

                    # Проверка на '</span>'
                    str513 = str449newsAuthor[ : len(tag_SpanFin) ]  # с начала строки по len(tag_SpanFin)_включительно
                    if str513 == tag_SpanFin:
                        str449newsAuthor = str449newsAuthor[ len(tag_SpanFin) : ]  # со следующего символа после len(tag_SpanFin), по конец строки включительно
                        ##print("4.5.4.5. N_703: ", "str449newsAuthor=str({Fstr1})str".format(Fstr1=str449newsAuthor) )

                # end of while len(str449newsAuthor) > 0:
            # end of if index462 >= 0:
            ##print("4.5.4.5. N_707: ", "oneNewsHdlin1_newsAuthor=str({Fstr1})str".format(Fstr1=oneNewsHdlin1_newsAuthor) )

        # end of if str189 != tag_AnchorSta:

        # 4.5.3. Заполняем oneNewsHdlin1_asDict

        oneNewsHdlin1_asDict['agency'] = oneNewsHdlin1_agency
        oneNewsHdlin1_asDict['newsHdlin'] = oneNewsHdlin1_newsHdlin
        oneNewsHdlin1_asDict['newsAnnot'] = oneNewsHdlin1_newsAnnot
        oneNewsHdlin1_asDict['newsAuthor'] = oneNewsHdlin1_newsAuthor
        oneNewsHdlin1_asDict['newsURL'] = oneNewsHdlin1_newsURL
        oneNewsHdlin1_asDict['match1'] = Chk4DemocrParty( oneNewsHdlin1_newsHdlin, oneNewsHdlin1_newsAnnot )  # Democratic Party
        oneNewsHdlin1_asDict['match2'] = Chk4RepublParty( oneNewsHdlin1_newsHdlin, oneNewsHdlin1_newsAnnot )  # Republican Party
        oneNewsHdlin1_asDict['datetime'] = oneNewsHdlin1_asDatetime
        ##print("4.5.3. N_721: ", "type=", type(oneNewsHdlin1_asDict), "; oneNewsHdlin1_asDict=", oneNewsHdlin1_asDict )

        # 4.5.4. Дополняем List1NewsHdlin_Unflt_asList и List2NewsHdlin_Flt_asList+

        NewsHdlin_Add( oneNewsHdlin1_asDict )
        ##print("4.5.4. N_726: ", "len(str_pageNews1)=", len(str_pageNews1) )
        ###if len(List1NewsHdlin_Unflt_asList) == 63:  # 63 - номер действительно последней новости на HTML-страничка
        ###    print("4.5.4. N_728: ", "len(str_pageNews1)=", len(str_pageNews1) )

    # end of while len(str_pageNews1) > 0:
    ##print("4.5. N_731: ", "; len(List1NewsHdlin_Unflt_asList)=", len(List1NewsHdlin_Unflt_asList), flush=True )
    ##print("4.5. N_732: ", "type=", type(List1NewsHdlin_Unflt_asList), "; List1NewsHdlin_Unflt_asList=", List1NewsHdlin_Unflt_asList )
    ##str734 = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S+03')
    ##print("4.5. N_735: ", str734, "; len(List2NewsHdlin_Flt_asList)=", len(List2NewsHdlin_Flt_asList), flush=True )
    str751 = datetime.datetime.today().minute
    RotatBarProgrs_Step()
    RotatBarProgrs_Print2( str751, len(List2NewsHdlin_Flt_asList) )
# end of def Mk_NYTimes_List2NewsHdlin( prm_pageNews1 ):



# 4.6. Функция
#      1) Добавляет НОВЫЕ заголовок-новости-NewsHdlin
#         в списки List1NewsHdlin_Unflt_asList и List2NewsHdlin_Flt_asList
#         Проверка новый заголовок-новости-NewsHdlin или нет - по 'newsURL'
#      2) Добавляет строку в лог/протокол
#      NewsHdlin_Add( oneNewsHdlin1_asDict )

def NewsHdlin_Add( oneNewsHdlin2_asDict ):
    List1NewsHdlin_Unflt_asList.append(oneNewsHdlin2_asDict)
    ##print("4.6. N_747: ", "len(List1NewsHdlin_Unflt_asList)=", len(List1NewsHdlin_Unflt_asList) )
    ##print("4.6. N_748: ", "type=", type(List1NewsHdlin_Unflt_asList), "; List1NewsHdlin_Unflt_asList=", List1NewsHdlin_Unflt_asList )

    # Проверяем, нужно ли вообще этот заголовок-новости-NewsHdlin обрабатывать
    if oneNewsHdlin2_asDict['match1'] or oneNewsHdlin2_asDict['match2']:
        if not NewsHdlin_FindBy_newsURL( oneNewsHdlin2_asDict['newsURL'] ):
            # Новый заголовок-новости-NewsHdlin
            List2NewsHdlin_Flt_asList.append(oneNewsHdlin2_asDict)
            RotatBarProgrs_PrintNewlineIfNeeds()
            ##print("4.6. N_755: ", "len(List2NewsHdlin_Flt_asList)=", len(List2NewsHdlin_Flt_asList))
            ##print("4.6. N_756: ", "type=", type(List2NewsHdlin_Flt_asList), "; List2NewsHdlin_Flt_asList=", List2NewsHdlin_Flt_asList )
            str569 = oneNewsHdlin2_asDict['datetime'].strftime('%Y-%m-%dT%H:%M:%S+03')
            print("{Fdattim1} {Fagen1} // {FHdlin1} // {FAnnot1} // {FAuth1}".format(
                     Fdattim1=str569
                    ,Fagen1=oneNewsHdlin2_asDict['agency']
                    ,FHdlin1=oneNewsHdlin2_asDict['newsHdlin']
                    ,FAnnot1=oneNewsHdlin2_asDict['newsAnnot']
                    ,FAuth1=oneNewsHdlin2_asDict['newsAuthor']
                ))
        # end of if not NewsHdlin_FindBy_newsURL( oneNewsHdlin2_asDict['newsURL'] ):
    # end of if oneNewsHdlin2_asDict['match1'] or oneNewsHdlin2_asDict['match2']:

# end of def NewsHdlin_Add( oneNewsHdlin2_asDict ):



# 4.7. Функция ищет указанный URL в List2NewsHdlin_Flt_asList[*]['newsURL']
#      NewsHdlin_FindBy_newsURL( oneNewsHdlin2_asDict['newsURL']

def NewsHdlin_FindBy_newsURL( newsURL2_asStr ):
    res594 = False

    ##print("4.7. N_778: ", "newsURL2_asStr=", newsURL2_asStr )
    ##print("4.7. N_779: ", "type=", type(List2NewsHdlin_Flt_asList), "; len(List2NewsHdlin_Flt_asList)=", len(List2NewsHdlin_Flt_asList))
    ##print("4.7. N_780: ", "; List2NewsHdlin_Flt_asList=", List2NewsHdlin_Flt_asList )
    for oneNewsHdlin3_asDict in List2NewsHdlin_Flt_asList:
        ##print("4.7. N_782: ", "type=", type(oneNewsHdlin3_asDict), "; oneNewsHdlin3_asDict=", oneNewsHdlin3_asDict )
        if newsURL2_asStr == oneNewsHdlin3_asDict['newsURL']:
            res594 = True
            break
    ##print("4.7. N_786: ", "res594=", res594 )
    return res594



# 4.8. Функция читает новости CBSNews в течение не более 4 часов
#      запоминает и логирует поступающие новости
#      ReadNews4h_CBSNews()

def ReadNews4h_CBSNews ():
    global proxies_asDict
    ##print("4.8 N_810: ", "proxies_asDict=", proxies_asDict )
    page1_waitForNewsUpto_asDatetime = (datetime.datetime.today() +
    #                                   library |class_exemplar|method
                                            ##datetime.timedelta(minutes=15)  # только на время отладки
                                            datetime.timedelta(hours=4)
    #                                       library |class_exemplar|parameters
                                        )
    page1_maxAge_asInt = 1  # задержка между перечитываниями по-умолчанию = 1 sec
    toWaitForNews = True

    while toWaitForNews:
        if page1_maxAge_asInt > 0:
            ##if page1_maxAge_asInt >  10:  page1_maxAge_asInt =  10  # только на время отладки
            if page1_maxAge_asInt > 300:  page1_maxAge_asInt = 300  # Перечитываем HTML-страничка разумно часто
            time.sleep(page1_maxAge_asInt)

        now_asDatetime = datetime.datetime.today()
        if now_asDatetime > now_asDatetime:
            # Закончилось время ожидания заголовок-новости-NewsHdlin
            break

        # 4.8.1. Считываем HTML-страничку 'https://www.cbsnews.com/'
        #        и её атрибуты

        url842_asStr = 'https://www.cbsnews.com/'
        ##print("4.8.1. N_843: ", "url842_asStr=str({Fstr1})str".format(Fstr1=url842_asStr))
        headers844_asDict = {'Cache-Control': 'no-cache'}
        req845 = requests.get(url842_asStr, stream=True, proxies=proxies_asDict, headers=headers844_asDict )
        # Считаем, что HTML-страничка всегда считывается

        # 4.8.2. Сохраняем технические-заголовки-странички, строка в формате JSON

        page1Html_Hdr_asDict = req845.headers
        ##print("4.8.2. N_822: ", "type=", type(page1Html_Hdr_asDict), "; req634.page1Html_Hdr_asDict=", page1Html_Hdr_asDict )
        page1Html_Hdr_asStr = str(page1Html_Hdr_asDict)  # Convert the dictionary to a string using str() function
        ##print("4.8.2. N_824: ", "page1Html_Hdr_asStr=str({Fstr1})str".format(Fstr1=page1Html_Hdr_asStr))

        # 4.8.3. Сохраняем текст HTML-странички, строка в формате ByteStr

        page1Html_enc_asBytestr = req845.content  # (decode_unicode=True)

        '''
        with open('l_tests/newsCBS02a-pageTechHdr.json', 'r') as file648:
            page1Html_Hdr_asStr = file648.read().replace('\n', '')
        with open('l_tests/newsCBS02b.html', 'rb') as file650:
            page1Html_enc_asBytestr = file650.read()
        '''
        ##print("4.8.3. N_836: ", "type=", type(page1Html_Hdr_asStr), "req634.page1Html_Hdr_asStr=str({Fstr1})str".format(Fstr1=page1Html_Hdr_asStr) )
        ##print("4.8.3. N_837: ", "type=", type(page1Html_enc_asBytestr), "page1Html_enc_asBytestr=bytestring({Fbytestr1})bytestring".format(Fbytestr1=page1Html_enc_asBytestr[0:512] ) )

        # 4.8.4. Выделяем Max-Age, он же LifeTime, этот параметр описывает, насколько часто обновляется HTML-страничка
        #        Ищем подстроки вида: сначала "'max-age=90", затем ';Max-Age=1800', затем "'s-maxage=600"

        index660 = Attrib_find_n_read(page1Html_Hdr_asStr, "'max-age=")
        ##print("4.8.4. N_843: ", "index660=", index660 )
        if index660 == -1:
            index660 = Attrib_find_n_read(page1Html_Hdr_asStr, ';Max-Age=')
            ##print("4.8.4. N_846: ", "index659=", index660 )
            if index660 == -1:
                index660 = Attrib_find_n_read(page1Html_Hdr_asStr, "'s-maxage=")
                ##print("4.8.4. N_849: ", "index659=", index660 )
        page1_maxAge_asInt = index660
        ##print("4.8.4. N_851: ", "page1_maxAge_asInt=", page1_maxAge_asInt )

        # 4.8.5. Декодируем полученную HTML-страничка, считаем что используется кодировка utf-8

        page1Html_encodg_asStr = 'utf-8'
        page1Html_dec_asStr = page1Html_enc_asBytestr.decode(page1Html_encodg_asStr)
        ##print("4.8.5. N_857: ", "page1Html_dec_asStr=str({Fstr1})str".format(Fstr1=page1Html_dec_asStr[:512] ) )

        # 4.8.6.
        Mk_CBSNews_List2NewsHdlin(page1Html_dec_asStr)
        ##print("4.8.6. N_861: ", "Mk_CBSNews_List2NewsHdlin()" )

        toWaitForNews = datetime.datetime.today() <= page1_waitForNewsUpto_asDatetime
        #               library |class_exemplar|method
    # end of while toWaitForNews:

# end of def ReadNews4h_CBSNews



# 4.9. Функция читает новости NYTimes в течение не более 4 часов
#      запоминает и логирует поступающие новости
#      ReadNews4h_NYTimes()

def ReadNews4h_NYTimes ():
    global proxies_asDict
    ##print("4.9 N_897: ", "proxies_asDict=", proxies_asDict )
    page1_waitForNewsUpto_asDatetime = (datetime.datetime.today() +
    #                                   library |class_exemplar|method
                                            ##datetime.timedelta(minutes=15)  # только на время отладки
                                            datetime.timedelta(hours=4)
    #                                       library |class_exemplar|parameters
                                        )
    page1_maxAge_asInt = 1  # задержка между перечитываниями по-умолчанию = 1 sec
    toWaitForNews = True

    while toWaitForNews:
        if page1_maxAge_asInt > 0:
            ##if page1_maxAge_asInt >  10:  page1_maxAge_asInt =  10  # только на время отладки
            if page1_maxAge_asInt > 300:  page1_maxAge_asInt = 300  # Перечитываем HTML-страничка разумно часто
            time.sleep(page1_maxAge_asInt)

        now_asDatetime = datetime.datetime.today()
        if now_asDatetime > now_asDatetime:
            # Закончилось время ожидания заголовок-новости-NewsHdlin
            break

        # 4.9.1. Считываем HTML-страничку 'https://www.nytimes.com/section/politics'
        #        и её атрибуты

        url930_asStr = 'https://www.nytimes.com/section/politics'
        ##print("4.9.1. N_930: ", "url929_asStr=str({Fstr1})str".format(Fstr1=url929_asStr))
        headers932_asDict = {'Cache-Control': 'no-cache'}
        req933 = requests.get(url930_asStr, stream=True, proxies=proxies_asDict, headers=headers932_asDict )
        # Считаем, что HTML-страничка всегда считывается

        # 4.9.2. Сохраняем технические-заголовки-странички, строка в формате JSON

        page1Html_Hdr_asDict = req933.headers
        ##print("4.9.2. N_900: ", "type=", type(page1Html_Hdr_asDict), "; req708.page1Html_Hdr_asDict=", page1Html_Hdr_asDict )
        page1Html_Hdr_asStr = str(page1Html_Hdr_asDict)  # Convert the dictionary to a string using str() function
        ##print("4.9.2. N_902: ", "page1Html_Hdr_asStr=str({Fstr1})str".format(Fstr1=page1Html_Hdr_asStr))

        # 4.9.3. Сохраняем текст HTML-странички, строка в формате ByteStr
        
        page1Html_enc_asBytestr = req933.content  # (decode_unicode=True)

        '''
        with open('l_tests/newsNYT01a-pageTechHdr.json', 'r') as file722:
            page1Html_Hdr_asStr = file722.read().replace('\n', '')
        with open('l_tests/newsNYT03b.html', 'rb') as file724:
            page1Html_enc_asBytestr = file724.read()
        '''
        ##print("4.9.3. N_914: ", "type=", type(page1Html_Hdr_asStr), "req708.page1Html_Hdr_asStr=str({Fstr1})str".format(Fstr1=page1Html_Hdr_asStr) )
        ##print("4.9.3. N_915: ", "type=", type(page1Html_enc_asBytestr), "page1Html_enc_asBytestr=bytestring({Fbytestr1})bytestring".format(Fbytestr1=page1Html_enc_asBytestr[0:512] ) )

        # 4.9.4. Выделяем Max-Age, он же LifeTime, этот параметр описывает, насколько часто обновляется HTML-страничка
        #        Ищем подстроки вида: сначала ';Max-Age=1800', затем "'s-maxage=600"

        index733 = Attrib_find_n_read(page1Html_Hdr_asStr, ';Max-Age=')
        ##print("4.9.4. N_921: ", "index733=", index733 )
        if index733 == -1:
            index733 = Attrib_find_n_read(page1Html_Hdr_asStr, "'s-maxage=")
            ##print("4.9.4. N_924: ", "index733=", index733 )
        page1_maxAge_asInt = index733
        ##print("4.9.4. N_926: ", "page1_maxAge_asInt=", page1_maxAge_asInt )

        # 4.9.5. Декодируем полученную HTML-страничку, считаем что используется кодировка utf-8

        page1Html_encodg_asStr = 'utf-8'
        page1Html_dec_asStr = page1Html_enc_asBytestr.decode(page1Html_encodg_asStr)
        ##print("4.9.5. N_932: ", "page1Html_dec_asStr=str({Fstr1})str".format(Fstr1=page1Html_dec_asStr[:512] ) )

        # 4.9.6.
        Mk_NYTimes_List2NewsHdlin(page1Html_dec_asStr)
        ##print("4.9.6. N_936: ", "Mk_NYTimes_List2NewsHdlin()" )

        toWaitForNews = datetime.datetime.today() <= page1_waitForNewsUpto_asDatetime
        #               library |class_exemplar|method
    # end of while toWaitForNews:

# end of def ReadNews4h_NYTimes



# 4.10. Функция выводит в строку stdout отображение Крутилка-RotatingBarProgressor
#       и два уточняющих целых числа
#       RotatBarProgrs_PrintNewlineIfNeeds()

def RotatBarProgrs_PrintNewlineIfNeeds():
    global RotatBarPrg_NinLine
    if RotatBarPrg_NinLine > 0:
        RotatBarPrg_NinLine = 0
        print("\n", end='', flush=True )
# end of def RotatBarProgrs_PrintNewlineIfNeeds():



# 4.11. Функция выводит в строку stdout отображение Крутилка-RotatingBarProgressor
#       и два уточняющих целых числа: минуту-в-часе и счётчик-заголовок-новости-NewsHdlin
#       RotatBarProgrs_Print2( int1, int2 )

def RotatBarProgrs_Print2( int1, int2 ):
    global RotatBarPrg_patt
    global RotatBarPrg_currPos
    global RotatBarPrg_NinLine
    global RotatBarPrg_NinLineMax
    print("{Fchar1}m{Fint1:02}/n{Fint2:02} ".format(
              Fchar1=RotatBarPrg_patt[RotatBarPrg_currPos]
            , Fint1=int1
            , Fint2=int2
        ), end='', flush=True )
    RotatBarPrg_NinLine = RotatBarPrg_NinLine + 1
    if RotatBarPrg_NinLine >= RotatBarPrg_NinLineMax:
        RotatBarPrg_NinLine = 0
        print("\n", end='', flush=True)
# end of def RotatBarProgrs_Print2( int1, int2 ):



# 4.12. Функция выполняет один внутренний шаг в отображении Крутилка-RotatingBarProgressor
#       RotatBarProgrs_Step()

def RotatBarProgrs_Step ():
    global RotatBarPrg_currPos
    RotatBarPrg_currPos = RotatBarPrg_currPos + 1
    if RotatBarPrg_currPos >= len(RotatBarPrg_patt):
        RotatBarPrg_currPos = 0
# end of def RotatBarProgrs_Step



# 5. Основная часть программы

# 5.1. Инициализации

List1NewsHdlin_Unflt_asList = []  # create an empty list
List2NewsHdlin_Flt_asList = []  # create an empty list

# 5.2. Читаем HTML-заголовки новостей NYTimes в течение не более 4 часов, запоминаем и логируем поступающие заголовки новостей
ReadNews4h_NYTimes()

# 5.3. Читаем HTML-заголовки новостей CBSNews в течение не более 4 часов, запоминаем и логируем поступающие заголовки новостей
ReadNews4h_CBSNews()

# END

