# Lab 4: Follow the Gap (Python)

> RoboRacer SW 해커톤 2026 (IEEE ITSS 한국지회 x 충북대) 참가팀을 위한 Lab 04 과제 저장소입니다. 이 저장소는 팀원과 운영자만 볼 수 있습니다.

## 0. 이 대회의 과제, 제출, 채점 (먼저 읽으십시오)

이 장은 이 대회에만 해당하며, 아래 I 절부터 III 절까지의 원문 안내(영어)보다 우선합니다. 일정, 마감, 순위, 자격, AI 튜터, 사용할 수 있는 도구와 규칙은 이 문서에 쓰지 않았습니다. 참가 공지를 따르십시오.

### 과제

`gap_follow/scripts/reactive_node.py` 의 `ReactiveFollowGap` 클래스를 완성합니다. 라이다 스캔에서 가장 넓은 빈 공간(gap)을 찾아 그 안의 한 점을 향해 조향하고, `/drive` 로 속도와 조향각을 발행하는 노드입니다. 클래스 이름은 바꾸지 마십시오. 채점기가 이름으로 불러옵니다. 채점은 Python 노드만 합니다.

### 제출과 채점

- `main` 브랜치에 commit 하고 push 하면 자동 채점이 실행됩니다. 이 대회에서는 동영상이나 `SUBMISSION.md` 를 제출하지 않아도 됩니다.
- 결과는 보통 몇 분 안에 해당 commit 의 `autograde` 체크에 `Score N/14` 로 표시됩니다. 항목마다 1점이며, 통과하지 못한 항목에는 이유가 함께 표시됩니다.
- 14개 항목: 빌드 3개(모듈 import, 클래스 생성, 필요한 메서드), 정적 검사 6개(`preprocess_lidar`, `find_max_gap`, `find_best_point`, `lidar_callback` 을 작은 입력으로 확인), 시뮬레이션 3개(주행 명령을 발행하는지, 복도를 끝까지 완주하는지, 충돌이 없는지), 스타일 2개(PEP8, 남은 TODO 가 없는지).
- 순위에 쓰는 기록은 시뮬레이션 3개 항목을 통과한 주행의 완주 시간입니다. 자격과 순위 규칙은 참가 공지를 따릅니다. 그러므로 `Score N/14` 가 같아도 기록은 다를 수 있습니다.
- AI 튜터의 한국어 피드백이 저장소의 Issues 에 `AI tutor feedback` 이라는 제목으로 남을 수 있습니다. 남는 조건은 참가 공지를 따릅니다. 튜터의 설명은 참고용이며 틀릴 수 있습니다. 점수는 자동 채점 결과로만 정해집니다.
- commit 후 10분 정도 지나도 저장소에 아무 변화가 없으면(체크도, Issues 글도 없으면) 운영자에게 알려 주십시오. 문의처는 참가 공지에 있습니다. 코드의 문제가 아니라 채점 시스템의 문제일 수 있습니다.

### 시뮬레이션과 기록

채점용 시뮬레이션은 장애물이 있는 길이 30 m 의 직선 복도에서 한 번 실행됩니다. 라이다는 270도, 1080개 빔이고 잡음이 없으며, 같은 코드와 같은 채점 이미지에서는 같은 결과가 나옵니다. 결과의 마지막 줄에 기록이 나옵니다.

    RANK_METRIC lap_completed=1 collisions=0 sim_time_s=16.1000

`sim_time_s` 는 복도 끝까지 걸린 시뮬레이션 시간이고, `lap_completed=1 collisions=0` 인 주행만 순위에 오릅니다. 75초 안에 끝까지 가지 못하면 완주로 치지 않으며, 처음 3초 안에 주행 명령을 하나도 발행하지 않으면 거기서 끝납니다.

다음은 대회 규칙입니다. 하나라도 바뀌면 모든 팀의 기록이 바뀌므로 대회 중에는 바꾸지 않습니다.

- 속도 명령은 0 에서 6.0 m/s 사이로 잘립니다. 더 큰 명령은 6.0 m/s 로 적용되며 감점은 없습니다.
- 가속도는 4 m/s^2, 조향각은 +-0.4189 rad (약 +-24도), 조향 속도는 3.2 rad/s 로 제한됩니다. 제한을 넘는 명령도 같은 방식으로 잘려서 적용됩니다.
- 차는 반지름 0.15 m 의 원판이고, 0.005초 간격으로 충돌을 검사합니다. 첫 충돌이 일어나면 그 주행은 끝납니다.

### 채점 시 유의 사항

1. `lidar_callback` 은 반드시 반환해야 합니다. 반환하지 않으면(무한 반복 등) 그 호출에 의존하는 항목은 실패하고 이유가 표시됩니다.
2. 빔 각도는 `data.angle_min` 과 `data.angle_increment` 로 계산하십시오. 빔 번호를 코드에 고정하지 마십시오.
3. `/scan` 을 구독하고 `/drive` 로 `AckermannDriveStamped` 를 발행합니다. 발행자를 저장하는 변수 이름은 상관없습니다.
4. 스타일 항목은 `pycodestyle` (한 줄 120자까지)와 `TODO` 글자 검사입니다. 주석을 포함해 `TODO` 라는 글자가 한 군데라도 남아 있으면 그 항목은 실패합니다.

---

*The sections below are the Lab 4 handout, kept in English (section I to III as in the template; the paragraph about a C++ variant is dropped, because this event grades Python only). The original sections IV (Tiered grading, with a manual video) and V (Submission) do not apply to this event: section 0 above replaces them.*

Reactive obstacle avoidance for the F1TENTH platform. You will implement
the **Follow the Gap** algorithm: find the largest free-space gap in the
LiDAR scan, then steer the car toward a point inside it.

## I. Learning Goals

- Reactive methods for obstacle avoidance.
- LiDAR scan preprocessing (smoothing, outlier rejection, bounded ranges).
- Mapping geometric features (a "gap") to a control command (steering angle + speed).

## II. The Follow-the-Gap algorithm

For every LaserScan message:

1. **Preprocess** the ranges. Drop nan/inf, smooth (moving average), clamp values above some `max_range`.
2. Find the **closest** point in the preprocessed array.
3. Draw a **safety bubble** of radius `R_bubble` around the closest point — set all ranges inside that bubble to `0.0`. Anything still nonzero is "free space."
4. Find the longest contiguous run of nonzero ranges. That is the **max gap**.
5. Pick the **best target point** inside the max gap. Naive: the deepest beam. Better: midpoint of the widest sub-gap (see UNC video linked in the upstream README).
6. Convert the target beam index to a steering angle (`angle_min + target_i * angle_increment`) and publish on `/drive`.

The whole loop is ~120 lines of Python.

## III. What you edit

```
gap_follow/scripts/reactive_node.py   ← only file you need to touch
```

The class `ReactiveFollowGap(Node)` has 5 methods with `TODO` markers:

- `__init__` — wire up the `/scan` subscription and `/drive` publisher.
- `preprocess_lidar(ranges)` — smoothing + clamping.
- `find_max_gap(free_space_ranges)` — longest nonzero run.
- `find_best_point(start_i, end_i, ranges)` — pick the target inside the gap.
- `lidar_callback(data)` — orchestrate the pipeline and publish drive commands.

You may add helper methods or tune parameters (bubble radius, smoothing window, speed schedule). Do not rename `ReactiveFollowGap` — the autograder imports it by name.

## VI. Resources

- Upstream F1TENTH lecture slides on Follow-the-Gap (linked from the upstream README).
- UNC reference video: <https://youtu.be/ctTJHueaTcY>
