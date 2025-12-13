<template>
  <div class="register-page">
    <div class="register-container">
      <h1>Age Verification</h1>

      <!-- Age verification form -->
      <form @submit.prevent="handleVerifyAge" class="register-form" v-if="!ageVerified">
        <div class="form-group">
          <label for="image">Upload your photo</label>
          <p class="hint">Please upload a clear photo with your face visible. Make sure only one face is in the photo.</p>
          <input
              id="image"
              type="file"
              accept="image/*"
              @change="handleFileChange"
              required
              class="form-input"
          />
        </div>

        <!-- Photo preview -->
        <div v-if="preview" class="preview-box">
          <img :src="preview" alt="Preview" class="preview-img" />
        </div>

        <!-- Error message display -->
        <div v-if="errorMessage" class="error-box">
          <p>{{ errorMessage }}</p>
        </div>

        <button
            type="submit"
            class="submit-button"
            :disabled="isVerifying || !file"
        >
          <span v-if="!isVerifying">Verify Age</span>
          <span v-else>Verifying...</span>
        </button>
      </form>

      <!-- After age verified -->
      <div v-if="ageVerified">
        <div class="verification-result">
          <h2>Verification Complete</h2>
          <p class="age-result">Predicted Age: <strong>{{ userAge }}</strong> years</p>
          <p class="confidence-result">Confidence: <strong>{{ (confidence * 100).toFixed(1) }}%</strong></p>
        </div>
        <p v-if="isOldEnough" class="status-message success">
          ✓ You are old enough to register.
        </p>
        <p v-else class="status-message error">
          ✗ You are not old enough to register (must be 18+).
        </p>

        <!-- Registration form only if old enough -->
        <div v-if="isOldEnough">
          <h1>Create Account</h1>
          <form @submit.prevent="handleRegister" class="register-form">
            <div class="form-group">
              <label for="username">Username</label>
              <input
                  id="username"
                  type="text"
                  v-model="formData.username"
                  required
                  class="form-input"
              />
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <input
                  id="password"
                  type="password"
                  v-model="formData.password"
                  required
                  class="form-input"
              />
            </div>

            <button type="submit" class="submit-button" :disabled="isRegistering">
              <span v-if="!isRegistering">Register</span>
              <span v-else>Registering...</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import userService from '../services/userService.js'

const router = useRouter()

const file = ref(null)
const preview = ref(null)

const isVerifying = ref(false)
const isRegistering = ref(false)

const ageVerified = ref(false)
const userAge = ref(null)
const isOldEnough = ref(false)
const confidence = ref(null)
const errorMessage = ref(null)

const formData = reactive({
  username: '',
  password: ''
})

const handleFileChange = (event) => {
  const selected = event.target.files[0]
  file.value = selected
  if (selected) {
    preview.value = URL.createObjectURL(selected)
  }
}

const handleVerifyAge = async () => {
  if (!file.value) return

  isVerifying.value = true
  errorMessage.value = null

  const formDataForAge = new FormData()
  formDataForAge.append('file', file.value)  // Backend expects 'file' not 'image'

  try {
    // Use a temporary user_id (1) for now - in production, get this from auth
    const response = await userService.ageVerify(formDataForAge, 1)

    console.log('Age verification response:', response)

    if (response.success) {
      userAge.value = response.predicted_age
      confidence.value = response.confidence
      ageVerified.value = true
      isOldEnough.value = userAge.value >= 18 // minimum age limit
    } else {
      throw new Error(response.error || 'Verification failed')
    }
  } catch (err) {
    console.error('Verification failed:', err)

    // Extract error message from API response
    const errMsg = err.response?.data?.detail || err.message || 'Age verification failed. Please try again.'
    errorMessage.value = errMsg
    alert(errMsg)
  } finally {
    isVerifying.value = false
  }
}

const handleRegister = async () => {
  isRegistering.value = true
  try {
    await userService.register({
      username: formData.username,
      password: formData.password
    })
    router.push('/')
  } catch (err) {
    console.error('Registration failed:', err)
    alert('Registration failed. Please try again.')
  } finally {
    isRegistering.value = false
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
  background: rgba(255, 255, 255, 0.08);
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

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.verification-result {
  background: rgba(0, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1rem 0;
  border: 1px solid #00ffff;
}

.verification-result h2 {
  margin-top: 0;
  color: #00ffff;
  font-size: 1.3rem;
}

.age-result,
.confidence-result {
  font-size: 1.1rem;
  margin: 0.5rem 0;
}

.status-message {
  padding: 1rem;
  border-radius: 6px;
  margin: 1rem 0;
  font-weight: bold;
  font-size: 1.1rem;
}

.status-message.success {
  background: rgba(0, 255, 0, 0.2);
  color: lightgreen;
  border: 1px solid lightgreen;
}

.status-message.error {
  background: rgba(255, 0, 0, 0.2);
  color: tomato;
  border: 1px solid tomato;
}

.hint {
  font-size: 0.85rem;
  color: #aaa;
  margin: 0.3rem 0;
}

.error-box {
  background: rgba(255, 0, 0, 0.2);
  border: 1px solid tomato;
  padding: 1rem;
  border-radius: 6px;
  margin: 1rem 0;
  color: tomato;
}
</style>
