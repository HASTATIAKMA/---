# 요척 누락 방지 프로그램 - GitHub EXE 빌드

이 패키지는 사용자 PC에 Python을 설치하지 않고 GitHub Actions의 Windows 서버에서 EXE를 만드는 방식입니다.

1. GitHub에 새 Repository를 만듭니다.
2. 이 ZIP의 압축을 풉니다.
3. `요척_누락방지_프로그램.py`와 `.github/workflows/build.yml`을 Repository에 업로드합니다.
4. GitHub의 Actions 탭에서 `Build Windows EXE`를 선택합니다.
5. `Run workflow`를 누릅니다.
6. 빌드가 완료되면 해당 실행 화면의 Artifacts에서 `요척_누락방지_프로그램-Windows`를 다운로드합니다.
7. 압축을 풀고 `요척_누락방지_프로그램.exe`를 실행합니다.

완성된 EXE를 실행할 때는 Python이 필요 없습니다.
