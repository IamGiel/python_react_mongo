import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { decrement, increment } from '../reducers/counterSlice'

const Counter = () => {
    const count = useSelector((state)=> state.counter.count)
    const reaction = useSelector((state)=> state.counter.status)
    const dispatch = useDispatch();
   
  return (
    <section>
        <p>Count {count}</p>
        <p>Reacted: "{reaction}"</p>
        <div className='flex flex-row justify-center gap-[12px] m-[12px]'>
            <div>
                <button onClick={()=>dispatch(increment())}
                    type="button"
                    className="inline-flex items-center rounded border border-transparent bg-indigo-600 px-2.5 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                    ADD
                </button>
            </div>
            <div>
                <button onClick={()=>dispatch(decrement())}
                    type="button"
                    className="inline-flex items-center rounded border border-transparent bg-indigo-600 px-2.5 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                    Subtract
                </button>
            </div>
        </div>
    </section>
  )
}

export default Counter