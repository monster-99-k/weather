import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"




# 한글 도시명과 영문 도시명 매핑
city_name_map = {
    "서울": "Seoul",
    "인천": "Incheon",
    "대전": "Daejeon",
    "대구": "Daegu",
    "광주": "Gwangju",
    "부산": "Busan",
    "울산": "Ulsan",
    "세종": "Sejong",
    "강릉": "Gangneung",
    "춘천": "Chuncheon",
    "원주": "Wonju",
    "청주": "Cheongju",
    "전주": "Jeonju",
    "포항": "Pohang",
    "창원": "Changwon",
    "제주": "Jeju",
    # 경기도 주요 도시 (OpenWeather 표기 보완)
    "수원": "Suwon",
    "성남": "Seongnam",
    "고양": "Goyang",
    "일산": "Ilsan",
    "용인": "Yongin",
    "부천": "Bucheon",
    "안산": "Ansan",
    "안양": "Anyang",
    "평택": "Pyeongtaek",
    "의정부": "Uijeongbu",
    "파주": "Paju",
    "시흥": "Siheung",
    "김포": "Gimpo",
    "광명": "Gwangmyeong",
    "하남": "Hanam",
    "오산": "Osan",
    "군포": "Gunpo",
    "이천": "Icheon",
    "안성": "Anseong",
    "과천": "Gwacheon",
    "구리": "Guri",
    "남양주": "Namyangju",
    "양주": "Yangju",
    "동두천": "Dongducheon",
    "여주": "Yeoju",
    "포천": "Pocheon",
    "연천": "Yeoncheon",
    "가평": "Gapyeong",
    "양평": "Yangpyeong",
    # 전라남도 주요 행정구역
    "목포": "Mokpo",
    "여수": "Yeosu",
    "순천": "Suncheon",
    "나주": "Naju",
    "광양": "Gwangyang",
    "담양": "Damyang",
    "곡성": "Gokseong",
    "구례": "Gurye",
    "고흥": "Goheung",
    "보성": "Boseong",
    "화순": "Hwasun",
    "장흥": "Jangheung",
    "강진": "Gangjin",
    "해남": "Haenam",
    "영암": "Yeongam",
    "무안": "Muan",
    "함평": "Hampyeong",
    "영광": "Yeonggwang",
    "장성": "Jangseong",
    "완도": "Wando",
    "진도": "Jindo",
    "신안": "Sinan",
    # 전라북도 주요 행정구역
    "전주": "Jeonju",
    "군산": "Gunsan",
    "익산": "Iksan",
    "정읍": "Jeongeup",
    "남원": "Namwon",
    "김제": "Gimje",
    "완주": "Wanju",
    "진안": "Jinan",
    "무주": "Muju",
    "장수": "Jangsu",
    "임실": "Imsil",
    "순창": "Sunchang",
    "고창": "Gochang",
    "부안": "Buan",
    # 경상남도 주요 행정구역
    "창원": "Changwon",
    "김해": "Gimhae",
    "진주": "Jinju",
    "양산": "Yangsan",
    "거제": "Geoje",
    "통영": "Tongyeong",
    "사천": "Sacheon",
    "밀양": "Miryang",
    "함안": "Haman",
    "거창": "Geochang",
    "합천": "Hapcheon",
    "고성": "Goseong",
    "남해": "Namhae",
    "하동": "Hadong",
    "산청": "Sancheong",
    "함양": "Hamyang",
    "의령": "Uiryeong",
    # 경상북도 주요 행정구역
    "포항": "Pohang",
    "경주": "Gyeongju",
    "김천": "Gimcheon",
    "안동": "Andong",
    "구미": "Gumi",
    "영주": "Yeongju",
    "영천": "Yeongcheon",
    "상주": "Sangju",
    "문경": "Mungyeong",
    "경산": "Gyeongsan",
    "군위": "Gunwi",
    "의성": "Uiseong",
    "청송": "Cheongsong",
    "영양": "Yeongyang",
    "영덕": "Yeongdeok",
    "청도": "Cheongdo",
    "고령": "Goryeong",
    "성주": "Seongju",
    "칠곡": "Chilgok",
    "예천": "Yecheon",
    "봉화": "Bonghwa",
    "울진": "Uljin",
    "울릉": "Ulleung",
    # 강원도 주요 행정구역
    "춘천": "Chuncheon",
    "원주": "Wonju",
    "강릉": "Gangneung",
    "동해": "Donghae",
    "태백": "Taebaek",
    "속초": "Sokcho",
    "삼척": "Samcheok",
    "홍천": "Hongcheon",
    "횡성": "Hoengseong",
    "영월": "Yeongwol",
    "평창": "Pyeongchang",
    "정선": "Jeongseon",
    "철원": "Cheorwon",
    "화천": "Hwacheon",
    "양구": "Yanggu",
    "인제": "Inje",
    "고성": "Goseong",
    "양양": "Yangyang"
}
main_cities = list(city_name_map.keys())


# 스타일 개선: 배경색, 카드, 중앙정렬 등
st.markdown("""
    <style>
    .main {
        background-color: #e3f2fd;
    }
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#1976d2;'>🌤️ 날씨 웹앱</h1>", unsafe_allow_html=True)

# 내 위치(도시) 기준 날씨 표시
import json
def get_location_city():
    try:
        res = requests.get("https://ipinfo.io/json")
        if res.status_code == 200:
            info = res.json()
            city_en = info.get("city", "")
            # 영문 도시명을 한글로 변환
            for kor, eng in city_name_map.items():
                if eng.lower() == city_en.lower():
                    return kor, eng
            return city_en, city_en  # 한글 매핑 없으면 영문 그대로 반환
    except:
        pass
    return None, None

my_city_kor, my_city_eng = get_location_city()

@st.cache_data(show_spinner=False)
def get_weather_by_city(city_eng):
    params = {
        "q": city_eng,
        "appid": API_KEY,
        "units": "metric",
        "lang": "kr"
    }
    return requests.get(BASE_URL, params=params)

@st.cache_data(show_spinner=False)
def get_geo_by_city(city_eng):
    geo_url = "https://api.openweathermap.org/geo/1.0/direct"
    geo_params = {
        "q": city_eng,
        "limit": 1,
        "appid": API_KEY
    }
    return requests.get(geo_url, params=geo_params)

@st.cache_data(show_spinner=False)
def get_forecast_by_latlon(lat, lon):
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    forecast_params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "lang": "kr",
        "appid": API_KEY
    }
    return requests.get(forecast_url, params=forecast_params)

if my_city_eng:
    st.subheader("📍 내 위치의 날씨")
    response = get_weather_by_city(my_city_eng)
    if response.status_code == 200:
        data = response.json()
        city_label = my_city_kor if my_city_kor else my_city_eng
        st.write(f"<b>{city_label}의 현재 날씨</b>", unsafe_allow_html=True)
        st.write(f"🌡️ <span style='color:#1976d2'><b>{data['main']['temp']}°C</b></span>", unsafe_allow_html=True)
        st.write(f"☁️ {data['weather'][0]['description']}")
        st.write(f"💧 습도: {data['main']['humidity']}% | 🌬️ 풍속: {data['wind']['speed']} m/s")
    else:
        st.write("내 위치의 날씨 정보를 가져올 수 없습니다.")

# 검색창 안내 문구를 위에 배치 (label 제거)
st.markdown("<b>도시 이름을 한글로 입력하세요:</b>", unsafe_allow_html=True)
with st.form(key="search_form", clear_on_submit=False):
    cols = st.columns([4,1])
    city = cols[0].text_input("", label_visibility="collapsed")
    search_btn = cols[1].form_submit_button("🔍 검색")

# 5일 예보 카드 스타일 적용
if search_btn and city:
    eng_name = city_name_map.get(city)
    if eng_name:
        geo_res = get_geo_by_city(eng_name)
        if geo_res.status_code == 200 and geo_res.json():
            geo = geo_res.json()[0]
            lat, lon = geo["lat"], geo["lon"]
            forecast_res = get_forecast_by_latlon(lat, lon)
            if forecast_res.status_code == 200:
                forecast_data = forecast_res.json()
                st.markdown("---")
                st.subheader(f"📅 {city}의 5일간 날씨 요약")
                import datetime
                from collections import defaultdict
                daily_data = defaultdict(list)
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                time_labels = []
                temp_values = []
                for entry in forecast_data["list"]:
                    date = datetime.datetime.fromtimestamp(entry["dt"]).strftime("%Y-%m-%d")
                    hour = datetime.datetime.fromtimestamp(entry["dt"]).strftime("%H:%M")
                    temp = entry["main"]["temp"]
                    desc = entry["weather"][0]["description"]
                    rain = entry.get("rain", {}).get("3h", 0)
                    daily_data[date].append({"temp": temp, "desc": desc, "rain": rain})
                    if date == today:
                        time_labels.append(hour)
                        temp_values.append(temp)
                # ...기존 5일 요약 표...
                rows = []
                for date, items in list(daily_data.items())[:5]:
                    max_temp = max(i["temp"] for i in items)
                    desc = max(set(i["desc"] for i in items), key=lambda d: sum(j["desc"]==d for j in items))
                    rain_sum = sum(i["rain"] for i in items)
                    rows.append({"날짜": f"<b>{date}</b>", "최고기온(°C)": f"<span style='color:#1976d2'><b>{max_temp}</b></span>", "대표날씨": f"☁️ {desc}", "강수량합(mm)": f"💧 {rain_sum}"})
                table_html = "<table style='width:100%; text-align:center;'>"
                table_html += "<tr><th>날짜</th><th>최고기온(°C)</th><th>대표날씨</th><th>강수량합(mm)</th></tr>"
                for row in rows:
                    table_html += f"<tr><td>{row['날짜']}</td><td>{row['최고기온(°C)']}</td><td>{row['대표날씨']}</td><td>{row['강수량합(mm)']}</td></tr>"
                table_html += "</table>"
                st.markdown(table_html, unsafe_allow_html=True)
                # 곡선 그래프를 표 아래로 이동 (시간대별로 정확히 표시)
                import pandas as pd
                if len(time_labels) > 0:
                    df = pd.DataFrame({"시간": time_labels, "기온(°C)": temp_values})
                    df = df.sort_values(by="시간")
                    st.markdown(f"<b>오늘 시간대별 온도 변화</b>", unsafe_allow_html=True)
                    st.line_chart(df.set_index("시간"))
            else:
                st.markdown("---")
                st.error("5일 예보 정보를 가져올 수 없습니다.")
        else:
            st.markdown("---")
            st.error("도시의 위치 정보를 찾을 수 없습니다.")
    else:
        st.markdown("---")
        st.error("지원하지 않는 도시입니다. 주요 도시명을 한글로 입력해 주세요.")
