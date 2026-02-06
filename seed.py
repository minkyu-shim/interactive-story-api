import json
from app import create_app, db
from app.models import Story, StoryNode, Choice

# Initialize Flask App
app = create_app()

# --- The Full Story Data ---
STORY_DATA = {
  "project_meta": {
    "title": "런타임 에러 : 연애는 예외처리가 안 되나요? (Expanded)",
    "version": "1.1.0",
    "genre": "공대생 로맨스 시뮬레이션",
    "author": "AI Writer & User"
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
        {
          "speaker": "차수연",
          "text": "너, 0과 1 말고 사람 언어로 말하는 법 몰라? 코드가 이게 뭐야. 이번 주까지 최적화 안 해오면 멘토링 취소야."
        },
        {
          "speaker": "system",
          "text": "수연의 노트북이 갑자기 먹통이 된다. 당신은 하드웨어 지식을 발휘해 순식간에 고쳐주었다."
        },
        {
          "speaker": "차수연",
          "text": "...고, 고마워. 너 생각보다 쓸모가 있네? (얼굴을 붉힘)"
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
      "text": "며칠 뒤, 도서관. 수연이 당신에게 과제를 던져주었다. '이 알고리즘, 실행 속도가 너무 느려. 어떻게 고칠 거야?'",
      "choices": [
        {
          "label": "\"변수명부터 정리하고, 주석 달면서 정석대로 리팩토링하겠습니다.\" (정공법)",
          "target_node": "node_02_success",
          "effect": "차수연 호감도 대폭 상승"
        },
        {
          "label": "\"일단 돌아가기만 하면 되죠! StackOverflow에서 코드 복붙하겠습니다.\" (꼼수)",
          "target_node": "node_02_fail",
          "effect": "차수연 호감도 하락"
        }
      ]
    },
    {
      "id": "node_02_success",
      "type": "dialogue",
      "title": "이벤트 성공 : 수연의 인정",
      "background": "university_library",
      "characters": ["Cha Sooyeon"],
      "dialogue": [
        { "speaker": "차수연", "text": "오... 너 제법인데? 기본기는 갖춰져 있구나. 다시 봤어." },
        { "speaker": "system", "text": "수연이 캔커피를 당신 책상에 툭 놓고 갔다." }
      ],
      "affinity_change": { "cha_sooyeon": 15 },
      "next_node": "node_03_common_night"
    },
    {
      "id": "node_02_fail",
      "type": "dialogue",
      "title": "이벤트 실패 : 수연의 경멸",
      "background": "university_library",
      "characters": ["Cha Sooyeon"],
      "dialogue": [
        { "speaker": "차수연", "text": "하... 내가 너한테 뭘 기대하니. 개발자 때려쳐라. 그건 코딩이 아니라 조립이야." },
        { "speaker": "system", "text": "수연은 한심하다는 듯 혀를 차고 가버렸다." }
      ],
      "affinity_change": { "cha_sooyeon": -5 },
      "next_node": "node_03_common_night"
    },


    {
      "id": "node_03_common_night",
      "type": "dialogue",
      "title": "공통 루트 (밤) : 이유리와의 비밀",
      "background": "pc_bang_midnight",
      "characters": ["Lee Yuri"],
      "dialogue": [
        {
          "speaker": "이유리",
          "text": "오빠! 오늘 야간은 내가 쏜다! 폐기 도시락 나왔어, 같이 먹자."
        },
        {
          "speaker": "system",
          "text": "새벽 시간, 당신은 유리의 가방에서 한정판 게임 굿즈가 쏟아지는 것을 목격한다."
        },
        {
          "speaker": "이유리",
          "text": "헐... 오빠도 이거 알아? 나 안 놀려? 와 대박! 우리 통하는 게 있네!"
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
      "title": "밤의 위기 : 샷건 치는 손님",
      "background": "pc_bang_counter",
      "text": "새벽 2시, 구석 자리 아저씨가 게임에서 졌는지 키보드를 내려치며 난동을 피운다. 유리가 겁을 먹고 떨고 있다. 당신의 행동은?",
      "choices": [
        {
          "label": "\"손님, 기물 파손하시면 경찰 부릅니다.\" (논리적/강경 대응)",
          "target_node": "node_03_fail",
          "effect": "유리의 걱정, 분위기 싸해짐"
        },
        {
          "label": "\"괜찮아? 저 아저씨 내가 가서 음료수 주면서 달래고 올게.\" (감성적/공감 대응)",
          "target_node": "node_03_success",
          "effect": "이유리 호감도 대폭 상승"
        }
      ]
    },
    {
      "id": "node_03_success",
      "type": "dialogue",
      "title": "이벤트 성공 : 유리의 감동",
      "background": "pc_bang_counter",
      "characters": ["Lee Yuri"],
      "dialogue": [
        { "speaker": "이유리", "text": "와... 오빠 진짜 대단하다. 나였으면 울었을 거야. 오빠 덕분에 살았다 ㅠㅠ" },
        { "speaker": "system", "text": "유리가 당신의 팔을 꼭 붙잡는다. 샴푸 향기가 난다." }
      ],
      "affinity_change": { "lee_yuri": 15 },
      "next_node": "node_04_climax_trigger"
    },
    {
      "id": "node_03_fail",
      "type": "dialogue",
      "title": "이벤트 실패 : 너무 딱딱해",
      "background": "pc_bang_counter",
      "characters": ["Lee Yuri"],
      "dialogue": [
        { "speaker": "이유리", "text": "아니 오빠... 그렇게 무섭게 말하면 어떡해; 더 큰일 나면 어쩌려고..." },
        { "speaker": "system", "text": "상황은 해결됐지만, 유리는 당신의 냉정함에 약간 거리를 두는 눈치다." }
      ],
      "affinity_change": { "lee_yuri": -5 },
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
        {
          "label": "차수연에게 간다 (학점/미래)",
          "target_node": "root_sooyeon_start",
          "effect": "학업 성취도 상승, 자금 확보 실패"
        },
        {
          "label": "이유리에게 간다 (돈/의리)",
          "target_node": "root_yuri_start",
          "effect": "RTX 5070 자금 확보, 학사 경고 위험"
        }
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
        { "speaker": "차수연", "text": "3분 늦었어. 그래도... 왔네? 안 올 줄 알았는데." },
        { "speaker": "주인공", "text": "선배가 부르는데 와야죠. 제적당하기 싫으니까." },
        { "speaker": "차수연", "text": "흥, 앉아. 오늘 밤새워서 이 알고리즘 머리에 때려 박을 거니까 각오해." }
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
        {
          "label": "\"선배 덕분에 A+ 확정이에요. 진짜 최고의 멘토였습니다!\" (존경 표현)",
          "target_node": "end_sooyeon_bad",
          "effect": "수연의 실망, 관계의 선 긋기"
        },
        {
          "label": "\"선배, 저 이제 논리 회로 말고 선배 마음 회로도 분석해 봐도 됩니까?\" (고백)",
          "target_node": "end_sooyeon_happy",
          "effect": "연인 관계 발전"
        }
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
        { "speaker": "이유리", "text": "오빠!! 진짜 왔구나! 나 오빠 믿고 있었다고 ㅠㅠ 얼른 앞치마 입어!" },
        { "speaker": "주인공", "text": "상황 설명 나중에 해. 주방 내가 맡을게. 너는 홀 봐!" },
        { "speaker": "이유리", "text": "알았어! 와... 오빠 오니까 갑자기 든든하네." }
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
        {
          "label": "\"미안, 나 이거 바로 입금해야 돼. 그래픽카드 특가 떴거든.\" (물질 우선)",
          "target_node": "end_yuri_bad",
          "effect": "유리의 실망, 관계 소원"
        },
        {
          "label": "\"그래픽카드는 나중에 사지 뭐. 일단 너 사고 싶다던 그 한정판 굿즈부터 사러 가자.\" (유리 우선)",
          "target_node": "end_yuri_happy",
          "effect": "연인 관계 발전"
        }
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

# --- Seeding Logic ---

with app.app_context():
    print("🌱 Starting Database Seed...")

    # 1. Clean Slate (Reset DB)
    db.drop_all()
    db.create_all()

    # 2. Create Story
    meta = STORY_DATA['project_meta']
    story = Story(
        title=meta['title'],
        description=f"Version {meta['version']}",
        genre=meta['genre'],
        author=meta['author'],
        initial_state=STORY_DATA['player_state']
    )
    db.session.add(story)
    db.session.commit()  # Commit to get story.id
    print(f"✅ Created Story: {story.title}")

    # 3. Create Nodes (First Pass)
    # Note: We create nodes first without choices, because choices need target nodes to exist (conceptually),
    # although here we use string IDs (custom_id) so order is less strict, but good practice.

    nodes_data = STORY_DATA['story_nodes']

    for n_data in nodes_data:
        # Normalize Content: Convert explicit 'text' to JSON format if 'dialogue' is missing
        content = []
        if 'dialogue' in n_data:
            content = n_data['dialogue']
        elif 'text' in n_data:
            # Wrap narrative text in a generic speaker object
            content = [{"speaker": "System", "text": n_data['text']}]

        node = StoryNode(
            story_id=story.id,
            custom_id=n_data['id'],
            node_type=n_data.get('type', 'narrative'),
            background=n_data.get('background'),
            content_data=content,
            affinity_change=n_data.get('affinity_change', {}),
            is_ending=n_data.get('is_ending', False),
            ending_outcome=n_data.get('outcome')  # Only relevant for ending nodes
        )
        db.session.add(node)

    db.session.commit()  # Commit to save all nodes
    print(f"✅ Created {len(nodes_data)} Story Nodes.")

    # 4. Create Choices & Links (Second Pass)
    # We loop through data again to link nodes via Choice objects.

    choice_count = 0

    for n_data in nodes_data:
        # Find the parent node we just created
        parent_node = StoryNode.query.filter_by(story_id=story.id, custom_id=n_data['id']).first()

        # A. Explicit Choices (Branching)
        if 'choices' in n_data:
            for c_data in n_data['choices']:
                choice = Choice(
                    text=c_data['label'],
                    node_id=parent_node.id,
                    target_node_custom_id=c_data['target_node'],
                    effect_description=c_data.get('effect')
                )
                db.session.add(choice)
                choice_count += 1

        # B. Implicit Linear Link (Next Node)
        # If there are no choices, but there is a 'next_node', we create a "Continue" button.
        elif 'next_node' in n_data and n_data['next_node'] != "TBD":
            choice = Choice(
                text="계속하기",  # Default label for linear progression
                node_id=parent_node.id,
                target_node_custom_id=n_data['next_node']
            )
            db.session.add(choice)
            choice_count += 1

    db.session.commit()
    print(f"✅ Created {choice_count} Choices/Links.")
    print("🚀 Seeding Complete! The game is ready to play.")