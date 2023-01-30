import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { CreateBlogModal } from '../components/CreateBlogModal'
import { reset } from '../reducers/counterSlice'

export const Dashboard = () => {

  const dispatch = useDispatch()
  
  return (
    <div className='dashboard-container flex flex-col gap-[12px] border border-[3px] rounded-[12px] h-[450px] w-[99%] p-[12px] m-[12px]'>
      <div className='dashboard-page-title flex'>
        <h1>This is Dashboard</h1>
      </div>
      <div className='dashboard-page-body flex flex-col'>
        <div className='flex'>
          <p>Here we will manage your posts where you can View, Delete, Edit/Update your posts.</p>
        </div>
        <div className='flex'>
          <p>Try to click the reset button to reset the count and status.</p>
        </div>
        <div className='flex'>
          <button
            onClick={()=>dispatch(reset())}
            type="button"
            className="inline-flex items-center rounded border border-transparent bg-indigo-100 px-2.5 py-1.5 text-xs font-medium text-indigo-700 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            RESET COUNT 
          </button>
        </div>
      </div>
    </div>
  )
}
