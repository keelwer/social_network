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
        return instance.get(`profile/` + userId);
    }
};

export const authAPI = {
    me() {
        return instance.get(`auth/me`);
    }
};