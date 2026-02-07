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
    "version": "1.3.0",
    "genre": "하이퍼 리얼리즘 공대생 로맨스",
    "author": "Minkyu + Gemini"
  },
  "player_state": {
    "name": "주인공",
    "department": "컴퓨터공학과 3학년",
    "status": {
      "academic": "학사 경고 (전필 '알고리즘' F 위기)",
      "financial": "잔고 3,400원 (편의점 '혜자 도시락' 1개 가능)",
      "equipment": "내장 그래픽 인생 (RTX 5070 냉납 현상으로 사망)"
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
      "title": "프롤로그 : 인생에 블루스크린이 떴다",
      "background": "dark_room_computer_smoke",
      "text": "내 인생은 'Segmentation Fault (Core Dumped)'다. \n\n전공 필수 알고리즘은 재수강 확정, 유일한 친구였던 RTX 5070은 '사이버펑크 2077'을 돌리다 장렬히 전사했다. \n\nGTA 6 출시까지 6개월... 내장 그래픽으로 버티는 삶은 지옥이다.",
      "next_node": "node_02_common_day"
    },
    {
      "id": "node_02_common_day",
      "type": "dialogue",
      "title": "공통 루트 (낮) : 차수연과의 만남",
      "background": "university_lab_room",
      "text": "과방 구석에서 한숨을 쉬고 있는데, 과탑 차수연이 내 모니터를 보며 인상을 찌푸린다.",
      "characters": [
        "Cha Sooyeon"
      ],
      "dialogue": [
        {
          "speaker": "차수연",
          "text": "야, 너 코드를 발로 짰냐? O(n^2)로 돌리면 서버 터지는 거 몰라? 이중 for문 당장 걷어내."
        },
        {
          "speaker": "system",
          "text": "그때, 수연의 노트북에서 '비행기 이륙 소리'가 나더니 화면이 멈췄다. \n당신은 익숙하게 노트북 뒷판을 따고, 접촉 불량인 RAM을 지우개로 쓱쓱 문질러 다시 끼워주었다."
        },
        {
          "speaker": "차수연",
          "text": "...어? 부팅되네? 너... 코딩은 잼병인데 하드웨어는 좀 만진다? (안경을 추어올리며 얼굴을 붉힘)"
        }
      ],
      "affinity_change": {
        "cha_sooyeon": 5
      },
      "next_node": "node_02_mini_event"
    },
    {
      "id": "node_02_mini_event",
      "type": "choice",
      "title": "낮의 위기 : 스파게티 코드",
      "background": "university_library",
      "text": "며칠 뒤 도서관. 수연이 노트북을 돌려 보여준다. \n'이 탐색 함수, 데이터 10만 개 넘어가니까 렉 걸려. 어떻게 최적화할래?'",
      "choices": [
        {
          "label": "\"배열 정렬하고 '이진 탐색(Binary Search)'으로 바꾸면 O(log n)으로 줄어듭니다.\"",
          "target_node": "node_02_success",
          "effect": "차수연 호감도 대폭 상승 (지능적 매력 어필)"
        },
        {
          "label": "\"일단 돌아가면 장땡 아닌가요? CPU 쿨러 성능을 믿죠.\"",
          "target_node": "node_02_fail",
          "effect": "차수연 호감도 하락 (공학적 마인드 부족)"
        }
      ]
    },
    {
      "id": "node_02_success",
      "type": "dialogue",
      "title": "이벤트 성공 : 수연의 인정",
      "background": "university_library",
      "characters": [
        "Cha Sooyeon"
      ],
      "dialogue": [
        {
          "speaker": "차수연",
          "text": "오... 정답이야. 변수명도 camelCase로 깔끔하게 맞췄네? 이제야 좀 사람 같구나."
        },
        {
          "speaker": "system",
          "text": "수연이 '몬스터 에너지 드링크' 화이트 맛을 당신 책상에 툭 놓고 갔다."
        }
      ],
      "affinity_change": {
        "cha_sooyeon": 15
      },
      "next_node": "node_03_common_night"
    },
    {
      "id": "node_02_fail",
      "type": "dialogue",
      "title": "이벤트 실패 : 수연의 경멸",
      "background": "university_library",
      "characters": [
        "Cha Sooyeon"
      ],
      "dialogue": [
        {
          "speaker": "차수연",
          "text": "하... 너랑 무슨 얘길 하냐. 개발자 때려치워. 넌 그냥 '전기 먹는 하마'나 만들어."
        },
        {
          "speaker": "system",
          "text": "수연은 깃허브(GitHub) 커밋 로그를 닫아버리고 한숨을 쉬었다."
        }
      ],
      "affinity_change": {
        "cha_sooyeon": -5
      },
      "next_node": "node_03_common_night"
    },
    {
      "id": "node_03_common_night",
      "type": "dialogue",
      "title": "공통 루트 (밤) : 이유리와의 비밀",
      "background": "pc_bang_midnight",
      "characters": [
        "Lee Yuri"
      ],
      "dialogue": [
        {
          "speaker": "이유리",
          "text": "오빠! 오늘 폐기 도시락 '치킨 마요' 나왔어! 전자레인지 돌려왔으니까 같이 먹자!"
        },
        {
          "speaker": "system",
          "text": "새벽 시간, 유리의 가방이 엎어지며 내용물이 쏟아진다. \n화장품 대신 '페이커 친필 사인 키캡'과 '원신 라이덴 쇼군 피규어'가 굴러나왔다."
        },
        {
          "speaker": "이유리",
          "text": "헐... 오빠 설마 이거 알아? 나 덕후인 거 비밀인데... (눈을 반짝이며) 혹시 오빠도 '여행자'야?"
        }
      ],
      "affinity_change": {
        "lee_yuri": 5
      },
      "next_node": "node_03_mini_event"
    },
    {
      "id": "node_03_mini_event",
      "type": "choice",
      "title": "밤의 위기 : 샷건 치는 야스오",
      "background": "pc_bang_counter",
      "text": "새벽 2시, C구역 45번 손님이 '롤 승급전'에서 졌는지 키보드를 샷건 치며 난동을 피운다. \n\"아 정글 차이 XX!\" \n유리가 겁을 먹고 카운터 아래로 숨었다.",
      "choices": [
        {
          "label": "\"손님, 영업 방해 및 기물 파손으로 경찰에 신고하겠습니다.\"",
          "target_node": "node_03_fail",
          "effect": "상황 종료되나 분위기 경직됨"
        },
        {
          "label": "(냉장고에서 음료를 꺼내며) \"형님, 미드가 던져서 화나신 거 다 압니다. 서비스 드릴 테니 화 푸시죠.\"",
          "target_node": "node_03_success",
          "effect": "이유리 호감도 대폭 상승 (듬직함 + 센스)"
        }
      ]
    },
    {
      "id": "node_03_success",
      "type": "dialogue",
      "title": "이벤트 성공 : 서포터의 마음",
      "background": "pc_bang_counter",
      "characters": [
        "Lee Yuri"
      ],
      "dialogue": [
        {
          "speaker": "이유리",
          "text": "와... 오빠 방금 진짜 쩔었어. 거의 뭐 '브라움'이 방패 들어준 느낌? 심장 떨어질 뻔했네 ㅠㅠ"
        },
        {
          "speaker": "system",
          "text": "유리가 당신의 소매를 잡는다. 은은한 복숭아 향 샴푸 냄새가 난다."
        }
      ],
      "affinity_change": {
        "lee_yuri": 15
      },
      "next_node": "node_03_5_weekend_anxiety"
    },
    {
      "id": "node_03_fail",
      "type": "dialogue",
      "title": "이벤트 실패 : 너무 딱딱한 GM",
      "background": "pc_bang_counter",
      "characters": [
        "Lee Yuri"
      ],
      "dialogue": [
        {
          "speaker": "이유리",
          "text": "아니 오빠... 경찰까지 부르면 어떡해; 사장님이 알면 나 혼난단 말이야..."
        },
        {
          "speaker": "system",
          "text": "경찰차 사이렌 소리에 유리는 오히려 더 불안해하는 눈치다."
        }
      ],
      "affinity_change": {
        "lee_yuri": -5
      },
      "next_node": "node_03_5_weekend_anxiety"
    },
    {
      "id": "node_03_5_weekend_anxiety",
      "type": "narrative",
      "title": "브릿지 : 폭풍전야",
      "background": "my_room_night",
      "text": "월요일 아침. \n책상 위엔 쿨러가 멈춘 5070이 시체처럼 누워있고, 학교 포털엔 [학사 경고 위험 대상자 알림] 팝업이 떴다.\n\n이번 주 금요일, 내 인생의 코드가 컴파일되느냐, 에러를 뿜느냐가 결정된다.",
      "next_node": "node_04_climax_trigger"
    },
    {
      "id": "node_04_climax_trigger",
      "type": "event",
      "title": "임계점 : 운명의 금요일",
      "background": "street_sunset",
      "text": "금요일 저녁, 두 개의 알림이 동시에 울린다.\n\n[차수연]: 오늘 밤샘 디버깅. 안 오면 너 F 확정이야. 족보 줄 테니까 튀어와.\n[이유리]: 오빠! 야간 알바 대타가 잠수탔어 ㅠㅠ 오늘 오면 사장님이 5070 살 돈 맞춰준대!\n\nThread는 하나다. 동시에 두 개의 프로세스를 돌릴 순 없다.",
      "next_node": "node_05_branch_selection"
    },
    {
      "id": "node_05_branch_selection",
      "type": "choice",
      "title": "선택 : 학점인가, 그래픽카드인가?",
      "text": "당신의 우선순위 큐(Priority Queue)에 넣을 작업은?",
      "choices": [
        {
          "label": "차수연에게 간다 (학점 구제 & 지적인 사랑)",
          "target_node": "root_sooyeon_start",
          "effect": "학업 성취도 상승, RTX 5070 포기"
        },
        {
          "label": "이유리에게 간다 (자금 확보 & 덕질 메이트)",
          "target_node": "root_yuri_start",
          "effect": "RTX 5070 자금 확보, 학사 경고 위험 감수"
        }
      ]
    },
    {
      "id": "root_sooyeon_start",
      "type": "dialogue",
      "title": "차수연 루트 : 차가운 서버실 같은 스터디룸",
      "background": "study_room_night",
      "text": "유리에게 '미안, 급한 에러가 터져서'라고 문자를 보내고 스터디룸 문을 열었다.",
      "characters": [
        "Cha Sooyeon"
      ],
      "dialogue": [
        {
          "speaker": "차수연",
          "text": "3분 12초 늦었어. ...그래도 왔네? 난 네가 런타임 에러 내고 도망갈 줄 알았는데."
        },
        {
          "speaker": "주인공",
          "text": "선배가 부르는데 와야죠. 제적당하면 인생 로그아웃이니까요."
        },
        {
          "speaker": "차수연",
          "text": "흥, 앉아. 오늘 '레드-블랙 트리(Red-Black Tree)' 구조 완벽하게 이해할 때까지 집에 못 가."
        }
      ],
      "next_node": "sooyeon_snack_time"
    },
    {
      "id": "sooyeon_snack_time",
      "type": "dialogue",
      "title": "차수연 루트 : 새벽 2시의 카페인",
      "background": "study_room_break",
      "characters": [
        "Cha Sooyeon"
      ],
      "dialogue": [
        {
          "speaker": "system",
          "text": "새벽 2시. 수연이 한숨을 쉬며 가방에서 편의점 김밥과 핫식스를 꺼낸다."
        },
        {
          "speaker": "차수연",
          "text": "먹고 해. 당 떨어져서 헛소리 코딩하지 말고. ...너 요즘 밥은 먹고 다니니?"
        },
        {
          "speaker": "주인공",
          "text": "학식 라면으로 때우죠. 선배는 왜 이렇게까지 챙겨주세요? 저 바보라면서요."
        },
        {
          "speaker": "차수연",
          "text": "몰라. 그냥... 네가 짠 그 스파게티 코드 속에, 가끔 기가 막힌 알고리즘이 숨어 있어서. \n그거 버그라고 버리기엔 아깝잖아. 왜."
        }
      ],
      "next_node": "sooyeon_mid_event"
    },
    {
      "id": "sooyeon_mid_event",
      "type": "narrative",
      "title": "새벽 4시의 코드 리뷰",
      "background": "study_room_dawn",
      "text": "새벽 4시. 수연이 꾸벅꾸벅 졸다가 내 어깨에 머리를 기댔다. \n항상 날카롭던 눈매가 풀려 있다. 모니터 불빛에 비친 그녀의 얼굴은 생각보다... 예외적으로 예쁘다.",
      "next_node": "sooyeon_final_choice"
    },
    {
      "id": "sooyeon_final_choice",
      "type": "choice",
      "title": "최종 분기 : 마음의 컴파일",
      "background": "university_campus_morning",
      "text": "기말고사가 끝난 날. 수연이 쭈뼛거리며 묻는다. \n'이번 학기 끝났네. 멘토링도 끝이고. ...이제 어쩔 거야?'",
      "choices": [
        {
          "label": "\"선배 덕분에 A+ 확정입니다! 최고의 멘토였어요. (90도 인사)\"",
          "target_node": "end_sooyeon_bad",
          "effect": "수연의 실망, 비즈니스 관계 확정"
        },
        {
          "label": "\"논리 회로는 마스터했으니까, 이제 선배의 '연애 알고리즘'도 분석해봐도 됩니까?\"",
          "target_node": "end_sooyeon_happy",
          "effect": "연인 관계 발전"
        }
      ]
    },
    {
      "id": "end_sooyeon_happy",
      "type": "ending",
      "title": "Happy Ending : 완벽한 최적화",
      "background": "cherry_blossom_campus",
      "text": "수연의 얼굴이 홍당무처럼 붉어진다. \n'참나... 너 지금 나 상대로 베타 테스트 하냐?' \n그녀는 고개를 돌리며 내 손을 슬쩍 잡았다.\n\n'그래... 승인할게. 대신 버그 나면 바로 디버깅 들어간다. 각오해.'\n\n[결과] 학점 A+, 차수연과 CC 달성. 인생 최고의 알고리즘을 발견했다.",
      "is_game_over": True
    },
    {
      "id": "end_sooyeon_bad",
      "type": "ending",
      "title": "Bad Ending : 404 Not Found",
      "background": "empty_classroom",
      "text": "수연의 표정이 차갑게 식는다. \n'...그래. 멘토로서 뿌듯하네. 졸업 잘 하고, 좋은 개발자 돼라.'\n\n그녀는 미련 없이 뒤돌아 나갔다. \n내 성적표엔 A+가 찍혔지만, 가슴 한구석엔 영원히 해결되지 않을 'Null Pointer Exception'이 남았다.",
      "is_game_over": True
    },
    {
      "id": "root_yuri_start",
      "type": "dialogue",
      "title": "이유리 루트 : 디펜스 게임 시작",
      "background": "pc_bang_chaos",
      "text": "수연의 문자를 읽씹하고 PC방으로 달렸다. 문을 열자마자 라면 냄새와 고성이 섞인 헬게이트가 펼쳐져 있다.",
      "characters": [
        "Lee Yuri"
      ],
      "dialogue": [
        {
          "speaker": "이유리",
          "text": "오빠!! 진짜 왔구나! 나 오빠 딜량만 믿고 있었다고 ㅠㅠ 얼른 앞치마 입어! 지금 주문 밀려서 웨이브 10단계야!"
        },
        {
          "speaker": "주인공",
          "text": "상황 브리핑은 나중에. 내가 라면 물 맞출 테니까 넌 아이스티 샷 내려!"
        },
        {
          "speaker": "이유리",
          "text": "알았어! 와... 오빠 오니까 갑자기 만렙 버스 타는 기분이다."
        }
      ],
      "next_node": "yuri_storage_talk"
    },
    {
      "id": "yuri_storage_talk",
      "type": "dialogue",
      "title": "이유리 루트 : 창고에서의 휴식",
      "background": "pc_bang_storage",
      "characters": [
        "Lee Yuri"
      ],
      "dialogue": [
        {
          "speaker": "system",
          "text": "손님이 빠진 틈을 타 창고 박스 위에 앉았다. 유리가 얼음 컵을 건넨다."
        },
        {
          "speaker": "이유리",
          "text": "하아... 힘들다. 오빠 없었으면 나 진짜 탈주했을 거야."
        },
        {
          "speaker": "주인공",
          "text": "근데 넌 알바 왜 이렇게 빡세게 하냐? 굿즈 사려고?"
        },
        {
          "speaker": "이유리",
          "text": "음... 사실 나중에 내 이름 걸고 인디 게임 만드는 게 꿈이거든. '스타듀 밸리' 같은 거 혼자 만들어보고 싶어서.\n지금 유니티(Unity) 엔진 독학 중인데, 에셋 살 돈 모으는 거야. ...웃기지?"
        },
        {
          "speaker": "system",
          "text": "평소의 장난기 어린 눈빛이 진지하게 변했다. 그녀가 단순한 알바생이 아니라 '미래의 개발자'로 보이기 시작했다."
        }
      ],
      "next_node": "yuri_mid_event"
    },
    {
      "id": "yuri_mid_event",
      "type": "narrative",
      "title": "보스 레이드 종료",
      "background": "pc_bang_dawn",
      "text": "전쟁 같은 새벽이 지나고, 사장님이 약속한 두툼한 현금 봉투가 내 손에 쥐어졌다. \n드디어 RTX 5070을, 아니 그 이상의 하이엔드급을 살 수 있는 돈이다.",
      "next_node": "yuri_final_choice"
    },
    {
      "id": "yuri_final_choice",
      "type": "choice",
      "title": "최종 분기 : 파티 탈퇴 vs 듀오 신청",
      "background": "pc_bang_dawn",
      "text": "유리가 기대에 찬 눈빛으로 바라본다. \n'오빠, 오늘 진짜 고생했어! 우리 이 돈으로 맛있는 거 먹으러 갈까? 아님 오빠 그래픽카드 사러 갈래?'",
      "choices": [
        {
          "label": "\"미안, 지금 용산 상가 오픈런 해야 돼. 특가 떴거든.\"",
          "target_node": "end_yuri_bad",
          "effect": "유리의 실망, 솔로 플레이 확정"
        },
        {
          "label": "\"그래픽카드는 좀 더 참지 뭐. 네가 말한 그 게임 엔진 에셋, 내가 투자할게. 밥도 먹고.\"",
          "target_node": "end_yuri_happy",
          "effect": "연인 관계 발전, 파트너십 결성"
        }
      ]
    },
    {
      "id": "end_yuri_happy",
      "type": "ending",
      "title": "Happy Ending : 최고의 듀오(Duo)",
      "background": "game_convention_hall",
      "text": "유리의 눈이 동그랗게 커진다. '진짜? 오빠 5070 노래를 불렀잖아...'\n\n당신이 웃으며 대답한다. \n'게임은 풀옵션보다 같이 할 사람이 있는 게 더 재밌더라고. 나도 투자할게, 너라는 개발자에.'\n\n유리가 와락 당신을 끌어안는다. '오빠는 이제 내 평생 힐러야! 도망 못 가!'\n\n[결과] 5070은 없지만, 평생을 함께할 'Player 2'를 얻었습니다.",
      "is_game_over": True
    },
    {
      "id": "end_yuri_bad",
      "type": "ending",
      "title": "Bad Ending : 고독한 랭커",
      "background": "dark_room_new_pc",
      "text": "당신은 그 돈으로 RTX 5080을 질렀다. GTA 6의 4K 레이트레이싱 그래픽은 눈물이 날 정도로 황홀하다. \n\n하지만 옆자리는 비어있다. 유리는 그날 이후 '개발 공부 집중하겠다'며 연락이 끊겼다. \n화면 속 세상은 화려하지만, 현실의 내 방은 너무나 조용하다.",
      "is_game_over": True
    }
  ]
}

# ==========================================
# 2. ENGLISH DATA (Translated Version)
# ==========================================
STORY_DATA_EN = {
  "project_meta": {
    "title": "[EN] Runtime Error: No Exception Handling for Love?",
    "version": "1.4.0 (Localized Names)",
    "genre": "Hyper-Realistic CS Major Romance Sim",
    "author": "Minkyu + Gemini"
  },
  "player_state": {
    "name": "Protagonist",
    "department": "CS Major (Junior Year)",
    "status": {
      "academic": "Academic Probation Risk (Failing 'Algorithms')",
      "financial": "Balance: $2.50 (Can barely afford a gas station sandwich)",
      "equipment": "Integrated Graphics Life (RTX 5070 died from thermal throttling)"
    },
    "affinity": {
      "cha_sujin": 0,
      "lee_yuna": 0
    }
  },
  "story_nodes": [
    {
      "id": "node_01_prologue",
      "type": "narrative",
      "title": "Prologue: My Life Screen of Death",
      "background": "dark_room_computer_smoke",
      "text": "My life is a 'Segmentation Fault (Core Dumped)'. \n\nI'm about to fail my core Algorithm class, and my only friend, the RTX 5070, died a hero's death running 'Cyberpunk 2077'. \n\nSix months until GTA 6... Surviving on integrated graphics is literal hell.",
      "next_node": "node_02_common_day"
    },
    {
      "id": "node_02_common_day",
      "type": "dialogue",
      "title": "Common Route (Day): Meeting Sujin",
      "background": "university_lab_room",
      "text": "Sighing in the corner of the lab, Sujin, the department's top student, glares at my monitor.",
      "characters": [
        "Cha Sujin"
      ],
      "dialogue": [
        {
          "speaker": "Sujin",
          "text": "Did you code this with your toes? Do you want to crash the server with O(n^2) complexity? Get rid of that nested loop right now."
        },
        {
          "speaker": "system",
          "text": "Suddenly, Sujin's laptop sounds like a jet engine taking off, then freezes. \nYou skillfully pop open the back case, take out the RAM, and clean the contacts with an eraser—the classic fix."
        },
        {
          "speaker": "Sujin",
          "text": "...Huh? It booted? You... you can't code to save your life, but you're decent with hardware? (Adjusts glasses, blushing slightly)"
        }
      ],
      "affinity_change": {
        "cha_sujin": 5
      },
      "next_node": "node_02_mini_event"
    },
    {
      "id": "node_02_mini_event",
      "type": "choice",
      "title": "Day Crisis: Spaghetti Code",
      "background": "university_library",
      "text": "A few days later at the library. Sujin turns her laptop to you. \n'This search function lags when data hits 100k. How would you optimize it?'",
      "choices": [
        {
          "label": "\"Sort the array and switch to 'Binary Search' to reduce it to O(log n).\"",
          "target_node": "node_02_success",
          "effect": "Sujin's Affection UP (Appeal to Intelligence)"
        },
        {
          "label": "\"If it runs, it's done. Let's just trust the CPU cooler.\"",
          "target_node": "node_02_fail",
          "effect": "Sujin's Affection DOWN (Lack of Engineering Mindset)"
        }
      ]
    },
    {
      "id": "node_02_success",
      "type": "dialogue",
      "title": "Event Success: Sujin's Approval",
      "background": "university_library",
      "characters": [
        "Cha Sujin"
      ],
      "dialogue": [
        {
          "speaker": "Sujin",
          "text": "Oh... that's correct. You even used camelCase for variables? You're acting like a human being for once."
        },
        {
          "speaker": "system",
          "text": "Sujin drops a 'Monster Energy White' on your desk and walks away."
        }
      ],
      "affinity_change": {
        "cha_sujin": 15
      },
      "next_node": "node_03_common_night"
    },
    {
      "id": "node_02_fail",
      "type": "dialogue",
      "title": "Event Fail: Sujin's Scorn",
      "background": "university_library",
      "characters": [
        "Cha Sujin"
      ],
      "dialogue": [
        {
          "speaker": "Sujin",
          "text": "Hah... Why do I even bother? Just quit coding. Go build electric heaters or something."
        },
        {
          "speaker": "system",
          "text": "Sujin aggressively closes the GitHub commit log and sighs."
        }
      ],
      "affinity_change": {
        "cha_sujin": -5
      },
      "next_node": "node_03_common_night"
    },
    {
      "id": "node_03_common_night",
      "type": "dialogue",
      "title": "Common Route (Night): Yuna's Secret",
      "background": "pc_bang_midnight",
      "characters": [
        "Lee Yuna"
      ],
      "dialogue": [
        {
          "speaker": "Yuna",
          "text": "Oppa! We got expired 'Chicken Mayo' bentos today! I heated them up, let's eat!"
        },
        {
          "speaker": "system",
          "text": "It's late at night. Yuna's bag tips over, spilling its contents. \nInstead of makeup, out rolls a 'Faker Signed Keycap' and a 'Genshin Impact Raiden Shogun Figure'."
        },
        {
          "speaker": "Yuna",
          "text": "Gasp... Oppa, you recognize these? Being an otaku is my secret... (Eyes sparkling) Are you a 'Traveler' too?"
        }
      ],
      "affinity_change": {
        "lee_yuna": 5
      },
      "next_node": "node_03_mini_event"
    },
    {
      "id": "node_03_mini_event",
      "type": "choice",
      "title": "Night Crisis: The Rage Quitter",
      "background": "pc_bang_counter",
      "text": "2 AM. The guy at Seat C-45 lost his LoL rank-up match and is smashing his keyboard. \n\"Jungle Diff! OMG!\" \nYuna is trembling, hiding behind the counter.",
      "choices": [
        {
          "label": "\"Sir, I'm calling the cops for property damage and disturbance.\"",
          "target_node": "node_03_fail",
          "effect": "Situation resolved, but the mood is awkward."
        },
        {
          "label": "(Handing him a drink) \"Bro, I saw your Mid feeding. I know it wasn't your fault. Drink this and cool down.\"",
          "target_node": "node_03_success",
          "effect": "Yuna's Affection UP (Dependable + Gamer Sense)"
        }
      ]
    },
    {
      "id": "node_03_success",
      "type": "dialogue",
      "title": "Event Success: A Support's Heart",
      "background": "pc_bang_counter",
      "characters": [
        "Lee Yuna"
      ],
      "dialogue": [
        {
          "speaker": "Yuna",
          "text": "Wow... Oppa, that was epic. You were like Braum raising his shield! My heart almost stopped ㅠㅠ"
        },
        {
          "speaker": "system",
          "text": "Yuna grabs your sleeve. You catch a scent of peach shampoo."
        }
      ],
      "affinity_change": {
        "lee_yuna": 15
      },
      "next_node": "node_03_5_weekend_anxiety"
    },
    {
      "id": "node_03_fail",
      "type": "dialogue",
      "title": "Event Fail: Too Formal GM",
      "background": "pc_bang_counter",
      "characters": [
        "Lee Yuna"
      ],
      "dialogue": [
        {
          "speaker": "Yuna",
          "text": "Oppa... isn't calling the cops too much? The owner's gonna kill me if he finds out..."
        },
        {
          "speaker": "system",
          "text": "The police siren makes Yuna look even more anxious."
        }
      ],
      "affinity_change": {
        "lee_yuna": -5
      },
      "next_node": "node_03_5_weekend_anxiety"
    },
    {
      "id": "node_03_5_weekend_anxiety",
      "type": "narrative",
      "title": "Bridge: Calm Before the Storm",
      "background": "my_room_night",
      "text": "Monday Morning. \nOn the desk lies the corpse of my 5070. On the screen, a pop-up: [Academic Probation Warning].\n\nThis Friday, my life code either compiles successfully or throws a fatal error.",
      "next_node": "node_04_climax_trigger"
    },
    {
      "id": "node_04_climax_trigger",
      "type": "event",
      "title": "Threshold: Fateful Friday",
      "background": "street_sunset",
      "text": "Friday evening. Two notifications ping simultaneously.\n\n[Sujin]: All-nighter debugging session. If you don't show, you fail. I have the past exams. Get here.\n[Yuna]: Oppa! The night shift guy ghosted us ㅠㅠ If you cover, Boss said he'll match the cash for your 5070!\n\nSingle Thread. Cannot run two processes properly.",
      "next_node": "node_05_branch_selection"
    },
    {
      "id": "node_05_branch_selection",
      "type": "choice",
      "title": "Selection: GPA or GPU?",
      "text": "What goes into your Priority Queue?",
      "choices": [
        {
          "label": "Go to Sujin (Save GPA & Intellectual Love)",
          "target_node": "root_sujin_start",
          "effect": "Academics UP, Give up RTX 5070"
        },
        {
          "label": "Go to Yuna (Secure Funds & Otaku Mate)",
          "target_node": "root_yuna_start",
          "effect": "Secure RTX 5070 Fund, Risk Academic Probation"
        }
      ]
    },
    {
      "id": "root_sujin_start",
      "type": "dialogue",
      "title": "Sujin Route: The Cold Server Room",
      "background": "study_room_night",
      "text": "I texted Yuna 'Sorry, critical error occurred' and opened the study room door.",
      "characters": [
        "Cha Sujin"
      ],
      "dialogue": [
        {
          "speaker": "Sujin",
          "text": "You're 3 minutes and 12 seconds late. ...But you came? I thought you'd runtime error and flee."
        },
        {
          "speaker": "Protagonist",
          "text": "When the senior calls, I answer. Getting expelled is basically logging out of life."
        },
        {
          "speaker": "Sujin",
          "text": "Hmph, sit. You're not going home until you fully understand 'Red-Black Trees'."
        }
      ],
      "next_node": "sujin_snack_time"
    },
    {
      "id": "sujin_snack_time",
      "type": "dialogue",
      "title": "Sujin Route: 2 AM Caffeine",
      "background": "study_room_break",
      "characters": [
        "Cha Sujin"
      ],
      "dialogue": [
        {
          "speaker": "system",
          "text": "2 AM. Sujin sighs and pulls out convenience store kimbap and hot coffee."
        },
        {
          "speaker": "Sujin",
          "text": "Eat. Don't write garbage code because of low blood sugar. ...Do you even eat properly these days?"
        },
        {
          "speaker": "Protagonist",
          "text": "Just instant ramen. Why do you care so much, Sunbae? You said I was an idiot."
        },
        {
          "speaker": "Sujin",
          "text": "I don't know. It's just... inside your spaghetti code, there's occasionally a brilliant algorithm hidden. \nIt's a waste to treat it as a bug. That's why."
        }
      ],
      "next_node": "sujin_mid_event"
    },
    {
      "id": "sujin_mid_event",
      "type": "narrative",
      "title": "4 AM Code Review",
      "background": "study_room_dawn",
      "text": "4 AM. Sujin nods off and rests her head on my shoulder. \nHer usually sharp eyes are relaxed. In the monitor's glow, her face is... exceptionally pretty.",
      "next_node": "sujin_final_choice"
    },
    {
      "id": "sujin_final_choice",
      "type": "choice",
      "title": "Final Branch: Compilation of Heart",
      "background": "university_campus_morning",
      "text": "Finals are over. Sujin asks hesitantly. \n'Semester's over. Mentoring too. ...What now?'",
      "choices": [
        {
          "label": "\"Thanks to you, I got an A! You were the best mentor. (Bow 90 degrees)\"",
          "target_node": "end_sujin_bad",
          "effect": "Sujin disappointed, Business Relationship locked."
        },
        {
          "label": "\"I've mastered logic circuits, so can I analyze your 'Love Algorithm' now?\"",
          "target_node": "end_sujin_happy",
          "effect": "Romantic Relationship Start"
        }
      ]
    },
    {
      "id": "end_sujin_happy",
      "type": "ending",
      "title": "Happy Ending: Perfect Optimization",
      "background": "cherry_blossom_campus",
      "text": "Sujin's face turns beet red. \n'Wow... are you beta testing on me right now?' \nShe looks away but gently holds my hand.\n\n'Fine... Request approved. But if you cause a bug, I'm debugging you immediately. Be prepared.'\n\n[Result] Straight A's + Campus Couple. Discovered the best algorithm of life.",
      "is_game_over": True
    },
    {
      "id": "end_sujin_bad",
      "type": "ending",
      "title": "Bad Ending: 404 Not Found",
      "background": "empty_classroom",
      "text": "Sujin's expression turns cold. \n'...Right. Glad I could help as a mentor. Congrats on graduating.'\n\nShe turns and leaves without hesitation. \nMy transcript says A, but my heart is left with a permanent 'Null Pointer Exception'.",
      "is_game_over": True
    },
    {
      "id": "root_yuna_start",
      "type": "dialogue",
      "title": "Yuna Route: Defense Game Start",
      "background": "pc_bang_chaos",
      "text": "I ignored Sujin's text and ran to the PC Cafe. It's a hellgate of ramen smells and shouting.",
      "characters": [
        "Lee Yuna"
      ],
      "dialogue": [
        {
          "speaker": "Yuna",
          "text": "Oppa!! You really came! I was trusting your DPS ㅠㅠ Put on this apron! We're at Wave 10 of orders!"
        },
        {
          "speaker": "Protagonist",
          "text": "Briefing later. I'll handle the ramen water, you pull the iced tea shots!"
        },
        {
          "speaker": "Yuna",
          "text": "Got it! Wow... having you here feels like getting carried by a smurf."
        }
      ],
      "next_node": "yuna_storage_talk"
    },
    {
      "id": "yuna_storage_talk",
      "type": "dialogue",
      "title": "Yuna Route: Safe Room Break",
      "background": "pc_bang_storage",
      "characters": [
        "Lee Yuna"
      ],
      "dialogue": [
        {
          "speaker": "system",
          "text": "During a lull, we sit on boxes in the storage room. Yuna hands you a cup of ice."
        },
        {
          "speaker": "Yuna",
          "text": "Phew... that was hard. If you weren't here, I would've gone AFK IRL."
        },
        {
          "speaker": "Protagonist",
          "text": "Why are you grinding so hard here anyway? Buying merch?"
        },
        {
          "speaker": "Yuna",
          "text": "Hmm... actually, my dream is to make an indie game under my name. Like a solo 'Stardew Valley'.\nI'm self-learning Unity, and I'm saving up for assets. ...Is it funny?"
        },
        {
          "speaker": "system",
          "text": "Her playful eyes turn serious. She's not just a part-timer; she's a 'Future Developer'."
        }
      ],
      "next_node": "yuna_mid_event"
    },
    {
      "id": "yuna_mid_event",
      "type": "narrative",
      "title": "Raid Boss Defeated",
      "background": "pc_bang_dawn",
      "text": "The dawn breaks after the war. The boss hands me a thick envelope of cash. \nFinally, I have enough for the RTX 5070... no, maybe even high-end tier.",
      "next_node": "yuna_final_choice"
    },
    {
      "id": "yuna_final_choice",
      "type": "choice",
      "title": "Final Branch: Leave Party vs. Duo Queue",
      "background": "pc_bang_dawn",
      "text": "Yuna looks at you with anticipation. \n'Oppa, good game today! Should we use this money to eat something good? Or are you gonna go buy your GPU?'",
      "choices": [
        {
          "label": "\"Sorry, I gotta do an open-run at the Electronics Market. There's a sale.\"",
          "target_node": "end_yuna_bad",
          "effect": "Yuna disappointed, Solo Play confirmed."
        },
        {
          "label": "\"The GPU can wait. I'll invest in those game assets you mentioned. And let's eat.\"",
          "target_node": "end_yuna_happy",
          "effect": "Romantic Relationship Start, Partnership Formed."
        }
      ]
    },
    {
      "id": "end_yuna_happy",
      "type": "ending",
      "title": "Happy Ending: Best Duo",
      "background": "game_convention_hall",
      "text": "Yuna's eyes go wide. 'Really? But you were singing about the 5070...'\n\nYou smile. \n'Games are better with friends than max settings. I'm investing in you, the developer.'\n\nYuna hugs you tight. 'Oppa, you're my healer for life! You can't escape!'\n\n[Result] No 5070, but obtained a permanent 'Player 2'.",
      "is_game_over": True
    },
    {
      "id": "end_yuna_bad",
      "type": "ending",
      "title": "Bad Ending: Lonely Ranker",
      "background": "dark_room_new_pc",
      "text": "You bought the RTX 5080. GTA 6 in 4K Ray Tracing is tear-jerkingly beautiful. \n\nBut the seat next to you is empty. Yuna stopped contacting you, saying she needs to 'focus on dev studies'. \nThe screen is vibrant, but my reality is dead silent.",
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