<template>
  <div class="fp-wrapper">
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
    </div>

    <div class="fp-container">
      <header class="fp-nav-header">
        <button class="back-link" @click="$router.push('/profile')">
          <span>←</span> 마이 페이지
        </button>
        <h1 class="page-title">친구 프로필</h1>
      </header>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
      </div>

      <template v-else-if="friend">
        <!-- 요약 카드 -->
        <section class="section-card">
          <div class="user-main">
            <div class="avatar-large">👤</div>
            <div class="text-info">
              <h2>{{ friend.username }}님</h2>
              <div class="badge-group">
                <span class="role-badge">학생</span>
                <span v-if="friend.grade" class="grade-badge">{{ friend.grade }}학년</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 시간표 (읽기 전용) -->
        <section class="section-card">
          <TimetableGrid :readonly="true" :initial-entries="friend.timetable" />
        </section>

        <!-- 친구 삭제 -->
        <section class="section-card">
          <button class="remove-btn" @click="removeFriend" :disabled="removing">
            {{ removing ? '처리 중...' : '👋 친구 삭제' }}
          </button>
        </section>
      </template>

      <div v-else class="error-state">
        <p>프로필을 불러올 수 없습니다.<br>친구 관계가 아니거나 존재하지 않는 유저입니다.</p>
        <button class="back-link" @click="$router.push('/profile')">마이 페이지로 돌아가기</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import TimetableGrid from '@/components/TimetableGrid.vue'

export default {
  components: { TimetableGrid },
  data() {
    return {
      friend: null,
      loading: true,
      removing: false,
    }
  },
  async created() {
    const token = localStorage.getItem('token')
    if (!token) { this.$router.push('/login'); return }
    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/friends/${this.$route.params.userId}/profile`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      this.friend = res.data
    } catch {
      this.friend = null
    } finally {
      this.loading = false
    }
  },
  methods: {
    async removeFriend() {
      if (!confirm(`${this.friend.username}님을 친구 목록에서 삭제할까요?`)) return
      const token = localStorage.getItem('token')
      this.removing = true
      try {
        await axios.delete(
          `http://127.0.0.1:8000/friends/${this.friend.user_id}`,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.$router.push('/profile')
      } finally {
        this.removing = false
      }
    },
  },
}
</script>

<style scoped>
.fp-wrapper {
  min-height: 100vh; background-color: #f8fbff;
  font-family: 'Pretendard', sans-serif; position: relative;
  overflow-x: hidden; padding-bottom: 100px;
}
.bg-decoration { position: fixed; width: 100%; height: 100%; z-index: 0; pointer-events: none; }
.circle { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.3; }
.circle-1 { width: 500px; height: 500px; background: #004ea2; top: -100px; right: -100px; }
.circle-2 { width: 400px; height: 400px; background: #0072bc; bottom: -100px; left: -100px; }

.fp-container { position: relative; z-index: 10; max-width: 650px; margin: 0 auto; padding: 0 20px; }

.fp-nav-header { padding: 40px 0 30px; display: flex; justify-content: space-between; align-items: center; }
.back-link { background: none; border: none; color: #718096; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 15px; }
.back-link:hover { color: #004ea2; }
.page-title { font-size: 24px; font-weight: 800; color: #1a202c; margin: 0; }

.section-card {
  background: white; border-radius: 28px; padding: 32px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02); margin-bottom: 24px;
  border: 1px solid rgba(0,78,162,0.03);
}

.user-main { display: flex; align-items: center; gap: 24px; }
.avatar-large { font-size: 44px; background: #f7fafc; width: 88px; height: 88px; display: flex; align-items: center; justify-content: center; border-radius: 34px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05); }
.text-info h2 { font-size: 24px; margin: 0 0 10px; color: #1a202c; }
.badge-group { display: flex; gap: 8px; }
.role-badge { background: #004ea2; color: white; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 700; }
.grade-badge { background: #eef2ff; color: #004ea2; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 700; }

.remove-btn {
  width: 100%; background: white; color: #e53e3e;
  border: 1px solid #fed7d7; padding: 14px; border-radius: 16px;
  font-weight: 700; font-size: 15px; cursor: pointer; transition: all 0.2s;
}
.remove-btn:hover { background: #fff5f5; }
.remove-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.loading-state { text-align: center; padding: 100px 0; }
.spinner { width: 40px; height: 40px; border: 3px solid #edf2f7; border-top-color: #004ea2; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto; }
@keyframes spin { to { transform: rotate(360deg); } }

.error-state { text-align: center; padding: 60px 20px; color: #718096; line-height: 1.8; }
</style>
