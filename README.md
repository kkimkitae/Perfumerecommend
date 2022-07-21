# 봄:향
향수 추천 프로젝트

빅데이터 향수 추천 프로젝트

시연 영상 https://youtu.be/gnfD5Lw2DHQ

img파일 약 1.2기가 flask-3/static/   https://drive.google.com/file/d/1FU0sj5oh_B_kFGHHBzxfdkJskVd0UuAa/view?usp=sharing


<hr>

<img width="300" alt="image" src="https://user-images.githubusercontent.com/85480964/180188576-288c8a72-21a9-4d29-8877-3a954f1ccf70.png">



## 0. 팀 소개


* 팀원 남종호 : 백엔드 
* 팀원 김기태 : 프론트엔드
* 팀원 송수림 : 자료조사
* 팀장 공경민 : 데이터분석 / 디자인

## 1. 서비스의 목적 및 가치


• 향수를 일상적인 액세서리로 보는 시간이 확산되면서 향수를 뿌리는 소비자가 많아지는 추세

• 대표적인 자기만족 제품으로서 최근 소비 경향인 가치소비와 맞아 떨어짐

• 향수가 부담스러운 사람들에게 직 접 시향을 하지 않아도 선택할 수 있음

• 구매자들에게 자신이 사용했던 향수를 검색하면 그 향수와 비슷한 향수를 찾을 수 있도록 도움

## 2. 이용 아키텍처
<img width="518" alt="image" src="https://user-images.githubusercontent.com/85480964/180190082-fd5ee387-ad5f-4c37-88e3-102ece4b3e82.png">

## 3. 알고리즘 설명
<img width="400" alt="image" src="https://user-images.githubusercontent.com/85480964/180190171-ad2c8039-485d-4392-87af-cd9d966dd489.png">
<img width="400" alt="image" src="https://user-images.githubusercontent.com/85480964/180190188-9fc097d7-0bc0-4354-b894-904f86fbfc86.png">

## 4. 데이터 수집 과정
<img width="350" alt="image" src="https://user-images.githubusercontent.com/85480964/180190575-e9c1c236-339f-4819-b3c2-9fe916cddb35.png">
<img width="350" alt="image" src="https://user-images.githubusercontent.com/85480964/180190591-76b81767-5af2-41d1-986a-9724d1f4ff5a.png">
<img width="350" alt="image" src="https://user-images.githubusercontent.com/85480964/180190631-b142a68d-6e83-47f9-b6c3-4df3f58b00f1.png">
<img width="150" alt="image" src="https://user-images.githubusercontent.com/85480964/180190683-8266f350-bdaa-4ab0-b22b-9d82eda6a88b.png">
selenium 라이브러리를 이용하여 웹 최대 규모 향수 사이트인 fragrantica를 대상으로 향수 데이터를 크롤링하였으며, 적당한 전처리 후 약 25000개의 데이터가 모였고, 
약 24545개의 데이터를 데이터베이스에 적재하였습니다.

## 5. front

봄:향은 크게 네가지 서비스를 제공합니다. 
답변을 통한 향수 추천받기, 향수 초심자에게 낯선 용어들이 정리된 향수 용어 사전, 향수 검색하기, 향수 명을 입력하면 비슷한 향수를 추천받는 비슷한 향수 찾기입니다. 

<img width="500" alt="image" src="https://user-images.githubusercontent.com/85480964/180186908-ffc5d0b1-47a7-4a20-ab34-1d8472355241.png">
