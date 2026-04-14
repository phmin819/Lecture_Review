<template>
  <div class="container">
    
    <!-- 로고 -->
    <h1 class="logo">📚 명지전문대</h1>
    <p class="subtitle">당신의 완벽한 시간표를 위한 최소한의 강의 기록.</p>

    <!-- 검색 -->
    <input class="search" placeholder="과목명, 교수명, 코드 검색..." />

    <!-- 인기 강의 -->
    <div class="card highlight">
      <h3>🔥 오늘의 인기 강의</h3>
      <p>수강신청 기간, 학생들이 많이 찾은 강의입니다.</p>

      <div class="tags">
        <span>💻 데이터 구조</span>
        <span>🎨 현대미술</span>
      </div>
    </div>

    <!-- 강의 리스트 -->
    <div class="lecture" v-for="lecture in lectures" :key="lecture.id">
      <div>
        <h4>{{ lecture.name }}</h4>
        <p>{{ lecture.prof }}</p>
      </div>
      <span class="rating">⭐ {{ lecture.rating }}</span>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      lectures: [
        { id: 1, name: '데이터 구조 및 알고리즘', prof: '김개발', rating: 4.8 },
        { id: 2, name: '현대미술의 이해', prof: '이예술', rating: 4.5 },
        { id: 3, name: '스타트업 경영론', prof: '박창업', rating: 3.9 }
      ]
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 50px auto;
  font-family: sans-serif;
}

/* 로고 */
.logo {
  font-size: 32px;
}

.subtitle {
  color: gray;
  margin-bottom: 20px;
}

/* 검색 */
.search {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  border: none;
  background: #f3f3f3;
  margin-bottom: 20px;
}

/* 카드 */
.card {
  background: #eef2ff;
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 20px;
}

/* 태그 */
.tags span {
  background: white;
  padding: 5px 10px;
  border-radius: 10px;
  margin-right: 10px;
}

/* 강의 리스트 */
.lecture {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  background: #fafafa;
  border-radius: 10px;
  margin-bottom: 10px;
}

.rating {
  font-weight: bold;
}
</style>