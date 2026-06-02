<template>
  <div class="home-wrapper">
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
    </div>

    <div class="container">
      <header class="header">
        <div v-if="!isLoggedIn" class="auth-buttons">
          <button class="auth-btn" @click="$router.push('/login')">로그인</button>
        </div>
        <div v-else class="user-nav">
          <button class="profile-nav-btn" @click="$router.push('/profile')" aria-label="프로필로 이동">
            <span class="avatar-sm">👤</span>
            <span class="nav-text">내 프로필</span>
          </button>
          <button class="auth-btn logout" @click="logout">로그아웃</button>
        </div>
      </header>

      <div class="brand-section">
        <h1 class="logo">명지전문대 강의 후기</h1>
        <p class="subtitle">당신의 완벽한 시간표를 위한 최소한의 강의 기록.</p>
      </div>

      <form class="search-form" @submit.prevent>
        <label for="search" class="visually-hidden">강의 검색</label>
        <div class="search-wrapper">
          <span class="search-icon">🔍</span>
          <input
            id="search"
            v-model="searchQuery"
            class="search-input"
            placeholder="과목명, 교수명 검색..."
            aria-label="강의 검색"
          />
        </div>
      </form>

      <div v-if="loading" class="loading-container" role="status">
        <div class="spinner"></div>
        <p class="loading-text">강의 정보를 불러오고 있습니다...</p>
      </div>

      <div v-else>
        <!-- 검색 모드 -->
        <template v-if="searchQuery">
          <p class="result-label">검색 결과 {{ lectures.length }}건</p>
          <div class="lecture-list">
            <button
              v-for="lecture in lectures"
              :key="lecture.lecture_id"
              type="button"
              class="lecture-card"
              @click="$router.push(`/lecture/${lecture.lecture_id}`)"
            >
              <div class="lecture-info">
                <h3>{{ lecture.lecture_name }}</h3>
                <p class="professor">{{ lecture.professor_name }} 교수님</p>
                <p class="dept">{{ lecture.category }} · {{ lecture.department }}</p>
              </div>
              <div class="lecture-stats">
                <span class="rating-badge">⭐ {{ lecture.avg_rating > 0 ? lecture.avg_rating.toFixed(1) : '0.0' }}</span>
              </div>
            </button>
          </div>
        </template>

        <!-- 탐색 모드 -->
        <template v-else>
          <!-- 브레드크럼 -->
          <nav v-if="selectedFaculty" class="breadcrumb" aria-label="현재 위치">
            <button class="crumb-btn" @click="goToFacultyList">전체 학부</button>
            <span class="crumb-sep">›</span>
            <button v-if="selectedDepartment" class="crumb-btn" @click="goToDepartmentList">{{ selectedFaculty.faculty }}</button>
            <span v-else class="crumb-current">{{ selectedFaculty.faculty }}</span>
            <template v-if="selectedDepartment">
              <span class="crumb-sep">›</span>
              <span class="crumb-current">{{ selectedDepartment }}</span>
            </template>
          </nav>

          <!-- 학부 선택 전: 인기 강의 + 학부 목록 -->
          <template v-if="!selectedFaculty">
            <div class="card highlight-card">
              <div class="card-header">
                <h2>🔥 오늘의 인기 강의</h2>
                <p>학생들이 가장 많이 찾은 강의입니다.</p>
              </div>
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

            <h2 class="section-title">학부별 강의</h2>
            <div class="faculty-grid">
              <button
                v-for="f in faculties"
                :key="f.faculty"
                type="button"
                class="faculty-card"
                @click="selectFaculty(f)"
              >
                <span class="faculty-name">{{ f.faculty }}</span>
                <span class="dept-count">{{ f.departments.length }}개 학과</span>
              </button>
            </div>
          </template>

          <!-- 학부 선택 후, 학과 선택 전: 학과 목록 -->
          <template v-else-if="!selectedDepartment">
            <div class="dept-grid">
              <button
                v-for="dept in selectedFaculty.departments"
                :key="dept"
                type="button"
                class="dept-card"
                @click="selectDepartment(dept)"
              >
                {{ dept }}
              </button>
            </div>
          </template>

          <!-- 학과 선택 후: 강의 목록 -->
          <template v-else>
            <div v-if="lecturesLoading" class="loading-container">
              <div class="spinner"></div>
            </div>
            <div v-else class="lecture-list">
              <p v-if="lectures.length === 0" class="empty-text">등록된 강의가 없습니다.</p>
              <button
                v-for="lecture in lectures"
                :key="lecture.lecture_id"
                type="button"
                class="lecture-card"
                @click="$router.push(`/lecture/${lecture.lecture_id}`)"
              >
                <div class="lecture-info">
                  <h3>{{ lecture.lecture_name }}</h3>
                  <p class="professor">{{ lecture.professor_name }} 교수님</p>
                  <p class="dept">{{ lecture.department }}</p>
                </div>
                <div class="lecture-stats">
                  <span class="rating-badge">⭐ {{ lecture.avg_rating > 0 ? lecture.avg_rating.toFixed(1) : '0.0' }}</span>
                </div>
              </button>
            </div>
          </template>
        </template>
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
      trendingLectures: [],
      faculties: [],
      selectedFaculty: null,
      selectedDepartment: null,
      isLoggedIn: false,
      loading: true,
      lecturesLoading: false,
      searchQuery: "",
      searchTimer: null
    }
  },
  async created() {
    this.isLoggedIn = !!localStorage.getItem("token");
    await Promise.all([this.fetchFaculties(), this.fetchTrendingLectures()]);
    this.loading = false;
  },
  watch: {
    searchQuery(val) {
      if (this.searchTimer) clearTimeout(this.searchTimer);
      if (!val) {
        this.lectures = [];
        if (this.selectedDepartment) {
          this.selectDepartment(this.selectedDepartment);
        }
        return;
      }
      this.searchTimer = setTimeout(() => this.fetchLectures(), 300);
    }
  },
  methods: {
    async fetchFaculties() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/lectures/faculties");
        this.faculties = res.data;
      } catch (err) {
        console.error("학부 목록 로드 실패", err);
      }
    },
    async fetchTrendingLectures() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/lectures/trending");
        this.trendingLectures = res.data;
      } catch (err) {
        console.error("인기 강의 로드 실패", err);
      }
    },
    async fetchLectures() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/lectures", {
          params: { search: this.searchQuery }
        });
        this.lectures = res.data;
      } catch (err) {
        console.error(err);
      }
    },
    async selectDepartment(dept) {
      this.selectedDepartment = dept;
      this.lecturesLoading = true;
      try {
        const res = await axios.get("http://127.0.0.1:8000/lectures", {
          params: { department: dept }
        });
        this.lectures = res.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.lecturesLoading = false;
      }
    },
    selectFaculty(faculty) {
      this.selectedFaculty = faculty;
      this.selectedDepartment = null;
      this.lectures = [];
    },
    goToFacultyList() {
      this.selectedFaculty = null;
      this.selectedDepartment = null;
      this.lectures = [];
    },
    goToDepartmentList() {
      this.selectedDepartment = null;
      this.lectures = [];
    },
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("isAdmin");
      this.isLoggedIn = false;
      alert("로그아웃 되었습니다.");
      this.$router.push("/");
    }
  }
}
</script>

<style scoped>
.home-wrapper { min-height: 100vh; background-color: #f8fbff; font-family: 'Pretendard', sans-serif; position: relative; overflow-x: hidden; padding-bottom: 80px; }
.bg-decoration { position: fixed; width: 100%; height: 100%; z-index: 0; pointer-events: none; }
.circle { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.3; }
.circle-1 { width: 500px; height: 500px; background: #004ea2; top: -100px; right: -100px; }
.circle-2 { width: 400px; height: 400px; background: #0072bc; bottom: -100px; left: -100px; }
.container { position: relative; z-index: 10; max-width: 600px; margin: 0 auto; padding: 0 20px; }
.header { display: flex; justify-content: flex-end; padding: 20px 0; margin-bottom: 20px; }
.user-nav { display: flex; align-items: center; gap: 12px; }
.profile-nav-btn { background: white; border: 1px solid #edf2f7; padding: 8px 16px; border-radius: 12px; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
.profile-nav-btn:hover { background: #f7fafc; transform: translateY(-1px); }
.avatar-sm { font-size: 18px; }
.nav-text { font-size: 14px; font-weight: 700; color: #4a5568; }
.auth-btn { background: #004ea2; color: white; border: none; padding: 10px 20px; border-radius: 12px; cursor: pointer; font-weight: 700; transition: 0.2s; }
.auth-btn:hover { background: #003a85; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,78,162,0.2); }
.auth-btn.logout { background: white; color: #e53e3e; border: 1px solid #fed7d7; }
.auth-btn.logout:hover { background: #fff5f5; box-shadow: none; }
.brand-section { margin-bottom: 30px; }
.logo { font-size: 34px; font-weight: 800; color: #004ea2; margin: 0 0 8px 0; letter-spacing: -1px; }
.subtitle { color: #718096; font-size: 16px; font-weight: 500; }
.search-wrapper { position: relative; display: flex; align-items: center; }
.search-icon { position: absolute; left: 16px; color: #a0aec0; font-size: 18px; }
.search-input { width: 100%; padding: 16px 16px 16px 48px; border-radius: 18px; border: 2px solid transparent; background: white; margin-bottom: 24px; box-sizing: border-box; font-size: 16px; outline: none; transition: 0.2s; box-shadow: 0 4px 15px rgba(0,78,162,0.05); }
.search-input:focus { border-color: #004ea2; box-shadow: 0 0 0 4px rgba(0,78,162,0.1); }
.card { background: white; border-radius: 28px; padding: 24px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,78,162,0.06); border: 1px solid rgba(0,78,162,0.03); }
.highlight-card { background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 100%); }
.card-header h2 { font-size: 20px; font-weight: 800; color: #1a202c; margin: 0 0 4px 0; }
.card-header p { font-size: 14px; color: #718096; margin: 0; }
.tags { display: flex; gap: 12px; margin-top: 20px; }
.trending-item { background: white; padding: 12px 18px; border-radius: 16px; border: 1px solid #edf2f7; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.trending-item:hover { transform: translateY(-3px); box-shadow: 0 6px 15px rgba(0,78,162,0.1); border-color: #004ea2; }
.trending-item .name { font-weight: 700; font-size: 14px; color: #2d3748; }
.trending-item .rating { font-size: 13px; color: #004ea2; font-weight: 800; }
.section-title { font-size: 20px; font-weight: 800; color: #1a202c; margin: 0 0 16px 0; }
.faculty-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 24px; }
.faculty-card { background: white; border-radius: 20px; padding: 20px; border: 1px solid rgba(0,78,162,0.06); cursor: pointer; text-align: left; transition: 0.2s; box-shadow: 0 4px 12px rgba(0,0,0,0.03); display: flex; flex-direction: column; gap: 8px; }
.faculty-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,78,162,0.1); border-color: rgba(0,78,162,0.2); }
.faculty-name { font-size: 15px; font-weight: 800; color: #1a202c; line-height: 1.4; }
.dept-count { font-size: 12px; color: #a0aec0; font-weight: 600; }
.breadcrumb { display: flex; align-items: center; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.crumb-btn { background: none; border: none; color: #004ea2; font-size: 14px; font-weight: 700; cursor: pointer; padding: 0; text-decoration: underline; }
.crumb-btn:hover { color: #003a85; }
.crumb-sep { color: #a0aec0; font-size: 14px; }
.crumb-current { font-size: 14px; font-weight: 700; color: #1a202c; }
.dept-grid { display: flex; flex-direction: column; gap: 10px; }
.dept-card { background: white; border-radius: 16px; padding: 16px 20px; border: 1px solid rgba(0,78,162,0.06); cursor: pointer; text-align: left; font-size: 15px; font-weight: 700; color: #2d3748; transition: 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
.dept-card:hover { transform: translateX(4px); border-color: rgba(0,78,162,0.2); color: #004ea2; }
.result-label { font-size: 14px; font-weight: 600; color: #718096; margin-bottom: 16px; }
.lecture-list { display: flex; flex-direction: column; gap: 16px; }
.lecture-card { display: flex; justify-content: space-between; align-items: center; padding: 24px; background: white; border-radius: 24px; border: 1px solid rgba(0,78,162,0.03); transition: 0.2s; width: 100%; text-align: left; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }
.lecture-card:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,78,162,0.08); border-color: rgba(0,78,162,0.2); }
.lecture-info h3 { margin: 0 0 6px 0; font-size: 18px; font-weight: 800; color: #1a202c; }
.professor { margin: 0 0 4px 0; font-size: 14px; color: #4a5568; font-weight: 600; }
.dept { margin: 0; font-size: 12px; color: #a0aec0; font-weight: 500; }
.rating-badge { background: #eef2ff; color: #004ea2; padding: 6px 12px; border-radius: 10px; font-weight: 800; font-size: 14px; white-space: nowrap; }
.loading-container { display: flex; flex-direction: column; align-items: center; margin-top: 60px; }
.spinner { width: 40px; height: 40px; border: 4px solid #edf2f7; border-top: 4px solid #004ea2; border-radius: 50%; animation: spin 1s linear infinite; }
.loading-text { margin-top: 16px; color: #004ea2; font-weight: 700; }
.empty-text { text-align: center; color: #a0aec0; font-weight: 600; padding: 40px 0; }
.visually-hidden { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0 0 0 0); border: 0; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
