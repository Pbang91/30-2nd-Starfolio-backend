![header](https://capsule-render.vercel.app/api?type=waving&color=4c4ca0&height=100&section=header&fontSize=90)

![transparency](https://user-images.githubusercontent.com/57164712/160241939-35ffe254-c193-40c3-b405-3bd1eb31d25a.png)

---
# 참고 사이트

![스크린샷 2022-03-27 오전 8 32 18](https://user-images.githubusercontent.com/57164712/160260490-bb77a1ef-916f-4819-84be-280992f29d7d.png)

[스테이폴리오](https://www.stayfolio.com/)

"머무는 것 자체로 여행이 되는 공간"

스테이폴리오는 좋은 공간의 가치를 세상에 소개하고 머무름 만으로 여행이 되는 경험을 제공합니다.

스테이폴리오는 좋은 공간을 만들어가는 사람들과 이를 체험하는 고객들을 연결해 주는 플랫폼입니다. 

<br>

---
# 기획 & ERD

* ## 기획목표
* 짧은 기간동안 기능구현에 집중해야하므로 사이트의 디자인과 기획만 클론
* 개발은 초기세팅부터 전부 직접 구현
* 필수 구현 사항으로 로그인, 행성 리스트, 숙소 디테일, 예약, 마이페이지기능으로 설정

* ## ERD

![스크린샷 2022-03-27 오전 8 51 20](https://user-images.githubusercontent.com/57164712/160260848-f1a46bf0-591d-407b-8d25-4587dac95378.png)

<br>

---
# 개발기간 & 팀원

* ## 개발기간
    2022.03.14 ~ 2022.03.25
    
* ## 개발인원 & 맡은부분
  
  * #### FRONTEND
      
      박철진 - Header 컴포넌트, Footer 컴포넌트, main 페이지, 숙소 Detail 페이지
      
      정건희 - 초기세팅, 행성 List 페이지
      
      유강호 - 소셜로그인, 마이페이지
      
      [FRONTEND GITHUB](https://github.com/wecode-bootcamp-korea/30-2nd-Starfolio-frontend)
      
  * #### BACKEND
      
      박건규 - 모델링, 회원가입&소셜로그인, 로그인 데코레이터, 숙소 Detail API, users 테스트코드 작성, 숙소 Detail 테스트코드 작성
      
      김가람휘 - 초기세팅, 모델링, 행성 List API, 예약 API, 위시리스트 API, 행성 List 테스트코드 작성, bookings 테스트코드 작성, wishlists 테스트코드 작성, AWS EC2서버에 Docker Container를 활용하여 배포

<br>

---
# 적용기술 & 구현기능

* ## 기술스택

  * #### FRONTEND
    <a href="#"><img src="https://img.shields.io/badge/HTML-DD4B25?style=plastic&logo=html&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/SASS-254BDD?style=plastic&logo=sass&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/javascript-EFD81D?style=plastic&logo=javascript&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/React-68D5F3?style=plastic&logo=react&logoColor=white"/></a>
    
  * #### BACKEND
    <a href="#"><img src="https://img.shields.io/badge/python-3873A9?style=plastic&logo=python&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/Django-0B4B33?style=plastic&logo=django&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/MySQL-005E85?style=plastic&logo=mysql&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/AWS-FF9701?style=plastic&logo=aws&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/docker-0040FF?style=plastic&logo=docker&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/postman-F76934?style=plastic&logo=postman&logoColor=white"/></a>
    
  * #### COMMUNICATION
    <a href="#"><img src="https://img.shields.io/badge/github-1B1E23?style=plastic&logo=github&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/Slack-D91D57?style=plastic&logo=slack&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/Trello-2580F7?style=plastic&logo=trello&logoColor=white"/></a>

* ## 구현기능
  * 회원가입/로그인
    * 카카오 엑세스 토큰을 받아 유저를 확인하고 유저 정보를 암호화하여 db에 저장하고 jwt 토큰 발행
    * request.header에 담긴 토큰을 이용하여 로그인 여부 확인
  
  * 행성 List API
    * 선택한 은하계, 테마, 검색, 인원수, 최소가격, 최대가격에 따라 행성을 불러오는 필터링기능 구현
    * 체크인, 체크아웃 날짜 선택 시 예약되어있지 않은 행성을 불러오는 필터링기능 구현
    * 페이지네이션, 최신순, 가격순 정렬기능 구현

  * 숙소 Detail API
    * 체크인, 체크아웃 날짜를 선택한 후 행성을 선택하여 숙소 디테일로 들어갈 경우 숙소정보를 불러올 수 있는 기능 구현
    * 날짜를 선택하지 않고 숙소 디테일로 들어갈 경우 숙소정보와 예약가능한 날짜들을 불러올 수 있는 기능 구현

  * 예약 API
    * 예약할 인원 수가 숙소의 기준인원보다 클 경우 요금이 추가되는 기능 구현
    * 예약하고 예약정보를 불러올 수 있으며 예약상태를 변경하고 예약을 삭제할 수 있는 기능 구현
  
  * 위시리스트 API
    * 유저가 행성을 선택하여 위시리스트에 추가할 수 있고 위시리스트를 불러올 수 있는 기능 구현

<br>

---
# API Document

[API Document](https://documenter.getpostman.com/view/19725087/UVsSMigh)

<br>

---
# 시연영상

[starfolio](https://www.youtube.com/watch?v=BfIAwz-oeyc)

<br>

---
# Reference

* 이 프로젝트는 [스테이폴리오](https://www.stayfolio.com/) 사이트를 참조하여 학습목적으로 만들었습니다.
* 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
* 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
* 이 프로젝트에서 사용하고 있는 로고와 배너는 해당 프로젝트 팀원 소유이므로 해당 프로젝트 외부인이 사용할 수 없습니다.

![Footer](https://capsule-render.vercel.app/api?type=waving&color=4c4ca0&height=100&section=footer)
