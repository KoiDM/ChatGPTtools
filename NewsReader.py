import requests
from bs4 import BeautifulSoup
from googletrans import Translator   #pip install googletrans==4.0.0rc1
from datetime import date

#update with your api keys
api_key ='Your OPENAI API key'   #https://platform.openai.com/account/api-keys
news_api_key = 'Your NEWS API key'  #https://newsapi.org/

api_endpoint = "https://api.openai.com/v1/chat/completions"

request_headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key
}

#get GPT response
def ask_GPT(task):
    request_data = {
        "model": "gpt-3.5-turbo",
        "messages": [{
            "role": "user", 
            "content": #the prompt
                f"You are a financial analyst. Tell me if the following news is positive or negative: {task}. Reply with 'Positve', 'Negative', or 'Mixed'. You may explain your rationale in a sentence or two."}],
        "temperature": 0.3  #more conservative and accurate
    }

    response = requests.post(api_endpoint, headers=request_headers, json=request_data)

    if response.status_code == 200:
        response_text = response.json()["choices"][0]["message"]['content']
        print(task, "\n", response_text)
    else:
        response_text = "error"
        print(f"Request failed with status code: {str(response.status_code)}")

    return response_text 


#get headline news from NewsAPI
url = (
    'https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'category=business&'
       'apiKey='+ news_api_key 
       )

response = requests.get(url).json()

headers = []
summary = []
for n in range(len(response['articles'])):
    headers.append(response['articles'][n]['title'])
    summary.append(response['articles'][n]['description'])

#write to html file

today = date.today()

with open(f"newsreader {str(today)}.html", 'w') as f:
    f.write('<html>\n<head>\n<title>' + str(today) + '</title>\n</head>\n<body>\n')
    f.write('<h2>'+'Top Headlines    ' + str(today)+'</h2>\n')
    for j in range(len(headers)):
        header = headers[j]
        des = summary[j]
        task = str(header) + str(des)
   
        sentiment = ask_GPT(task)

        translator = Translator()
        chinese_text = translator.translate(header, dest ='zh-cn').text
        chinese_answer = translator.translate(sentiment, dest = 'zh-cn').text      

        f.write("\n<h3 style='color:blue'>"+str(header)+"</h3>\n"+ str(des)+'<br><br>'+str(chinese_text) + "<br><br>"+ str(sentiment) + "<br>" + str(chinese_answer)+ "\n<p></p>\n")

    f.write('\n</body>\n</html>')


