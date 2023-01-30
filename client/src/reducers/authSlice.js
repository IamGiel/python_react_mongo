import { createSlice } from "@reduxjs/toolkit"
const greeting = {
    normal:'👋 Oy, mate! ',
    login:'Hi, ',
    logout:'See you soon!',
    error:'Oy! Something went wrong on the login process.. ',
}
const initialState = {
    "user": {
        "_id": null,
        "name":null,
        "email":null,
        "password":null,
        "imageUrl":null,
        "__v":null
    },
    "status":greeting.normal,
    "isLoggedIn":false
}

export const authSlice = createSlice({
    name:'userAuthSlice',
    initialState,
    reducers: {
        signedInSuccessState: (state, payload) => {
            console.log("dispatching user auth payload ", payload)
            // console.log("dispatching user state ", state)
            state.user = payload.payload.user
            state.status = greeting.login
            state.isLoggedIn = payload.payload.isLoggedin
        },
        signedInErrorState: (state, payload) => {
            state.user  = null
            state.status = greeting.error
        },
        signoutState: (state) => {
           state.user = {
            "user": {
                "_id": null,
                "name":null,
                "email":null,
                "password":null,
                "imageUrl":null,
                "__v":null
            }
           }
           state.status = greeting.logout
           state.isLoggedIn = false
        }
    }
})

export const { signedInSuccessState, signoutState, signedInErrorState } = authSlice.actions;

export default authSlice.reducer

