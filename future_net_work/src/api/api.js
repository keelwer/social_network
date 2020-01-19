import * as axios from "axios";

const instance = axios.create({
    withCredentials: true,
    baseURL: 'https://social-network.samuraijs.com/api/1.0/',
    headers: {"API-KEY": "5ffffc5c-ac7f-444a-ad2c-673d8d1f9696"}
});

export const userAPI = {
    getUsers(currentPage, pageSize) {
        debugger;
        return instance.get(`users?page=${currentPage}&count=${pageSize}`)
            .then(response => {return response.data})
    },
    follow(useId){
        return instance.post(`https://social-network.samuraijs.com/api/1.0/follow/${useId}`)
    },
    unfollow(useId){
        return instance.delete(`https://social-network.samuraijs.com/api/1.0/follow/${useId}`)
    },
};
// export const userAPI = (currentPage, pageSize) => {
//     return axios.get(`users?page=${currentPage}&count=${pageSize}`,
//         {
//             withCredentials: true
//         }).then(response => {return response.data});
// }