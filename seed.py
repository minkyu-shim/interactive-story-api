import json
from app import create_app, db
from app.models import Story, StoryNode, Choice

app = create_app()

# ==========================================
# 1. KOREAN DATA (Expanded Version)
# ==========================================
STORY_DATA_KR = {
    "project_meta": {
        "title": "[KR] 런타임 에러 : 연애는 예외처리가 안 되나요?",
        "version": "1.1.0",
        "genre": "공대생 로맨스 시뮬레이션",
        "author": "Minkyu + Gemini"
    },
    "player_state": {
        "name": "주인공",
        "department": "컴퓨터공학과 3학년",
        "status": {
            "academic": "제적 위기 (이산수학 F)",
            "financial": "파산 (잔고 3,400원)",
            "equipment": "RTX 5070 사망"
        },
        "affinity": {
            "cha_sooyeon": 0,
            "lee_yuri": 0
        }
    },
    "story_nodes": [
        {
            "id": "node_01_prologue",
            "type": "narrative",
            "title": "프롤로그 : 블루스크린이 뜬 인생",
            "background": "dark_room_computer_smoke",
            "text": "내 인생은 Segmentation Fault다. 전공 필수 이산수학은 낙제 위기, 유일한 친구였던 RTX 5070 그래픽카드는 과열로 사망했다. GTA 6 출시까지 남은 시간은 6개월... 나는 살아남아야 한다.",
            "next_node": "node_02_common_day"
        },
        {
            "id": "node_02_common_day",
            "type": "dialogue",
            "title": "공통 루트 (낮) : 차수연과의 만남",
            "background": "university_lab_room",
            "characters": ["Cha Sooyeon"],
            "dialogue": [
                {"speaker": "차수연", "text": "너, 0과 1 말고 사람 언어로 말하는 법 몰라? 코드가 이게 뭐야. 이번 주까지 최적화 안 해오면 멘토링 취소야."},
                {"speaker": "system", "text": "수연의 노트북이 갑자기 먹통이 된다. 당신은 하드웨어 지식을 발휘해 순식간에 고쳐주었다."},
                {"speaker": "차수연", "text": "...고, 고마워. 너 생각보다 쓸모가 있네? (얼굴을 붉힘)"}
            ],
            "affinity_change": {"cha_sooyeon": 5},
            "next_node": "node_02_mini_event"
        },
        {
            "id": "node_02_mini_event",
            "type": "choice",
            "title": "낮의 위기 : 스파게티 코드",
            "background": "university_library",
            "text": "며칠 뒤, 도서관. 수연이 당신에게 과제를 던져주었다. '이 알고리즘, 실행 속도가 너무 느려. 어떻게 고칠 거야?'",
            "choices": [
                {"label": "\"변수명부터 정리하고, 주석 달면서 정석대로 리팩토링하겠습니다.\"", "target_node": "node_02_success",
                 "effect": "차수연 호감도 대폭 상승"},
                {"label": "\"일단 돌아가기만 하면 되죠! StackOverflow에서 코드 복붙하겠습니다.\"", "target_node": "node_02_fail",
                 "effect": "차수연 호감도 하락"}
            ]
        },
        {
            "id": "node_02_success",
            "type": "dialogue",
            "title": "이벤트 성공 : 수연의 인정",
            "background": "university_library",
            "characters": ["Cha Sooyeon"],
            "dialogue": [
                {"speaker": "차수연", "text": "오... 너 제법인데? 기본기는 갖춰져 있구나. 다시 봤어."},
                {"speaker": "system", "text": "수연이 캔커피를 당신 책상에 툭 놓고 갔다."}
            ],
            "affinity_change": {"cha_sooyeon": 15},
            "next_node": "node_03_common_night"
        },
        {
            "id": "node_02_fail",
            "type": "dialogue",
            "title": "이벤트 실패 : 수연의 경멸",
            "background": "university_library",
            "characters": ["Cha Sooyeon"],
            "dialogue": [
                {"speaker": "차수연", "text": "하... 내가 너한테 뭘 기대하니. 개발자 때려쳐라. 그건 코딩이 아니라 조립이야."},
                {"speaker": "system", "text": "수연은 한심하다는 듯 혀를 차고 가버렸다."}
            ],
            "affinity_change": {"cha_sooyeon": -5},
            "next_node": "node_03_common_night"
        },
        {
            "id": "node_03_common_night",
            "type": "dialogue",
            "title": "공통 루트 (밤) : 이유리와의 비밀",
            "background": "pc_bang_midnight",
            "characters": ["Lee Yuri"],
            "dialogue": [
                {"speaker": "이유리", "text": "오빠! 오늘 야간은 내가 쏜다! 폐기 도시락 나왔어, 같이 먹자."},
                {"speaker": "system", "text": "새벽 시간, 당신은 유리의 가방에서 한정판 게임 굿즈가 쏟아지는 것을 목격한다."},
                {"speaker": "이유리", "text": "헐... 오빠도 이거 알아? 나 안 놀려? 와 대박! 우리 통하는 게 있네!"}
            ],
            "affinity_change": {"lee_yuri": 5},
            "next_node": "node_03_mini_event"
        },
        {
            "id": "node_03_mini_event",
            "type": "choice",
            "title": "밤의 위기 : 샷건 치는 손님",
            "background": "pc_bang_counter",
            "text": "새벽 2시, 구석 자리 아저씨가 게임에서 졌는지 키보드를 내려치며 난동을 피운다. 유리가 겁을 먹고 떨고 있다. 당신의 행동은?",
            "choices": [
                {"label": "\"손님, 기물 파손하시면 경찰 부릅니다.\"", "target_node": "node_03_fail", "effect": "유리의 걱정, 분위기 싸해짐"},
                {"label": "\"괜찮아? 저 아저씨 내가 가서 음료수 주면서 달래고 올게.\"", "target_node": "node_03_success",
                 "effect": "이유리 호감도 대폭 상승"}
            ]
        },
        {
            "id": "node_03_success",
            "type": "dialogue",
            "title": "이벤트 성공 : 유리의 감동",
            "background": "pc_bang_counter",
            "characters": ["Lee Yuri"],
            "dialogue": [
                {"speaker": "이유리", "text": "와... 오빠 진짜 대단하다. 나였으면 울었을 거야. 오빠 덕분에 살았다 ㅠㅠ"},
                {"speaker": "system", "text": "유리가 당신의 팔을 꼭 붙잡는다. 샴푸 향기가 난다."}
            ],
            "affinity_change": {"lee_yuri": 15},
            "next_node": "node_04_climax_trigger"
        },
        {
            "id": "node_03_fail",
            "type": "dialogue",
            "title": "이벤트 실패 : 너무 딱딱해",
            "background": "pc_bang_counter",
            "characters": ["Lee Yuri"],
            "dialogue": [
                {"speaker": "이유리", "text": "아니 오빠... 그렇게 무섭게 말하면 어떡해; 더 큰일 나면 어쩌려고..."},
                {"speaker": "system", "text": "상황은 해결됐지만, 유리는 당신의 냉정함에 약간 거리를 두는 눈치다."}
            ],
            "affinity_change": {"lee_yuri": -5},
            "next_node": "node_04_climax_trigger"
        },
        {
            "id": "node_04_climax_trigger",
            "type": "event",
            "title": "임계점 : 운명의 금요일",
            "background": "street_sunset",
            "text": "며칠 뒤 금요일 저녁. 그동안의 일들이 주마등처럼 스쳐 지나간다. 핸드폰이 동시에 울린다. 수연은 밤샘 스터디를, 유리는 알바 대타를 요청해왔다.",
            "next_node": "node_05_branch_selection"
        },
        {
            "id": "node_05_branch_selection",
            "type": "choice",
            "title": "선택 : 학점인가, 돈인가?",
            "text": "몸은 하나뿐이다. 어디로 갈 것인가?",
            "choices": [
                {"label": "차수연에게 간다 (학점/미래)", "target_node": "root_sooyeon_start", "effect": "학업 성취도 상승, 자금 확보 실패"},
                {"label": "이유리에게 간다 (돈/의리)", "target_node": "root_yuri_start", "effect": "RTX 5070 자금 확보, 학사 경고 위험"}
            ]
        },
        {
            "id": "root_sooyeon_start",
            "type": "dialogue",
            "title": "선택의 결과 : 차가운 스터디룸",
            "background": "study_room_night",
            "text": "당신은 떨리는 손으로 유리에게 '미안하다'는 문자를 보내고 스터디룸 문을 열었다.",
            "characters": ["Cha Sooyeon"],
            "dialogue": [
                {"speaker": "차수연", "text": "3분 늦었어. 그래도... 왔네? 안 올 줄 알았는데."},
                {"speaker": "주인공", "text": "선배가 부르는데 와야죠. 제적당하기 싫으니까."},
                {"speaker": "차수연", "text": "흥, 앉아. 오늘 밤새워서 이 알고리즘 머리에 때려 박을 거니까 각오해."}
            ],
            "next_node": "sooyeon_mid_event"
        },
        {
            "id": "sooyeon_mid_event",
            "type": "narrative",
            "title": "새벽 4시의 디버깅",
            "background": "study_room_dawn",
            "text": "새벽 4시. 문제를 풀던 수연이 깜빡 졸며 당신의 어깨에 머리를 기댔다. 평소의 독기는 사라지고, 무방비한 얼굴만이 남아있다.",
            "next_node": "sooyeon_final_choice"
        },
        {
            "id": "sooyeon_final_choice",
            "type": "choice",
            "title": "최종 분기 : 마음의 컴파일",
            "background": "university_campus_morning",
            "text": "기말고사가 끝난 날. 수연이 당신을 불렀다. '이번 학기 고생했어. 근데... 너한테 마지막으로 물어볼 게 있어.'",
            "choices": [
                {"label": "\"선배 덕분에 A+ 확정이에요. 진짜 최고의 멘토였습니다!\"", "target_node": "end_sooyeon_bad",
                 "effect": "수연의 실망, 관계의 선 긋기"},
                {"label": "\"선배, 저 이제 논리 회로 말고 선배 마음 회로도 분석해 봐도 됩니까?\"", "target_node": "end_sooyeon_happy",
                 "effect": "연인 관계 발전"}
            ]
        },
        {
            "id": "end_sooyeon_happy",
            "type": "ending",
            "title": "Happy Ending : 완벽한 컴파일",
            "background": "cherry_blossom_campus",
            "text": "수연의 얼굴이 붉어진다. '...하? 너 진짜 미쳤구나? 멘토링 끝났다고 막 나가네?' 그녀는 고개를 돌리며 작게 웃었다. \n\n'그래... 예외 처리 승인할게. 대신, 내 마음 분석하다가 버그 나면 죽는다.' \n\n[결과] 학점 A+, 차수연과 CC 달성. 당신의 인생 코드가 완벽하게 최적화되었습니다.",
            "is_game_over": True
        },
        {
            "id": "end_sooyeon_bad",
            "type": "ending",
            "title": "Bad Ending : 런타임 에러",
            "background": "empty_classroom",
            "text": "수연의 표정이 차갑게 굳는다. '...그래. 멘토로서 들을 수 있는 최고의 칭찬이네. 학점 잘 챙겨. 졸업 축하한다.' \n\n그녀는 미련 없이 뒤돌아 나갔다. 당신은 A+를 받았지만, 그녀와의 거리는 영원히 '선후배' 사이로 고정되었다. \n\n[결과] 학점 구제 성공, 그러나 공허한 캠퍼스 라이프.",
            "is_game_over": True
        },
        {
            "id": "root_yuri_start",
            "type": "dialogue",
            "title": "선택의 결과 : 전쟁터 같은 PC방",
            "background": "pc_bang_chaos",
            "text": "당신은 수연의 문자를 씹고 PC방으로 달렸다. 문을 열자마자 헬게이트가 펼쳐져 있다.",
            "characters": ["Lee Yuri"],
            "dialogue": [
                {"speaker": "이유리", "text": "오빠!! 진짜 왔구나! 나 오빠 믿고 있었다고 ㅠㅠ 얼른 앞치마 입어!"},
                {"speaker": "주인공", "text": "상황 설명 나중에 해. 주방 내가 맡을게. 너는 홀 봐!"},
                {"speaker": "이유리", "text": "알았어! 와... 오빠 오니까 갑자기 든든하네."}
            ],
            "next_node": "yuri_mid_event"
        },
        {
            "id": "yuri_mid_event",
            "type": "narrative",
            "title": "폭풍이 지나간 후",
            "background": "pc_bang_storage",
            "text": "전쟁 같은 시간이 지나고, 사장님이 약속한 보너스 봉투가 책상 위에 놓여 있다. 유리가 땀에 젖은 앞머리를 넘기며 환하게 웃는다.",
            "next_node": "yuri_final_choice"
        },
        {
            "id": "yuri_final_choice",
            "type": "choice",
            "title": "최종 분기 : 보상의 의미",
            "background": "pc_bang_dawn",
            "text": "사장님이 주신 두툼한 봉투. 드디어 RTX 5070을 살 수 있는 돈이다. 유리가 기대에 찬 눈빛으로 바라본다. '오빠, 우리 이 돈으로 뭐 할까?'",
            "choices": [
                {"label": "\"미안, 나 이거 바로 입금해야 돼. 그래픽카드 특가 떴거든.\" (물질 우선)", "target_node": "end_yuri_bad",
                 "effect": "유리의 실망, 관계 소원"},
                {"label": "\"그래픽카드는 나중에 사지 뭐. 일단 너 사고 싶다던 그 한정판 굿즈부터 사러 가자.\" (유리 우선)", "target_node": "end_yuri_happy",
                 "effect": "연인 관계 발전"}
            ]
        },
        {
            "id": "end_yuri_happy",
            "type": "ending",
            "title": "Happy Ending : 최고의 듀오",
            "background": "game_convention_hall",
            "text": "유리의 눈이 동그랗게 커진다. '진짜? 오빠 5070 노래 불렀잖아...' 당신이 웃으며 대답한다. '게임은 혼자 하면 고사양이고 뭐고 재미없더라고. 너랑 같이 하는 게 더 중요해.' \n\n유리가 와락 당신을 끌어안는다. \n\n[결과] RTX 5070은 놓쳤지만, 평생을 함께할 'Player 2'를 얻었습니다.",
            "is_game_over": True
        },
        {
            "id": "end_yuri_bad",
            "type": "ending",
            "title": "Bad Ending : 솔로 랭크",
            "background": "dark_room_new_pc",
            "text": "당신은 그 돈으로 즉시 RTX 5070을 구매했다. GTA 6의 그래픽은 황홀하다. 하지만 옆자리는 비어있다. 유리는 그날 이후 '야간 알바 그만둔다'는 문자 하나만 남기고 사라졌다. \n\n[결과] 4K 120프레임의 완벽한 그래픽. 하지만 게임을 같이 즐길 사람은 아무도 없다.",
            "is_game_over": True
        }
    ]
}

# ==========================================
# 2. ENGLISH DATA (Translated Version)
# ==========================================
STORY_DATA_EN = {
    "project_meta": {
        "title": "[EN] Runtime Error: Can't Love Handle Exceptions?",
        "version": "1.1.0",
        "genre": "Engineering Student Romance Simulation",
        "author": "Minkyu + Gemini"
    },
    "player_state": {
        "name": "Protagonist",
        "department": "CS Junior",
        "status": {
            "academic": "Risk of Expulsion (Discrete Math F)",
            "financial": "Bankrupt (Balance: $3.40)",
            "equipment": "RTX 5070 Dead"
        },
        "affinity": {
            "cha_sooyeon": 0,
            "lee_yuri": 0
        }
    },
    "story_nodes": [
        {
            "id": "node_01_prologue",
            "type": "narrative",
            "title": "Prologue: Life is a Blue Screen",
            "background": "dark_room_computer_smoke",
            "text": "My life is a Segmentation Fault. I'm failing Discrete Math, a required major course, and my only friend, my RTX 5070 graphics card, just died from overheating. GTA 6 comes out in 6 months... I must survive.",
            "next_node": "node_02_common_day"
        },
        {
            "id": "node_02_common_day",
            "type": "dialogue",
            "title": "Common Route (Day): Meeting Sooyeon",
            "background": "university_lab_room",
            "characters": ["Cha Sooyeon"],
            "dialogue": [
                {"speaker": "Cha Sooyeon",
                 "text": "Do you know how to speak human, or do you only speak binary? What is this code? If you don't optimize this by this week, the mentoring is off."},
                {"speaker": "system",
                 "text": "Suddenly, Sooyeon's laptop freezes. You use your hardware knowledge to fix it in an instant."},
                {"speaker": "Cha Sooyeon", "text": "...Th-thanks. You're surprisingly useful. (Blushes)"}
            ],
            "affinity_change": {"cha_sooyeon": 5},
            "next_node": "node_02_mini_event"
        },
        {
            "id": "node_02_mini_event",
            "type": "choice",
            "title": "Day Crisis: Spaghetti Code",
            "background": "university_library",
            "text": "A few days later, at the library. Sooyeon throws an assignment at you. 'This algorithm is way too slow. How are you going to fix it?'",
            "choices": [
                {
                    "label": "\"I'll clean up the variable names and refactor it properly with comments.\" (Standard Method)",
                    "target_node": "node_02_success", "effect": "Sooyeon Affinity Large Increase"},
                {"label": "\"As long as it runs, right? I'll copy-paste from StackOverflow.\" (Hack Method)",
                 "target_node": "node_02_fail", "effect": "Sooyeon Affinity Decrease"}
            ]
        },
        {
            "id": "node_02_success",
            "type": "dialogue",
            "title": "Event Success: Sooyeon's Approval",
            "background": "university_library",
            "characters": ["Cha Sooyeon"],
            "dialogue": [
                {"speaker": "Cha Sooyeon",
                 "text": "Oh... not bad? You actually have the basics down. I misjudged you."},
                {"speaker": "system", "text": "Sooyeon places a canned coffee on your desk before leaving."}
            ],
            "affinity_change": {"cha_sooyeon": 15},
            "next_node": "node_03_common_night"
        },
        {
            "id": "node_02_fail",
            "type": "dialogue",
            "title": "Event Fail: Sooyeon's Disdain",
            "background": "university_library",
            "characters": ["Cha Sooyeon"],
            "dialogue": [
                {"speaker": "Cha Sooyeon",
                 "text": "Hah... What did I expect? You should quit being a dev. That's not coding, that's just assembly."},
                {"speaker": "system", "text": "Sooyeon clicks her tongue in disappointment and leaves."}
            ],
            "affinity_change": {"cha_sooyeon": -5},
            "next_node": "node_03_common_night"
        },
        {
            "id": "node_03_common_night",
            "type": "dialogue",
            "title": "Common Route (Night): Yuri's Secret",
            "background": "pc_bang_midnight",
            "characters": ["Lee Yuri"],
            "dialogue": [
                {"speaker": "Lee Yuri",
                 "text": "Oppa! The night shift is on me! We got some expired bento boxes, let's eat!"},
                {"speaker": "system",
                 "text": "Late at night, you witness limited edition game merch spilling out of Yuri's bag."},
                {"speaker": "Lee Yuri",
                 "text": "Hul... You know what this is? You won't make fun of me? Wow! We actually connect!"}
            ],
            "affinity_change": {"lee_yuri": 5},
            "next_node": "node_03_mini_event"
        },
        {
            "id": "node_03_mini_event",
            "type": "choice",
            "title": "Night Crisis: Rage Gamer",
            "background": "pc_bang_counter",
            "text": "2 AM. A customer in the corner slams his keyboard in a rage. Yuri is trembling in fear. What do you do?",
            "choices": [
                {"label": "\"Sir, if you damage the equipment, I'll have to call the police.\" (Logical/Strict)",
                 "target_node": "node_03_fail", "effect": "Yuri worries, Atmosphere gets cold"},
                {"label": "\"Are you okay? I'll go give him a free drink and calm him down.\" (Emotional/Empathy)",
                 "target_node": "node_03_success", "effect": "Yuri Affinity Large Increase"}
            ]
        },
        {
            "id": "node_03_success",
            "type": "dialogue",
            "title": "Event Success: Yuri's Admiration",
            "background": "pc_bang_counter",
            "characters": ["Lee Yuri"],
            "dialogue": [
                {"speaker": "Lee Yuri",
                 "text": "Wow... Oppa, you're amazing. I would have cried. You saved my life! ㅠㅠ"},
                {"speaker": "system", "text": "Yuri grabs your arm tightly. You smell her shampoo."}
            ],
            "affinity_change": {"lee_yuri": 15},
            "next_node": "node_04_climax_trigger"
        },
        {
            "id": "node_03_fail",
            "type": "dialogue",
            "title": "Event Fail: Too Rigid",
            "background": "pc_bang_counter",
            "characters": ["Lee Yuri"],
            "dialogue": [
                {"speaker": "Lee Yuri",
                 "text": "No, Oppa... You can't talk so scarily; what if something worse happens..."},
                {"speaker": "system",
                 "text": "The situation is resolved, but Yuri seems to distance herself slightly due to your coldness."}
            ],
            "affinity_change": {"lee_yuri": -5},
            "next_node": "node_04_climax_trigger"
        },
        {
            "id": "node_04_climax_trigger",
            "type": "event",
            "title": "Critical Point: Fateful Friday",
            "background": "street_sunset",
            "text": "Friday evening, a few days later. Past events flash before your eyes. Your phone buzzes simultaneously. Sooyeon demands an all-night study session, while Yuri begs you to cover a shift.",
            "next_node": "node_05_branch_selection"
        },
        {
            "id": "node_05_branch_selection",
            "type": "choice",
            "title": "Choice: Grades or Money?",
            "text": "You only have one body. Where will you go?",
            "choices": [
                {"label": "Go to Sooyeon (Grades/Future)", "target_node": "root_sooyeon_start",
                 "effect": "Academic Success, Failed to secure funds"},
                {"label": "Go to Yuri (Money/Loyalty)", "target_node": "root_yuri_start",
                 "effect": "Secure RTX 5070 funds, Risk of Expulsion"}
            ]
        },
        {
            "id": "root_sooyeon_start",
            "type": "dialogue",
            "title": "Choice Result: The Cold Study Room",
            "background": "study_room_night",
            "text": "Trembling, you text Yuri 'I'm sorry' and open the study room door.",
            "characters": ["Cha Sooyeon"],
            "dialogue": [
                {"speaker": "Cha Sooyeon", "text": "You're 3 minutes late. But... you came? I thought you wouldn't."},
                {"speaker": "Protagonist", "text": "You called, so I came. I don't want to get expelled."},
                {"speaker": "Cha Sooyeon",
                 "text": "Hmph, sit down. Be prepared, I'm going to hard-code this algorithm into your brain tonight."}
            ],
            "next_node": "sooyeon_mid_event"
        },
        {
            "id": "sooyeon_mid_event",
            "type": "narrative",
            "title": "4 AM Debugging",
            "background": "study_room_dawn",
            "text": "4 AM. While solving problems, Sooyeon dozes off and leans her head on your shoulder. Her usual toxicity is gone, leaving only a defenseless face.",
            "next_node": "sooyeon_final_choice"
        },
        {
            "id": "sooyeon_final_choice",
            "type": "choice",
            "title": "Final Branch: Compiling the Heart",
            "background": "university_campus_morning",
            "text": "Finals are over. Sooyeon calls you. 'You worked hard this semester. But... I have one last question for you.'",
            "choices": [
                {"label": "\"Thanks to you, I secured an A+. You were truly the best mentor!\" (Respect)",
                 "target_node": "end_sooyeon_bad", "effect": "Sooyeon disappointed, Friend-zoned"},
                {"label": "\"Senior, can I analyze your heart's circuit instead of logic circuits now?\" (Confession)",
                 "target_node": "end_sooyeon_happy", "effect": "Develop into Lovers"}
            ]
        },
        {
            "id": "end_sooyeon_happy",
            "type": "ending",
            "title": "Happy Ending: Compilation Success",
            "background": "cherry_blossom_campus",
            "text": "Sooyeon's face turns red. '...Huh? Are you crazy? Mentoring is over and you're acting up?' She turns away and laughs softly. \n\n'Fine... I'll approve the exception handling. But if you cause a bug while analyzing my heart, you're dead.' \n\n[Result] A+ Grade, Campus Couple with Sooyeon. Your life code has been perfectly optimized.",
            "is_game_over": True
        },
        {
            "id": "end_sooyeon_bad",
            "type": "ending",
            "title": "Bad Ending: Runtime Error",
            "background": "empty_classroom",
            "text": "Sooyeon's expression turns cold. '...Right. That's the best compliment a mentor could hear. Take care of your grades. Congrats on graduating.' \n\nShe leaves without looking back. You got the A+, but the distance between you remains fixed as 'Senior and Junior'. \n\n[Result] Saved grades, but a hollow campus life.",
            "is_game_over": True
        },
        {
            "id": "root_yuri_start",
            "type": "dialogue",
            "title": "Choice Result: The Battlefield PC Bang",
            "background": "pc_bang_chaos",
            "text": "Ignoring Sooyeon's text, you ran to the PC Bang. It's a total hellscape.",
            "characters": ["Lee Yuri"],
            "dialogue": [
                {"speaker": "Lee Yuri",
                 "text": "Oppa!! You really came! I knew I could count on you! Put on your apron, quick!"},
                {"speaker": "Protagonist", "text": "Explain later. I'll take the kitchen. You handle the hall!"},
                {"speaker": "Lee Yuri", "text": "Got it! Wow... I feel so safe now that you're here."}
            ],
            "next_node": "yuri_mid_event"
        },
        {
            "id": "yuri_mid_event",
            "type": "narrative",
            "title": "After the Storm",
            "background": "pc_bang_storage",
            "text": "After a war-like shift, the bonus envelope promised by the boss sits on the desk. Yuri wipes her sweaty bangs and smiles brightly.",
            "next_node": "yuri_final_choice"
        },
        {
            "id": "yuri_final_choice",
            "type": "choice",
            "title": "Final Branch: Meaning of the Reward",
            "background": "pc_bang_dawn",
            "text": "The thick envelope. Finally, enough money for the RTX 5070. Yuri looks at you with expectant eyes. 'Oppa, what should we do with this money?'",
            "choices": [
                {"label": "\"Sorry, I need to deposit this immediately. The GPU is on sale.\" (Materialism)",
                 "target_node": "end_yuri_bad", "effect": "Yuri disappointed, Relationship distant"},
                {
                    "label": "\"I can buy the GPU later. Let's go buy that limited edition figure you wanted first.\" (Yuri First)",
                    "target_node": "end_yuri_happy", "effect": "Develop into Lovers"}
            ]
        },
        {
            "id": "end_yuri_happy",
            "type": "ending",
            "title": "Happy Ending: Best Duo",
            "background": "game_convention_hall",
            "text": "Yuri's eyes widen. 'Really? You sang songs about the 5070...' You smile and answer. 'Games aren't fun alone, high specs or not. Playing with you is more important.' \n\nYuri hugs you tightly. \n\n[Result] Missed the RTX 5070, but gained a 'Player 2' for life.",
            "is_game_over": True
        },
        {
            "id": "end_yuri_bad",
            "type": "ending",
            "title": "Bad Ending: Solo Rank",
            "background": "dark_room_new_pc",
            "text": "You bought the RTX 5070 immediately. The graphics in GTA 6 are breathtaking. But the seat next to you is empty. Yuri quit the night shift after that day, leaving only a short text. \n\n[Result] Perfect 4K 120FPS graphics. But no one to play with.",
            "is_game_over": True
        }
    ]
}


# ==========================================
# 3. HELPER FUNCTION
# ==========================================

def seed_story(story_data, default_continue_text="Continue"):
    """
  Parses a Story Data Dictionary and inserts it into the DB.
  """
    meta = story_data['project_meta']
    print(f"--> Processing Story: {meta['title']}...")

    # A. Create Story Entry
    story = Story(
        title=meta['title'],
        description=f"Version {meta['version']}",
        genre=meta['genre'],
        author=meta['author'],
        initial_state=story_data['player_state']
    )
    db.session.add(story)
    db.session.commit()  # Commit to get story.id

    nodes_data = story_data['story_nodes']

    # B. Create Nodes
    for n_data in nodes_data:
        # Normalize Content
        content = []
        if 'dialogue' in n_data:
            content = n_data['dialogue']
        elif 'text' in n_data:
            content = [{"speaker": "System", "text": n_data['text']}]

        node = StoryNode(
            story_id=story.id,
            custom_id=n_data['id'],
            node_type=n_data.get('type', 'narrative'),
            background=n_data.get('background'),
            content_data=content,
            affinity_change=n_data.get('affinity_change', {}),
            is_ending=n_data.get('is_ending', False),
            ending_outcome=n_data.get('outcome')
        )
        db.session.add(node)

    db.session.commit()

    # C. Create Choices/Links
    for n_data in nodes_data:
        parent_node = StoryNode.query.filter_by(story_id=story.id, custom_id=n_data['id']).first()

        # Explicit Choices
        if 'choices' in n_data:
            for c_data in n_data['choices']:
                choice = Choice(
                    text=c_data['label'],
                    node_id=parent_node.id,
                    target_node_custom_id=c_data['target_node'],
                    effect_description=c_data.get('effect')
                )
                db.session.add(choice)

        # Implicit Linear Link
        elif 'next_node' in n_data and n_data['next_node'] != "TBD":
            choice = Choice(
                text=default_continue_text,
                node_id=parent_node.id,
                target_node_custom_id=n_data['next_node']
            )
            db.session.add(choice)

    db.session.commit()
    print(f"✅ Successfully seeded: {meta['title']}")


# ==========================================
# 4. MAIN EXECUTION
# ==========================================

with app.app_context():
    print("🌱 Starting Database Seed...")

    # Reset DB
    db.drop_all()
    db.create_all()

    # Seed Korean Version
    seed_story(STORY_DATA_KR, default_continue_text="계속하기")

    # Seed English Version
    seed_story(STORY_DATA_EN, default_continue_text="Continue")

    print("🚀 All stories seeded! Ready to play.")