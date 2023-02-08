import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { signIn } from "../api/apiCall";
import { signedInSuccessState } from "../reducers/authSlice";
import qs from "qs";
import axios from "axios";

export const Signin = () => {
  const [email, setEmail] = useState(null || "");
  const [password, setPassword] = useState(null || "");
  const [formCompleteStatus, setFormCompleteStatus] = useState(false);

  const whatIsState = useSelector((state) => state);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    console.log("whatIsState ", whatIsState);
  }, []);

  const inputClass = `border rounded border-[2px] w-[300px] px-[5px] leading-normal`;
  const handleSubmitSigninForm = (e) => {
    e.preventDefault();
    console.log("handling submit");
    const payload = qs.stringify({
      username: email,
      password: password,
    });
    console.log(payload);
    if (email.length > 0 && password.length > 0) {
      console.log(email, password);
      setFormCompleteStatus(true);
    }

    const headers = {
      Accept: "application/json",
      "Content-Type": "application/x-www-form-urlencoded",
      grant: "",
    };
    console.log("submitting payload to backjend ", payload);
    let config = {
      method: "post",
      url: "http://localhost:8000/user-auth/signin",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        grant: ""
      },
      data: payload,
    };

    axios(config)
      .then((response) => {
        console.log(response.data); 
        dispatch(signedInSuccessState(response.data));
        navigate("/home");
      })
      .catch((error) => {
        console.log(error);
      });

    // call signin api
    // signIn(payload, headers).then(
    //   (res) => {
    //     console.log(res);
    //     dispatch(signedInSuccessState(res));
    //     navigate("/home");
    //   }
    // ).catch(err=> {
    //   console.log(err)
    // });
  };
  return (
    <div className="singin-container flex flex-col">
      <div className="flex signin-title px-[12px] mx-[12px]">
        <h1 className="text-[24px]">Sign in here:</h1>
      </div>
      <form onSubmit={(e) => handleSubmitSigninForm(e)}>
        <div className="name-input flex gap-[12px] px-[12px] m-[12px]">
          <label>Email: </label>
          <input
            className={inputClass}
            onChange={(e) => setEmail(e.target.value)}
            value={email}
            htmlFor="email"
            type="text"
            placeholder="email here"
            autoComplete="off"
          />
        </div>
        <div className="password-input flex gap-[12px] px-[12px] m-[12px]">
          <label>Password: </label>
          <input
            className={inputClass}
            onChange={(e) => setPassword(e.target.value)}
            value={password}
            htmlFor="password"
            type="password"
            placeholder="password here"
            autoComplete="off"
          />
        </div>
        <div className="button-container w-[fit-content] flex gap-[12px] px-[12px] m-[12px] bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          <button
            className={`${
              formCompleteStatus ? "" : "disabled cursor-not-allowed"
            }`}
            type="submit"
          >
            Submit {formCompleteStatus ? "enabled" : "disabled"}
          </button>
        </div>
      </form>
    </div>
  );
};
