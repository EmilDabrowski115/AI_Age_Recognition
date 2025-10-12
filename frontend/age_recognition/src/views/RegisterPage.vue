<template>
  <div class="register-page">
    <!-- Animated Background -->
    <div class="animated-bg">
      <div class="grid-overlay"></div>
      <div class="floating-particles">
        <div class="particle" v-for="n in 15" :key="n" :style="getParticleStyle(n)"></div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="nav">
      <div class="nav-brand">
        <router-link to="/" class="brand-link">
          <h1 class="brand-text">AI Age Recognition</h1>
        </router-link>
      </div>
      <div class="nav-actions">
        <router-link to="/" class="nav-button">
          <span class="button-text">Back to Home</span>
          <div class="button-glow"></div>
        </router-link>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <div class="register-container">
        <div class="register-header">
          <h1 class="register-title">Create Your Account</h1>
          <p class="register-subtitle">Join the future of secure age verification</p>
        </div>

        <form @submit.prevent="handleSubmit" class="register-form">
          <div class="form-group">
            <label for="firstName" class="form-label">First Name</label>
            <input
              type="text"
              id="firstName"
              v-model="formData.firstName"
              class="form-input"
              :class="{ 'error': errors.firstName }"
              placeholder="Enter your first name"
              required
            />
            <span v-if="errors.firstName" class="error-message">{{ errors.firstName }}</span>
          </div>

          <div class="form-group">
            <label for="lastName" class="form-label">Last Name</label>
            <input
              type="text"
              id="lastName"
              v-model="formData.lastName"
              class="form-input"
              :class="{ 'error': errors.lastName }"
              placeholder="Enter your last name"
              required
            />
            <span v-if="errors.lastName" class="error-message">{{ errors.lastName }}</span>
          </div>

          <div class="form-group">
            <label for="email" class="form-label">Email Address</label>
            <input
              type="email"
              id="email"
              v-model="formData.email"
              class="form-input"
              :class="{ 'error': errors.email }"
              placeholder="Enter your email address"
              required
            />
            <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
          </div>

          <div class="form-group">
            <label for="phone" class="form-label">Phone Number</label>
            <input
              type="tel"
              id="phone"
              v-model="formData.phone"
              class="form-input"
              :class="{ 'error': errors.phone }"
              placeholder="Enter your phone number"
              required
            />
            <span v-if="errors.phone" class="error-message">{{ errors.phone }}</span>
          </div>

          <div class="form-group">
            <label for="birthDate" class="form-label">Birth Date</label>
            <div class="birth-date-container">
              <input
                type="date"
                id="birthDate"
                v-model="formData.birthDate"
                class="form-input birth-date-input"
                :class="{ 'error': errors.birthDate }"
                required
              />
              <button
                type="button"
                @click="verifyAge"
                class="verify-button"
                :disabled="!formData.birthDate || isVerifying"
              >
                <span v-if="!isVerifying" class="verify-text">Verify Age</span>
                <span v-else class="verify-text">Verifying...</span>
                <div class="verify-glow"></div>
                <div class="verify-icon">🔍</div>
              </button>
            </div>
            <span v-if="errors.birthDate" class="error-message">{{ errors.birthDate }}</span>
            <div v-if="ageVerification" class="verification-result">
              <div class="verification-success" v-if="ageVerification.success">
                <span class="success-icon">✅</span>
                <span class="success-text">Age verified: {{ ageVerification.age }} years old</span>
              </div>
              <div class="verification-error" v-else>
                <span class="error-icon">❌</span>
                <span class="error-text">{{ ageVerification.message }}</span>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              id="password"
              v-model="formData.password"
              class="form-input"
              :class="{ 'error': errors.password }"
              placeholder="Create a secure password"
              required
            />
            <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
          </div>

          <div class="form-group">
            <label for="confirmPassword" class="form-label">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="formData.confirmPassword"
              class="form-input"
              :class="{ 'error': errors.confirmPassword }"
              placeholder="Confirm your password"
              required
            />
            <span v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</span>
          </div>

          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input
                type="checkbox"
                v-model="formData.agreeTerms"
                class="checkbox-input"
                required
              />
              <span class="checkbox-custom"></span>
              <span class="checkbox-text">
                I agree to the <a href="#" class="terms-link">Terms of Service</a> and 
                <a href="#" class="terms-link">Privacy Policy</a>
              </span>
            </label>
            <span v-if="errors.agreeTerms" class="error-message">{{ errors.agreeTerms }}</span>
          </div>

          <button
            type="submit"
            class="submit-button"
            :disabled="!isFormValid || isSubmitting"
          >
            <span v-if="!isSubmitting" class="submit-text">Create Account</span>
            <span v-else class="submit-text">Creating Account...</span>
            <div class="submit-glow"></div>
            <div class="submit-arrow">→</div>
          </button>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
// import apiService from '../services/api.js'

const router = useRouter()

const formData = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  birthDate: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

const errors = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  birthDate: '',
  password: '',
  confirmPassword: '',
  agreeTerms: ''
})

const isSubmitting = ref(false)
const isVerifying = ref(false)
const ageVerification = ref(null)

const isFormValid = computed(() => {
  return formData.firstName && 
         formData.lastName && 
         formData.email && 
         formData.phone && 
         formData.birthDate && 
         formData.password && 
         formData.confirmPassword && 
         formData.agreeTerms &&
         Object.values(errors).every(error => !error)
})

const getParticleStyle = (index) => {
  const delay = Math.random() * 5
  const duration = 3 + Math.random() * 4
  const size = 2 + Math.random() * 3
  const left = Math.random() * 100
  
  return {
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`,
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`
  }
}

const validateForm = () => {
  // Clear previous errors
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })

  let isValid = true

  // First name validation
  if (!formData.firstName.trim()) {
    errors.firstName = 'First name is required'
    isValid = false
  }

  // Last name validation
  if (!formData.lastName.trim()) {
    errors.lastName = 'Last name is required'
    isValid = false
  }

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!formData.email.trim()) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!emailRegex.test(formData.email)) {
    errors.email = 'Please enter a valid email address'
    isValid = false
  }

  // Phone validation
  const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/
  if (!formData.phone.trim()) {
    errors.phone = 'Phone number is required'
    isValid = false
  } else if (!phoneRegex.test(formData.phone.replace(/\s/g, ''))) {
    errors.phone = 'Please enter a valid phone number'
    isValid = false
  }

  // Birth date validation
  if (!formData.birthDate) {
    errors.birthDate = 'Birth date is required'
    isValid = false
  } else {
    const birthDate = new Date(formData.birthDate)
    const today = new Date()
    const age = today.getFullYear() - birthDate.getFullYear()
    
    if (age < 13) {
      errors.birthDate = 'You must be at least 13 years old to register'
      isValid = false
    } else if (age > 120) {
      errors.birthDate = 'Please enter a valid birth date'
      isValid = false
    }
  }

  // Password validation
  if (!formData.password) {
    errors.password = 'Password is required'
    isValid = false
  } else if (formData.password.length < 8) {
    errors.password = 'Password must be at least 8 characters long'
    isValid = false
  }

  // Confirm password validation
  if (!formData.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password'
    isValid = false
  } else if (formData.password !== formData.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  // Terms agreement validation
  if (!formData.agreeTerms) {
    errors.agreeTerms = 'You must agree to the terms and conditions'
    isValid = false
  }

  return isValid
}

const verifyAge = async () => {
  if (!formData.birthDate) return

  isVerifying.value = true
  ageVerification.value = null

  try {
    const result = await apiService.verifyAge(formData.birthDate)
    ageVerification.value = result
  } catch (error) {
    ageVerification.value = {
      success: false,
      message: 'Age verification failed. Please try again.'
    }
  } finally {
    isVerifying.value = false
  }
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isSubmitting.value = true

  try {
    const result = await apiService.registerUser(formData)
    console.log('Registration successful:', result)
    
    // Redirect to success page or dashboard
    router.push('/')
  } catch (error) {
    console.error('Registration failed:', error)
    // Handle registration error
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  color: #ffffff;
  position: relative;
  overflow-x: hidden;
}

/* Animated Background */
.animated-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(0, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: grid-move 20s linear infinite;
}

@keyframes grid-move {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

.floating-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  background: radial-gradient(circle, rgba(0, 255, 255, 0.6) 0%, transparent 70%);
  border-radius: 50%;
  animation: float infinite ease-in-out;
}

@keyframes float {
  0%, 100% { 
    transform: translateY(100vh) scale(0);
    opacity: 0;
  }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { 
    transform: translateY(-100px) scale(1);
    opacity: 0;
  }
}

/* Navigation */
.nav {
  position: relative;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 4rem;
  backdrop-filter: blur(10px);
  background: rgba(0, 0, 0, 0.3);
}

.brand-link {
  text-decoration: none;
}

.brand-text {
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-button {
  position: relative;
  padding: 0.8rem 2rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  border: none;
  border-radius: 50px;
  color: #000;
  text-decoration: none;
  font-weight: 600;
  overflow: hidden;
  transition: all 0.3s ease;
}

.nav-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 255, 255, 0.3);
}

.button-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.nav-button:hover .button-glow {
  left: 100%;
}

/* Main Content */
.main-content {
  position: relative;
  z-index: 5;
  padding: 2rem 4rem 4rem;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px);
}

.register-container {
  width: 100%;
  max-width: 600px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 20px;
  padding: 3rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.register-header {
  text-align: center;
  margin-bottom: 3rem;
}

.register-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.register-subtitle {
  color: #cccccc;
  font-size: 1.1rem;
}

/* Form Styles */
.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #00ffff;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input {
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 10px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.form-input:focus {
  outline: none;
  border-color: #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.15);
}

.form-input::placeholder {
  color: #888;
}

.form-input.error {
  border-color: #ff4444;
  box-shadow: 0 0 20px rgba(255, 68, 68, 0.2);
}

.error-message {
  color: #ff4444;
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

/* Birth Date Container */
.birth-date-container {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
}

.birth-date-input {
  flex: 1;
}

.verify-button {
  position: relative;
  padding: 1rem 1.5rem;
  background: linear-gradient(45deg, #ff00ff, #00ffff);
  border: none;
  border-radius: 10px;
  color: #000;
  font-weight: 600;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}

.verify-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(255, 0, 255, 0.3);
}

.verify-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.verify-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.verify-button:hover:not(:disabled) .verify-glow {
  left: 100%;
}

.verify-icon {
  font-size: 1rem;
}

/* Verification Result */
.verification-result {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.verification-success {
  background: rgba(0, 255, 0, 0.1);
  border: 1px solid rgba(0, 255, 0, 0.3);
  color: #00ff00;
}

.verification-error {
  background: rgba(255, 0, 0, 0.1);
  border: 1px solid rgba(255, 0, 0, 0.3);
  color: #ff4444;
}

.success-icon, .error-icon {
  font-size: 1.2rem;
}

/* Checkbox Styles */
.checkbox-group {
  margin-top: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  cursor: pointer;
}

.checkbox-input {
  display: none;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(0, 255, 255, 0.5);
  border-radius: 4px;
  background: transparent;
  position: relative;
  transition: all 0.3s ease;
  flex-shrink: 0;
  margin-top: 2px;
}

.checkbox-input:checked + .checkbox-custom {
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  border-color: #00ffff;
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #000;
  font-weight: bold;
  font-size: 12px;
}

.checkbox-text {
  color: #cccccc;
  line-height: 1.5;
}

.terms-link {
  color: #00ffff;
  text-decoration: none;
}

.terms-link:hover {
  text-decoration: underline;
}

/* Submit Button */
.submit-button {
  position: relative;
  padding: 1.2rem 3rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  border: none;
  border-radius: 50px;
  color: #000;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(0, 255, 255, 0.4);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.submit-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.6s ease;
}

.submit-button:hover:not(:disabled) .submit-glow {
  left: 100%;
}

.submit-arrow {
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.submit-button:hover:not(:disabled) .submit-arrow {
  transform: translateX(5px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .nav {
    padding: 1rem 2rem;
  }
  
  .main-content {
    padding: 1rem 2rem 2rem;
  }
  
  .register-container {
    padding: 2rem;
  }
  
  .register-title {
    font-size: 2rem;
  }
  
  .birth-date-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .verify-button {
    justify-content: center;
  }
}
</style>
