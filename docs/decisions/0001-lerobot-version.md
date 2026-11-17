# 0001. LeRobot 버전을 0.7.0으로 고정

- 날짜: 2026-11-15
- 결정: 데스크톱, 학습 서버, Jetson에서 모두 LeRobot 0.7.0을 쓴다. 이 저장소에서는 `pyproject.toml`의 `robot` 항목(`lerobot[core_scripts,feetech]==0.7.0`)으로 고정한다.

## 근거

1. 0.7.0은 2026-11-05에 나온 최신 버전이고 Python 3.12 이상이 필요하다. 데스크톱(Ubuntu 24.04)과 Jetson(JetPack 7.2.1)의 Python이 모두 3.12다.
2. 비동기 추론 비교(계획 D7)에 쓰는 원격 추론 명령(`lerobot-policy-server`, `lerobot-rollout --inference.type=remote`)이 0.7.0 기준이다. 이전 방식(`lerobot.async_inference`)은 0.7.0에서 없어졌다.
3. 버전마다 명령과 설정이 달라지므로(0.7.0에도 이전 버전과 호환되지 않는 변경이 있다) 세 장비를 같은 버전으로 맞춘다.

## 이 결정이 바뀌는 경우

Jetson 설치 단계(J)에서 JetPack 7.2.1로 추론이 안 되면 JetPack 6.2.2로 다시 설치한다. JetPack 6.2.2의 Python은 3.10이라 0.7.0을 직접 설치할 수 없으므로, LeRobot 설치 문서가 안내하는 JetPack 6.2용 `docker/Dockerfile.jetson`으로 실행한다.

## 조건

0.7.0은 Linux에서 PyTorch를 PyPI의 CUDA 13 빌드로 설치한다. 이 빌드로 GPU를 쓰는 장비(학습 서버)는 NVIDIA 드라이버가 580.65 이상이어야 하고, 그보다 낮으면 CUDA 12 인덱스에서 torch를 먼저 설치한 뒤 LeRobot을 설치한다(0.7.0 릴리스 노트). 학습 서버의 드라이버 버전은 A4에서 확인한다.

## 확인 결과

- 데스크톱에 설치된 버전(`pip show lerobot`):
- 공개 데이터셋 `lerobot/svla_so101_pickplace` 1프레임 읽기 출력:

~~~
Version: 0.7.0
frames: 11939
action (6,)
observation.state (6,)
timestamp ()
frame_index ()
episode_index ()
index ()
task_index ()
observation.images.up (3, 480, 640)
observation.images.side (3, 480, 640)
~~~
