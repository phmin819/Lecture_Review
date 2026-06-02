<template>
  <div class="tt-section">
    <div class="tt-card-header">
      <h3>📅 {{ readonly ? '시간표' : '나의 시간표' }}</h3>
      <span v-if="readonly" class="tt-readonly-badge">👁️ 읽기 전용</span>
      <button v-else :class="['tt-edit-btn', { active: editMode }]" @click="toggleEdit">
        {{ editMode ? '✅ 완료' : '✏️ 편집 모드' }}
      </button>
    </div>

    <!-- 편집 힌트 -->
    <div v-if="editMode && !readonly" class="tt-hint">
      <span>🖱️ 빈 칸 드래그 → 수업 추가</span>
      <span class="hint-divider">|</span>
      <span>🗑️ 수업 블록 클릭 → 삭제</span>
    </div>

    <div v-if="loading" class="tt-loading">
      <div class="spinner"></div>
    </div>

    <div v-else class="tt-wrapper">
      <div
        class="tt-grid"
        :class="{ 'edit-active': editMode }"
        @mouseup="onMouseUp"
        @mouseleave="onGridLeave"
      >
        <!-- 헤더 행 -->
        <div class="tt-header tt-time-header"></div>
        <div class="tt-header" v-for="day in DAYS" :key="day">{{ day }}</div>

        <!-- 시간 행 -->
        <template v-for="hour in HOURS" :key="hour">
          <div class="tt-time-label">{{ hour }}시</div>
          <div
            v-for="day in DAYS"
            :key="`${day}-${hour}`"
            :class="['tt-cell', {
              'has-block': !!getEntry(day, hour),
              'dragging': isDragging(day, hour),
              'hoverable': editMode && !getEntry(day, hour)
            }]"
            @mousedown.prevent="onMouseDown(day, hour)"
            @mouseenter="onMouseEnter(day, hour)"
          >
            <!-- 수업 블록 -->
            <div
              v-if="getEntry(day, hour)"
              class="tt-block"
              :style="{ background: getEntry(day, hour).color_bg, color: getEntry(day, hour).color_fg }"
              @click.stop="editMode && deleteEntry(getEntry(day, hour).id)"
            >
              {{ getEntry(day, hour).subject_name }}
              <button v-if="editMode" class="tt-delete-btn" @click.stop="deleteEntry(getEntry(day, hour).id)">×</button>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- 추가 팝업 -->
    <div v-if="showPopup" class="tt-popup-overlay" @click.self="closePopup">
      <div class="tt-popup">
        <div class="tt-popup-title">수업 추가</div>
        <div class="tt-popup-range">{{ popupRangeText }}</div>

        <label class="tt-popup-label">수업명</label>
        <input
          ref="subjectInputRef"
          v-model="newSubject"
          :class="['tt-popup-input', { error: inputError }]"
          type="text"
          placeholder="예: 모바일프로그래밍"
          @keydown.enter="saveEntry"
          @keydown.esc="closePopup"
        />

        <label class="tt-popup-label">색상 선택</label>
        <div class="tt-palette">
          <div
            v-for="c in COLORS"
            :key="c.bg"
            :class="['tt-palette-dot', { selected: selectedColor.bg === c.bg }]"
            :style="{ background: c.bg, borderColor: selectedColor.bg === c.bg ? '#1a202c' : 'transparent' }"
            @click="selectedColor = c"
          ></div>
        </div>

        <div class="tt-popup-actions">
          <button class="tt-btn-save" @click="saveEntry">저장</button>
          <button class="tt-btn-cancel" @click="closePopup">취소</button>
        </div>
      </div>
    </div>

    <!-- 삭제 토스트 -->
    <transition name="toast-fade">
      <div v-if="showToast" class="tt-toast">🗑️ 수업이 삭제되었습니다</div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios'

const DAYS = ['월', '화', '수', '목', '금']
const HOURS = [9, 10, 11, 12, 13, 14, 15, 16, 17]
const COLORS = [
  { bg: '#dbeafe', fg: '#1d4ed8' },
  { bg: '#d1fae5', fg: '#065f46' },
  { bg: '#ede9fe', fg: '#5b21b6' },
  { bg: '#fce7f3', fg: '#9d174d' },
  { bg: '#fef3c7', fg: '#92400e' },
  { bg: '#fee2e2', fg: '#991b1b' },
]

export default {
  name: 'TimetableGrid',
  props: {
    readonly: { type: Boolean, default: false },
    initialEntries: { type: Array, default: null },
  },
  data() {
    return {
      DAYS,
      HOURS,
      COLORS,
      entries: [],
      loading: true,
      editMode: false,

      // 드래그 상태
      dragging: false,
      dragDay: null,
      dragStart: null,
      dragEnd: null,

      // 팝업 상태
      showPopup: false,
      newSubject: '',
      inputError: false,
      selectedColor: COLORS[0],

      showToast: false,
      toastTimer: null,
    }
  },
  computed: {
    popupRangeText() {
      if (this.dragDay === null || this.dragStart === null) return ''
      const lo = Math.min(this.dragStart, this.dragEnd ?? this.dragStart)
      const hi = Math.max(this.dragStart, this.dragEnd ?? this.dragStart)
      return `${this.dragDay}요일  ${lo}:00 ~ ${hi + 1}:00`
    },
  },
  async created() {
    if (this.initialEntries !== null) {
      this.entries = this.initialEntries
      this.loading = false
    } else {
      await this.fetchEntries()
    }
  },
  methods: {
    async fetchEntries() {
      const token = localStorage.getItem('token')
      if (!token) return
      try {
        const res = await axios.get('http://127.0.0.1:8000/timetable/me', {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.entries = res.data
      } finally {
        this.loading = false
      }
    },

    getEntry(day, hour) {
      return this.entries.find(
        e => e.day === day && hour >= e.start_hour && hour <= e.end_hour
      ) || null
    },

    isDragging(day, hour) {
      if (!this.dragging || this.dragDay !== day) return false
      const lo = Math.min(this.dragStart, this.dragEnd ?? this.dragStart)
      const hi = Math.max(this.dragStart, this.dragEnd ?? this.dragStart)
      return hour >= lo && hour <= hi
    },

    // ── 드래그 ──────────────────────────────────────────
    onMouseDown(day, hour) {
      if (!this.editMode || this.getEntry(day, hour)) return
      this.dragging = true
      this.dragDay = day
      this.dragStart = hour
      this.dragEnd = hour
    },

    onMouseEnter(day, hour) {
      if (!this.dragging || this.dragDay !== day) return
      if (this.getEntry(day, hour)) return
      this.dragEnd = hour
    },

    onMouseUp() {
      if (!this.dragging) return
      this.dragging = false
      if (this.dragStart !== null) {
        this.newSubject = ''
        this.inputError = false
        this.selectedColor = COLORS[0]
        this.showPopup = true
        this.$nextTick(() => this.$refs.subjectInputRef?.focus())
      }
    },

    onGridLeave() {
      // 그리드 벗어나면 드래그 취소
      if (this.dragging) {
        this.dragging = false
        this.dragDay = null
        this.dragStart = null
        this.dragEnd = null
      }
    },

    // ── 저장 / 삭제 ─────────────────────────────────────
    async saveEntry() {
      if (!this.newSubject.trim()) {
        this.inputError = true
        setTimeout(() => (this.inputError = false), 800)
        this.$refs.subjectInputRef?.focus()
        return
      }
      const lo = Math.min(this.dragStart, this.dragEnd ?? this.dragStart)
      const hi = Math.max(this.dragStart, this.dragEnd ?? this.dragStart)
      const token = localStorage.getItem('token')
      try {
        const res = await axios.post(
          'http://127.0.0.1:8000/timetable/me',
          {
            day: this.dragDay,
            start_hour: lo,
            end_hour: hi,
            subject_name: this.newSubject.trim(),
            color_bg: this.selectedColor.bg,
            color_fg: this.selectedColor.fg,
          },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.entries.push(res.data)
        this.closePopup()
      } catch {
        // 저장 실패 시 팝업 유지
      }
    },

    async deleteEntry(id) {
      const token = localStorage.getItem('token')
      try {
        await axios.delete(`http://127.0.0.1:8000/timetable/me/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.entries = this.entries.filter(e => e.id !== id)
        this.triggerToast()
      } catch {
        // 삭제 실패 무시
      }
    },

    closePopup() {
      this.showPopup = false
      this.dragDay = null
      this.dragStart = null
      this.dragEnd = null
    },

    triggerToast() {
      this.showToast = true
      clearTimeout(this.toastTimer)
      this.toastTimer = setTimeout(() => (this.showToast = false), 2000)
    },

    toggleEdit() {
      this.editMode = !this.editMode
      if (!this.editMode) this.closePopup()
    },
  },
}
</script>

<style scoped>
/* ── 카드 헤더 ─────────────────────────────────────── */
.tt-card-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px;
}
.tt-card-header h3 { font-size: 18px; font-weight: 700; margin: 0; }

.tt-edit-btn {
  background: #004ea2; color: white; border: none;
  padding: 7px 16px; border-radius: 10px; font-size: 13px;
  font-weight: 700; cursor: pointer; transition: background 0.2s;
}
.tt-edit-btn:hover { background: #003a85; }
.tt-readonly-badge { background: #fef3c7; color: #92400e; padding: 4px 12px; border-radius: 10px; font-size: 12px; font-weight: 700; }
.tt-edit-btn.active { background: #e53e3e; }
.tt-edit-btn.active:hover { background: #c53030; }

/* ── 힌트 ──────────────────────────────────────────── */
.tt-hint {
  background: #f0f7ff; border-radius: 12px; padding: 8px 16px;
  font-size: 12px; color: #4a5568; margin-bottom: 14px;
  display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;
}
.hint-divider { color: #cbd5e0; }

/* ── 로딩 ──────────────────────────────────────────── */
.tt-loading { text-align: center; padding: 40px 0; }
.spinner {
  width: 32px; height: 32px; border: 3px solid #edf2f7;
  border-top-color: #004ea2; border-radius: 50%;
  animation: spin 1s linear infinite; margin: 0 auto;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── 그리드 래퍼 ────────────────────────────────────── */
.tt-wrapper { overflow-x: auto; }

.tt-grid {
  display: grid;
  grid-template-columns: 42px repeat(5, 1fr);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  overflow: hidden;
  min-width: 380px;
  user-select: none;
  -webkit-user-select: none;
}

/* ── 헤더 ──────────────────────────────────────────── */
.tt-header {
  background: #004ea2; color: white;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; padding: 8px 4px;
}
.tt-time-header { background: #003a85; }

/* ── 시간 라벨 ─────────────────────────────────────── */
.tt-time-label {
  background: #f7fafc; border-right: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; color: #a0aec0; font-weight: 600; padding: 4px;
}

/* ── 셀 ────────────────────────────────────────────── */
.tt-cell {
  border-right: 1px solid #edf2f7;
  border-bottom: 1px solid #edf2f7;
  position: relative; height: 44px;
  transition: background 0.1s;
}
.tt-cell.hoverable:hover { background: #f0f7ff; cursor: cell; }
.tt-cell.dragging { background: #bfdbfe !important; }

/* ── 수업 블록 ─────────────────────────────────────── */
.tt-block {
  position: absolute; inset: 2px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700; text-align: center;
  padding: 2px 6px; line-height: 1.3; overflow: hidden;
  transition: filter 0.15s;
}
.edit-active .tt-block { cursor: pointer; }
.edit-active .tt-block:hover { filter: brightness(0.88); }

.tt-delete-btn {
  position: absolute; top: 3px; right: 3px;
  background: rgba(0, 0, 0, 0.2); color: white;
  border: none; border-radius: 50%;
  width: 15px; height: 15px; font-size: 10px; line-height: 15px;
  text-align: center; cursor: pointer; display: none;
  transition: background 0.15s;
}
.tt-delete-btn:hover { background: #e53e3e; }
.edit-active .tt-block:hover .tt-delete-btn { display: block; }

/* ── 팝업 ──────────────────────────────────────────── */
.tt-popup-overlay {
  position: fixed; inset: 0; background: rgba(0, 0, 0, 0.25);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.tt-popup {
  background: white; border-radius: 20px; padding: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  width: 290px; animation: popIn 0.18s ease;
}
@keyframes popIn {
  from { transform: scale(0.92); opacity: 0; }
  to   { transform: scale(1);    opacity: 1; }
}
.tt-popup-title { font-size: 16px; font-weight: 800; margin-bottom: 4px; color: #1a202c; }
.tt-popup-range { font-size: 12px; color: #a0aec0; margin-bottom: 16px; }
.tt-popup-label { display: block; font-size: 12px; font-weight: 700; color: #4a5568; margin-bottom: 6px; margin-top: 14px; }
.tt-popup-input {
  width: 100%; background: #f7fafc; border: 2px solid #e2e8f0;
  border-radius: 12px; padding: 10px 14px; font-size: 14px;
  outline: none; transition: border 0.2s; color: #1a202c; box-sizing: border-box;
}
.tt-popup-input:focus { border-color: #004ea2; background: white; }
.tt-popup-input.error { border-color: #e53e3e; }

.tt-palette { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 4px; }
.tt-palette-dot {
  width: 28px; height: 28px; border-radius: 50%; cursor: pointer;
  border: 3px solid transparent; transition: transform 0.15s, border-color 0.15s;
}
.tt-palette-dot.selected { transform: scale(1.2); }

.tt-popup-actions { display: flex; gap: 8px; margin-top: 20px; }
.tt-btn-save {
  flex: 1; background: #004ea2; color: white; border: none;
  padding: 12px; border-radius: 12px; font-weight: 700;
  font-size: 14px; cursor: pointer; transition: background 0.2s;
}
.tt-btn-save:hover { background: #003a85; }
.tt-btn-cancel {
  flex: 1; background: #f7fafc; color: #718096;
  border: 1px solid #e2e8f0; padding: 12px; border-radius: 12px;
  font-weight: 700; font-size: 14px; cursor: pointer;
}

/* ── 토스트 ────────────────────────────────────────── */
.tt-toast {
  position: fixed; bottom: 32px; left: 50%; transform: translateX(-50%);
  background: #1a202c; color: white; padding: 10px 20px;
  border-radius: 12px; font-size: 13px; font-weight: 600;
  z-index: 1100; pointer-events: none;
}
.toast-fade-enter-active, .toast-fade-leave-active { transition: opacity 0.3s; }
.toast-fade-enter-from, .toast-fade-leave-to { opacity: 0; }
</style>
