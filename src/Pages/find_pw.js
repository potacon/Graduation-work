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

function Find_pw() {
    const [startDate, setStartDate] = useState(new Date());
  return (
    <Container component="main" maxWidth="xs">
            <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center', }} >
                <Avatar sx ={{m:1, bgcolor:'secondary.main'}}>
                </Avatar>
                <Typography component="h1" variant="h5">
                    비밀번호 찾기
                </Typography>
                <TextField margin="normal" label="이름" required fullWidth name="name" autoFocus/>
                <TextField margin="normal" label="아이디" required fullWidth name="email" autoFocus/>
                <Grid container>
                    <Grid item xs>
                        생년월일
                    </Grid>
                </Grid>
                <DatePicker 
                    dateFormat="yyyy년 MM월 dd일" 
                    selected={startDate} 
                    onChange={date => setStartDate(date)} 
                    locale={ko} 
                    placeholderText='Weeks start on Monday'
                    className='DatePicker_birth'/>
                <Button type="submit" fullWidth variant='contained' sx={{ mt : 3, mb : 2}}>비밀번호 찾기</Button>
            </Box>
        </Container>
  );
}

export default Find_pw;
