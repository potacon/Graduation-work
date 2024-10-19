//redux의 action 부분
//즉 dispatch로 부터 데이터를 받고
//Reducer에게 보내주는 부분


import axios from 'axios'

import {
    LOGIN_USER,
    REGISTER_USER,
    AUTH_USER
} from './types.js' //type을 types.js에서 가지고오기

//Login
//dataTosubmit에 LoginPage의 email, pwd를 받음
export function loginUser(dataTosubmit) {

    const request = axios.post('/api/users/login', dataTosubmit)//서버 /login에 request를 날린 다음
        .then(response => response.data)// 서버에 받은 data를 request에 저장시킨다.

    //request를 reduer로 보내야한다.
    //redux정리한 곳에 action에 관한 설명 참고하기
    return {
        type: LOGIN_USER, //type: 'like_article', articleId:42
        payload: request //type:'FETCH_USER_SUCCESS', RESPONSE:{id:3, name:'mary'}

    }
}

//회원가입
export function registerUser(dataTosubmit) {

    const request = axios.post('/api/users/register', dataTosubmit)//서버 /login에 request를 날린 다음
        .then(response => response.data)// 서버에 받은 data를 request에 저장시킨다.

    //request를 reduer로 보내야한다.
    //redux정리한 곳에 action에 관한 설명 참고하기
    return {
        type: REGISTER_USER,
        payload: request

    }
}

//auth 인증체크
//get메소드여서 body(dataTosubmit)가 필요없다.
//action 다음 reducer로 가기
export function auth() {

    const request = axios.get('/api/users/auth')//서버 /login에 request를 날린 다음
        .then(response => response.data)// 서버에 받은 data를 request에 저장시킨다.

    //request를 reduer로 보내야한다.
    //redux정리한 곳에 action에 관한 설명 참고하기
    return {
        type: AUTH_USER,
        payload: request

    }
}

/*
import axios from 'axios';
import {
    LOGIN_USER,
    REGISTER_USER,
    AUTH_USER
} from './types';
export function loginUser(dataToSubmit) {

    const request = axios.post('/api/users/login', dataToSubmit)
        .then(response => {response.data})

    return {
        type: LOGIN_USER,
        payload: request
    }
}

export function registerUser(dataToSubmit) {

    const request = axios.post('/api/users/register', dataToSubmit)
        .then(response => {response.data})

    return {
        type: REGISTER_USER,
        payload: request
    }
}



export function auth() {

    const request = axios.get('/api/users/auth')
        .then(response => response.data)

    return {
        type: AUTH_USER,
        payload: request
    }
}
*/