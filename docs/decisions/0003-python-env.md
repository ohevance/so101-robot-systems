# 0003. 데스크톱의 Python 환경은 venv로 만든다

- 날짜: 2026-11-16
- 결정: 데스크톱(WSL2 Ubuntu 24.04)의 Python 환경은 시스템 Python 3.12의 venv(`.venv`)로 만들고, ffmpeg는 apt로 설치한다. conda는 쓰지 않는다.

## 근거

1. LeRobot 설치 문서는 conda를 권장하지만, 다른 환경 관리자(uv, venv)도 Python 3.12 이상, PyTorch 2.10 이상이면 쓸 수 있다고 안내한다. PyTorch 2.10(TorchCodec 0.10)부터 TorchCodec이 시스템에 설치된 ffmpeg를 불러올 수 있기 때문이다.
2. 두 조건이 충족된다. Ubuntu 24.04의 Python은 3.12이고, LeRobot 0.7.0은 PyTorch 2.15와 TorchCodec 0.17을 기본으로 설치한다(huggingface/lerobot PR #5210, 0.7.0에 포함).
3. CI(`.github/workflows/ci.yml`)가 pip로 설치하므로 로컬과 CI의 설치 방식이 같다.
4. Jetson(JetPack 7.2)의 TensorRT 파이썬 모듈은 시스템 Python 패키지로 제공되고, 확인한 JetPack 7.2 설치 사례 3건은 모두 시스템 Python 3.12로 만든 venv에서 이를 불러온다(예: `--system-site-packages`). 데스크톱도 venv로 두면 두 장비의 환경 도구가 같다.

## 조건

- Ubuntu 24.04의 ffmpeg는 6.1.1이다. TorchCodec은 FFmpeg 4~8을 지원한다(TorchCodec 0.14 문서 기준). TorchCodec이 ffmpeg를 불러오지 못하면 LeRobot 0.7.0은 경고를 내고 PyAV로 영상을 읽는다.
- WSL에서는 evdev를 따로 설치한다(LeRobot 설치 문서): apt로 `libevdev-dev`, 그다음 `pip install evdev`. evdev는 설치할 때 컴파일되므로 `build-essential`과 `python3-dev`가 필요하다.
- 데스크톱의 셸에는 ROS 2 Jazzy가 적용되어 있어 `PYTHONPATH`로 ROS의 Python 패키지가 venv에서도 보인다. pytest가 ROS의 플러그인(`launch_testing`)을 자동으로 불러오다가 venv에 없는 `lark`를 찾지 못해 멈추므로, `pyproject.toml`에서 플러그인 자동 로드를 끈다(`--disable-plugin-autoload`). 이 저장소의 테스트는 플러그인을 쓰지 않는다.

## 확인 결과

- `PYTHONPATH`의 경로별로 venv와 이름이 겹치는 패키지: /opt/ros/jazzy/lib/python3.12/site-packages → 없음
- 설치된 버전(Python, lerobot, torch, torchcodec, torchvision, ffmpeg):

~~~
Python 3.12.3
lerobot                              0.7.0
torch                                2.15.0
torchcodec                           0.17.0
torchvision                          0.29.2
ffmpeg version 6.1.1-3ubuntu5 Copyright (c) 2000-2023 the FFmpeg developers
~~~

- TorchCodec 직접 확인: 데이터셋 영상 1프레임 디코딩 성공, 크기 (3, 480, 640), 불러온 libavcodec: /usr/lib/x86_64-linux-gnu/libavcodec.so.60.31.102
