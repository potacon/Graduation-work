//배포된 경우
if(process.env.NODE_ENV === 'production'){
    module.exports = require('./prod.js')
}
else{//즉 development면 ./dev 파일을 가지고온다는 뜻
    module.exports = require('./dev.js')
}