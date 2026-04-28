<template>
  <div class="wrapper">
    <div class="signup-box">
      <h1>명지전문대 강의 후기</h1>
      <h2>회원가입</h2>

      <form class="signup-form" @submit.prevent="signup" novalidate>
        <div class="input-group">
          <label for="username">아이디</label>
          <input id="username" v-model="username" placeholder="아이디" />
        </div>

        <div class="input-group">
          <label for="email">이메일</label>
          <input id="email" v-model="email" type="email" placeholder="이메일" />
        </div>

        <div class="input-group">
          <label for="password">비밀번호</label>
          <input id="password" v-model="password" type="password" placeholder="비밀번호" />
        </div>

        <button type="submit">회원가입</button>
        <p role="status" aria-live="polite" class="alert">{{ errorMessage }}</p>
      </form>

      <p class="link-row">
        이미 계정이 있나요?
        <button type="button" class="link-button" @click="$router.push('/login')">로그인</button>
      </p>
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
      errorMessage: ''
    }
  },
  methods: {
    async signup() {
      this.errorMessage = '';
      if (!this.username || !this.email || !this.password) {
        this.errorMessage = "모든 값을 입력하세요.";
        return;
      }

      try {
        await axios.post("http://127.0.0.1:8000/auth/signup", {
          username: this.username,
          email: this.email,
          password: this.password
        });

        this.errorMessage = "회원가입 성공!";
        this.$router.push("/login");
      } catch (err) {
        console.error(err);
        this.errorMessage = "회원가입 실패 (이미 존재하는 이메일)";
      }
    }
  }
}
</script>

<style scoped>
.wrapper {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.signup-box {
  background: white;
  padding: 40px;
  border-radius: 15px;
  width: 300px;
  text-align: center;
}

input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
}

button {
  width: 100%;
  padding: 10px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

.input-group label {
  display: block;
  text-align: left;
  margin-bottom: 6px;
  font-size: 14px;
  color: #333;
}

.alert {
  margin-top: 12px;
  color: #d63333;
  min-height: 1.2em;
}

.link-button {
  background: none;
  border: none;
  color: #667eea;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  font-size: 14px;
  font-weight: bold;
}

.link-button:hover {
  color: #764ba2;
}
</style>