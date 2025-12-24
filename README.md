# HA-Geupshik-Allimi (HA급식알리미) 🍱

[한국어](#한국어) | [English](#english)

Use the Korean NEIS API to fetch school lunch menus and create sensors in Home Assistant. The text is automatically cleaned for TTS (Text-to-Speech) so you can have your smart speaker announce the menu!

---

## 한국어

### 소개
전국 교육청(NEIS) 오픈 API를 사용하여 학교 급식 정보를 가져옵니다. 
가져온 정보는 특수문자나 알레르기 코드를 제거하여 AI 스피커가 자연스럽게 읽을 수 있도록 가공됩니다.

### 기능
- **오늘/내일 급식 센서**: `sensor.ha_geupshik_allimi_lunch_today`, `..._tomorrow`
- **TTS 최적화**: "★조각사과(1.2)" -> "조각사과" 와 같이 깔끔하게 변환
- **칼로리 정보 제공**
- **UI 설정 지원**: YAML 파일 수정 없이 홈어시스턴트 설정 화면에서 추가 가능

### 설치 방법
1. 이 저장소를 HACS > Custom Repositories 에 추가하거나, `custom_components` 폴더에 직접 복사합니다.
2. 홈어시스턴트를 재시작합니다.
3. 설정 > 기기 및 서비스 > 통합 구성요소 추가 > **HA 급식알리미** 검색 후 선택합니다.

### 학교 코드 찾기
설정 시 **시도교육청코드** 와 **행정표준코드**가 필요합니다.
아래 공식 포털에서 학교 이름을 검색하여 코드를 확인하세요.

👉 [학교 코드 검색하기 (NEIS 포털)](https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17020190531110010104913&infSeq=1)

예시:
- **시도교육청코드**: `C10` (부산광역시교육청)
- **행정표준코드**: `7201202` (화정초등학교)

### 사용 방법 (자동화 예시)
이 컴포넌트는 매 시간 자동으로 급식 정보를 업데이트하여 센서에 저장합니다.
별도의 업데이트 자동화는 필요하지 않으며, **알림 자동화**만 작성하면 됩니다.

**예: 매일 아침 7시에 거실 스피커로 급식 메뉴 읽어주기**

```yaml
alias: "오늘의 급식 알림"
description: "매일 아침 7시에 급식 메뉴를 읽어줍니다."
trigger:
  - platform: time
    at: "07:00:00"
condition: []
action:
  - service: tts.cloud_say  # 또는 tts.google_translate_say
    data:
      entity_id: media_player.bedroom_speaker
      message: "{{ state_attr('sensor.ha_geupshik_allimi_lunch_today', 'menu_tts') }}"
```

**예: 밤 11시에 내일 급식 메뉴 미리 알려주기**

```yaml
alias: "내일 급식 미리 알림"
description: "매일 밤 11시에 다음 날 급식 메뉴를 미리 알려줍니다."
trigger:
  - platform: time
    at: "23:00:00"
action:
  - service: tts.cloud_say
    data:
      entity_id: media_player.bedroom_speaker
      message: "{{ state_attr('sensor.ha_geupshik_allimi_lunch_tomorrow', 'menu_tts') }}"
```

---

## English

### Introduction
Fetches school meal information in Korea via the NEIS Open API.
It cleans up the text (removing allergy numbers and symbols) to make it suitable for TTS announcements.

### Features
- **Today/Tomorrow Sensors**: `sensor.ha_geupshik_allimi_lunch_today`
- **TTS Ready**: Cleans text like "Apple(1.2)" -> "Apple".
- **Calories Info**
- **Config Flow**: Setup entirely via UI.

### Installation
1. Add this repo to HACS or copy to `custom_components`.
2. Restart Home Assistant.
3. Settings > Devices & Services > Add Integration > Search **HA Geupshik Allimi**.

### Finding School Codes
You need the **Education Office Code** and **School Code**.
Find them here:

👉 [Search School Codes (NEIS Portal)](https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17020190531110010104913&infSeq=1)

### Usage (Automation Example)
The component updates automatically. You just need an automation to read the text.

**Example: Announce lunch menu at 7 AM**

```yaml
alias: "School Lunch Announcement"
trigger:
  - platform: time
    at: "07:00:00"
action:
  - service: tts.cloud_say
    data:
      entity_id: media_player.bedroom_speaker
      message: "{{ state_attr('sensor.ha_geupshik_allimi_lunch_today', 'menu_tts') }}"
```

**Example: Announce tomorrow's lunch at 11 PM**

```yaml
alias: "Tomorrow's Lunch Preview"
trigger:
  - platform: time
    at: "23:00:00"
action:
  - service: tts.cloud_say
    data:
      entity_id: media_player.bedroom_speaker
      message: "{{ state_attr('sensor.ha_geupshik_allimi_lunch_tomorrow', 'menu_tts') }}"
```
