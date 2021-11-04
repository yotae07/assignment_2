```
pip install virtualenv
assignment_2 디렉토리안에서 python3 -m venv venv ./venv로 가상환경 생성
source ./venv/bin/activate로 가상환경 활성화
pip install -r ./requirements.txt로 패키지 설치
마이그레이션 후 서버 작동

가급적 post쪽 코드를 보시면서 공부하실길 추천드리고
주석된 코드는 내부적으로 사용되고 있는 코드들이니 궁금하시면 주석을 해제하시고 사용해보시면 됩니다.
```

```
전체적인 흐름은
요청 => urls.py => views.py => serializers.py => models.py => serializers.py => views.py => urls.py => 응답

viewset의 역할
viewset은 CRUD를 추상화한 역할이며 각 메소드마다 맵핑이되어있습니다.
각 CRUD에 맵핑된 매소드마다 호출하는 형태가 다르기 때문에 하나로 정리할 순없지만 전체적인 그림은
입력된 값들을 serializer로 옮겨주고 serializer는 값을 검증하고 db에 저장합니다.
요청받은 값들을 응답할때도 ORM을 통해 나온 값을 보여주고 싶은 형태로 가공해서 응답할 수 있습니다.

serializer의 역할
serializer는 요청으로 받은 데이터를 serializer에 맵핑된 형태의 값이 맞는지 확인하고 값들을 약속된 형태로 변환하는 역할입니다.
물론 응답으로 내보내야되는 데이터의 경우에도 ORM을 통해 나오는 값들이 원하는 형태의 값들로 변환되어 나올 수 있게 변환하는 역할이기도 합니다.
항상 serializer를 통해야만 되는건 아닙니다.

serializer를 호출할시 실행되는 메소드의 흐름은
to_internal_value => validate => create or update => to_representation
각 메소드는 오버라이딩을 통해 원하는 형태로 가공할 수 있습니다.
to_internal_value는 write시 오버라이드되어 활용됩니다.
to_representation은 read시 오버라이드되어 활용됩니다.
validate는 .is_valid()값을 호출할 시 타게 됩니다.
.is_valid()호출시 to_internal_value를 호출하고 validate 함수를 호출하게 됩니다.
.data를 호출시 to_representation을 타게 됩니다. 
```
