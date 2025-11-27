import apiClient from "@/services/abstract/ApiClient.js";

class UserPanelService {
    async register(data) {
        const response = await apiClient.post(`/signup`, data)
        console.log('response',response)
        return response.data;
    }

    async login(data) {
        const response = await apiClient.post(`/login`, data)
        console.log('response',response)
        return response.data;
    }

}
export default new UserPanelService();