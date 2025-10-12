<template>
  <div class="landing-page">
    <!-- Animated Background -->
    <div class="animated-bg">
      <div class="grid-overlay"></div>
      <div class="floating-particles">
        <div class="particle" v-for="n in 20" :key="n" :style="getParticleStyle(n)"></div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="nav">
      <div class="nav-brand">
        <h1 class="brand-text">AI Age Recognition</h1>
      </div>
      <div class="nav-actions">
        <router-link to="/register" class="nav-button">
          <span class="button-text">Register</span>
          <div class="button-glow"></div>
        </router-link>
      </div>
    </nav>

    <!-- Hero Section -->
    <main class="hero">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="main-title">
            <span class="title-line">Advanced</span>
            <span class="title-line">Age Recognition</span>
            <span class="title-line accent">Technology</span>
          </h1>
          <p class="hero-description">
            Experience the future of biometric verification with our cutting-edge AI-powered age recognition system. 
            Secure, accurate, and lightning-fast.
          </p>
          <div class="hero-actions">
            <router-link to="/register" class="cta-button">
              <span class="cta-text">Get Started</span>
              <div class="cta-glow"></div>
              <div class="cta-arrow">→</div>
            </router-link>
          </div>
        </div>
        
        <div class="hero-visual">
          <div class="tech-circle">
            <div class="circle-ring"></div>
            <div class="circle-ring"></div>
            <div class="circle-ring"></div>
            <div class="center-core">
              <div class="core-pulse"></div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Features Section -->
    <section class="features">
      <div class="features-container">
        <h2 class="features-title">Powered by Innovation</h2>
        <div class="features-grid">
          <div class="feature-card" v-for="feature in features" :key="feature.id">
            <div class="feature-icon">
              <div class="icon-bg"></div>
              <span class="icon-text">{{ feature.icon }}</span>
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 AI Age Recognition. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const features = ref([
  {
    id: 1,
    icon: '🧠',
    title: 'AI-Powered',
    description: 'Advanced machine learning algorithms for precise age detection'
  },
  {
    id: 2,
    icon: '⚡',
    title: 'Lightning Fast',
    description: 'Real-time processing with instant verification results'
  },
  {
    id: 3,
    icon: '🔒',
    title: 'Secure',
    description: 'Enterprise-grade security with encrypted data transmission'
  },
  {
    id: 4,
    icon: '📱',
    title: 'Cross-Platform',
    description: 'Works seamlessly across all devices and platforms'
  }
])

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
</script>

<style scoped>
.landing-page {
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
    linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
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
  background: radial-gradient(circle, rgba(0, 255, 255, 0.8) 0%, transparent 70%);
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

/* Hero Section */
.hero {
  position: relative;
  z-index: 5;
  min-height: 80vh;
  display: flex;
  align-items: center;
  padding: 0 4rem;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.main-title {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 2rem;
}

.title-line {
  display: block;
  opacity: 0;
  animation: slideInUp 0.8s ease forwards;
}

.title-line:nth-child(1) { animation-delay: 0.2s; }
.title-line:nth-child(2) { animation-delay: 0.4s; }
.title-line:nth-child(3) { animation-delay: 0.6s; }

.title-line.accent {
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-description {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #cccccc;
  margin-bottom: 3rem;
  opacity: 0;
  animation: fadeIn 1s ease 0.8s forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.cta-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 1rem;
  padding: 1.2rem 3rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  border: none;
  border-radius: 50px;
  color: #000;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.1rem;
  overflow: hidden;
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(0, 255, 255, 0.4);
}

.cta-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.6s ease;
}

.cta-button:hover .cta-glow {
  left: 100%;
}

.cta-arrow {
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.cta-button:hover .cta-arrow {
  transform: translateX(5px);
}

/* Hero Visual */
.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.tech-circle {
  position: relative;
  width: 300px;
  height: 300px;
}

.circle-ring {
  position: absolute;
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 50%;
  animation: rotate 10s linear infinite;
}

.circle-ring:nth-child(1) {
  width: 100%;
  height: 100%;
  animation-duration: 15s;
}

.circle-ring:nth-child(2) {
  width: 80%;
  height: 80%;
  top: 10%;
  left: 10%;
  animation-duration: 12s;
  animation-direction: reverse;
}

.circle-ring:nth-child(3) {
  width: 60%;
  height: 60%;
  top: 20%;
  left: 20%;
  animation-duration: 8s;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.center-core {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: radial-gradient(circle, rgba(0, 255, 255, 0.8) 0%, rgba(255, 0, 255, 0.4) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.core-pulse {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.7; }
}

/* Features Section */
.features {
  position: relative;
  z-index: 5;
  padding: 6rem 4rem;
  background: rgba(0, 0, 0, 0.2);
}

.features-container {
  max-width: 1400px;
  margin: 0 auto;
}

.features-title {
  text-align: center;
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 4rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.feature-card:hover {
  transform: translateY(-10px);
  border-color: rgba(0, 255, 255, 0.5);
  box-shadow: 0 20px 40px rgba(0, 255, 255, 0.1);
}

.feature-icon {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, rgba(0, 255, 255, 0.2), rgba(255, 0, 255, 0.2));
  border-radius: 50%;
  animation: iconPulse 3s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.icon-text {
  font-size: 2rem;
  z-index: 1;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #00ffff;
}

.feature-description {
  color: #cccccc;
  line-height: 1.6;
}

/* Footer */
.footer {
  position: relative;
  z-index: 5;
  padding: 2rem 4rem;
  text-align: center;
  background: rgba(0, 0, 0, 0.3);
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

.footer-content {
  color: #888;
}

/* Responsive Design */
@media (max-width: 768px) {
  .nav {
    padding: 1rem 2rem;
  }
  
  .hero {
    padding: 0 2rem;
  }
  
  .hero-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }
  
  .main-title {
    font-size: 2.5rem;
  }
  
  .tech-circle {
    width: 250px;
    height: 250px;
  }
  
  .features {
    padding: 4rem 2rem;
  }
  
  .features-title {
    font-size: 2rem;
  }
}
</style>
