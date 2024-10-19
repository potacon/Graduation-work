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
import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { ko } from 'date-fns/esm/locale';
import './App.css';
import { useDispatch } from 'react-redux';
import { registerUser } from '../_actions/user_action';
import { Axios } from 'axios';
import { useNavigate } from 'react-router-dom';
import Auth from '../hoc/auth';

//자동완성 기능 사용할꺼면 autoComplete="email", autoComplete="password" 기입

function Sign_up(props) {
    const dispatch = useDispatch();
    const navigate = useNavigate();//react 에서 href역할

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [passwordcheck, setPasswordcheck] = useState("");
    const [startDate, setStartDate] = useState(new Date());

    const onEmailHandler = (event) => {
        setEmail(event.currentTarget.value)
    }

    const onPasswordHandler = (event) => {
        setPassword(event.currentTarget.value)
    }

    const onNameHandler = (event) => {
        setName(event.currentTarget.value)
    }

    const onsetPasswordcheckHandler = (event) => {
        setPasswordcheck(event.currentTarget.value)
    }

    const onstartdateHandler = (event) => {
        setStartDate(event.currentTarget.value)
    }

    const onSubmitHandler = (event) => {
        event.preventDefault();//이걸 안해주면 버튼클릭시 계속 새로고침이 일어남

        //현재 state에 무엇이 들었는지 console로 찍어봄
        console.log('email: ', email)
        console.log('pwd: ', password)
        console.log('name: ', name)
        console.log('passwordcheck: ', passwordcheck)

        //비밀번호와 비밀번호 확인 일치하지 않을 경우 error 메시지
        //즉 다음으로 못넘어감
        if (password !== passwordcheck) {
            return alert('비밀번호와 비밀번호 확인이 같지 않습니다.')
        }

        //서버에 보낼 때는 Axios를 사용함 
        let body = {
            email: email,
            password: password,
            name: name
        }

        //redux dispatch
        dispatch(registerUser(body))//회원가입 action명은 registerUser임
            .then(response => {
                // console.log(response)
                if (response.action.payload.success) {
                    navigate('/')
                }
                else {
                    alert('회원가입 실패')
                }
            })
    }

    return (
        <Container component="form" maxWidth="xs" onSubmit={onSubmitHandler}>
            <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center', }} >
                <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                </Avatar>
                <Typography component="h1" variant="h5">
                    회원가입
                </Typography>
                <TextField margin="normal" label="이름" required fullWidth name="name" autoFocus value={name} onChange={(event) => { setName(event.target.value); }} />
                <TextField margin="normal" label="아이디" required fullWidth name="email" autoFocus value={email} onChange={(event) => { setEmail(event.target.value); }} />
                <TextField margin="normal" label="비밀먼호" type="password" required fullWidth name="password" value={password} onChange={(event) => { setPassword(event.target.value); }} />
                <TextField margin="normal" label="비밀번호 확인" type="password" required fullWidth name="password_check" value={passwordcheck} onChange={(event) => { setPasswordcheck(event.target.value); }} />
                <Grid container>
                    <Grid item xs>
                        생년월일
                    </Grid>
                </Grid>
                <DatePicker
                    dateFormat="yyyy년 MM월 dd일"
                    selected={startDate}
                    value={startDate}
                    onChange={date => setStartDate(date)}
                    locale={ko}
                    placeholderText='Weeks start on Monday'
                    className='DatePicker_birth' />
                <Button type="submit" fullWidth variant='contained' sx={{ mt: 3, mb: 2 }} onClick={onSubmitHandler}>회원가입</Button>
                <Grid container>
                    <Grid item xs>
                    </Grid>
                    <Grid item>
                        <Link>아이디가 있으신가요?</Link>
                    </Grid>
                </Grid>
            </Box>
        </Container>
    );
}

export default Auth(Sign_up, false)