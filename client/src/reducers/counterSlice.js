import { createSlice } from "@reduxjs/toolkit"
const status = {
    normal:'ey - whats up',
    added:'adding i see!',
    subtracted:'subracting eh!',
    error:'oy! cant do that man!'
}
const initialState = {
    count:0,
    status:status.normal
}

export const counterSlice = createSlice({
    name:'counter',
    initialState,
    reducers: {
        increment: (state) => {
            state.count += 1
            state.status = status.added
        },
        decrement: (state) => {
            let currentCount = state.count;
            if(state.count > 0){
                state.count -= 1
                state.status = status.subtracted
            } else {
                state.count = -1
                state.status = status.error
            }
        },
        reset: (state) => {
            return initialState
        }
    }
})

export const { increment, decrement, reset } = counterSlice.actions;

export default counterSlice.reducer

