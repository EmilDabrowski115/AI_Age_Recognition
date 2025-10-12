// API service for future backend integration
class ApiService {
  constructor() {
    this.baseURL = process.env.VUE_APP_API_URL || 'http://localhost:3000/api'
  }

  // Age verification endpoint (placeholder)
  async verifyAge(birthDate) {
    try {
      // This will be implemented when backend is ready
      console.log('Verifying age for:', birthDate)
      
      // Placeholder response
      return {
        success: true,
        age: this.calculateAge(birthDate),
        message: 'Age verification successful'
      }
    } catch (error) {
      console.error('Age verification error:', error)
      throw error
    }
  }

  // Calculate age from birth date
  calculateAge(birthDate) {
    const today = new Date()
    const birth = new Date(birthDate)
    let age = today.getFullYear() - birth.getFullYear()
    const monthDiff = today.getMonth() - birth.getMonth()
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--
    }
    
    return age
  }

  // User registration endpoint (placeholder)
  async registerUser(userData) {
    try {
      console.log('Registering user:', userData)
      
      // Placeholder response
      return {
        success: true,
        message: 'User registered successfully',
        userId: Math.random().toString(36).substr(2, 9)
      }
    } catch (error) {
      console.error('Registration error:', error)
      throw error
    }
  }
}

export default new ApiService()
