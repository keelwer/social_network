import * as axios from "axios";

const instance = axios.create({
    withCredentials: true,
    baseURL: 'https://social-network.samuraijs.com/api/1.0/',
    headers: {"API-KEY": "5ffffc5c-ac7f-444a-ad2c-673d8d1f9696"}
});

export const userAPI = {
    getUsers(currentPage, pageSize) {
        return instance.get(`users?page=${currentPage}&count=${pageSize}`)
            .then(response => {
                return response.data
            })
    },
    follow(useId) {
        return instance.post(`follow/${useId}`)
    },
    unfollow(useId) {
        return instance.delete(`follow/${useId}`)
    },
    getProfile(userId) {
        console.warn('Old method')
        return profileAPI.getProfile(userId);
    }
};


export const profileAPI = {
    getProfile(userId) {
        return instance.get(`profile/` + userId);
    },
    getStatus(userId){
        return instance.get(`profile/status/` + userId);
    },
    updateStatus(status){
        return instance.put(`profile/status`, {status: status});
    },
};

export const authAPI = {
    me() {
        return instance.get(`auth/me`);
    },
    login(email, password, rememberMe = false) {
        return instance.post(`auth/login`, { email, password, rememberMe });
    },
    logout() {
        return instance.delete(`auth/login`);
    },
};
