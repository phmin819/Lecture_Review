<template>
  <div class="container">
    <header class="header">
      <button v-if="!isLoggedIn" class="auth-btn" @click="$router.push('/login')">로그인</button>
      <button v-else class="auth-btn logout" @click="logout">로그아웃</button>
    </header>
    
    <h1 class="logo"> 명지전문대 강의 후기</h1>
    <p class="subtitle">당신의 완벽한 시간표를 위한 최소한의 강의 기록.</p>

    <input class="search" placeholder="과목명, 교수명, 코드 검색..." />

    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">강의 정보를 불러오고 있습니다...</p>
    </div>

    <div v-else>
      <div class="card highlight">
        <h3> 오늘의 인기 강의</h3>
        <p>수강신청 기간, 학생들이 많이 찾은 강의입니다.</p>
        <div class="tags">
          <span v-for="lecture in lectures.slice(0,2)" :key="lecture.lecture_id">
            {{ lecture.lecture_name }}
          </span>
        </div>
      </div>

      <div 
        class="lecture" 
        v-for="lecture in lectures" 
        :key="lecture.lecture_id"
        @click="$router.push(`/lecture/${lecture.lecture_id}`)"
        style="cursor: pointer;"
      >
        <div>
          <h4>{{ lecture.lecture_name }}</h4>
          <p>{{ lecture.professor_name }}</p>
        </div>
        <span class="rating">
          ⭐ {{ lecture.avg_rating > 0 ? lecture.avg_rating : '평점 없음' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      lectures: [],
      isLoggedIn: false,
      loading: true // 로딩 상태값 추가
    }
  },
  async created() {
    this.isLoggedIn = !!localStorage.getItem("token");
    this.fetchLectures();
  },
  methods: {
    async fetchLectures() {
      try {
        this.loading = true; // 로딩 시작
        const res = await axios.get("http://127.0.0.1:8000/lectures");
        this.lectures = res.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false; // 성공하든 실패하든 로딩 종료
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.isLoggedIn = false;
      alert("로그아웃 되었습니다.");
      this.$router.push("/");
    }
  }
}
</script>

<style scoped>
/* 기존 스타일 */
.container { max-width: 600px; margin: 20px auto 50px auto; font-family: sans-serif; }
.header { display: flex; justify-content: flex-start; margin-bottom: 20px; }
.auth-btn { background: #667eea; color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: bold; }
.auth-btn.logout { background: #ff4d4d; }
.logo { font-size: 32px; margin-top: 10px; }
.subtitle { color: gray; margin-bottom: 20px; }
.search { width: 100%; padding: 12px; border-radius: 10px; border: none; background: #f3f3f3; margin-bottom: 20px; box-sizing: border-box; }
.card { background: #eef2ff; padding: 20px; border-radius: 15px; margin-bottom: 20px; }
.tags span { background: white; padding: 5px 10px; border-radius: 10px; margin-right: 10px; font-size: 14px; }
.lecture { display: flex; justify-content: space-between; align-items: center; padding: 15px; background: #fafafa; border-radius: 10px; margin-bottom: 10px; border: 1px solid #eee; transition: 0.2s; }
.lecture:hover { background: #f0f0f0; transform: translateY(-2px); }
.lecture h4 { margin: 0 0 5px 0; }
.lecture p { margin: 0; font-size: 14px; color: #666; }
.rating { font-weight: bold; color: #333; }

/* 로딩 애니메이션 스타일 추가 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 100px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #667eea; /* 로고 색상 계열인 파란색 사용 */
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 15px;
  color: #667eea;
  font-weight: 500;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>