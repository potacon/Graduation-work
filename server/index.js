const express = require('express')
const app = express()
const port = 5000
//body-parser
const bodyParser = require('body-parser')
app.use(bodyParser.urlencoded({extended: true}))
app.use(bodyParser.json())
//cookie-parser
const cookieParser = require('cookie-parser')
app.use(cookieParser());

const { User } = require('./models/User.js')// model/user.js 가지고오기
const { auth } = require('./middleware/auth.js');// auth기능 가지고오기

//몽고db 연동
const mongoose = require('mongoose')
const config = require('./config/key.js')// 몽고db 숨기기

mongoose.connect(config.mongoURL,{
    useNewUrlParser:true, useUnifiedTopology: true, useCreateIndex:true, useFindAndModify: false
})
.then(() => console.log('MongoDB connected')).catch(err =>console.log('에러',err))

//db에 정보 전달
app.post('/api/users/register', (req,res)=>{
    //client로부터 데이터를 가져오면 그 데이터를 db에 넣어줌
    const user = new User(req.body)

    user.save((err, userInfo)=>{
        if(err) return res.json({success: false, err}) //실패
        return res.status(200).json({
            success:true
        })//성공
    })
})

//db에 회원가입이 되어있는지 확인
app.post('/api/users/login', (req,res)=>{
    //요청된 email 데이터베이스에서 있는지 찾는다.
    User.findOne({email: req.body.email}, (err, userInfo)=>{
        if(!userInfo){// 이메일이 없는경우
            return res.json({
                loginSuccess: false,
                message: "해당 이메일의 유저가 없습니다."
            })
        }

        //비밀번호가 일치할경우 이부분은 User.js에서 처리
        userInfo.comparePassword(req.body.password, (err, isMatch)=>{
            if(!isMatch){//비밀번호가 틀린경우
                return res.json({ 
                    loginSuccess: false, 
                    message: "비밀번호가 틀렸습니다."
                })
            }

            //비밀번호가 일치하면 토큰을 생성하기.
            userInfo.generateToken((err, user)=>{
                if(err) return req.status(400).send(err) //400이면 에러

                //토큰을 생성한다음에 쿠키에 저장시키기
                res.cookie("x_auth", user.token)// name=x_auth 내용= user.token이 쿠키에 들어감
                .status(200) //성공
                .json({loginSuccess: true, userId: user._id})
            })
        })
    })
})

//auth
app.get('/api/users/auth', auth, (req, res)=>{
    //여기 까지 미들웨어를 통과했다는 얘기는 authentication이 true라는 말 
    res.status(200).json({
        _id: req.user._id,
        isAdmin: req.user.role === 0 ? false : true,
        isAuth: true,
        email: req.user.email,
        name: req.user.name,
        date: req.user.date,
        role: req.user.role,
        date: req.user.date
    })
})

//로그아웃
app.get('/api/users/logout', auth, (req, res) => {
    User.findOneAndUpdate({ _id: req.user._id },//_id: req.user._id이 부분은 auth 미들웨어에서 데이터를 가져옴
      { token: "" }//토큰을 지워줌
      , (err, user) => {
        if (err) return res.json({ success: false, err });//실패
        return res.status(200).send({//성공
          success: true
        })
      })
  })

app.get('/', (req, res) => res.send('hello world'))
app.listen(port, ()=> console.log(`${port}`))
