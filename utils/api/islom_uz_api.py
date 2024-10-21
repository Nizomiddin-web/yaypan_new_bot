import requests
import datetime
import pytz

tz_Tosh = pytz.timezone('Asia/Tashkent')


async def prayer_time(region):
    data = requests.get(url=f"https://islomapi.uz/api/present/day?region={region}").json()
    now = datetime.datetime.now(tz_Tosh)
    text = f"""Namoz Vaqtlari:
=========================
📌 《 🏙 {region} 》 vaqti bilan
--------------------------------------------
🌓  Tong:         -  {data['times']['tong_saharlik']} 
🌞  Quyosh:     -  {data['times']['quyosh']} 

🕰  Bomdod:   -  {data['times']['tong_saharlik']}  
🕰  Peshin:      -  {data['times']['peshin']}  
🕰  Asr:           -  {data['times']['asr']} 
🕰  Shom:       -  {data['times']['shom_iftor']}  
🕰  Xufton:      -  {data['times']['hufton']} 
--------------------------------------------
    
📅 {now.year}-yil|Oyning {now.month}-kuni|{data['weekday']}|Soat {now.strftime("%H:%M")}"""
    return text
