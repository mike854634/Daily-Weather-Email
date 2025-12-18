import os
import requests
import smtplib
from email.mime.text import MIMEText

# 1. 獲取天氣 (以 OpenWeatherMap 為例)
def get_weather():
    # 替換成你的城市或 API 呼叫
    return "今日天氣預報：晴天，溫度 25-30 度。"

# 2. 寄送郵件
def send_email(content):
    msg = MIMEText(content)
    msg['Subject'] = '每日天氣報告'
    msg['From'] = os.environ['EMAIL_USER']
    msg['To'] = 'mike854634@gmail.com'

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        server.send_message(msg)

if __name__ == "__main__":
    weather_info = get_weather()
    send_email(weather_info)
    print("Email sent successfully!")
