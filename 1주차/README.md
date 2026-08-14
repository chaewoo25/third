# 코디세이 1주차 과제: 개발 환경 구축 및 Docker 웹 서버 실습 보고서

## 📌 1. 과제 개요 (Overview)
본 과제는 최신 컨테이너 가상화 기술인 Docker를 활용하여 개발 환경을 구축하고, Nginx 웹 서버 컨테이너 구동, 커스텀 이미지 빌드, 데이터 영속성 관리를 포함한 기본 실습을 목표로 합니다. WSL 2 기반 가상화 환경에서 Docker Engine 및 VSCode를 연동하고, 리눅스 기초 CLI 명령어와 핵심 Docker 명령어를 통해 컨테이너 생태계의 동작 메커니즘을 분석 및 기록하였습니다.

- **교육 과정**: 코디세이 AI All-in-One 2기
- **작성자**: 박채우
- **GitHub 계정**: chaewoo25
- **저장소 주소**: [https://github.com/chaewoo25/first](https://github.com/chaewoo25/first)

---

## 💻 2. 개발 및 실습 환경 (Environment)

| 구분 | 환경 명세 |
| :--- | :--- |
| **Host OS** | Windows 11 Home |
| **Virtualization** | WSL 2 (Windows Subsystem for Linux) |
| **Container Engine** | Docker Desktop 4.85.0 |
| **IDE / Editor** | Visual Studio Code |
| **CLI Terminal** | PowerShell / Windows Terminal |
| **Version Control** | Git / GitHub |

---

## 📁 3. 리눅스 기본 CLI 명령어 및 파일 권한 실습

### 3.1 디렉토리 및 파일 생성/이동/삭제
```bash
# 1. 작업 디렉토리 생성 및 이동
mkdir -p ~/workspace/test_dir && cd ~/workspace/test_dir

# 2. 테스트 파일 생성
touch sample.txt

# 3. 파일 이동 및 이름 변경
mv sample.txt test_file.txt

# 4. 파일 및 디렉토리 삭제
cd .. && rm -rf test_dir

3.2 파일 권한 변경 (chmod) 검증
# 1. 파일 생성 및 기본 권한 확인
touch permission_test.sh
ls -l permission_test.sh
# 출력: -rw-r--r-- 1 user user 0 permission_test.sh

# 2. 실행 권한 부여 (755 설정)
chmod 755 permission_test.sh
ls -l permission_test.sh
# 출력: -rwxr-xr-x 1 user user 0 permission_test.sh
```
🚀 4. Docker Engine 및 Hello-World 실행 검증
```bash
4.1 docker --version 출력
docker --version
# 출력: Docker version 29.6.2, build dfc4efb
4.2 docker run hello-world 정상 실행
docker run hello-world
```
🌐 5. Nginx 웹 서버 컨테이너 구동 및 포트 매핑
```bash
5.1 컨테이너 실행 명령어 (포트 매핑)
docker run -d -p 80:80 --name my-web-server nginx
```
🛠️ 6. Dockerfile 작성 및 커스텀 이미지 빌드
6.1 Dockerfile 작성
```bash
# Base 이미지 설정
FROM nginx:alpine

# 커스텀 index.html 복사
COPY index.html /usr/share/nginx/html/index.html

# 80번 포트 노출
EXPOSE 80
```
6.2 이미지 빌드 및 매핑 포트 접속
```bash
# 1. 커스텀 이미지 빌드
docker build -t my-custom-nginx:1.0 .

# 2. 빌드된 커스텀 이미지 구동 (포트 8080 매핑)
docker run -d -p 8080:80 --name custom-web my-custom-nginx:1.0
```
💾 7. Docker Volume을 활용한 데이터 영속성 유지 검증
```bash
# 1. 호스트 OS 및 컨테이너 간 볼륨 마운트 실행 (-v 옵션)
docker run -d -p 8081:80 -v ~/nginx_data:/usr/share/nginx/html --name vol-test nginx

# 2. 호스트 마운트 폴더에 테스트 파일 생성
echo "Volume Data Test" > ~/nginx_data/test.html

# 3. 컨테이너 강제 삭제
docker rm -f vol-test

# 4. 데이터 영속성 검증 (컨테이너 삭제 후에도 호스트 폴더 파일 보존 확인)
cat ~/nginx_data/test.html
# 출력 결과: Volume Data Test
```
🧹 8. 이미지 및 컨테이너 목록 확인 및 자원 정리
```bash
8.1 목록 확인 (ps -a, images)

# 실행 중 및 정지된 전체 컨테이너 목록 확인
docker ps -a

# 다운로드 및 빌드된 전체 이미지 목록 확인
docker images

8.2 자원 정리 (rm, rmi)

# 1. 컨테이너 정지 및 삭제
docker stop my-web-server custom-web
docker rm my-web-server custom-web

# 2. 미사용 이미지 삭제
docker rmi my-custom-nginx:1.0 hello-world
```
🐙 9. Git 설정 및 GitHub 연동
```bash
# 1. Git 사용자 환경 설정
git config --global user.name "chaewoo25"

# 2. 원격 저장소(first) 연결 및 최종 푸시
git remote set-url origin https://github.com/chaewoo25/first.git
git add .
git commit -m "docs: 1주차 과제 보고서 9가지 항목 완벽 정리"
git push origin main --force
```