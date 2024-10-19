import React, { useEffect } from 'react'
import axios from 'axios'
function Test_1() {

    axios.defaults.withCredentials =true;

    useEffect(()=>{
        axios.get('http://localhost:8000/api/hello')// 이 부분이 get req를 server로 보내는부분이다.
        .then(response => console.log(response.data))
    }, [])

  return (
    <div>
      
    </div>
  )
}

export default Test_1
