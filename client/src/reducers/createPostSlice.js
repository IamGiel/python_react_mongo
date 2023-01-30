import { createSlice } from "@reduxjs/toolkit"
const greeting = {
    normal:'👋 Oy, mate! ',
    login:'Hi, ',
    logout:'See you soon!',
    error:'Oy! Something went wrong on the login process.. ',
}
const initialState = {
    isOpen:false
}

export const modalBlogForm = createSlice({
    name:'ModalBlogFormSlice',
    initialState,
    reducers: {
        isModalOpened: (state) => {
            console.log('ModalBlogFormSlice is opening')
            state.isOpen = true;
        },
        isModalClosed: (state) => {
            console.log('ModalBlogFormSlice is closing')
            state.isOpen = false;
        }
           
    }
})

export const { isModalOpened, isModalClosed } = modalBlogForm.actions;

export default modalBlogForm.reducer

