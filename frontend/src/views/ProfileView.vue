<template>
  <div class="profile-wrapper">
    <!-- 배경 장식 -->
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
    </div>

    <div class="profile-container">
      <header class="profile-nav-header">
        <button class="back-link" @click="$router.push('/')">
          <span class="icon">←</span> 메인으로 돌아가기
        </button>
        <h1 class="page-title">마이 페이지</h1>
      </header>

      <main class="profile-content" v-if="profile">
        <!-- 상단 카드: 요약 정보 -->
        <section class="summary-card">
          <div class="user-main">
            <div class="avatar-large">👤</div>
            <div class="text-info">
              <h2>{{ profile.username }}님</h2>
              <p class="email">{{ profile.email }}</p>
              <div class="badge-group">
                <span class="role-badge">{{ profile.isAdmin ? '관리자' : '학생' }}</span>
                <span v-if="profile.grade" class="grade-badge">{{ profile.grade }}학년</span>
              </div>
            </div>
          </div>
          <div class="user-stats">
            <div class="stat-item">
              <span class="stat-num">{{ profile.total_reviews }}</span>
              <span class="stat-label">작성한 후기</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-num">0</span>
              <span class="stat-label">등록한 강의</span>
            </div>
          </div>
        </section>

        <!-- 내 시간표 (준비 중) -->
        <section class="section-card timetable-section">
          <div class="card-header">
            <h3>📅 나의 시간표</h3>
            <button class="manage-btn">설정</button>
          </div>
          <div class="empty-timetable">
            <p>아직 등록된 강의가 없습니다.<br>수강평을 보고 내 시간표에 담아보세요!</p>
          </div>
        </section>

        <!-- 정보 수정 -->
        <section class="section-card edit-section">
          <h3>⚙️ 내 정보 관리</h3>
          <form @submit.prevent="updateProfile" class="profile-form">
            <div class="form-grid">
              <div class="form-group">
                <label>학년</label>
                <select v-model="profile.grade">
                  <option :value="null">미설정</option>
                  <option v-for="n in 4" :key="n" :value="n">{{ n }}학년</option>
                </select>
              </div>
              <div class="form-group">
                <label>성별</label>
                <select v-model="profile.gender">
                  <option value="">미설정</option>
                  <option value="male">남성</option>
                  <option value="female">여성</option>
                  <option value="other">기타</option>
                </select>
              </div>
              <div class="form-group">
                <label>나이</label>
                <input type="number" v-model="profile.age" placeholder="나이 입력" />
              </div>
              <div class="form-group">
                <label>연락처</label>
                <input v-model="profile.phone_number" placeholder="010-0000-0000" />
              </div>
            </div>

            <div class="form-actions">
              <button type="submit" class="save-btn" :disabled="saving">
                {{ saving ? '저장 중...' : '변경사항 저장하기' }}
              </button>
              <button type="button" class="logout-btn" @click="logout">로그아웃</button>
            </div>

            <transition name="fade">
              <p v-if="statusMessage" :class="['status-msg', statusType]">{{ statusMessage }}</p>
            </transition>
          </form>
        </section>
      </main>

      <div v-else-if="loading" class="loading-state">
        <div class="spinner"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      profile: null,
      loading: true,
      saving: false,
      statusMessage: "",
      statusType: "success"
    }
  },
  async created() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      const token = localStorage.getItem("token");
      if (!token) {
        this.$router.push("/login");
        return;
      }
      try {
        const res = await axios.get("http://127.0.0.1:8000/users/me", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.profile = res.data;
      } catch (err) {
        if (err.response?.status === 401) this.logout();
      } finally {
        this.loading = false;
      }
    },
    async updateProfile() {
      const token = localStorage.getItem("token");
      this.saving = true;
      try {
        await axios.put("http://127.0.0.1:8000/users/me", this.profile, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.statusType = "success";
        this.statusMessage = "성공적으로 저장되었습니다.";
        setTimeout(() => this.statusMessage = "", 3000);
      } catch (err) {
        this.statusType = "error";
        this.statusMessage = "저장 중 오류가 발생했습니다.";
      } finally {
        this.saving = false;
      }
    },
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("isAdmin");
      this.$router.push("/login");
    }
  }
}
</script>

<style scoped>
.profile-wrapper {
  min-height: 100vh;
  background-color: #f8fbff;
  font-family: 'Pretendard', sans-serif;
  position: relative;
  overflow-x: hidden;
  padding-bottom: 100px;
}

.bg-decoration { position: fixed; width: 100%; height: 100%; z-index: 0; pointer-events: none; }
.circle { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.3; }
.circle-1 { width: 500px; height: 500px; background: #004ea2; top: -100px; right: -100px; }
.circle-2 { width: 400px; height: 400px; background: #0072bc; bottom: -100px; left: -100px; }

.profile-container { position: relative; z-index: 10; max-width: 650px; margin: 0 auto; padding: 0 20px; }

.profile-nav-header { padding: 40px 0 30px 0; display: flex; justify-content: space-between; align-items: center; }
.back-link { background: none; border: none; color: #718096; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 15px; }
.back-link:hover { color: #004ea2; }
.page-title { font-size: 24px; font-weight: 800; color: #1a202c; margin: 0; }

/* 요약 카드 */
.summary-card {
  background: white;
  border-radius: 28px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0,78,162,0.06);
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 30px;
  border: 1px solid rgba(0,78,162,0.03);
}

.user-main { display: flex; align-items: center; gap: 24px; }
.avatar-large { font-size: 50px; background: #f7fafc; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 40px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05); }
.text-info h2 { font-size: 26px; margin: 0 0 6px 0; color: #1a202c; }
.email { color: #a0aec0; margin: 0 0 14px 0; font-size: 15px; }
.badge-group { display: flex; gap: 8px; }
.role-badge { background: #004ea2; color: white; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 700; }
.grade-badge { background: #eef2ff; color: #004ea2; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 700; }

.user-stats { display: flex; justify-content: space-around; background: #f8fbff; padding: 20px; border-radius: 20px; }
.stat-item { text-align: center; }
.stat-num { display: block; font-size: 22px; font-weight: 800; color: #004ea2; }
.stat-label { font-size: 13px; color: #718096; font-weight: 600; margin-top: 4px; }
.stat-divider { width: 1px; background: #edf2f7; }

/* 공통 섹션 카드 */
.section-card {
  background: white;
  border-radius: 28px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
  margin-bottom: 24px;
  border: 1px solid rgba(0,78,162,0.03);
}
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.card-header h3 { font-size: 18px; font-weight: 700; margin: 0; }
.manage-btn { background: none; border: 1px solid #edf2f7; padding: 6px 12px; border-radius: 10px; font-size: 13px; font-weight: 600; cursor: pointer; color: #718096; }

.empty-timetable { text-align: center; padding: 40px 0; color: #a0aec0; font-size: 14px; line-height: 1.6; border: 2px dashed #f7fafc; border-radius: 20px; }

/* 폼 스타일 */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { font-size: 13px; font-weight: 700; color: #4a5568; margin-left: 4px; }
input, select { background: #f7fafc; border: 2px solid transparent; padding: 14px; border-radius: 14px; font-size: 15px; outline: none; transition: all 0.2s; }
input:focus, select:focus { border-color: #004ea2; background: white; }

.form-actions { display: flex; flex-direction: column; gap: 12px; }
.save-btn { background: #004ea2; color: white; border: none; padding: 16px; border-radius: 16px; font-weight: 700; font-size: 16px; cursor: pointer; transition: all 0.2s; }
.save-btn:hover { background: #003a85; transform: translateY(-2px); }
.logout-btn { background: white; color: #e53e3e; border: 1px solid #fed7d7; padding: 12px; border-radius: 16px; font-weight: 700; cursor: pointer; }

.status-msg { text-align: center; margin-top: 15px; font-size: 14px; padding: 10px; border-radius: 10px; }
.status-msg.success { background: #f0fff4; color: #38a169; }
.status-msg.error { background: #fff5f5; color: #e53e3e; }

.loading-state { text-align: center; padding: 100px 0; }
.spinner { width: 40px; height: 40px; border: 3px solid #edf2f7; border-top-color: #004ea2; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto; }
@keyframes spin { to { transform: rotate(360deg); } }

.fade-enter-active, .fade-leave-active { transition: opacity 0.5s; }
.fade-enter, .fade-leave-to { opacity: 0; }
</style>