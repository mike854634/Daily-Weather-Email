import os
import requests
import smtplib
from email.mime.text import MIMEText

def get_weather():
    # 從 GitHub Secrets 讀取 API Key
    api_key = os.environ.get('WEATHER_API_KEY')
    city = "Taichung"  # 你可以改成你的城市，如 Taichung, Kaohsiung
    
    # 呼叫 OpenWeatherMap API (使用攝氏單位 units=metric)
    # url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_tw"
    # url = f"https://api.openweathermap.org/data/3.0/onecall?q={city}&appid={api_key}"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_tw"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            desc = data['weather'][0]['description']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            
            report = (f"【今日 {city} 天氣預報】\n"
                      f"天氣狀況：{desc}\n"
                      f"目前溫度：{temp}°C\n"
                      f"體感溫度：{feels_like}°C\n"
                      f"相對濕度：{humidity}%\n"
                      "祝你有美好的一天！")
            return report
        else:
            return f"天氣抓取失敗，錯誤碼：{response.status_code}"
    except Exception as e:
        return f"發生錯誤：{e}"

def send_email(content):
    my_email = os.environ.get('EMAIL_USER') 
    password = os.environ.get('EMAIL_PASS')

    email_1 = os.environ.get('RECEIVED_EMAIL_USER_1') 
    email_2 = os.environ.get('RECEIVED_EMAIL_USER_2') 

    # 1. 定義收件人清單 (用串列 List 儲存)
    # recipients = ['mike854634@gmail.com', 'jenna2375@gmail.com']

    msg = MIMEText(content)
    msg['Subject'] = '🌍 每日天氣報告'
    msg['From'] = my_email
    
    msg['To'] = f"{email_1}, {email_2}"

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(my_email, password)
            # 3. 傳送郵件時傳入收件人清單
            server.send_message(msg)
        print(f"郵件已成功寄送至: {', '.join(recipients)}")
    except Exception as e:
        print(f"寄送失敗: {e}")

if __name__ == "__main__":
    weather_info = get_weather()
    send_email(weather_info)
    print("Email sent successfully!")
