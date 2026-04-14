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
export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login() {
      if (!this.username || !this.password) {
        alert('아이디와 비밀번호를 입력하세요')
        return
      }

      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
/* 전체 배경 */
.wrapper {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea, #764ba2);
}

/* 로그인 박스 */
.login-box {
  background: white;
  padding: 40px;
  border-radius: 15px;
  width: 300px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

h2 {
  margin-bottom: 20px;
}

/* 입력창 */
.input-group input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: 0.3s;
}

/* 포커스 효과 */
.input-group input:focus {
  border-color: #667eea;
  box-shadow: 0 0 5px rgba(102,126,234,0.5);
}

/* 버튼 */
button {
  width: 100%;
  padding: 10px;
  margin-top: 15px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background: #5a67d8;
}
</style>