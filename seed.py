from copy import deepcopy

from app import create_app, db
from app.models import Story, StoryNode, Choice

app = create_app()

# ==========================================
# 1. KOREAN DATA (Expanded Version)
# ==========================================
STORY_DATA_KR_RAW = {
  "project_meta": {
    "title": "[KR] 런타임 에러 : 연애는 예외처리가 안 되나요?",
    "version": "1.6.0 (Narrative Flow Patch)",
    "genre": "하이퍼 리얼리즘 공대생 로맨스",
    "author": "Minkyu + Gemini"
  },
  "player_state": {
    "name": "user",
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
      "text": "내 인생은 'Segmentation Fault' 다. \n\n전공 필수 알고리즘은 재수강 확정, 유일한 친구였던 RTX 5070은 '사이버펑크 2077'을 돌리다 장렬히 전사했다. \n\nGTA 6 출시까지 6개월... 내장 그래픽으로 버티는 삶은 지옥이다.",
      "next_node": "node_01_5_professor_call"
    },
    {
      "id": "node_01_5_professor_call",
      "type": "dialogue",
      "title": "이벤트 : 교수님의 호출",
      "background": "professor_office",
      "characters": [
        "Professor Park"
      ],
      "text": "박 교수님 연구실로 불려갔다. 에어컨 바람이 유난히 차갑다.",
      "dialogue": [
        {
          "speaker": "박 교수",
          "text": "자네 중간고사 점수 꼬라지가 이게 뭔가? 12점? 공부 대신 뇌로 비트코인 채굴이라도 했나?"
        },
        {
          "speaker": "진",
          "text": "저... 하드웨어 이슈가 좀 있어서..."
        },
        {
          "speaker": "박 교수",
          "text": "변명은. 자네 멘토로 과탑 붙여줄 테니 낙제하기 싫으면 가서 배워. 당장 실습실로 튀어가."
        }
      ],
      "next_node": "node_02_common_day"
    },
    {
      "id": "node_02_common_day",
      "type": "dialogue",
      "title": "공통 루트 (낮) : 차수연과의 만남",
      "background": "university_lab_room",
      "text": "쫓겨나듯 실습실로 갔다. 구석에서 날카로운 안경을 쓴 여학생이 발을 구르며 기다리고 있다.",
      "characters": [
        "Cha Sooyeon"
      ],
      "dialogue": [
        {
          "speaker": "차수연",
          "text": "네가 그 '12점'짜리야? 교수님이 너 사람 좀 만들어 놓으라더라. \n...야, 너 코드를 발로 짰냐? O(n^2)로 돌리면 서버 터지는 거 몰라? 이중 for문 당장 걷어내."
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
      "next_node": "node_02_5_work_login"
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
      "next_node": "node_02_5_work_login"
    },
    {
      "id": "node_02_5_work_login",
      "type": "narrative",
      "title": "전환 : 현실 로그인",
      "background": "street_night_neon",
      "text": "학교 일과는 끝났지만, 내 하루는 끝나지 않았다. \n\n사망한 그래픽카드(RTX 5070)를 되살리려면 현금이 필요하다. 야간 알바를 위해 '넥서스 PC방'으로 향한다. \n\n라면 냄새와 기계식 키보드 소리... 파밍의 시간이다.",
      "next_node": "node_03_common_night"
    },
    {
      "id": "node_03_common_night",
      "type": "dialogue",
      "title": "공통 루트 (밤) : 이유리와의 만남",
      "background": "pc_bang_midnight",
      "text": "카운터로 들어서자 교대자인 유리(Yuri)가 지친 기색이지만 밝게 인사한다.",
      "characters": [
        "Lee Yuri"
      ],
      "dialogue": [
        {
          "speaker": "이유리",
          "text": "오빠! 왔어? 오늘 폐기 도시락 '치킨 마요' 나왔어! 전자레인지 돌려왔으니까 같이 먹자!"
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
          "label": "차수연에게 간다",
          "target_node": "root_sooyeon_start",
          "effect": "학업 성취도 상승, RTX 5070 포기"
        },
        {
          "label": "이유리에게 간다",
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
          "speaker": "진",
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
          "speaker": "진",
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
          "speaker": "진",
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
          "speaker": "진",
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
STORY_DATA_EN_RAW = {
  "project_meta": {
    "title": "[EN] Runtime Error: No Exception Handling for Love?",
    "version": "1.6.0 (Character Name Patch)",
    "genre": "Hyper-Realistic CS Major Romance Sim",
    "author": "Minkyu + Gemini"
  },
  "player_state": {
    "name": "user",
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
      "next_node": "node_01_5_professor_call"
    },
    {
      "id": "node_01_5_professor_call",
      "type": "dialogue",
      "title": "Event: The Professor's Summon",
      "background": "professor_office",
      "characters": [
        "Professor Park"
      ],
      "text": "You are summoned to Professor Park's office. The air is cold.",
      "dialogue": [
        {
          "speaker": "Professor Park",
          "text": "Look at this midterm score. 12 points? Are you mining crypto with your brain instead of studying?"
        },
        {
          "speaker": "Jin",
          "text": "I... I had some hardware issues..."
        },
        {
          "speaker": "Professor Park",
          "text": "Excuses. I'm assigning you a mandatory peer mentor. She's the top of the class. If you don't show up to her sessions, you fail. Get to the lab. Now."
        }
      ],
      "next_node": "node_02_common_day"
    },
    {
      "id": "node_02_common_day",
      "type": "dialogue",
      "title": "Common Route (Day): The Mentor",
      "background": "university_lab_room",
      "text": "Kicked out of the office, I trudge to the lab. A girl with sharp glasses is tapping her foot, waiting for me.",
      "characters": [
        "Cha Sujin"
      ],
      "dialogue": [
        {
          "speaker": "Sujin",
          "text": "So you're the '12 points' guy? Professor Park told me to fix you. \n...Wait, did you code this with your toes? Get rid of that nested loop right now."
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
      "next_node": "node_02_5_work_login"
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
      "next_node": "node_02_5_work_login"
    },
    {
      "id": "node_02_5_work_login",
      "type": "narrative",
      "title": "Transition: Login to Reality",
      "background": "street_night_neon",
      "text": "School is over, but my day isn't. \n\nTo resurrect my dead GPU (RTX 5070), I need cash. I head to 'Nexus PC Cafe' for the graveyard shift. \n\nThe smell of ramen and the sound of mechanical keyboards... it's time to grind.",
      "next_node": "node_03_common_night"
    },
    {
      "id": "node_03_common_night",
      "type": "dialogue",
      "title": "Common Route (Night): Yuna's Shift",
      "background": "pc_bang_midnight",
      "text": "I walk behind the counter. My coworker, Yuna, is already there, looking exhausted but cheerful.",
      "characters": [
        "Lee Yuna"
      ],
      "dialogue": [
        {
          "speaker": "Yuna",
          "text": "Oppa! You're here! We got expired 'Chicken Mayo' bentos today! I heated them up, let's eat!"
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
          "label": "Go to Sujin",
          "target_node": "root_sujin_start",
          "effect": "Academics UP, Give up RTX 5070"
        },
        {
          "label": "Go to Yuna",
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
          "speaker": "Jin",
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
          "speaker": "Jin",
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
          "speaker": "Jin",
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
          "speaker": "Jin",
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



def _set_next_node(nodes_by_id, node_id, next_node):
    node = nodes_by_id.get(node_id)
    if not node:
        return
    node["next_node"] = next_node
    node.pop("next_page_id", None)


def _append_node_if_missing(nodes, nodes_by_id, node_payload):
    node_id = node_payload.get("id")
    if not node_id or node_id in nodes_by_id:
        return
    nodes.append(node_payload)
    nodes_by_id[node_id] = node_payload


def _rename_speaker(nodes, from_name, to_name):
    for node in nodes:
        for key in ("dialogue", "content"):
            entries = node.get(key)
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if isinstance(entry, dict) and entry.get("speaker") == from_name:
                    entry["speaker"] = to_name


def _apply_story_refresh(raw_story_data, locale):
    refreshed = deepcopy(raw_story_data)
    meta = refreshed.setdefault("project_meta", {})
    meta["version"] = "1.8.2 (Expanded Story Beats + Deterministic Branch Patch)"

    nodes = refreshed.get("story_nodes", [])
    nodes_by_id = {node.get("id"): node for node in nodes if node.get("id")}

    # Keep illustration URLs optional.
    # If a node has no explicit illustration_url, clients should render by scene background.

    # Shared route expansion: both locales keep the same node IDs and branch structure.
    _set_next_node(nodes_by_id, "node_02_success", "node_02_aftermath")
    _set_next_node(nodes_by_id, "node_02_fail", "node_02_aftermath")
    _set_next_node(nodes_by_id, "node_03_success", "node_03_aftermath")
    _set_next_node(nodes_by_id, "node_03_fail", "node_03_aftermath")

    if locale == "en":
        mentor_mid_id = "sujin_mid_event"
        mentor_final_id = "sujin_final_choice"
        partner_mid_id = "yuna_mid_event"
        partner_final_id = "yuna_final_choice"

        text_updates = {
            "node_01_prologue": (
                "My life is one giant Segmentation Fault.\n\n"
                "Algorithms is one exam away from an F, my beloved RTX 5070 died mid-benchmark, "
                "and GTA 6 is still months away.\n\n"
                "If this week crashes, so do I."
            ),
            "node_02_5_work_login": (
                "Classes end, but survival mode starts.\n\n"
                "If I want my GPU back, I need cash. So I clock into the night shift at Nexus PC Cafe.\n\n"
                "Ramen steam, keyboard clacks, and tired eyes. Another raid begins."
            ),
            "node_03_5_weekend_anxiety": (
                "Monday morning.\n\n"
                "Dead GPU on my desk. Academic warning on my portal. "
                "Both tabs are open, both are red.\n\n"
                "By Friday, I either recover or hard fail."
            ),
            "node_04_climax_trigger": (
                "Friday evening. Two notifications hit at the exact same time.\n\n"
                "[Sujin]: All-night debug session. Miss this and your grade is over.\n"
                "[Yuna]: Emergency shift. Cover tonight and Boss will match your GPU fund.\n\n"
                "Single-thread life. You can only execute one branch."
            ),
            "node_05_branch_selection": "Which route gets priority in your queue?",
            "sujin_mid_event": (
                "4 AM. During code review, Sujin drifts asleep on your shoulder.\n"
                "For the first time, there is no sarcasm, no walls, no compiler warnings."
            ),
            "yuna_mid_event": (
                "Dawn after chaos. You survived the order rush and the owner hands over a thick envelope.\n"
                "Enough for the GPU, maybe more. But now the choice costs more than money."
            ),
            "end_sujin_happy": (
                "Sujin freezes, then laughs under her breath.\n"
                "\"Are you... seriously confessing with algorithm jokes?\"\n\n"
                "She squeezes your hand anyway.\n"
                "\"Fine. Request approved. But if you ship bugs, I'm reviewing everything.\"\n\n"
                "[Result] Straight A's + a relationship built on commits and trust."
            ),
            "end_sujin_bad": (
                "Sujin nods once, expression locked behind her glasses.\n"
                "\"Understood. Mentor mode complete. Good luck, junior.\"\n\n"
                "You pass the semester, but leave with an unhandled exception in your chest."
            ),
            "end_yuna_happy": (
                "Yuna blinks, speechless.\n"
                "\"You'd delay the 5070... for my indie game?\"\n\n"
                "\"Games run better in co-op,\" you say.\n\n"
                "She hugs you and laughs through tears.\n"
                "[Result] GPU delayed, future duo unlocked."
            ),
            "end_yuna_bad": (
                "You buy the new GPU and max every setting.\n"
                "The frame rate is perfect. The room is not.\n\n"
                "Yuna goes silent, focusing on her own path.\n"
                "Your monitor glows brighter than your life."
            ),
        }
        for node_id, text in text_updates.items():
            node = nodes_by_id.get(node_id)
            if node:
                node["text"] = text

        _rename_speaker(nodes, "Jin", "User")

    else:
        mentor_mid_id = "sooyeon_mid_event"
        mentor_final_id = "sooyeon_final_choice"
        partner_mid_id = "yuri_mid_event"
        partner_final_id = "yuri_final_choice"


    _set_next_node(nodes_by_id, mentor_mid_id, "route_mentor_checkpoint")
    _set_next_node(nodes_by_id, partner_mid_id, "route_partner_checkpoint")

    if locale == "en":
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "node_02_aftermath",
                "type": "narrative",
                "title": "Aftermath: Local Optimization",
                "background": "campus_walk_evening",
                "text": (
                    "After the daytime clash, you and Sujin rerun the benchmarks one last time. "
                    "The code finally stops stuttering.\n\n"
                    "You don't become friends instantly, but the cold sarcasm drops by one degree."
                ),
                "next_node": "node_02_5_work_login",
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "node_03_aftermath",
                "type": "dialogue",
                "title": "Aftermath: Closing Shift Debrief",
                "background": "pc_bang_cleanup",
                "characters": ["Lee Yuna"],
                "dialogue": [
                    {"speaker": "system", "text": "The rush ends. You stack trays and wipe keyboards side by side."},
                    {"speaker": "Yuna", "text": "That was intense... but with you here, I didn't panic."},
                    {"speaker": "User", "text": "Teamplay beats solo carry. Let's survive one shift at a time."},
                ],
                "next_node": "node_03_5_weekend_anxiety",
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_mentor_checkpoint",
                "type": "choice",
                "title": "Mentor Route: Trust Test",
                "background": "study_room_dawn",
                "text": "Final prep window: two hours. Sujin asks how you want to spend it.",
                "choices": [
                    {
                        "label": "\"Run the standard checklist. No surprises, no panic.\"",
                        "target_node": "route_mentor_bridge",
                        "effect": "Steady confidence and cleaner fundamentals.",
                    },
                    {
                        "label": "\"Let's attempt a risky optimization challenge and bet on speed.\"",
                        "target_node": "route_mentor_bridge_fail",
                        "effect": "High-risk call. You burn extra time patching gaps, then recover together.",
                    },
                ],
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_mentor_bridge",
                "type": "dialogue",
                "title": "Mentor Route: Clean Build",
                "background": "university_campus_morning",
                "characters": ["Cha Sujin"],
                "dialogue": [
                    {"speaker": "Sujin", "text": "Good call. Your logic is stable, and that's what wins finals."},
                    {"speaker": "User", "text": "I finally stopped brute-forcing everything. Mostly."},
                ],
                "next_node": mentor_final_id,
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_mentor_bridge_fail",
                "type": "narrative",
                "title": "Mentor Route: Hotfix Night",
                "background": "study_room_night",
                "text": (
                    "The gamble crashes hard. You and Sujin spend an extra hour patching logic holes.\n\n"
                    "It's messy, but you finish together and walk into finals with bruised confidence and real trust."
                ),
                "next_node": mentor_final_id,
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_partner_checkpoint",
                "type": "choice",
                "title": "Partner Route: Queue Management",
                "background": "pc_bang_counter",
                "text": "Another customer wave hits. Yuna looks at you for the call.",
                "choices": [
                    {
                        "label": "\"We split lanes: I handle ramen, you run orders and payments.\"",
                        "target_node": "route_partner_bridge",
                        "effect": "Safe macro play. Stable service quality.",
                    },
                    {
                        "label": "\"Let's run a flash combo promo to stabilize mood and sales.\"",
                        "target_node": "route_partner_bridge_fail",
                        "effect": "Aggressive promo call. Orders spike and cleanup gets harder, but you stabilize together.",
                    },
                ],
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_partner_bridge",
                "type": "dialogue",
                "title": "Partner Route: Combo Play",
                "background": "pc_bang_dawn",
                "characters": ["Lee Yuna"],
                "dialogue": [
                    {"speaker": "Yuna", "text": "Nice call! That flow was smooth. We actually controlled the chaos."},
                    {"speaker": "User", "text": "Shot-calling is easier when your support never tilts."},
                ],
                "next_node": partner_final_id,
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_partner_bridge_fail",
                "type": "narrative",
                "title": "Partner Route: Overtime Recovery",
                "background": "pc_bang_storage",
                "text": (
                    "The promo backfires and orders pile up. You two run overtime to recover the floor.\n\n"
                    "Exhausted, you still finish as a team, laughing at the disaster on the way out."
                ),
                "next_node": partner_final_id,
            },
        )
    else:
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "node_02_aftermath",
                "type": "narrative",
                "title": "후일담 : 로컬 최적화",
                "background": "campus_walk_evening",
                "text": (
                    "낮의 소동 이후, 너와 수연은 마지막 벤치마크를 다시 돌렸다.\n\n"
                    "코드는 드디어 버벅임을 멈췄고, 수연의 말투도 아주 조금 부드러워졌다."
                ),
                "next_node": "node_02_5_work_login",
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "node_03_aftermath",
                "type": "dialogue",
                "title": "후일담 : 마감 정리",
                "background": "pc_bang_cleanup",
                "characters": ["Lee Yuri"],
                "dialogue": [
                    {"speaker": "system", "text": "손님이 빠지고 나서, 둘은 나란히 키보드와 테이블을 정리했다."},
                    {"speaker": "이유리", "text": "오늘 진짜 살았다... 오빠 있어서 안 무서웠어."},
                    {"speaker": "진", "text": "솔로 캐리보다 듀오 호흡이 더 세지. 다음 웨이브도 버텨보자."},
                ],
                "next_node": "node_03_5_weekend_anxiety",
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_mentor_checkpoint",
                "type": "choice",
                "title": "수연 루트 : 신뢰도 테스트",
                "background": "study_room_dawn",
                "text": "시험 전 마지막 2시간. 수연이 준비 전략을 고르라고 한다.",
                "choices": [
                    {
                        "label": "\"기본 체크리스트부터. 안정적으로 가자.\"",
                        "target_node": "route_mentor_bridge",
                        "effect": "기초가 단단해지고 멘탈도 안정됨.",
                    },
                    {
                        "label": "\"고위험 최적화 문제로 한 방 노려보자.\"",
                        "target_node": "route_mentor_bridge_fail",
                        "effect": "고위험 분기. 성공: 대박 풀이. 실패: 야간 핫픽스.",
                    },
                ],
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_mentor_bridge",
                "type": "dialogue",
                "title": "수연 루트 : 클린 빌드",
                "background": "university_campus_morning",
                "characters": ["Cha Sooyeon"],
                "dialogue": [
                    {"speaker": "차수연", "text": "좋아. 오늘은 코드도 사고도 안정적이네. 이 감각 그대로 가."},
                    {"speaker": "진", "text": "무작정 박치기부터 하던 습관, 드디어 좀 고쳤어요."},
                ],
                "next_node": mentor_final_id,
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_mentor_bridge_fail",
                "type": "narrative",
                "title": "수연 루트 : 핫픽스의 밤",
                "background": "study_room_night",
                "text": (
                    "무리한 시도가 크게 터졌다. 둘은 추가로 한 시간을 붙잡고 버그를 뜯어냈다.\n\n"
                    "지쳤지만, 끝까지 함께 버텨낸 덕분에 시험장으로 가는 발걸음은 오히려 단단했다."
                ),
                "next_node": mentor_final_id,
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_partner_checkpoint",
                "type": "choice",
                "title": "유리 루트 : 운영 콜",
                "background": "pc_bang_counter",
                "text": "손님 웨이브가 다시 몰려온다. 유리가 너를 본다. 어떤 콜을 할까?",
                "choices": [
                    {
                        "label": "\"라인 분담하자. 나는 라면, 넌 주문/결제.\"",
                        "target_node": "route_partner_bridge",
                        "effect": "안정적인 운영, 큰 변수 없음.",
                    },
                    {
                        "label": "\"분위기 반전용 번개 프로모션 간다.\"",
                        "target_node": "route_partner_bridge_fail",
                        "effect": "고위험 분기. 성공: 분위기 반등. 실패: 추가 정리 지옥.",
                    },
                ],
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_partner_bridge",
                "type": "dialogue",
                "title": "유리 루트 : 콤보 플레이",
                "background": "pc_bang_dawn",
                "characters": ["Lee Yuri"],
                "dialogue": [
                    {"speaker": "이유리", "text": "방금 콜 미쳤다! 진짜 듀오 랭크 올리는 느낌이야."},
                    {"speaker": "진", "text": "너처럼 멘탈 안 터지는 서포터 있으면 콜하기 편하지."},
                ],
                "next_node": partner_final_id,
            },
        )
        _append_node_if_missing(
            nodes,
            nodes_by_id,
            {
                "id": "route_partner_bridge_fail",
                "type": "narrative",
                "title": "유리 루트 : 연장전 복구",
                "background": "pc_bang_storage",
                "text": (
                    "프로모션이 예상보다 크게 터지며 주문이 폭주했다. 둘은 연장 근무로 겨우 수습했다.\n\n"
                    "녹초가 됐지만, 나가면서 서로 웃었다. 오늘 멘붕도 함께 넘겼으니까."
                ),
                "next_node": partner_final_id,
            },
        )

    return refreshed


STORY_DATA_KR_RAW = _apply_story_refresh(STORY_DATA_KR_RAW, locale="kr")
STORY_DATA_EN_RAW = _apply_story_refresh(STORY_DATA_EN_RAW, locale="en")


def _normalize_content(node_data):
    if isinstance(node_data.get("content"), list):
        return node_data.get("content")
    if isinstance(node_data.get("dialogue"), list):
        return node_data.get("dialogue")
    if node_data.get("text"):
        return [{"speaker": "System", "text": node_data.get("text", "")}]
    return []


def _normalize_choices(node_data, default_continue_text):
    normalized = []

    if isinstance(node_data.get("choices"), list):
        for choice_data in node_data["choices"]:
            text = choice_data.get("text") or choice_data.get("label")
            next_page_id = choice_data.get("next_page_id") or choice_data.get("target_node")
            if not text or not next_page_id:
                continue
            normalized_choice = {
                "text": text,
                "next_page_id": str(next_page_id),
                "effect": choice_data.get("effect"),
            }
            normalized.append(normalized_choice)
        return normalized

    next_node = node_data.get("next_page_id") or node_data.get("next_node")
    if next_node and next_node != "TBD":
        normalized.append({
            "text": default_continue_text,
            "next_page_id": str(next_node),
        })

    return normalized


def normalize_story_for_django(raw_story_data, default_continue_text="Continue"):
    story_meta = dict(raw_story_data.get("project_meta", {}))
    story_meta.setdefault("status", "published")

    initial_state = dict(raw_story_data.get("initial_state") or raw_story_data.get("player_state") or {})
    # Requested rename: protagonist name should be "user".
    initial_state["name"] = "user"

    normalized_nodes = []
    for node_data in raw_story_data.get("story_nodes", []):
        custom_id = node_data.get("custom_id") or node_data.get("id")
        if not custom_id:
            continue

        node_type = node_data.get("type", "narrative")
        is_ending = bool(node_data.get("is_ending") or node_data.get("is_game_over") or node_type == "ending")
        ending_label = node_data.get("ending_label") or node_data.get("outcome")
        if is_ending and not ending_label:
            ending_label = node_data.get("title")

        normalized_nodes.append({
            "custom_id": str(custom_id),
            "type": node_type,
            "title": node_data.get("title"),
            "background": node_data.get("background"),
            "illustration_url": node_data.get("illustration_url"),
            "content": _normalize_content(node_data),
            "text": node_data.get("text"),
            "affinity_change": node_data.get("affinity_change", {}),
            "is_ending": is_ending,
            "ending_label": ending_label,
            "choices": _normalize_choices(node_data, default_continue_text),
        })

    return {
        "project_meta": story_meta,
        "initial_state": initial_state,
        "story_nodes": normalized_nodes,
    }


STORY_DATA_KR = normalize_story_for_django(STORY_DATA_KR_RAW, default_continue_text="계속하기")
STORY_DATA_EN = normalize_story_for_django(STORY_DATA_EN_RAW, default_continue_text="Continue")


def seed_story(story_data):
    """
    Parses a Django-compatible Story Data Dictionary and inserts it into the DB.
    """
    meta = story_data["project_meta"]
    story_title = meta.get("title", "Untitled")
    print("--> Processing story...")

    story = Story(
        title=story_title,
        description=f"Version {meta.get('version', 'N/A')}",
        genre=meta.get("genre"),
        author=meta.get("author"),
        initial_state=story_data.get("initial_state", {}),
        status=meta.get("status", "published"),
    )
    db.session.add(story)
    db.session.commit()

    nodes_data = story_data.get("story_nodes", [])

    for node_data in nodes_data:
        node = StoryNode(
            story_id=story.id,
            custom_id=node_data["custom_id"],
            node_type=node_data.get("type", "narrative"),
            background=node_data.get("background"),
            illustration_url=node_data.get("illustration_url"),
            content_data=node_data.get("content", []),
            affinity_change=node_data.get("affinity_change", {}),
            is_ending=node_data.get("is_ending", False),
            ending_outcome=node_data.get("ending_label"),
        )
        db.session.add(node)

    db.session.commit()

    for node_data in nodes_data:
        parent_node = StoryNode.query.filter_by(story_id=story.id, custom_id=node_data["custom_id"]).first()
        if not parent_node:
            continue

        for choice_data in node_data.get("choices", []):
            if not choice_data.get("text") or not choice_data.get("next_page_id"):
                continue
            choice = Choice(
                text=choice_data["text"],
                node_id=parent_node.id,
                target_node_custom_id=choice_data["next_page_id"],
                effect_description=choice_data.get("effect"),
            )
            db.session.add(choice)

    db.session.commit()
    print("Successfully seeded story.")


# ==========================================
# 4. MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    with app.app_context():
        print("Starting database seed...")

        db.drop_all()
        db.create_all()

        seed_story(STORY_DATA_KR)
        seed_story(STORY_DATA_EN)

        print("All stories seeded. Ready to play.")
