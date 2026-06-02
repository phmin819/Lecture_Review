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

        <!-- 내 시간표 -->
        <section class="section-card timetable-section">
          <TimetableGrid />
        </section>

        <!-- 친구 검색 -->
        <section class="section-card">
          <div class="card-header">
            <h3>🔍 친구 추가</h3>
          </div>
          <div class="search-row">
            <input
              v-model="friendQuery"
              class="friend-input"
              type="text"
              placeholder="username으로 검색..."
              @keydown.enter="searchFriends"
            />
            <button class="search-btn" @click="searchFriends">검색</button>
          </div>
          <div v-if="searchResults.length" class="search-results">
            <div v-for="u in searchResults" :key="u.user_id" class="search-result-item">
              <div class="fr-avatar">👤</div>
              <div class="fr-info">
                <span class="fr-name">{{ u.username }}</span>
                <span class="fr-meta">{{ u.grade ? u.grade + '학년' : '' }}</span>
              </div>
              <button
                v-if="u.friendship_status === 'none'"
                class="fr-btn"
                @click="sendRequest(u.username, u.user_id)"
              >요청 보내기</button>
              <span v-else-if="u.friendship_status === 'sent'" class="fr-btn sent">요청됨</span>
              <span v-else-if="u.friendship_status === 'friends'" class="fr-btn friends">친구</span>
              <span v-else-if="u.friendship_status === 'received'" class="fr-btn received">받은 요청</span>
            </div>
          </div>
          <p v-else-if="searched" class="empty-msg">검색 결과가 없어요</p>
        </section>

        <!-- 받은 친구 요청 -->
        <section class="section-card" v-if="receivedRequests.length">
          <div class="card-header">
            <h3>📬 받은 친구 요청</h3>
            <span class="req-count-badge">{{ receivedRequests.length }}</span>
          </div>
          <div v-for="req in receivedRequests" :key="req.friendship_id" class="request-item">
            <div class="fr-avatar">👤</div>
            <div class="fr-info">
              <span class="fr-name">{{ req.username }}</span>
              <span class="fr-meta">{{ req.grade ? req.grade + '학년' : '' }}</span>
            </div>
            <div class="req-actions">
              <button class="btn-accept" @click="acceptRequest(req.friendship_id)">수락</button>
              <button class="btn-reject" @click="declineRequest(req.friendship_id)">거절</button>
            </div>
          </div>
        </section>

        <!-- 친구 목록 -->
        <section class="section-card">
          <div class="card-header">
            <h3>👥 내 친구 <span class="friend-count">{{ friends.length }}명</span></h3>
          </div>
          <div v-if="friends.length" class="friend-grid">
            <div
              v-for="f in friends"
              :key="f.user_id"
              class="friend-card"
              @click="$router.push(`/friends/${f.user_id}`)"
            >
              <div class="fc-avatar">👤</div>
              <div class="fc-name">{{ f.username }}</div>
              <div class="fc-grade">{{ f.grade ? f.grade + '학년' : '' }}</div>
            </div>
          </div>
          <div v-else class="empty-friends">
            <p>아직 친구가 없어요.<br>위에서 username으로 검색해 친구를 추가해보세요!</p>
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
import TimetableGrid from "@/components/TimetableGrid.vue";

export default {
  components: { TimetableGrid },
  data() {
    return {
      profile: null,
      loading: true,
      saving: false,
      statusMessage: "",
      statusType: "success",
      // 친구
      friendQuery: "",
      searchResults: [],
      searched: false,
      receivedRequests: [],
      friends: [],
    }
  },
  async created() {
    this.fetchProfile();
    this.fetchFriends();
    this.fetchReceivedRequests();
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
    },

    // ── 친구 ────────────────────────────────────────────
    async fetchFriends() {
      const token = localStorage.getItem("token");
      if (!token) return;
      try {
        const res = await axios.get("http://127.0.0.1:8000/friends/me", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.friends = res.data;
      } catch {}
    },
    async fetchReceivedRequests() {
      const token = localStorage.getItem("token");
      if (!token) return;
      try {
        const res = await axios.get("http://127.0.0.1:8000/friends/requests", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.receivedRequests = res.data;
      } catch {}
    },
    async searchFriends() {
      if (!this.friendQuery.trim()) return;
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(`http://127.0.0.1:8000/friends/search?q=${encodeURIComponent(this.friendQuery)}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.searchResults = res.data;
        this.searched = true;
      } catch {}
    },
    async sendRequest(username, userId) {
      const token = localStorage.getItem("token");
      try {
        await axios.post("http://127.0.0.1:8000/friends/request",
          { username },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        const u = this.searchResults.find(r => r.user_id === userId);
        if (u) u.friendship_status = "sent";
      } catch {}
    },
    async acceptRequest(friendshipId) {
      const token = localStorage.getItem("token");
      try {
        await axios.put(`http://127.0.0.1:8000/friends/request/${friendshipId}/accept`, {},
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.receivedRequests = this.receivedRequests.filter(r => r.friendship_id !== friendshipId);
        await this.fetchFriends();
      } catch {}
    },
    async declineRequest(friendshipId) {
      const token = localStorage.getItem("token");
      try {
        await axios.delete(`http://127.0.0.1:8000/friends/request/${friendshipId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.receivedRequests = this.receivedRequests.filter(r => r.friendship_id !== friendshipId);
      } catch {}
    },
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

/* ── 친구 공통 ── */
.search-row { display: flex; gap: 8px; }
.friend-input {
  flex: 1; background: #f7fafc; border: 2px solid transparent;
  border-radius: 14px; padding: 12px 16px; font-size: 15px; outline: none; transition: all 0.2s;
}
.friend-input:focus { border-color: #004ea2; background: white; }
.search-btn {
  background: #004ea2; color: white; border: none;
  padding: 12px 20px; border-radius: 14px; font-size: 14px; font-weight: 700; cursor: pointer; transition: background 0.2s;
}
.search-btn:hover { background: #003a85; }

.search-results { margin-top: 12px; display: flex; flex-direction: column; gap: 8px; }
.search-result-item, .request-item {
  display: flex; align-items: center; gap: 12px;
  background: #f8fbff; border-radius: 14px; padding: 12px 14px;
  border: 1px solid #edf2f7;
}
.request-item { background: white; border-bottom: 1px solid #f7fafc; border-radius: 0; padding: 12px 0; }
.request-item:last-child { border-bottom: none; }

.fr-avatar { width: 38px; height: 38px; border-radius: 14px; background: #eef2ff; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
.fr-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.fr-name { font-size: 14px; font-weight: 700; color: #1a202c; }
.fr-meta { font-size: 12px; color: #a0aec0; }

.fr-btn { background: #004ea2; color: white; border: none; padding: 7px 14px; border-radius: 10px; font-size: 12px; font-weight: 700; cursor: pointer; white-space: nowrap; }
.fr-btn.sent { background: #edf2f7; color: #718096; cursor: default; }
.fr-btn.friends { background: #f0fff4; color: #38a169; cursor: default; border: 1px solid #c6f6d5; }
.fr-btn.received { background: #fef3c7; color: #92400e; cursor: default; }

.req-count-badge { background: #e53e3e; color: white; border-radius: 50%; width: 22px; height: 22px; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.req-actions { display: flex; gap: 6px; margin-left: auto; }
.btn-accept { background: #004ea2; color: white; border: none; padding: 7px 14px; border-radius: 10px; font-size: 12px; font-weight: 700; cursor: pointer; }
.btn-reject { background: #fff5f5; color: #e53e3e; border: 1px solid #fed7d7; padding: 7px 14px; border-radius: 10px; font-size: 12px; font-weight: 700; cursor: pointer; }

.friend-count { font-size: 14px; color: #a0aec0; font-weight: 400; margin-left: 4px; }
.friend-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.friend-card {
  background: #f8fbff; border-radius: 16px; padding: 16px 10px;
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  border: 1px solid #edf2f7; cursor: pointer; transition: all 0.2s;
}
.friend-card:hover { border-color: #004ea2; box-shadow: 0 4px 12px rgba(0,78,162,0.1); transform: translateY(-2px); }
.fc-avatar { width: 44px; height: 44px; border-radius: 16px; background: #eef2ff; display: flex; align-items: center; justify-content: center; font-size: 20px; }
.fc-name { font-size: 13px; font-weight: 700; color: #1a202c; text-align: center; }
.fc-grade { font-size: 11px; color: #a0aec0; }

.empty-friends { text-align: center; padding: 30px 0; color: #a0aec0; font-size: 14px; line-height: 1.8; border: 2px dashed #f7fafc; border-radius: 16px; }
.empty-msg { text-align: center; padding: 16px 0; color: #a0aec0; font-size: 13px; }
</style>