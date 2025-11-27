<template>
  <div class="register-page">
    <div class="register-container">
      <h1>Age Verification</h1>

      <form @submit.prevent="handleSubmit" class="register-form">

        <div class="form-group">
          <label for="image">Upload your photo</label>
          <input
              id="image"
              type="file"
              accept="image/*"
              @change="handleFileChange"
              required
              class="form-input"
          />
        </div>

        <!-- PODGLĄD ZDJĘCIA -->
        <div v-if="preview" class="preview-box">
          <img :src="preview" alt="Preview" class="preview-img" />
        </div>

        <button type="submit" class="submit-button" :disabled="isSubmitting || !file">
          <span v-if="!isSubmitting">Verify Age</span>
          <span v-else>Verifying...</span>
        </button>

      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const file = ref(null)
const preview = ref(null)
const isSubmitting = ref(false)

const handleFileChange = (event) => {
  const selected = event.target.files[0]
  file.value = selected

  if (selected) {
    preview.value = URL.createObjectURL(selected)
  }
}

const handleSubmit = async () => {
  if (!file.value) return

  isSubmitting.value = true

  const formData = new FormData()
  formData.append('image', file.value)

  try {
    const response = await axios.post('/getAge', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    console.log('Age verification result:', response.data)

  } catch (err) {
    console.error('Verification failed:', err)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #111;
  color: white;
}

.register-container {
  background: rgba(255,255,255,0.08);
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 350px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-input {
  width: 100%;
  padding: 0.8rem;
  border-radius: 6px;
  border: none;
  margin-top: 0.3rem;
  background: #fff;
}

/* KWADRAT NA PODGLĄD ZDJĘCIA */
.preview-box {
  width: 200px;
  height: 200px;
  margin: 1rem auto;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #00ffff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.submit-button {
  width: 100%;
  padding: 1rem;
  background: #00ffff;
  border: none;
  border-radius: 6px;
  color: #000;
  font-weight: bold;
  cursor: pointer;
}
</style>
