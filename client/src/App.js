import "./App.css";
import { Route, Routes, useNavigate } from "react-router-dom";
import { Home } from "./screens/Home";
import { Dashboard } from "./screens/Dashboard";
import { Navbar } from "./components/Navbar";
import { Signin } from "./screens/Signin";
import Counter from "./components/Counter";
import { useSelector } from "react-redux";
import {Protect} from "./Protect" 
import { useEffect } from "react";
import { store } from "./app/store";

const Routing = (isloggedInStatus) => {
  return (
    <Routes>
      <Route path="/home" element={<Home />} />
      <Route
        path="/dashboard"
        element={
          <Protect isLoggedIn={isloggedInStatus}>
            <Dashboard />
          </Protect>
        }
      />
      <Route path="/signin" element={<Signin />} />
    </Routes>
    
  );
};

function App () {
  const navigate = useNavigate();
  const user = useSelector((state) => state.user);
  console.log("user in appjs ", user)
  const getNavbarAction = (routeTo) => {
    navigate(`/${routeTo}`);
  };

  return (
    <div className="App">
      <Counter />
      <div className="navbar-component-container m-[12px] p-[12px]">
        <Navbar action={getNavbarAction} />
      </div>

      <div className="routing-container m-[12px] p-[12px]">
        <Routing isloggedInStatus={user.data.isLoggedIn} />
      </div>
    </div>
  );
};

export default App;
