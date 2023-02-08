import { createSlice } from "@reduxjs/toolkit"
const greeting = {
    normal:'👋 Oy, mate! ',
    login:'Hi, ',
    logout:'See you soon!',
    error:'Oy! Something went wrong on the login process.. ',
}
const initialState = {
  "data":{
    "access_token": null,
    "refresh_token": null,
    "name": null,
    "email": null,
    "password": null,
    "imageUrl": null,
    "isLoggedin": false,
  },
  "status":greeting.normal
}

export const authSlice = createSlice({
    name:'userAuthSlice',
    initialState,
    reducers: {
        signedInSuccessState: (state, user) => {
            console.log("dispatching user auth payload ", user.payload.detail)
            state.data = user.payload.detail
            state.status = greeting.login
        },
        signedInErrorState: (state, payload) => {
            state  = null
            state.status = greeting.error
        },
        signoutState: (state) => {
           state.data = {
            "access_token": null,
            "refresh_token": null,
            "name": null,
            "email": null,
            "password": null,
            "imageUrl": null,
            "isLoggedin": false
          }
          state.status = greeting.logout
        }
    }
})

export const { signedInSuccessState, signoutState, signedInErrorState } = authSlice.actions;

export default authSlice.reducer

