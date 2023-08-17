
#insiderbot was a python project I decided to make when I began trading in the stock market
#the bot has functionality to report stock information such as 50 day average, daily high, daily low, and current price
#however, it also reports stocks that were purchased by canadian insiders on the day you specify 

import discord
import asyncio
import requests
from bs4 import BeautifulSoup
import time

##############################################
link_buys_NYSE = 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=3&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1'
link_sells_NYSE = 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=3&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1'

link_buys_CEO = 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=3&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&isofficer=1&iscob=1&isceo=1&ispres=1&iscoo=1&iscfo=1&isgc=1&isvp=1&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1'
link_sells_CEO = 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=3&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&isofficer=1&iscob=1&isceo=1&ispres=1&iscoo=1&iscfo=1&isgc=1&isvp=1&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1'

link_TSX = 'https://www.marketbeat.com/insider-trades/canada/'
##############################################

def openinsider(link):
    """Retrieves and sorts data from openinsider.com

    Args:
        link (string): link to openinsider (changes depending on sell, buy, ...)

    Returns:
        list: list of stocks that were bought or sold & their data
    """
    data = requests.get(link)

    soup = BeautifulSoup(data.text, 'html.parser')

    for table in soup.find_all('table', {'class': 'tinytable'}):
        for tr in table.find_all('tr'):
            values = [td.text for td in table.find_all('td')]

    dates = values[1::17]
    tickers = values[3::17]
    stock_name = values[4::17]
    buyers = values[5::17]
    prices = values[8::17]
    amount = values[9::17]
    value_added = values[11::17]

    data = []
    for i in range(0, len(dates)):
        tickers2 = tickers[i].lstrip()
        amount2 = amount[i].lstrip('+')
        amount2 = amount[i].lstrip('-')
        temp = []
        temp.append(dates[i]) #0
        temp.append(tickers2) #1
        temp.append(stock_name[i]) #2
        temp.append(buyers[i]) #3
        temp.append(prices[i]) #4
        temp.append(amount2) #5
        temp.append(value_added[i]) #6
        data.append(temp)

    recent_10 = []
    for i in range(0,10):
        recent_10.append(data[i])
    
    return recent_10


def recent(move):
    """Forms a string describing the data collected from openinsider()

    Args:
        move (string): describes the move (buy/sell...) that the user specified

    Returns:
        string: sentence combining stock's info i.e. 20 shares of facebook ($fb) were sold by Alex
    """
    if move == 'BUY':
        temp_move = 'purchased'
        link = link_buys_NYSE

    elif move == 'SELL':
        temp_move = 'sold'
        link = link_sells_NYSE

    elif move == 'BUYS CEO':
        temp_move = 'purchased'
        link = link_buys_CEO

    elif move == 'SELLS CEO':
        temp_move = 'sold'
        link = link_sells_CEO

    recent_10 = openinsider(link)
    sentence3 = []
    for i in range(0, 10):
        sentence = ['\n :arrow_forward: **', recent_10[i][5], '** shares of **', recent_10[i][2], '** ($' ,recent_10[i][1], ') were **', temp_move, '** by ' ,recent_10[i][3]]
        sentence2 = ''.join(sentence)
        sentence3.append(sentence2)
    result = ' '.join(sentence3)

    return result


def canadian_insider(condition):
    """Forms a string joining the data collected from canadianinsider.com

    Args:
        condition (string): specifies whether to get data from sells or buys

    Returns:
        string: sentence combining the stock's info
    """
    data = requests.get(link_TSX)
    soup = BeautifulSoup(data.text, 'html.parser')

    values = []
    for tr in soup.find_all('tr'):
        tmp = [td.text for td in tr.find_all('td')]
        values.append(tmp)

    tickers = [div.text for div in soup.find_all('div', {'class':'ticker-area'})]
    names = [div.text for div in soup.find_all('div', {'class':'title-area'})]

    values = values[1:-1]


    for i in range(0,len(values)):
        values[i].append(tickers[i])
        values[i].append(names[i])

    '''
    for i in range(0,len(values)):
        values[i].append(tickers[i])
        values[i].append(names[i])
    '''
    buy_list = []
    sell_list = []
    for i in values:
        for j in i:
            if j == 'Buy':
                buy_list.append(i)
            elif j == 'Sell':
                sell_list.append(i)
    print(buy_list)

    if condition == 'BUY':
        master_list = buy_list
        temp_move = 'purchased'
    elif condition == 'SELL':
        master_list = sell_list
        temp_move = 'sold'

    sentence3 = []
    for i in range(0, len(master_list)):
        sentence = ['\n :arrow_forward: **', master_list[i][3],
                    '** shares of **', master_list[i][-1],
                    '** ($' ,master_list[i][-2], ') were **', temp_move,
                    '** by ' ,master_list[i][1]]
        
        sentence2 = ''.join(sentence)
        sentence3.append(sentence2)
    result = ' '.join(sentence3)
        
    return result


def string_spacer(info):
    try:
        for i in info:
            if i[0] == 'Headquarters':
                i[1] = i[1].replace(" ", "")
                for j in (str(i[1])):
                    z = ''.join(' ' + j if j.isupper() else j.strip() for j in i[1]).strip()
        formatted_string = z
        
        
        ''' #puts spaces between numbers and letters, doesnt work
        i[1] = z
        string = z
        num = 0
        for i in info:
            if i[0] == 'Headquarters':
                for j in range(1, len(i[1])):
                    if i[1][j-1].isalpha() == True and i[1][j].isdigit() == True:
                        num = i[1][j]
            if num != 0:
                print(i[1])
                temp = i[1].split(num)
                spacenum = ''.join([' ', str(num)])
                formatted_string = ''.join([temp[0], spacenum, temp[1]])
            else:
                formatted_string = z
        '''
        for i in info:
            if i[0] == 'Headquarters':
                i[1] = formatted_string
        return info
    except Exception:
        return info


def shorten(values):
    """Eliminates duplicates in lists

    Args:
        values (list): a list of elements

    Returns:
        values: same list with no duplicates
    """
    for i in values:
        if i in values[values.index(i)+1:]:
            count = values.count(i)
            for n in range(0, count-1):
                values.remove(i)
    return values


def matrix_duplicate_eraser(A):
    categories = []
    for i in A:
        categories.append(i[0])

    categories.reverse()

    B = A.copy()
    B.reverse()

    indices = []
    for i in categories:
        if i in categories[categories.index(i)+1:]:
            indices.append(categories.index(i))

    for i in indices:
        if i in indices[indices.index(i)+1:]:
            indices.remove(i)
    C = B.copy()

    i = 0
    for j in indices:
        if i == 0:
            C.pop(j)
        
        elif i != 0:
            C.pop(j-i)
        i+=1


    C.reverse()
    return C


def convert(lst):
    """Converts lists of lists (matrices) into dictionaries of the form 'i[0]':'i[1]'

    Args:
        lst (lst): list of any length containing lists of length 2

    Returns:
        dictionary: a dictionary of the format 'i[0]':'i[1]'
    """
    temp = shorten(lst)
    res_dct = {temp[i][0]: temp[i][1] for i in range(0, len(lst))}
    return res_dct


def berkshire(name):
    search_link = "".join(['https://www.google.com/search?q=', name, '+stock'])

    data = requests.get(str(search_link))
    soup = BeautifulSoup(data.text, 'html.parser')

    newlist = []
    for span in soup.find_all('span', {'class':'r0bn4c rQMQod'}):
        newlist.append(span.text)
    
    temp = []
    for i in range(0, len(newlist)):
        if newlist[i].find('NYSE') != -1 or newlist[i].find('NASDAQ') != -1 or newlist[i].find('TSE') != -1 or newlist[i].find('TSX') != -1 or newlist[i].find('CSE') != -1:
            temp.append(newlist[i])
    info = temp[0]

    ticker, market = info.strip(')').split('(')
    
    return [ticker, market]


def ticker_market(name):
    """Searches google for the specified companies and finds the ticker symbol and the market

    Args:
        name (string): name of the company or its ticker symbol

    Returns:
        list: list containing the ticker and the market of the company
    """
    name = name.lower()
    if name.find(' ') != -1:
        temp = name.split(' ')
        new = '+'.join(temp)
        name = new
    
    if name == 'berkshire+hathaway':
        ticker, market = berkshire(name)
    else:
        link = "".join(['https://www.google.com/search?q=', name, '+stock'])

        data = requests.get(str(link))
        soup = BeautifulSoup(data.text, 'html.parser')

        newlist = []
        for div in soup.find_all('div'):
            tmp = [span.text for span in div.find_all('span', {'class':'r0bn4c rQMQod'})]
            for i in tmp:
                if i.find(')') != -1:
                    newlist.append(tmp)
                
        values = []
        for i in range(0, len(newlist)):
            for j in range(0, len(newlist[i])):
                values.append(newlist[i][j])
        for i in values:
            if i in values[values.index(i)+1:]:
                count = values.count(i)
                for n in range(0, count-1):
                    values.remove(i)
        
        for i in range(0, len(values)):
            if values[i].find(')') != -1:
                index = i
            
        info = values[index].strip(')')
        ticker, market = info.split('(')

    return [ticker, market]


def get_info(message):
    message = message.lower()

    link1 = 'https://www.google.com/finance/quote/'

    ticker, market = ticker_market(message)
    search_link = "".join([link1, ticker, ':', market])

    data = requests.get(str(search_link))
    soup = BeautifulSoup(data.text, 'html.parser')

    info = []

    for i in soup.find_all('div', {'class':'gyFHrc'}):
        category_numbers = [div.text for div in i.find_all('div', {'class':'iYuiXc'})]
        category_things = [div.text for div in i.find_all('div', {'class':'mfs7Fc'})]
        information = [div.text for div in i.find_all('div', {'class':'P6K39c'})]

        messy_info = [category_numbers, category_things, information]

        if len(messy_info[0]) == 0: 
            messy_info.pop(0)
        else:
            messy_info.pop(1)

        messy_info_2 = [messy_info[0][0], messy_info[1][0]]
        
        info.append(messy_info_2)
    
    temp = [h1.text for h1 in soup.find_all('h1', {'class':'KY7mAb'})]
    if len(temp) == 0:
        name = message
    else:    
        name = temp[0]

    info = string_spacer(info)

    info.append(['Link', str(search_link)])
    info.append(['Company Name', name])
    info.append(['Ticker', ticker])

    info = matrix_duplicate_eraser(info)

    return info




bot = discord.Client()

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    try:
        msg = message.content

        if msg =='&hello': #test
            await message.channel.send('hi')

        elif msg =='&help':
            await message.channel.send('''
            InsiderBot is a discord bot that tells you what moves the 1% are making in the market\n
    **Current command list:**
    `&USbuys` gives 10 large *american* positions that the 1% acquired over the last day
    `&USsells` gives 10 large *american* positions that the 1% have sold over the last day

    `&tsxbuys` gives large positions that the 1% acquired in the *Canadian* market
    `&tsxsells` gives large positions that the 1% sold in the *Canadian* market

    `&stats [company name/ticker]` gives statistics related to a stock
    `&info [company name/ticker]` gives more information related to the company
    ''')

        elif msg == '&USbuys': #today command
            movelist = recent('BUY')
            await message.channel.send('10 american stocks insiders bought recently:' + movelist)

        elif msg == '&USsells':
            movelist = recent('SELL')
            await message.channel.send('10 american stocks insiders sold recently:' + movelist)

        elif msg == '&tsxbuys':
            movelist = canadian_insider('BUY')
            await message.channel.send('10 stocks canadian insiders bought recently:' + movelist)

        elif msg == '&tsxsells':
            movelist = canadian_insider('SELL')
            await message.channel.send('Stocks canadian insiders sold recently:' + movelist)

        elif msg == '&CEObuys':
            movelist = recent('BUYS CEO')
            await message.channel.send('10 american stocks CEOs bought recently:' + movelist)
        
        elif msg == '&CEOsells':
            movelist = recent('SELLS CEO')
            await message.channel.send('10 american stocks CEOs sold recently:' + movelist)

        elif msg.startswith('&stats'):
            temp1 = msg.strip('&stats ')
            
            info1 = convert(get_info(temp1))
            title1 = ''.join(['Statistics for ', info1['Company Name'],])
            
            embedVar = discord.Embed(title= str(title1), description= '', color=0xDFCF00, url = info1['Link'])
            embedVar.add_field(name="Company", value= info1['Company Name'], inline=False)
            try:
                embedVar.add_field(name="Ticker", value= info1['Ticker'], inline=False)
            except Exception:
                embedVar.add_field(name="Ticker", value= 'Unknown', inline=False)
            try:
                embedVar.add_field(name="Day Range", value= info1['Day range'], inline=False)
            except Exception:
                embedVar.add_field(name="Day Range", value= 'Unknown', inline=False)
            try:
                embedVar.add_field(name="Previous Close", value= info1['Previous close'], inline=False)
            except Exception:
                embedVar.add_field(name="Previous Close", value= 'Unknown', inline=False)
            try:
                embedVar.add_field(name="Year Range", value= info1['Year range'], inline=False)
            except Exception:
                embedVar.add_field(name="Year Range", value= 'Unknown', inline=False)
            try:
                embedVar.add_field(name="Dividend Yield", value= info1['Dividend yield'], inline=False)
            except Exception:
                embedVar.add_field(name="Dividend Yield", value= 'Unknown', inline=False)
            try:
                embedVar.add_field(name="Market Cap", value=info1['Market cap'], inline=False)
            except Exception:
                embedVar.add_field(name="Market Cap", value='Unknown', inline=False)
            try:
                embedVar.add_field(name="Volume", value=info1['Volume'], inline=False)
            except Exception:
                embedVar.add_field(name="Volume", value='Unknown', inline=False)
            try:
                embedVar.add_field(name="Primary Exchange", value=info1['Primary exchange'], inline=False)
            except Exception:
                embedVar.add_field(name="Primary Exchange", value= 'Unknown', inline=False)
            await message.channel.send(embed=embedVar)

        elif msg.startswith('&info'):
            temp2 = msg.strip('&info ')
            info2 = convert(get_info(temp2))
            title2 = ''.join(['Information about ', info2['Company Name'],])

            embedVar = discord.Embed(title= str(title2), description= '', color=0xDFCF00, url = info2['Link'])
            embedVar.add_field(name="Company", value= info2['Company Name'], inline=False)
            embedVar.add_field(name="Website", value= info2['Website'], inline=False)
            embedVar.add_field(name="Founded", value= info2['Founded'], inline=False)
            embedVar.add_field(name="Employees", value= info2['Employees'], inline=False)
            embedVar.add_field(name="Headquarters", value= info2['Headquarters'], inline=False)
            await message.channel.send(embed=embedVar)

    except UnboundLocalError:
        await message.channel.send("Please specify a stock name")
        print(UnboundLocalError)

    except Exception:
        await message.channel.send("An unknown error occurred")
        print(Exception)


bot.run('ODM0MjMzNjMzOTAzNjA3ODE5.YH96nQ.07UtTpzpnejsWGz_GHX29M8mtaQ')
