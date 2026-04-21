<template>
  <div class="container">
    <h2>강의 상세 및 후기 페이지</h2>
    <p>강의 ID: {{ $route.params.id }}</p>
    <button @click="$router.push('/')">홈으로 돌아가기</button>
  </div>
</template>

<style scoped>
.container { padding: 20px; text-align: center; }
</style>