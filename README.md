# 요척 누락 방지 프로그램 - 개선 버전

개선 내용:
- 글자와 입력칸 크기 확대
- 패턴 개수는 별도 창 없이 표 안에서 바로 입력
- 비고도 표 안에서 바로 수정
- 패턴 확인 / 요척 입력 확인은 표에서 클릭으로 바로 체크
- 상의 / 하의 탭으로 구분하여 해당 항목만 표시
- 항목별 패턴 개수 합계를 화면 하단에 항상 표시
- 패턴 개수를 수정하면 합계가 즉시 업데이트
- GitHub Actions로 Windows EXE 자동 생성

GitHub에 `요척_누락방지_프로그램.py`와 `.github/workflows/build.yml`을 올린 뒤
Actions → Build Windows EXE → Run workflow를 실행하면 됩니다.
