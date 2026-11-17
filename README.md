# so101-robot-systems

SO-101 로봇 팔로 시연 수집 → 학습 → Jetson 실행 → 평가를 한 번 끝까지 하고, 결과를 숫자로 남기는 저장소.

## 장비 역할

| 장비 | 역할 |
|---|---|
| 데스크톱(WSL2 Ubuntu 24.04) | 개발, 테스트, 분석 |
| Jetson Orin Nano Super 8GB | 팔 2대와 카메라 2대 연결: 조립·캘리브레이션, 수집, 실행, 평가 |
| GPU 클라우드 | 학습 |

팔과 카메라를 Jetson에 연결하는 이유는 `docs/decisions/0002-robot-host.md`에 있다.

## 환경

Ubuntu 24.04, 시스템 Python 3.12의 venv, LeRobot 0.7.0. 버전을 고정한 이유는 `docs/decisions/0001-lerobot-version.md`, venv를 쓰는 이유는 `docs/decisions/0003-python-env.md`에 있다.

```bash
sudo apt install -y python3-venv python3-dev build-essential ffmpeg libevdev-dev
/usr/bin/python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install evdev
pip install -e ".[robot,dev]"
```

새 터미널에서는 `source .venv/bin/activate`를 먼저 실행한다.

## 폴더 구조

| 폴더 | 내용 |
|---|---|
| `src/robot_systems/` | Python 코드: 검증기, 수집 도우미, 평가·어노테이션 화면, MCAP 변환기, 리타겟팅, TensorRT 실행기 |
| `ros2/` | ROS 2 패키지: C++ 추론 노드, 팔 제어 노드 |
| `experiments/` | 측정 스크립트와 결과: 추론 시간, 가지치기, 배치 |
| `docs/decisions/` | 결정 기록: 왜 했는지, 결과를 보고 어떻게 판단했는지 |
| `tests/` | 단위 테스트 |

`ros2/`와 `experiments/`는 해당 단계에서 추가한다.

## 개발 규칙

- 모든 변경은 브랜치에서 작업해 PR로 올리고, CI의 `test`가 통과한 뒤 병합한다.
- main에는 직접 push할 수 없다. 규칙은 `.github/rulesets/main-protection.json`에 있다.
- PR을 올리기 전에 아래 명령이 통과해야 한다.

```bash
ruff check . && ruff format --check . && pytest
```
