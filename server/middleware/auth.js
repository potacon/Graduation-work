//auth 미들웨어

const { User } = require('../models/User.js')

let auth = (req, res, next)=>{
    //1. 클라이언트 쿠키에서 토큰을 가지고옴
    let token = req.cookies.x_auth

    //2. 토큰을 디코딩한 후 db에서 유저를 찾는다.
    User.findByToken(token, (err, user)=>{
        if(err) throw err;
        //유저가 없는경우
        if(!user) return res.json({isAuth: false, error: true})

        //유저가 있는 경우
        req.token=token
        req.user=user
        next()
    })
}

module.exports = {auth};