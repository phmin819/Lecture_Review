<template>
  <div class="wrapper">
    <div class="login-box">
      <h2>회원가입</h2>


      <input v-model="username" placeholder="아이디" />
      <input v-model="email" placeholder="이메일" />
      <input v-model="password" type="password" placeholder="비밀번호" />
      

      <button @click="register">회원가입</button>

      <p @click="$router.push('/login')" style="cursor:pointer; margin-top:10px;">
        이미 계정이 있나요? 로그인
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
      email: '',     //  추가
      password: ''
    }
  },
  methods: {
    async register() {
      if (!this.username || !this.email || !this.password) {
        alert("모두 입력하세요");
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
        alert("회원가입 실패");
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
  background: linear-gradient(135deg, #43cea2, #185a9d);
}

.login-box {
  background: white;
  padding: 40px;
  border-radius: 15px;
  width: 300px;
  text-align: center;
}
</style>