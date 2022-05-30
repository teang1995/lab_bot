# LAB BOT
연구실 생활에 필요한 기능들을 담을 slack bot.  
가명 lab_bot

## SETTINGS
python: `3.9.12`  
Flask: `2.1.2`  
FastAPI: `0.75.1`

## DIRECTORY(TODO)

## COMMANDS
### nvidia-smi
- nvidia-smi {server_num}
    - {server_num} 번 서버의 gpu 사용 현황을 출력함.

- nvidia-smi summary(TODO)
    - 전체 서버의 사용 현황을 요약하여 출력함.

### gs(google scholar)(TODO)
- gs {keyword} cite
    - google scholar에 {keyword}를 검색했을 때 나오는 논문을 ciatation기준으로 정렬