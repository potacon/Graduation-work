import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import FormControlLabel from '@mui/material/FormControlLabel';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import './App.css';
import { useState } from 'react';
import { Axios } from 'axios';
import React from 'react'
import { Email, Password } from '@mui/icons-material';
//import { response } from 'express';
import { useDispatch } from 'react-redux';
import { loginUser } from '../_actions/user_action';
import { useNavigate } from 'react-router-dom';
//자동완성 기능 사용할꺼면 autoComplete="email", autoComplete="password" 기입
import Auth from '../hoc/auth';

function Login(props) {

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const [name, setName] = useState("");
    const [Email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [Passwordcheck, setPasswordcheck] = useState("");
    const [startDate, setStartDate] = useState(new Date());

    const onEmailHandler = (event) => {
        setEmail(event.currentTarget.value)

        console.log('email', Email) //email state가 궁금하면 콘솔로 찍어보기
    }

    //pwd state 변경
    const onPasswordHandler = (event) => {
        setPassword(event.currentTarget.value)//이 코드를 안해주면 버튼클릭시마다 "새로고침"이 된다.

        console.log('pwd', Password) //password state가 궁금하면 콘솔로 찍어보기
    }

    const onSubmitHandler = (event) => {
        event.preventDefault();

        let body = {
            email: Email,
            password: password
        }

        dispatch(loginUser(body))
            .then(response => {
                console.log(response.action.payload.loginSuccess)
                if (response.action.payload.loginSuccess) {
                    navigate('/');
                }
                else {
                    alert('error')
                }
            })
    }

    return (
        <Container component="main" maxWidth="xs" onSubmit={onSubmitHandler}>
            <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center', }} >
                <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    로그인
                </Typography>
                <TextField margin="normal" label="Email Address" required fullWidth name="email" autoFocus onChange={(event) => { setEmail(event.target.value); }} />
                <TextField margin="normal" label="Password" type="password" required fullWidth name="password" onChange={(event) => { setPassword(event.target.value); }} />
                <FormControlLabel control={<Checkbox value="remember" clolor="primary" />} label="계정 저장" />
                <Button type="submit" fullWidth variant='contained' sx={{ mt: 3, mb: 2 }} onClick={onSubmitHandler}>로그인</Button>
                <Grid container>
                    <Grid item xs>
                        <Link>비밀번호 찾기</Link>
                    </Grid>
                    <Grid item xs>
                        <Link>계정 만들기</Link>
                    </Grid>
                </Grid>
            </Box>
        </Container>
    );
}

export default Auth(Login, false)
