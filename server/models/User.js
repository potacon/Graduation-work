const mongoose = require('mongoose')
const bcrypt = require('bcrypt')
const saltRounds = 10
const jwt = require('jsonwebtoken')

const userSchema = mongoose.Schema({
    name : {
        type: String,
        maxlength:50
    },
    email : {
        type: String,
        trim: true,
        unique: 1
    },
    password: {
        type: String,
        minlength: 5
    },
    role: { //관리자랑 일반유저를 구분하기위함
        type: Number,
        default: 0
    },
    token: {
        type: String
    },
    date: {
        type: String
    }
})

//회원가입하고 db에 비밀번호를 암호화시키기
userSchema.pre('save', function(next){
    var user = this;

    if(user.isModified('password')){//비밀번호 변경시 암호화
        bcrypt.genSalt(saltRounds, function(err, salt){
            if(err) return next(err)

            bcrypt.hash(user.password, salt, function(err, hash){
                if(err) return next(err)
                user.password = hash
                next()
            })
        })
    }
    else{//비밀번호 변경외에는 그냥 바로 next
        next()
    }
})

//비밀번호 일치확인
userSchema.methods.comparePassword = function(plainPassword, cb){

    bcrypt.compare(plainPassword, this.password, function(err, isMatch){
        if(err) return cb(err) //같지 않을 경우
            cb(null, isMatch)// 같을경우 에러=null isMatch=true
    })
}

//token 생성
userSchema.methods.generateToken = function(cb){
    var user = this

    //jsonwbtoken을 이용해서 토큰 생성하기
    var token = jwt.sign(user._id.toHexString(), 'secretToken')

    user.token = token //user.token은 db 토큰 token은 위에서 만든 토큰 db토큰에 넣어줌
    user.save(function(err, user){
        if(err) return cb(err) //실패
        cb(null, user) //성공
    })
}

//auth
userSchema.statics.findByToken = function(token, cb){
    var user = this;

    //토큰 decode verify()가 디코딩
    jwt.verify(token, 'secretToken', function(err, decoded){
        //user id를 이용해 해당 user를 db에서 찾고
        //클라이언트에서 가져온 token과 db에 보관된 토큰이 일치하는지 확인
        user.findOne({"_id": decoded, "token": token}, function(err, user){
            if(err) return cb(err)
            cb(null, user)
        })
    })
}


const User = mongoose.model('User', userSchema)
module.exports = {User}