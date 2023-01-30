import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import { getAllPost } from '../api/apiCall';
import { BlogV1 } from '../components/Blogv1';
import { Preview } from './Preview';

export const Home = () => {

  const count = useSelector((state)=> state.counter.count)
  const reaction = useSelector((state)=> state.counter.status)
  const user = useSelector((state)=> state.user)

  const [blogs, setBlogs] = useState([])
  const [loading, setLoading] = useState(false)

  // const dispatch = useDispatch();
  useEffect(() => {
    console.log('user state in Home ', user)
  }, [user])
  useEffect(() => {    
    if(user.isLoggedIn){
      getBlogs()
    }
    
  }, [])

  const getBlogs = () => {
    setLoading(true)
    setTimeout(() => {
      getAllPost()
      .then(res=> {
        
        setBlogs([...res])
        setLoading(false)
      })
      .catch(err=>{
        
        console.log(err)
        setLoading(false)
      })
    }, 1500);
  }

  return (
    <>
      {/* <pre>{JSON.stringify(blogs)}</pre> */}
      {user.isLoggedIn && 
        <div className='home-container flex flex-col gap-[12px] border border-[3px] rounded-[12px] min-h-[450px] w-[99%] p-[12px] m-[12px]'>
          <BlogV1 data={blogs} hasLoaded={loading}/>
      </div>
      }
      {!user.isLoggedIn && 
        <div className='home-container flex flex-col gap-[12px] border border-[3px] rounded-[12px] min-h-[450px] w-[99%] p-[12px] m-[12px]'>
          <Preview />
      </div>
      }
    </>
  )
}
