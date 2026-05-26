<template>
  <div class="signup-wrapper">
    <!-- 배경 장식 -->
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
    </div>

    <div class="signup-container">
      <div class="signup-header">
        <h1 class="logo-text">MJC Lecture</h1>
        <p class="step-text">새로운 계정 만들기</p>
      </div>

      <form class="signup-card" @submit.prevent="signup">
        <div class="input-section">
          <div class="input-group">
            <label for="username">사용자 이름(닉네임)</label>
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
            <label for="email">계정 아이디(또는 이메일)</label>
            <div class="input-wrapper">
              <input
                id="email"
                v-model="email"
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

        <button type="submit" class="signup-submit-btn" :disabled="loading">
          <span v-if="!loading">회원가입 완료</span>
          <span v-else class="loader"></span>
        </button>

        <p v-if="errorMessage" role="status" aria-live="polite" class="error-msg">
          {{ errorMessage }}
        </p>

        <div class="form-footer">
          <p>이미 계정이 있으신가요?</p>
          <button type="button" class="login-link" @click="$router.push('/login')">
            로그인 화면으로
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      errorMessage: '',
      loading: false
    }
  },
  methods: {
    async signup() {
      this.errorMessage = '';
      this.loading = true;

      try {
        await axios.post("http://127.0.0.1:8000/auth/signup", {
          username: this.username,
          email: this.email,
          password: this.password
        });
        alert("회원가입을 축하합니다! 로그인을 진행해 주세요.");
        this.$router.push("/login");
      } catch (err) {
        console.error(err);
        this.errorMessage = err.response?.data?.detail || "회원가입 중 오류가 발생했습니다.";
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.signup-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8fbff;
  font-family: 'Pretendard', sans-serif;
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
  width: 350px;
  height: 350px;
  background: #004ea2;
  top: -50px;
  left: -100px;
}
.circle-2 {
  width: 450px;
  height: 450px;
  background: #0072bc;
  bottom: -150px;
  right: -100px;
}

.signup-container {
  width: 100%;
  max-width: 420px;
  padding: 20px;
  z-index: 10;
  animation: fadeIn 0.8s ease-out;
}

.signup-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-text {
  font-size: 28px;
  font-weight: 800;
  color: #004ea2;
  margin-bottom: 8px;
}

.step-text {
  color: #718096;
  font-weight: 500;
}

.signup-card {
  background: white;
  padding: 32px;
  border-radius: 24px;
  box-shadow: 0 10px 25px rgba(0, 78, 162, 0.08);
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-group label {
  font-size: 13px;
  font-weight: 600;
  color: #4a5568;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: #f7fafc;
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 0 14px;
  transition: all 0.2s;
}

.input-wrapper:focus-within {
  border-color: #004ea2;
  background: white;
}

.input-icon {
  font-size: 16px;
  margin-right: 10px;
  color: #a0aec0;
}

.input-wrapper input {
  width: 100%;
  padding: 12px 0;
  border: none;
  background: transparent;
  font-size: 15px;
  outline: none;
}

.signup-submit-btn {
  width: 100%;
  padding: 14px;
  background: #004ea2;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.signup-submit-btn:hover {
  background: #003a85;
  transform: translateY(-2px);
}

.error-msg {
  color: #e53e3e;
  font-size: 13px;
  text-align: center;
  margin-top: 12px;
  background: #fff5f5;
  padding: 8px;
  border-radius: 8px;
}

.form-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 13px;
  color: #718096;
}

.login-link {
  background: none;
  border: none;
  color: #004ea2;
  font-weight: 700;
  text-decoration: underline;
  cursor: pointer;
  margin-top: 4px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

.loader {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>