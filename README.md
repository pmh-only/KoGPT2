## KoGPT2 http server
실행방법:
```
python3.8 -m pip install -r requirements.txt
port=8080 python3.8 app.py
```

예시:
```
req: GET /job?query=깃허브
res: {"result":["는","털","▁이"],"success":true}

result: 정확도 별로 정렬된 추천 키워드, (▁는 스페이스, </s>는 문장 끝을 의미)
```

```
req: GET /job?query=2021년은&loop=100
res: {"result":"2021년은▁‘세계적▁경제대국’으로▁도약하는▁원년으로▁삼겠다는▁목표를▁세웠다.</s>","success":true}

result: 생성된 문자열
```
