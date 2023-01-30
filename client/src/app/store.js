import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../reducers/authSlice';
import counterReducer from '../reducers/counterSlice';
import createModalReducer from '../reducers/createPostSlice';

export const store = configureStore({
    reducer: {
        counter: counterReducer,
        user: authReducer,
        createModal:createModalReducer
    }
})