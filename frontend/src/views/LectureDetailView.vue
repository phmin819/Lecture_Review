<template>
  <div class="page-wrapper">
    <header class="detail-header">
      <div class="nav-content">
        <button type="button" class="back-btn" @click="$router.push('/')" aria-label="목록으로 돌아가기">← 목록으로</button>
        <button type="button" class="logo" @click="$router.push('/')" aria-label="홈으로 이동">명지전문대</button>
        <button class="login-btn" type="button" @click="$router.push('/login')">로그인</button>
      </div>
    </header>

    <main class="container" v-if="lecture">
      <section class="card info-section">
        <div class="badge-row">
          <span class="dept-badge">{{ lecture.department }}</span>
          <span class="info-text">3학점 · 시간표 정보 없음</span>
        </div>
        <h2 class="lecture-title">{{ lecture.lecture_name }}</h2>
        <p class="professor-name">{{ lecture.professor_name }} 교수님</p>

        <div class="rating-display" aria-label="강의 평점 정보">
          <div class="score-main">
            <span class="score-num">{{ lecture.avg_rating || '0.0' }}</span>
            <span class="score-max">/ 5</span>
            <div class="stars" aria-hidden="true">☆☆☆☆☆</div>
            <p class="review-count">리뷰 {{ reviews.length }}개</p>
          </div>
          
          <div class="rating-bars" aria-hidden="true">
            <div class="bar-item" v-for="n in [5,4,3,2,1]" :key="n">
              <span>{{ n }}점</span>
              <div class="bar-bg"><div class="bar-fill" style="width: 0%"></div></div>
              <span class="bar-num">0</span>
            </div>
          </div>
        </div>

        <div class="stats-grid">
          <div class="stat-card"><strong>-</strong><span>강의력</span></div>
          <div class="stat-card"><strong>-</strong><span>과제량</span></div>
          <div class="stat-card"><strong>-</strong><span>성적 만족</span></div>
          <div class="stat-card"><strong>-</strong><span>난이도</span></div>
        </div>
      </section>

      <section class="card keywords-section">
        <h3>이런 점이 좋았어요</h3>
        <p class="empty-text">아직 수집된 키워드가 없습니다.</p>
      </section>

      <section class="card reviews-section">
        <div class="section-header">
          <h3>수강 후기 {{ reviews.length }}</h3>
        </div>

        <div v-if="reviews.length === 0" class="empty-reviews">
          <p>작성된 후기가 없습니다.<br>첫 번째 후기의 주인공이 되어주세요!</p>
        </div>

        <div v-else class="review-list">
          <div class="review-item" v-for="review in reviews" :key="review.review_id">
            <div class="review-user">
              <div class="user-avatar" aria-hidden="true">👤</div>
              <div class="user-info">
                <time datetime="2026">2026년 작성됨</time>
              </div>
              <div class="item-rating">⭐ {{ review.rating.toFixed(1) }}</div>
            </div>
            <p class="review-text">{{ review.comment }}</p>
          </div>
        </div>
      </section>

      <section class="card write-section">
        <h3>후기 작성하기</h3>
        <form @submit.prevent="submitReview" aria-label="후기 작성 폼">
          <fieldset class="star-rating-input" aria-label="별점 선택">
            <legend class="visually-hidden">별점 선택</legend>
            <label v-for="i in 5" :key="i" class="star-label">
              <input
                type="radio"
                name="rating"
                :value="i"
                v-model="rating"
                class="visually-hidden"
              />
              <span class="star" :aria-pressed="rating >= i ? 'true' : 'false'">{{ i <= rating ? '⭐' : '☆' }}</span>
              <span class="visually-hidden">{{ i }}점</span>
            </label>
          </fieldset>

          <label for="review-text" class="visually-hidden">후기 내용</label>
          <textarea
            id="review-text"
            v-model="newReview"
            placeholder="이 강의에 대한 솔직한 후기를 남겨주세요. 후배들에게 큰 도움이 됩니다 :)"
          ></textarea>

          <button type="submit" class="submit-btn">후기 등록하기</button>
          <p role="status" aria-live="polite" class="form-status">{{ formStatus }}</p>
        </form>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      lecture: null,
      reviews: [],
      newReview: "",
      rating: 5,
      formStatus: ""
    }
  },
  async created() {
    const lectureId = this.$route.params.id;
    try {
      // 모든 강의를 가져와서 해당 ID 찾기 (상세조회 API가 없을 경우 대비)
      const res = await axios.get("http://127.0.0.1:8000/lectures");
      this.lecture = res.data.find(l => l.lecture_id == lectureId);
      
      // 해당 강의의 리뷰 가져오기
      const revRes = await axios.get(`http://127.0.0.1:8000/lectures/${lectureId}/reviews`);
      this.reviews = revRes.data;
    } catch (err) {
      console.error("데이터 로드 실패", err);
    }
  },
  methods: {
    async submitReview() {
      const token = localStorage.getItem("token");
      if (!token) {
        this.formStatus = "로그인이 필요한 기능입니다.";
        return;
      }
      if (!this.newReview.trim()) {
        this.formStatus = "후기 내용을 입력해 주세요.";
        return;
      }
      this.formStatus = "리뷰 등록 준비 중입니다.";
      // 리뷰 등록 로직은 다음 단계에서 구현!
    }
  }
}
</script>

<style scoped>
.page-wrapper { background-color: #f8f9fa; min-height: 100vh; padding-bottom: 50px; }
.detail-header { background: white; border-bottom: 1px solid #eee; padding: 15px 0; position: sticky; top: 0; z-index: 100; }
.nav-content { max-width: 600px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; }
.back-btn { cursor: pointer; color: #666; font-size: 14px; }
.logo { font-weight: bold; color: #4e73df; cursor: pointer; }
.login-btn { background: #4e73df; color: white; border: none; padding: 6px 15px; border-radius: 5px; cursor: pointer; }

.container { max-width: 600px; margin: 20px auto; padding: 0 15px; }
.card { background: white; border-radius: 15px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }

.dept-badge { background: #eef2ff; color: #4e73df; padding: 4px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; margin-right: 10px; }
.info-text { color: #999; font-size: 12px; }
.lecture-title { font-size: 24px; margin: 10px 0 5px 0; font-weight: bold; }
.professor-name { color: #666; margin-bottom: 20px; }

.rating-display { display: flex; gap: 30px; margin-bottom: 30px; align-items: center; }
.score-num { font-size: 48px; font-weight: bold; }
.score-max { color: #ccc; font-size: 20px; }
.review-count { color: #999; font-size: 13px; margin-top: 5px; }

.rating-bars { flex-grow: 1; }
.bar-item { display: flex; align-items: center; gap: 10px; font-size: 12px; color: #666; margin-bottom: 4px; }
.bar-bg { flex-grow: 1; height: 6px; background: #eee; border-radius: 3px; }
.bar-fill { height: 100%; background: #ff9f43; border-radius: 3px; }
.bar-num { width: 20px; text-align: right; color: #ccc; }

.visually-hidden { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0 0 0 0); border: 0; }

.star-rating-input { display: flex; gap: 8px; margin-bottom: 10px; }
.star-label { cursor: pointer; }
.star-label input { position: absolute; opacity: 0; width: 1px; height: 1px; overflow: hidden; }
.star { display: inline-flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 10px; background: #f3f4f6; transition: background 0.2s; }
.star:hover,
.star:focus-visible { background: #e2e8f0; outline: none; }

.form-status { margin-top: 12px; color: #4e73df; font-size: 14px; min-height: 1.2em; }

.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; border-top: 1px solid #f1f1f1; padding-top: 20px; }
.stat-card { background: #f8f9fa; padding: 15px 5px; border-radius: 10px; text-align: center; }
.stat-card strong { display: block; font-size: 18px; color: #333; }
.stat-card span { font-size: 12px; color: #888; }

.empty-text { color: #bbb; font-size: 14px; text-align: center; padding: 10px 0; }
.empty-reviews { text-align: center; padding: 50px 0; color: #adb5bd; line-height: 1.6; }

.star-rating-input { font-size: 24px; margin-bottom: 10px; cursor: pointer; }
textarea { width: 100%; height: 100px; border: 1px solid #eee; border-radius: 10px; padding: 15px; margin: 15px 0; box-sizing: border-box; resize: none; background: #f8f9fa; }
.submit-btn { width: 100%; background: #4e73df; color: white; border: none; padding: 15px; border-radius: 10px; font-weight: bold; cursor: pointer; }

.review-item { border-bottom: 1px solid #eee; padding: 20px 0; text-align: left; }
.review-user { display: flex; align-items: center; margin-bottom: 10px; }
.user-avatar { font-size: 20px; margin-right: 10px; }
.user-info span { font-size: 12px; color: #adb5bd; }
.item-rating { margin-left: auto; font-weight: bold; color: #ff9f43; }
.review-text { font-size: 14px; line-height: 1.6; color: #444; margin: 0; }
</style>