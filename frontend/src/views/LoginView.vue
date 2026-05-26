<template>
  <div class="login-wrapper">
    <!-- 배경 장식 요소 -->
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
    </div>

    <div class="login-container">
      <div class="login-header">
        <div class="university-logo">
          <span class="logo-icon">🎓</span>
          <h1 class="logo-text">MJC Lecture</h1>
        </div>
        <p class="welcome-text">명지전문대 강의 후기 커뮤니티</p>
      </div>

      <form class="login-card" @submit.prevent="login">
        <div class="input-section">
          <div class="input-group">
            <label for="username">계정(아이디 또는 이메일)</label>
            <div class="input-wrapper">
              <input
                id="username"
                v-model="username"
                type="text"
                required
              />
            </div>
          </div>

          <div class="input-group">
            <label for="password">비밀번호</label>
            <div class="input-wrapper">
              <input
                id="password"
                v-model="password"
                type="password"
                required
              />
            </div>
          </div>
        </div>

        <button type="submit" class="login-submit-btn" :disabled="loading">
          <span v-if="!loading">로그인</span>
          <span v-else class="loader"></span>
        </button>

        <p v-if="errorMessage" role="status" aria-live="polite" class="error-msg">
          {{ errorMessage }}
        </p>

        <div class="form-footer">
          <p>아직 회원이 아니신가요?</p>
          <button type="button" class="register-link" @click="$router.push('/register')">
            회원가입 하기
          </button>
        </div>
      </form>

      <p class="copyright">© 2026 Myongji Junior College Lecture Review. All rights reserved.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      loading: false
    }
  },
  methods: {
    async login() {
      this.errorMessage = '';
      this.loading = true;

      const formData = new URLSearchParams();
      formData.append("username", this.username);
      formData.append("password", this.password);

      try {
        const res = await axios.post(
          "http://127.0.0.1:8000/auth/login",
          formData,
          { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
        );

        localStorage.setItem("token", res.data.access_token);
        localStorage.setItem("isAdmin", res.data.is_admin ? "true" : "false");
        this.$router.push("/");
      } catch (err) {
        console.error(err);
        this.errorMessage = err.response?.data?.detail || "이메일 또는 비밀번호를 확인해 주세요.";
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
/* MJC 브랜드 컬러 정의 */
:root {
  --primary-color: #004ea2; /* 명지 블루 */
  --secondary-color: #0072bc;
  --bg-light: #f8fbff;
  --text-dark: #1a202c;
  --text-muted: #718096;
}

.login-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8fbff;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  position: relative;
  overflow: hidden;
}

/* 배경 장식 */
.bg-decoration {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 0;
}
.circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}
.circle-1 {
  width: 400px;
  height: 400px;
  background: #004ea2;
  top: -100px;
  right: -100px;
}
.circle-2 {
  width: 300px;
  height: 300px;
  background: #0072bc;
  bottom: -50px;
  left: -50px;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
  z-index: 10;
  animation: fadeIn 0.8s ease-out;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.university-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
}

.logo-icon {
  font-size: 32px;
}

.logo-text {
  font-size: 32px;
  font-weight: 800;
  color: #004ea2;
  letter-spacing: -1px;
}

.welcome-text {
  color: #718096;
  font-size: 16px;
  font-weight: 500;
}

/* 로그인 카드 */
.login-card {
  background: white;
  padding: 40px;
  border-radius: 24px;
  box-shadow: 0 10px 25px rgba(0, 78, 162, 0.08);
  border: 1px solid rgba(0, 78, 162, 0.05);
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-size: 14px;
  font-weight: 600;
  color: #4a5568;
  margin-left: 4px;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: #f7fafc;
  border: 2px solid transparent;
  border-radius: 14px;
  padding: 0 16px;
  transition: all 0.2s;
}

.input-wrapper:focus-within {
  border-color: #004ea2;
  background: white;
  box-shadow: 0 0 0 4px rgba(0, 78, 162, 0.1);
}

.input-icon {
  font-size: 18px;
  margin-right: 12px;
  color: #a0aec0;
}

.input-wrapper input {
  width: 100%;
  padding: 14px 0;
  border: none;
  background: transparent;
  font-size: 16px;
  color: #1a202c;
  outline: none;
}

/* 로그인 버튼 */
.login-submit-btn {
  width: 100%;
  padding: 16px;
  background: #004ea2;
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-submit-btn:hover {
  background: #003a85;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 78, 162, 0.25);
}

.login-submit-btn:active {
  transform: translateY(0);
}

.login-submit-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
  transform: none;
}

/* 오류 메시지 */
.error-msg {
  color: #e53e3e;
  font-size: 14px;
  text-align: center;
  margin-top: 16px;
  background: #fff5f5;
  padding: 10px;
  border-radius: 8px;
}

/* 하단 푸터 */
.form-footer {
  margin-top: 32px;
  text-align: center;
  font-size: 14px;
  color: #718096;
}

.register-link {
  background: none;
  border: none;
  color: #004ea2;
  font-weight: 700;
  text-decoration: underline;
  cursor: pointer;
  margin-top: 8px;
  padding: 4px;
}

.register-link:hover {
  color: #0072bc;
}

.copyright {
  text-align: center;
  font-size: 12px;
  color: #a0aec0;
  margin-top: 30px;
}

/* 애니메이션 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 로더 */
.loader {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>