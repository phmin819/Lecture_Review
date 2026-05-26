<template>
  <div class="home-wrapper">
    <!-- 배경 장식 (로그인 화면과 일관성 유지) -->
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
    </div>

    <div class="home-container">
      <header class="main-header">
        <div class="logo-area" @click="$router.push('/')">
          <h1 class="logo-text">MJC Lecture</h1>
        </div>
        
        <nav class="nav-actions">
          <div v-if="!isLoggedIn" class="guest-nav">
            <button class="nav-btn primary" @click="$router.push('/login')">로그인</button>
          </div>
          <div v-else class="user-nav">
            <button class="profile-nav-btn" @click="$router.push('/profile')" aria-label="프로필">
              <span class="nav-label">내 정보</span>
            </button>
            <button class="nav-btn logout" @click="logout">로그아웃</button>
          </div>
        </nav>
      </header>

      <main class="content-area">
        <section class="hero-section">
          <h2 class="hero-title">당신의 완벽한 시간표를 위한<br>강의 기록</h2>
          <div class="search-box-wrapper">
            <input
              v-model="searchQuery"
              @input="handleSearch"
              class="main-search-input"
              placeholder="강의명 또는 교수님 성함을 입력하세요"
            />
          </div>
        </section>

        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>강의를 불러오는 중입니다...</p>
        </div>

        <div v-else class="data-sections">
          <!-- 오늘의 인기 강의 -->
          <section class="trending-section">
            <div class="section-header">
              <h3>오늘의 인기 강의</h3>
            </div>
            <div class="trending-grid">
              <div
                v-for="lecture in trendingLectures.slice(0, 2)"
                :key="lecture.lecture_id"
                class="trending-card"
                @click="$router.push(`/lecture/${lecture.lecture_id}`)"
              >
                <div class="trending-info">
                  <span class="dept-label">{{ lecture.department }}</span>
                  <h4>{{ lecture.lecture_name }}</h4>
                  <p>{{ lecture.professor_name }} 교수님</p>
                </div>
                <div class="trending-rating">
                  <span class="rating-label">평점</span>
                  <span class="score">{{ lecture.avg_rating || '0.0' }}</span>
                </div>
              </div>
            </div>
          </section>

          <!-- 전체 강의 목록 -->
          <section class="all-lectures-section">
            <div class="section-header">
              <h3>모든 강의</h3>
              <span class="count-badge">총 {{ lectures.length }}개</span>
            </div>
            <div class="lecture-list">
              <div
                v-for="lecture in lectures"
                :key="lecture.lecture_id"
                class="lecture-item"
                @click="$router.push(`/lecture/${lecture.lecture_id}`)"
              >
                <div class="lecture-main-info">
                  <span class="dept-text">{{ lecture.department }}</span>
                  <h4>{{ lecture.lecture_name }}</h4>
                  <p class="prof-text">{{ lecture.professor_name }} 교수님</p>
                </div>
                <div class="lecture-meta">
                  <div class="rating-badge">
                    {{ lecture.avg_rating > 0 ? '평점 ' + lecture.avg_rating : '평점 없음' }}
                  </div>
                  <div v-if="lecture.class_time" class="time-badge">
                    {{ lecture.class_time }}
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>

      <footer class="main-footer">
        <p>© 2026 MJC Lecture Review. Built for Students.</p>
      </footer>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      lectures: [],
      trendingLectures: [],
      isLoggedIn: false,
      loading: true,
      searchQuery: "",
      searchTimer: null
    }
  },
  async created() {
    this.isLoggedIn = !!localStorage.getItem("token");
    this.fetchLectures();
    this.fetchTrendingLectures();
  },
  methods: {
    async fetchTrendingLectures() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/lectures/trending");
        this.trendingLectures = res.data;
      } catch (err) {
        console.error(err);
      }
    },
    handleSearch() {
      if (this.searchTimer) clearTimeout(this.searchTimer);
      this.searchTimer = setTimeout(() => {
        this.fetchLectures(true);
      }, 300);
    },
    async fetchLectures(isSearch = false) {
      try {
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
      localStorage.removeItem("isAdmin");
      this.isLoggedIn = false;
      alert("정상적으로 로그아웃되었습니다.");
      this.$router.push("/");
    }
  }
}
</script>

<style scoped>
.home-wrapper {
  min-height: 100vh;
  background-color: #f8fbff;
  font-family: 'Pretendard', sans-serif;
  position: relative;
  overflow-x: hidden;
}

/* 배경 장식 */
.bg-decoration {
  position: fixed;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}
.circle { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.3; }
.circle-1 { width: 500px; height: 500px; background: #004ea2; top: -100px; left: -100px; }
.circle-2 { width: 400px; height: 400px; background: #0072bc; bottom: -100px; right: -100px; }

.home-container {
  position: relative;
  z-index: 10;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 헤더 */
.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 0;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}
.logo-icon { font-size: 24px; }
.logo-text { font-size: 22px; font-weight: 800; color: #004ea2; letter-spacing: -0.5px; }

.nav-actions { display: flex; align-items: center; gap: 12px; }
.nav-btn {
  padding: 10px 18px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}
.nav-btn.primary { background: #004ea2; color: white; }
.nav-btn.logout { background: white; color: #718096; border: 1px solid #edf2f7; }
.nav-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.05); }

.user-nav { display: flex; align-items: center; gap: 15px; }
.profile-nav-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  border: 1px solid #edf2f7;
  padding: 8px 14px;
  border-radius: 100px;
  cursor: pointer;
  transition: all 0.2s;
}
.avatar-circle { font-size: 18px; background: #f7fafc; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border-radius: 50%; }
.nav-label { font-weight: 600; font-size: 14px; color: #4a5568; }

/* 히어로 섹션 */
.hero-section {
  text-align: center;
  padding: 60px 0 40px 0;
}
.hero-title {
  font-size: 36px;
  font-weight: 800;
  color: #1a202c;
  line-height: 1.3;
  margin-bottom: 30px;
  letter-spacing: -1px;
}

.search-box-wrapper {
  position: relative;
  max-width: 500px;
  margin: 0 auto;
}
.main-search-input {
  width: 100%;
  padding: 18px 24px 18px 50px;
  border-radius: 20px;
  border: 1px solid rgba(0,78,162,0.1);
  background: white;
  font-size: 16px;
  box-shadow: 0 10px 30px rgba(0,78,162,0.05);
  outline: none;
  transition: all 0.2s;
}
.main-search-input:focus {
  border-color: #004ea2;
  box-shadow: 0 10px 30px rgba(0,78,162,0.1);
}
.search-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
}

/* 데이터 섹션 */
.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
.section-header h3 { font-size: 18px; font-weight: 700; color: #1a202c; }
.count-badge { font-size: 12px; color: #718096; background: #edf2f7; padding: 2px 8px; border-radius: 6px; }

.trending-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 40px;
}
.trending-card {
  background: white;
  padding: 24px;
  border-radius: 24px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.02);
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid rgba(0,78,162,0.03);
}
.trending-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,78,162,0.08); }
.dept-label { font-size: 11px; font-weight: 700; color: #004ea2; background: #eef2ff; padding: 2px 8px; border-radius: 4px; margin-bottom: 10px; display: inline-block; }
.trending-card h4 { font-size: 17px; font-weight: 700; margin: 0 0 4px 0; }
.trending-card p { font-size: 14px; color: #718096; margin: 0; }
.trending-rating { display: flex; align-items: center; gap: 4px; background: #fffaf0; padding: 4px 10px; border-radius: 12px; }
.trending-rating .score { font-weight: 800; color: #dd6b20; font-size: 14px; }

.lecture-list { display: flex; flex-direction: column; gap: 12px; margin-bottom: 60px; }
.lecture-item {
  background: white;
  padding: 20px;
  border-radius: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid rgba(0,78,162,0.03);
}
.lecture-item:hover { transform: scale(1.01); background: #fcfdfe; border-color: rgba(0,78,162,0.1); }
.dept-text { font-size: 12px; color: #a0aec0; margin-bottom: 4px; display: block; }
.lecture-item h4 { font-size: 16px; margin: 0 0 2px 0; font-weight: 700; }
.prof-text { font-size: 14px; color: #718096; margin: 0; }

.lecture-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }
.rating-badge { font-weight: 700; color: #1a202c; font-size: 14px; }
.time-badge { font-size: 11px; color: #718096; background: #f7fafc; padding: 2px 8px; border-radius: 4px; }

/* 상태 */
.loading-state { text-align: center; padding: 100px 0; color: #718096; }
.spinner { width: 40px; height: 40px; border: 3px solid #edf2f7; border-top-color: #004ea2; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px auto; }

.main-footer { text-align: center; padding: 40px 0; color: #a0aec0; font-size: 13px; }

@keyframes spin { to { transform: rotate(360deg); } }
</style>