<template>
  <div class="page-wrapper">
    <header class="detail-header">
      <div class="nav-content">
        <button type="button" class="back-btn" @click="$router.push('/')" aria-label="목록으로 돌아가기">목록으로</button>
        <button type="button" class="logo" @click="$router.push('/')" aria-label="홈으로 이동">MJC Lecture</button>
        <div v-if="!isLoggedIn" class="auth-buttons">
          <button class="login-btn" type="button" @click="$router.push('/login')">로그인</button>
        </div>
        <div v-else class="user-nav">
          <button class="profile-nav-btn" @click="$router.push('/profile')" aria-label="프로필로 이동">
            <span class="nav-label">내 정보</span>
          </button>
        </div>
      </div>
    </header>

    <main class="container" v-if="lecture">
      <section class="card info-section">
        <div class="badge-row">
          <span class="dept-badge">{{ lecture.department }}</span>
          <span class="info-text">3학점 · {{ lecture.class_time || '시간표 정보 없음' }}</span>
        </div>
        <div v-if="isAdmin && !isEditing" class="admin-controls">
          <span class="admin-badge">관리자 권한</span>
          <button @click="startEdit" class="edit-btn">정보 수정</button>
        </div>

        <div v-if="isEditing" class="edit-form card">
          <h3>강의 정보 수정</h3>
          <div class="form-group">
            <label>강의명</label>
            <input v-model="editData.lecture_name" placeholder="강의명" />
          </div>
          <div class="form-group">
            <label>교수명</label>
            <input v-model="editData.professor_name" placeholder="교수명" />
          </div>
          <div class="form-group">
            <label>학과</label>
            <input v-model="editData.department" placeholder="학과" />
          </div>
          <div class="form-group">
            <label>강의 시간 (예: 월1,2 / 수4)</label>
            <input v-model="editData.class_time" placeholder="강의 시간" />
          </div>
          <div class="edit-actions">
            <button @click="saveEdit" class="save-edit-btn">저장</button>
            <button @click="isEditing = false" class="cancel-edit-btn">취소</button>
          </div>
        </div>

        <div v-if="!isEditing">
          <h2 class="lecture-title">{{ lecture.lecture_name }}</h2>
          <p class="professor-name">{{ lecture.professor_name }} 교수님</p>
        </div>

        <div class="rating-display" aria-label="강의 평점 정보">
          <div class="score-main">
            <span class="score-num">{{ lecture.avg_rating || '0.0' }}</span>
            <span class="score-max">/ 5</span>
            <div class="stars" aria-hidden="true">{{ getStarDisplay(lecture.avg_rating) }}</div>
            <p class="review-count">리뷰 {{ reviews.length }}개</p>
          </div>
          
          <div class="rating-bars" aria-hidden="true">
            <div class="bar-item" v-for="n in [5,4,3,2,1]" :key="n">
              <span>{{ n }}점</span>
              <div class="bar-bg"><div class="bar-fill" :style="{ width: getRatingBarWidth(n) + '%' }"></div></div>
              <span class="bar-num">{{ getRatingCount(n) }}</span>
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
              <div class="user-info">
                <span class="username">{{ review.username }}</span>
                <time :datetime="review.created_at">{{ formatDate(review.created_at) }} 작성됨</time>
              </div>
              <div class="item-rating">평점 {{ review.rating.toFixed(1) }}</div>
              <!-- 관리자 삭제 버튼 추가 -->
              <button 
                v-if="isAdmin" 
                @click="deleteReview(review.review_id)" 
                class="delete-review-btn"
                title="리뷰 삭제"
              >
                삭제
              </button>
            </div>
            <p class="review-text">{{ review.content }}</p>
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
              <span class="star-num" :class="{ active: rating >= i }">{{ i }}</span>
              <span class="visually-hidden">{{ i }}점</span>
            </label>
          </fieldset>

          <label for="review-text" class="visually-hidden">후기 내용</label>
          <textarea
            id="review-text"
            v-model="newReview"
            placeholder="이 강의에 대한 솔직한 후기를 남겨주세요."
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
      formStatus: "",
      isLoggedIn: false,
      isAdmin: false,
      isEditing: false, // 수정 모드 여부
      editData: {
        lecture_name: "",
        professor_name: "",
        department: "",
        class_time: ""
      }
    }
  },
  async created() {
    this.isLoggedIn = !!localStorage.getItem("token");
    this.isAdmin = localStorage.getItem("isAdmin") === "true";
    this.fetchLectureData();
  },
  methods: {
    async deleteReview(reviewId) {
      if (!confirm("정말로 이 리뷰를 삭제하시겠습니까?")) return;
      
      const token = localStorage.getItem("token");
      try {
        await axios.delete(`http://127.0.0.1:8000/reviews/${reviewId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("리뷰가 삭제되었습니다.");
        await this.fetchLectureData(); // 목록 새로고침
      } catch (err) {
        console.error("리뷰 삭제 실패:", err);
        alert(err.response?.data?.detail || "리뷰 삭제 중 오류가 발생했습니다.");
      }
    },
    startEdit() {
      this.editData = {
        lecture_name: this.lecture.lecture_name,
        professor_name: this.lecture.professor_name,
        department: this.lecture.department,
        class_time: this.lecture.class_time
      };
      this.isEditing = true;
    },
    async saveEdit() {
      const token = localStorage.getItem("token");
      const lectureId = this.$route.params.id;
      try {
        await axios.put(`http://127.0.0.1:8000/lectures/${lectureId}`, this.editData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("강의 정보가 수정되었습니다.");
        this.isEditing = false;
        await this.fetchLectureData();
      } catch (err) {
        console.error("강의 수정 실패:", err);
        alert("수정 중 오류가 발생했습니다.");
      }
    },
    async fetchLectureData() {
      const lectureId = this.$route.params.id;
      try {
        const res = await axios.get(`http://127.0.0.1:8000/lectures/${lectureId}`);
        this.lecture = res.data;
        
        const revRes = await axios.get(`http://127.0.0.1:8000/lectures/${lectureId}/reviews`);
        this.reviews = revRes.data;
      } catch (err) {
        console.error("데이터 로드 실패", err);
      }
    },
    getStarDisplay(rating) {
      const fullStars = Math.floor(rating || 0);
      const hasHalfStar = (rating || 0) % 1 >= 0.5;
      let stars = '★'.repeat(fullStars);
      if (hasHalfStar && fullStars < 5) stars += '☆';
      stars += '☆'.repeat(5 - fullStars - (hasHalfStar ? 1 : 0));
      return stars;
    },
    getRatingCount(ratingScore) {
      return this.reviews.filter(r => r.rating === ratingScore).length;
    },
    getRatingBarWidth(ratingScore) {
      if (this.reviews.length === 0) return 0;
      const count = this.getRatingCount(ratingScore);
      return (count / this.reviews.length) * 100;
    },
    formatDate(dateStr) {
      if (!dateStr) return "";
      const date = new Date(dateStr);
      return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`;
    },
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
      
      try {
        this.formStatus = "리뷰 등록 중입니다...";
        
        const lectureId = this.$route.params.id;
        const reviewData = {
          rating: this.rating,
          content: this.newReview,
          lecture_id: parseInt(lectureId)
        };
        
        await axios.post(
          "http://127.0.0.1:8000/reviews",
          reviewData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json"
            }
          }
        );
        
        // 리뷰 등록 성공 후 전체 데이터 다시 불러오기 (평점 포함)
        this.formStatus = "✓ 리뷰가 등록되었습니다!";
        await this.fetchLectureData();
        
        // 폼 초기화
        setTimeout(() => {
          this.newReview = "";
          this.rating = 5;
          this.formStatus = "";
        }, 1500);
        
      } catch (err) {
        console.error("리뷰 등록 실패:", err);
        if (err.response?.status === 401) {
          this.formStatus = "로그인이 필요합니다.";
        } else {
          this.formStatus = "리뷰 등록 중 오류가 발생했습니다. 다시 시도해주세요.";
        }
      }
    }
  }
}
</script>

<style scoped>
.page-wrapper { background-color: #f8fbff; min-height: 100vh; padding-bottom: 80px; font-family: 'Pretendard', sans-serif; }
.detail-header { background: white; border-bottom: 1px solid #edf2f7; padding: 18px 0; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
.nav-content { max-width: 700px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; }
.back-btn { cursor: pointer; color: #718096; font-size: 14px; background: none; border: none; font-weight: 600; transition: color 0.2s; }
.back-btn:hover { color: #004ea2; }
.logo { font-weight: 800; color: #004ea2; cursor: pointer; background: none; border: none; font-size: 20px; letter-spacing: -0.5px; }
.login-btn { background: #004ea2; color: white; border: none; padding: 8px 16px; border-radius: 10px; cursor: pointer; font-weight: 700; }
.user-nav { display: flex; align-items: center; }
.profile-nav-btn { background: #f7fafc; border: 1px solid #edf2f7; padding: 8px 14px; border-radius: 100px; cursor: pointer; transition: all 0.2s; }
.nav-label { font-weight: 600; font-size: 14px; color: #4a5568; }

.container { max-width: 700px; margin: 30px auto; padding: 0 20px; position: relative; z-index: 10; }
.card { background: white; border-radius: 24px; padding: 32px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,78,162,0.04); border: 1px solid rgba(0,78,162,0.02); }

.dept-badge { background: #eef2ff; color: #004ea2; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 700; margin-right: 12px; }
.info-text { color: #a0aec0; font-size: 13px; font-weight: 500; }
.lecture-title { font-size: 28px; margin: 16px 0 6px 0; font-weight: 800; color: #1a202c; letter-spacing: -0.5px; }
.professor-name { color: #718096; font-size: 16px; margin-bottom: 24px; font-weight: 500; }

.admin-controls { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding: 12px; background: #fff5f5; border-radius: 14px; border: 1px solid #fed7d7; }
.admin-badge { color: #e53e3e; font-size: 12px; font-weight: 800; }
.edit-btn { background: white; color: #e53e3e; border: 1px solid #fed7d7; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-size: 12px; font-weight: 700; }

.edit-form h3 { margin-bottom: 20px; font-size: 18px; font-weight: 800; }
.edit-form .form-group { margin-bottom: 16px; }
.edit-form label { display: block; font-size: 13px; font-weight: 700; color: #4a5568; margin-bottom: 6px; margin-left: 4px; }
.edit-form input { width: 100%; padding: 12px; background: #f7fafc; border: 2px solid transparent; border-radius: 12px; outline: none; }
.edit-form input:focus { border-color: #004ea2; background: white; }
.edit-actions { display: flex; gap: 12px; margin-top: 24px; }
.save-edit-btn { flex: 1; background: #004ea2; color: white; border: none; padding: 14px; border-radius: 12px; font-weight: 700; cursor: pointer; }
.cancel-edit-btn { flex: 1; background: #edf2f7; color: #718096; border: none; padding: 14px; border-radius: 12px; font-weight: 700; cursor: pointer; }

.rating-display { display: flex; gap: 40px; margin-bottom: 40px; align-items: center; background: #f8fbff; padding: 30px; border-radius: 20px; }
.score-main { text-align: center; }
.score-num { font-size: 52px; font-weight: 800; color: #1a202c; }
.score-max { color: #cbd5e0; font-size: 20px; font-weight: 600; }
.review-count { color: #a0aec0; font-size: 14px; margin-top: 4px; font-weight: 600; }

.rating-bars { flex-grow: 1; }
.bar-item { display: flex; align-items: center; gap: 12px; font-size: 12px; color: #718096; margin-bottom: 6px; font-weight: 600; }
.bar-bg { flex-grow: 1; height: 8px; background: #edf2f7; border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; background: #004ea2; border-radius: 4px; }

.star-rating-input { display: flex; gap: 10px; margin-bottom: 20px; border: none; padding: 0; }
.star-label { cursor: pointer; }
.star-num { display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 12px; background: #f7fafc; color: #a0aec0; font-weight: 800; transition: all 0.2s; border: 2px solid transparent; }
.star-num.active { background: #004ea2; color: white; box-shadow: 0 4px 10px rgba(0,78,162,0.2); }
.star-num:hover { transform: translateY(-2px); }

textarea { width: 100%; height: 120px; border: 2px solid transparent; background: #f7fafc; border-radius: 16px; padding: 20px; margin: 16px 0; box-sizing: border-box; resize: none; font-size: 15px; outline: none; transition: all 0.2s; }
textarea:focus { background: white; border-color: #004ea2; }
.submit-btn { width: 100%; background: #004ea2; color: white; border: none; padding: 16px; border-radius: 14px; font-weight: 800; font-size: 16px; cursor: pointer; transition: all 0.2s; }
.submit-btn:hover { background: #003a85; transform: translateY(-2px); }

.review-list { display: flex; flex-direction: column; gap: 20px; }
.review-item { border-bottom: 1px solid #f7fafc; padding-bottom: 20px; }
.review-item:last-child { border-bottom: none; }
.review-user { display: flex; align-items: center; margin-bottom: 12px; }
.user-info { display: flex; flex-direction: column; }
.username { font-weight: 700; font-size: 15px; color: #1a202c; }
.user-info time { font-size: 12px; color: #a0aec0; font-weight: 500; }
.item-rating { margin-left: auto; font-weight: 800; color: #004ea2; font-size: 14px; background: #eef2ff; padding: 4px 10px; border-radius: 8px; }
.delete-review-btn { margin-left: 12px; background: white; color: #e53e3e; border: 1px solid #fed7d7; padding: 4px 10px; border-radius: 6px; cursor: pointer; font-size: 11px; font-weight: 700; }
.review-text { font-size: 15px; line-height: 1.7; color: #4a5568; margin: 0; font-weight: 400; }

.visually-hidden { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0; }
</style>