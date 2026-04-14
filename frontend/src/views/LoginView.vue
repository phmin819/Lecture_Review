<template>
  <div class="login-container">
    <h1>로그인</h1>

    <input v-model="username" placeholder="아이디" />
    <input v-model="password" type="password" placeholder="비밀번호" />

    <button @click="login">로그인</button>
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
      if (this.username === '' || this.password === '') {
        alert('아이디와 비밀번호를 입력하세요')
        return
      }

      alert(`로그인 시도: ${this.username}`)
    }
  }
}
</script>

<style>
.login-container {
  width: 300px;
  margin: 100px auto;
  text-align: center;
}

input {
  display: block;
  margin: 10px auto;
  padding: 8px;
  width: 100%;
}

button {
  padding: 10px;
  width: 100%;
}
</style>