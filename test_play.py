import requests
import json

# 서버 주소 (Flask 기본 포트)
BASE_URL = "http://127.0.0.1:5000/api"


def play_game():
    print("🎮 [런타임 에러] 게임 클라이언트 접속 중...")

    # 1. 스토리 목록 가져오기
    try:
        res = requests.get(f"{BASE_URL}/stories")
        stories = res.json()
    except Exception as e:
        print(f"서버 접속 실패: {e}")
        return

    if not stories:
        print("등록된 스토리가 없습니다. seed.py를 실행했나요?")
        return

    # 첫 번째 스토리 선택 (자동)
    story = stories[0]
    story_id = story['id']
    print(f"== {story['title']} 시작합니다 ==")
    print(f"설명: {story['description']}\n")

    # 2. 시작 노드 가져오기
    res = requests.get(f"{BASE_URL}/stories/{story_id}/start")
    if res.status_code != 200:
        print("시작 노드를 찾을 수 없습니다.")
        return

    current_node = res.json()

    # 3. 게임 루프 (엔딩이 아닐 때까지 반복)
    while True:
        print("-" * 50)
        # 배경 정보 출력 (디버깅용)
        # print(f"[Debug] Scene: {current_node['id']} | BG: {current_node['background']}")

        # 대사/지문 출력
        content_list = current_node.get('content', [])
        for content in content_list:
            speaker = content.get('speaker', 'System')
            text = content.get('text', '')
            if speaker == "System":
                print(f"\nExample: {text}")
            else:
                print(f"\n[{speaker}] {text}")

        # 엔딩 체크
        if current_node.get('is_ending'):
            print("\n" + "=" * 20 + " ENDING " + "=" * 20)
            print(f"결과: {current_node.get('outcome')}")
            break

        # 선택지 출력
        choices = current_node.get('choices', [])

        if not choices:
            print("\n더 이상 진행할 선택지가 없습니다 (Dead End).")
            break

        print("\n[선택지]")
        for idx, choice in enumerate(choices):
            print(f"{idx + 1}. {choice['label']}")

        # 사용자 입력 받기
        while True:
            try:
                selection = int(input("\n선택 > ")) - 1
                if 0 <= selection < len(choices):
                    chosen_next_id = choices[selection]['target_node']
                    print(f"--> 이동 중: {chosen_next_id}...")
                    break
                else:
                    print("잘못된 번호입니다.")
            except ValueError:
                print("숫자를 입력해주세요.")

        # 4. 다음 노드 불러오기 (API 호출)
        res = requests.get(f"{BASE_URL}/stories/{story_id}/nodes/{chosen_next_id}")
        if res.status_code == 200:
            current_node = res.json()
        else:
            print(f"\n오류 발생! 다음 노드({chosen_next_id})를 불러오지 못했습니다.")
            break


if __name__ == "__main__":
    play_game()