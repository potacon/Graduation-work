import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import Auth from '../../../hoc/auth';
import api from '../../../test/api';

function LandingPage() {

    const [data, setData] = useState([]);

    useEffect(() => {
        api.get('/data')
            .then(response => {
                setData(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }, []);

    const navigate = useNavigate();//react 에서 href역할

    useEffect(() => {
        axios.get('/api/test')// 이 부분이 get req를 server로 보내는부분이다.
            .then(response => console.log(response.data))
    }, [])

    //logout 이벤트 
    //redux 사용안하면 axios바로 사용
    const onClickHandler = (evnet) => {
        axios.get('/api/users/logout')
            .then(response => {
                if (response.data.success) {
                    navigate('/login')
                }
                else {
                    alert('로그아웃 실패')
                }
            })
    }

    return (
        <div style={{
            display: 'flex', justifyContent: 'center', alignItems: 'center'
            , width: '100%', height: '100vh'
        }}>
            <h2>시작 페이지</h2>

            <button onClick={onClickHandler}>
                로그아웃
            </button>

            <div>
                <h1>Data from Flask:</h1>
                <pre>{JSON.stringify(data, null, 2)}</pre>
            </div>
        </div>


    )
}

export default Auth(LandingPage, null)