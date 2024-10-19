import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import { auth } from '../_actions/user_action';
import { useNavigate } from 'react-router-dom'// react 에서 href역할

const Auth = (SpecificComponent, option, adminRoute = null) => {

    function AutenticationCheck() {
        //redux사용
        const dispatch = useDispatch()
        const navigate = useNavigate();//react 에서 href역할

        //server로부터 state정보 받기
        //server에서 미들웨어 auth로 가서
        //거기서 쿠키에 있는token을 이용해서 
        //쿠키에 토큰이 있으면 로그인한 유저 
        //쿠키에 토큰이 없으면 로그인안한 유저
        //그 결과를 react에 전잘함 
        useEffect(() => {
            //redux
            //server에서 가져온 정보는 response안에 다 들어있다.
            dispatch(auth()).then(response => {
                console.log(response)

                //즉, 인증이 완료되지 않은 유저는 접근못하게 하기
                //로그인 하지 않은 상태
                if (!response.action.payload.isAuth) {
                    if (option) {// option=== true 랑 같은 뜻
                        //로그인 하지 않았기 때문에 login page로 보내버림
                        navigate('/login')
                    }
                }
                else {
                    //로그인 한 상태

                    if (adminRoute && !response.action.payload.isAdmin) {
                        //admin이 아닌데admin만 들어갈 수 있는 사이트에 들어가려고 할 때
                        //main으로 보내버림
                        navigate('/')
                    }
                    else {
                        //로그인 한 유저가 출입불가능한 페이지(로그인페이지,회원가입페이지 등)
                        if (option === false) {
                            navigate('/')
                        }
                    }
                }

            })
        }, [])

        return <SpecificComponent />
    }
    return AutenticationCheck
}
export default Auth