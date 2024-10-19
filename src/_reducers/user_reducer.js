//redux의 action 다음인 reducer 부분
//Reducer에서는 이전state, 현재action을 이용해서 다음 state를 만들어줌
import {
    LOGIN_USER, REGISTER_USER, AUTH_USER
} from '../_actions/types.js'//type 가지고오기

//state=전 state / action=현재 state
export default function (state = {}, action) {
    //switch사용이유는 action에서 return해서 받은 type이 여러개 있기 때문이다.
    switch (action.type) {//현재 액션의 type
        //login
        case LOGIN_USER:
            return {
                ...state, // ...값(spread operator): 그 값을 그대로 가져오겠다라는 의미
                loginSuccess: action.payload
            }
            break;
        //회원가입
        case REGISTER_USER:
            return {
                ...state,
                regiser: action.payload
            }
            break;
        //AUTH 인증체크
        case AUTH_USER:
            return {
                ...state,
                userData: action.payload
                //즉, action.payload에 유저 id,name,email,isAdmin,image 등등 모든 데이터가 다 들어있음
            }
            break;
        default:
            return state;
    }
}