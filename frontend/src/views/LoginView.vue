<template>
  <div class="wrapper">
    <div class="login-box">
      <h2>로그인</h2>

      <div class="input-group">
        <input v-model="username" placeholder="아이디" />
      </div>

      <div class="input-group">
        <input v-model="password" type="password" placeholder="비밀번호" />
      </div>

      <button @click="login">로그인</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login() {
      if (!this.username || !this.password) {
        alert('아이디와 비밀번호를 입력하세요')
        return
      }

      const formData = new URLSearchParams();
      formData.append("username", this.username);
      formData.append("password", this.password);

      try {
        const res = await axios.post(
          "http://127.0.0.1:8000/auth/login",
          formData,
          {
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
          }
        );

        localStorage.setItem("token", res.data.access_token);

        alert("로그인 성공!");
        this.$router.push("/");

      } catch (err) {
        console.error(err);
        alert("로그인 실패");
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

.login-box {
  background: white;
  padding: 40px;
  border-radius: 15px;
  width: 300px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.input-group input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 8px;
}

button {
  width: 100%;
  padding: 10px;
  margin-top: 15px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
}
</style>