import './App.css';
import {BrowserRouter, Route, Routes} from 'react-router-dom';
import logo from './logo.svg'; // 로고 부분 나중에 이미지 넣을 꺼면 사용
import styled from 'styled-components';
import Login from './Pages/login';
import Main from './Pages/main';
import Sign_up from './Pages/register'; 
import Find_id from './Pages/find_id';
import Find_pw from './Pages/find_pw';
import Auth from './hoc/auth';
//import 'antd/dist/antd.css';
// AUTH 3번째 속성에 TRUE 넣으면 ADMIN만 접속가능
//element={Auth(<Main />,null)}
//<Route exact path="/find_id" Component={Auth(<Find_id/>)}/>
//<Route exact path="/find_pw" Component={Auth(<Find_pw/>)}/>

function App() {
  return (
    <BrowserRouter>
      <div className='App'>
        <Routes>
          <Route exact path="/" element={<Main />} />
          <Route exact path="/login" element={<Login />}/>
          <Route exact path="/register" element={<Sign_up />}/>
          <Route exact path="/find_id" element={<Find_id/>}/>
          <Route exact path="/find_pw" element={<Find_pw/>}/>
        </Routes>
      </div>
    </BrowserRouter>
    );
}

export default App;
