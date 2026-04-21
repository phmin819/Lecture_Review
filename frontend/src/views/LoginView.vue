<template>
  <div class="wrapper">
    <div class="login-box">
      <h2> 명지전문대 강의 후기</h2>
      <h2>로그인</h2>

      <div class="input-group">
        <input v-model="username" placeholder="아이디 (이메일)" />
      </div>

      <div class="input-group">
        <input v-model="password" type="password" placeholder="비밀번호" />
      </div>

      <button @click="login">로그인</button>

      <div class="footer-links">
        <p>계정이 없으신가요? 
          <span class="link" @click="$router.push('/register')">회원가입</span>
        </p>
      </div>
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
        alert("로그인 실패: 이메일 또는 비밀번호를 확인하세요.");
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
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-sizing: border-box; /* 패딩이 너비를 넘지 않게 조절 */
}

button {
  width: 100%;
  padding: 12px;
  margin-top: 15px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background: #5a6fd6;
}

/* 하단 링크 스타일 */
.footer-links {
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.link {
  color: #667eea;
  font-weight: bold;
  cursor: pointer;
  text-decoration: underline;
  margin-left: 5px;
}

.link:hover {
  color: #764ba2;
}
</style>