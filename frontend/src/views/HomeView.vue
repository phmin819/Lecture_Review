<template>
  <div class="container">
    <header class="header">
      <button v-if="!isLoggedIn" class="auth-btn" @click="$router.push('/login')">로그인</button>
      <button v-else class="auth-btn logout" @click="logout">로그아웃</button>
    </header>
    
    <h1 class="logo">명지전문대 강의 후기</h1>
    <p class="subtitle">당신의 완벽한 시간표를 위한 최소한의 강의 기록.</p>

    <form class="search-form" @submit.prevent>
      <label for="search" class="visually-hidden">강의 검색</label>
      <input
        id="search"
        v-model="searchQuery"
        @input="handleSearch"
        class="search"
        placeholder="과목명, 교수명 검색..."
        aria-label="강의 검색"
      />
    </form>

    <div v-if="loading" class="loading-container" role="status" aria-live="polite">
      <div class="spinner" aria-hidden="true"></div>
      <p class="loading-text">강의 정보를 불러오고 있습니다...</p>
    </div>

    <div v-else>
      <div class="card highlight">
        <h2>오늘의 인기 강의</h2>
        <p>수강신청 기간, 학생들이 많이 찾은 강의입니다.</p>
        <div class="tags">
          <button
            v-for="lecture in trendingLectures.slice(0, 2)"
            :key="lecture.lecture_id"
            type="button"
            class="trending-item"
            @click="$router.push(`/lecture/${lecture.lecture_id}`)"
          >
            <span class="name">{{ lecture.lecture_name }}</span>
            <span class="rating">⭐ {{ lecture.avg_rating || '0.0' }}</span>
          </button>
        </div>
      </div>

      <div class="lecture-list">
        <button
          v-for="lecture in lectures"
          :key="lecture.lecture_id"
          type="button"
          class="lecture"
          @click="$router.push(`/lecture/${lecture.lecture_id}`)"
        >
          <div>
            <h3>{{ lecture.lecture_name }}</h3>
            <p>{{ lecture.professor_name }}</p>
          </div>
          <span class="rating">
            ⭐ {{ lecture.avg_rating > 0 ? lecture.avg_rating : '평점 없음' }}
          </span>
        </button>
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
      trendingLectures: [], // 인기 강의 데이터 분리
      isLoggedIn: false,
      loading: true,
      searchQuery: "",
      searchTimer: null // 디바운스용 타이머
    }
  },
  async created() {
    this.isLoggedIn = !!localStorage.getItem("token");
    this.fetchLectures();
    this.fetchTrendingLectures(); // 초기 로드 시 인기 강의 가져오기
  },
  methods: {
    // 인기 강의(평점순) 가져오기
    async fetchTrendingLectures() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/lectures/trending");
        this.trendingLectures = res.data;
      } catch (err) {
        console.error("인기 강의 로드 실패", err);
      }
    },
    // 검색 입력 핸들러 (0.3초 대기 후 검색)
    handleSearch() {
      if (this.searchTimer) clearTimeout(this.searchTimer);
      this.searchTimer = setTimeout(() => {
        this.fetchLectures(true);
      }, 300);
    },
    async fetchLectures(isSearch = false) {
      try {
        // 검색 시에는 로딩 스피너를 띄우지 않아 깜빡임 방지
        if (!isSearch) this.loading = true;
        
        const res = await axios.get("http://127.0.0.1:8000/lectures", {
          params: { search: this.searchQuery }
        });
        this.lectures = res.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
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
.tags { display: flex; gap: 10px; margin-top: 15px; }
.trending-item { background: white; padding: 10px 15px; border-radius: 12px; border: 1px solid #dee2e6; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
.trending-item:hover { transform: translateY(-3px); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
.trending-item .name { font-weight: bold; font-size: 14px; color: #333; }
.trending-item .rating { font-size: 13px; color: #ff9f43; font-weight: bold; }
.lecture { display: flex; justify-content: space-between; align-items: center; padding: 15px; background: #fafafa; border-radius: 10px; margin-bottom: 10px; border: 1px solid #eee; transition: 0.2s; width: 100%; text-align: left; }
.lecture:hover,
.lecture:focus-visible { background: #f0f0f0; transform: translateY(-2px); outline: none; }
.lecture:focus-visible { box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3); }
.lecture h3 { margin: 0 0 5px 0; }
.lecture p { margin: 0; font-size: 14px; color: #666; }
.rating { font-weight: bold; color: #333; }

.visually-hidden { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0 0 0 0); border: 0; }

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