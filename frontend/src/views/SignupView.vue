<template>
  <div class="wrapper">
    <div class="signup-box">
    <h2>📚 명지전문대 강의 후기</h2>
      <h2>회원가입</h2>

      <input v-model="username" placeholder="아이디" />
      <input v-model="email" placeholder="이메일" />
      <input v-model="password" type="password" placeholder="비밀번호" />

      <button @click="signup">회원가입</button>

      <p @click="$router.push('/login')" class="link">
        로그인 하러가기
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
      password: ''
    }
  },
  methods: {
    async signup() {
      if (!this.username || !this.email || !this.password) {
        alert("모든 값을 입력하세요");
        return;
      }

      try {
        await axios.post("http://127.0.0.1:8000/auth/signup", {
          username: this.username,
          email: this.email,
          password: this.password
        });

        alert("회원가입 성공!");
        this.$router.push("/login");

      } catch (err) {
        console.error(err);
        alert("회원가입 실패 (이미 존재하는 이메일)");
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
}

.link {
  margin-top: 10px;
  color: #667eea;
  cursor: pointer;
}
</style>