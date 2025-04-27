import streamlit as st
import openai
import os
import random
import urllib.parse
import requests

# 환경 설정
os.environ["OPENAI_API_KEY"] = st.secrets["API_KEY"]
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 키워드 목록
positive_keywords = ["행복", "기쁨", "만족", "희망", "편안함", "안정감", "사랑", "설렘", "감사", "자신감", "흥분", "기대"]
negative_keywords = ["슬픔", "외로움", "우울", "불안", "스트레스", "분노", "짜증", "무기력", "상실감", "자존감 하락", "불만", "공허함"]
mixed_keywords = ["복잡함", "혼란", "갈등", "망설임", "서운함", "긴장", "두려움", "충동적", "후회", "죄책감", "실망"]
special_keywords = ["소외감", "압박감", "해방감", "허탈감", "권태로움", "감동", "열등감", "과잉행복", "지나친 자신감", "피로감"]
all_keywords = positive_keywords + negative_keywords + mixed_keywords + special_keywords

# 감정별 색상 + 이모지
emotion_colors = {
    "행복": "#FFE4E1", "기쁨": "#FFFACD", "만족": "#E0FFFF", "희망": "#E6E6FA", "편안함": "#F5F5DC",
    "안정감": "#E0F7FA", "사랑": "#FFE0B2", "설렘": "#F8BBD0", "감사": "#FFF9C4", "자신감": "#D1C4E9",
    "흥분": "#FFCCBC", "기대": "#DCEDC8",
    "슬픔": "#D6EAF8", "외로움": "#D1F2EB", "우울": "#FADBD8", "불안": "#F5CBA7", "스트레스": "#F9E79F",
    "분노": "#F1948A", "짜증": "#F7DC6F", "무기력": "#D7DBDD", "상실감": "#AEB6BF", "자존감 하락": "#F5EEF8",
    "불만": "#FAD7A0", "공허함": "#EBDEF0",
    "복잡함": "#D6DBDF", "혼란": "#D5F5E3", "갈등": "#FDEDEC", "망설임": "#FCF3CF", "서운함": "#F9EBEA",
    "긴장": "#FDEBD0", "두려움": "#F2D7D5", "충동적": "#F5F5F5", "후회": "#EAECEE", "죄책감": "#F8F9F9", "실망": "#F2F3F4",
    "소외감": "#E5E8E8", "압박감": "#E8DAEF", "해방감": "#D1F2EB", "허탈감": "#E5E7E9", "권태로움": "#EAEDED",
    "감동": "#FDEBD0", "열등감": "#F2D7D5", "과잉행복": "#F9E79F", "지나친 자신감": "#E8F8F5", "피로감": "#D6EAF8"
}
emotion_icons = {
    "행복": "😊", "기쁨": "😆", "만족": "😌", "희망": "🌈", "편안함": "🛋️",
    "안정감": "🛡️", "사랑": "❤️", "설렘": "💖", "감사": "🙏", "자신감": "💪",
    "흥분": "🤩", "기대": "🎈",
    "슬픔": "😢", "외로움": "😔", "우울": "🌧️", "불안": "😰", "스트레스": "😵",
    "분노": "😡", "짜증": "😤", "무기력": "😴", "상실감": "🕳️", "자존감 하락": "💔",
    "불만": "😒", "공허함": "🫥",
    "복잡함": "🌀", "혼란": "🌪️", "갈등": "⚡", "망설임": "🤷‍♂️", "서운함": "🥺",
    "긴장": "😬", "두려움": "👻", "충동적": "🤯", "후회": "😞", "죄책감": "😓", "실망": "😞",
    "소외감": "🥶", "압박감": "🧨", "해방감": "🕊️", "허탈감": "😶‍🌫️", "권태로움": "😪",
    "감동": "🥲", "열등감": "😥", "과잉행복": "🥳", "지나친 자신감": "😎", "피로감": "🥱"
}

# 페이지 세팅
st.set_page_config(page_title="도망가자..", page_icon="✈️", layout="wide")
st.markdown("<h1 style='text-align: center;'>도망가자..✈️</h1>", unsafe_allow_html=True)

# 세션 상태
if "feedback_ready" not in st.session_state:
    st.session_state.feedback_ready = False

# 감정 입력
keyword1 = st.text_area("지금 내 감정은....✍️")

# 감정 분석 버튼
if st.button("감정알기🔮", use_container_width=True):
        # ✅ 결과값 초기화 추가
    st.session_state.pop("show_recommendation", None)
    st.session_state.pop("selected_emotion", None)
    st.session_state.pop("travel_reply", None)
    st.session_state.pop("music_list", None)
    st.session_state.pop("feedback_ready", None)
    with st.spinner("🔮 감정을 분석하는 중..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 부드럽고 친근한 전문 심리상담사입니다."},
                {"role": "user", "content": f"""
                {keyword1}
                지금 상태를 분석해 한 문장으로 요약해줘.
                심리를 긍정/부정/혼합/특별 중 하나로 분류해줘.
                그리고 아래 키워드 중 3개를 골라줘:
                - 긍정적: {', '.join(positive_keywords)}
                - 부정적: {', '.join(negative_keywords)}
                - 혼합/복합: {', '.join(mixed_keywords)}
                - 특별한 심리: {', '.join(special_keywords)}
                """}
            ]
        )
        gpt_reply = response.choices[0].message.content
        st.success("나의 감정 분석 결과 ✨")
        st.write(gpt_reply)

        detected_keywords = [kw for kw in all_keywords if kw in gpt_reply][:3]
        st.session_state.detected_keywords = detected_keywords
        st.session_state.subtitle = "당신의 감정 키워드 ✨"

# 감정 키워드 카드
if "subtitle" in st.session_state:
    st.subheader(st.session_state.subtitle)
    cols = st.columns(len(st.session_state.detected_keywords))

    for idx, emotion in enumerate(st.session_state.detected_keywords):
        color = emotion_colors.get(emotion, "#F2F3F4")
        icon = emotion_icons.get(emotion, "✨")
        with cols[idx]:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style='background-color: {color}; padding: 20px; border-radius: 10px; text-align: center;'>
                        <div style='font-size: 40px;'>{icon}</div>
                        <div style='font-size: 24px; margin-top: 10px;'>{emotion}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col1, col2, col3 = st.columns([0.5, 2, 0.5])
                with col2:
                    if st.button("선택하기", key=f"emotion_button_{idx}", use_container_width=True):
                        st.session_state.selected_emotion = emotion.strip()
                        st.session_state.show_recommendation = True
                        st.session_state.pop("travel_reply", None)
                        st.session_state.pop("music_list", None)

# 여행지 + 음악 추천
if st.session_state.get("show_recommendation", False):
    selected_emotion = st.session_state.selected_emotion

    # 여행지 추천
    if "travel_reply" not in st.session_state:
        with st.spinner("✈️ 여행지를 추천하는 중..."):
            travel_query = f"'{selected_emotion}'이라는 감정에 어울리는 국내 여행지나 카페를 2개만 추천해줘. 주소와 설명을 블랙포인트로 구분해줘. 설명은 감성기반으로 30자내로 추가. 볼드체는 안써줘도 돼."
            travel_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": travel_query}]
            )
            st.session_state.travel_reply = travel_response.choices[0].message.content

    st.markdown("---")
    st.subheader(f"✈️ '{selected_emotion}' 감정 기반 도피처 추천")

    ## 🎯 여기서 2열 카드 스타일로 바꾼 부분
    travel_text = st.session_state.travel_reply
    places = travel_text.strip().split("\n\n")  # 2줄 띄움 기준으로 장소 나누기

    travel_cols = st.columns(2)

    for idx, place_info in enumerate(places):
        with travel_cols[idx % 2]:
            with st.container():
                # place_info_cleaned = place_info.replace("", "")
                place_name = place_info.strip().splitlines()[0]  # 첫 번째 줄: 장소 이름
                place_details = "<br>".join(place_info.strip().splitlines()[1:])  # 나머지 줄: 설명

            # HTML로 직접 출력
            st.markdown(
                f"""
                <div style='padding: 10px;'>
                    <p style='font-size: 20px; font-weight: bold;'>{place_name}</p>
                    <p style='font-size: 16px;'>{place_details}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        
    ## 음악 추천
    if "music_list" not in st.session_state:
        with st.spinner("🎵 여행 BGM 추천 중..."):
            st.session_state.music_list = []

            while len(st.session_state.music_list) < 3:
                music_prompt = f"""
                {selected_emotion}
                너는 사용자의 감정에 맞는 음악을 추천하는 DJ야.
                '{selected_emotion}' 감정에 어울리는 여행용 음악 20곡을 [노래 제목] - [가수명] 포맷으로 추천해줘. 국내 10곡, 해외 10곡. 추가 설명 없이.
                """
                music_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": music_prompt}]
                )
                music_text = music_response.choices[0].message.content
                music_candidates = music_text.strip().split("\n")
                random.shuffle(music_candidates)

                for music in music_candidates:
                    if len(st.session_state.music_list) >= 3:
                        break
                    if not music.strip():
                        continue

                    parts = music.split("-")
                    if len(parts) != 2:
                        continue

                    title = parts[0].strip().replace("[", "").replace("]", "")
                    artist = parts[1].strip().replace("[", "").replace("]", "")

                    search_query = urllib.parse.quote(f"{artist} {title}")
                    url = f"https://itunes.apple.com/search?term={search_query}&entity=song&limit=1"

                    try:
                        res = requests.get(url, timeout=5)
                        if res.status_code == 200 and res.content:
                            data = res.json()
                            if data.get("resultCount", 0) > 0:
                                result = data["results"][0]
                                artwork_url = result["artworkUrl100"].replace('100x100', '500x500')
                                preview_url = result.get("previewUrl")

                                st.session_state.music_list.append({
                                    "title": title,
                                    "artist": artist,
                                    "artwork": artwork_url,
                                    "preview_url": preview_url
                                })
                    except:
                        pass

    st.markdown("---")
    st.subheader("🎵이 기분엔 이 노래지~")

    music_cols = st.columns(3)
    for idx, music in enumerate(st.session_state.music_list):
        with music_cols[idx]:
            st.image(music["artwork"], width=150)
            st.write(f"🎵 **{music['title']}**")
            st.write(f"🎤 {music['artist']}")
            if music.get("preview_url"):
                st.audio(music["preview_url"], format="audio/mp3")

    st.session_state.feedback_ready = True

# 피드백 폼
if st.session_state.get("feedback_ready", False):
    st.markdown("---")
    st.subheader("📝도망갈만 했나요?")

    rating_messages = {
        1: "기대에 못 미쳐 죄송합니다. 좋은 여행 되세요!",
        2: "부족했던 점을 보완해나가겠습니다. 좋은 여행 되세요!",
        3: "소중한 의견 감사합니다. 좋은 여행 되세요!",
        4: "만족하셨다니 기쁩니다. 좋은 여행 되세요!",
        5: "최고의 여행을 선물해드릴 수 있어 영광입니다. 좋은 여행 되세요!"
    }

    with st.form("feedback_form", clear_on_submit=False):
        st.write("점수를 선택해주세요!")
        rating = st.slider("⭐만족도⭐", 0, 5, value=0)

        st.write("💬 한 줄 피드백을 남겨주세요:")
        feedback_text = st.text_input("예시: 추천 여행지가 마음에 들었어요!")

        submitted = st.form_submit_button("피드백 제출하기")

        if submitted:
            if rating in rating_messages:
                st.success(rating_messages[rating])
            else:
                st.success("피드백 감사합니다!")

            st.balloons()
            st.write(f"당신의 평가: {rating}점")

            st.markdown("<a href='#9fe67a9c'><button style='padding:10px 20px; background-color:#6c63ff; color:white; border:none; border-radius:5px; cursor:pointer;'>🔼 감정 키워드로 이동</button></a>", unsafe_allow_html=True)