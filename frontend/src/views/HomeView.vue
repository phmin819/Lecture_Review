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
        <span v-for="lecture in lectures.slice(0,2)" :key="lecture.lecture_id">
          {{ lecture.lecture_name }}
        </span>
      </div>
    </div>

    <!-- 강의 리스트 -->
    <div 
      class="lecture" 
      v-for="lecture in lectures" 
      :key="lecture.lecture_id"
    >
      <div>
        <h4>{{ lecture.lecture_name }}</h4>
        <p>{{ lecture.professor_name }}</p>
      </div>
      <span class="rating">⭐ 4.5</span>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      lectures: [] // 🔥 서버 데이터로 채움
    }
  },

  async created() {
    try {
      const res = await axios.get("http://127.0.0.1:8000/lectures");
      console.log(res.data);
      this.lectures = res.data;
    } catch (err) {
      console.error(err);
      alert("강의 데이터를 불러오지 못했습니다");
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