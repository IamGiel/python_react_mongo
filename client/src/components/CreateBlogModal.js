import { Fragment, useState } from "react";
import { Dialog, Transition } from "@headlessui/react";
import { CheckIcon } from "@heroicons/react/24/outline";
import { CloseIcon } from "../assets/closeIcon";
import { BlogForm } from "./BlogForm";
import { useDispatch, useSelector } from "react-redux";
import { isModalOpened, isModalClosed } from "../reducers/createPostSlice";

export const CreateBlogModal = (props) => {
  const createModalStatus = useSelector((state)=> state.createModal.isOpen)
  const [open, setOpen] = useState(createModalStatus.isOpen);
  const dispatch = useDispatch()

  const onModalClose = () => {
    console.log("closing!!!")
    dispatch(isModalClosed())
  }
  

  return (
    <>
      {/* <div className="modal-opener">
        <button onClick={()=>setOpen(true)}>{props.name}</button>
      </div> */}
      <Transition.Root show={true} as={Fragment}>
        <Dialog as="div" className="relative z-10" onClose={onModalClose}>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
          </Transition.Child>

          <div className="fixed inset-0 z-10 overflow-y-auto">
            <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                enterTo="opacity-100 translate-y-0 sm:scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 translate-y-0 sm:scale-100"
                leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              >
                <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 text-left shadow-xl transition-all sm:my-[0px] sm:w-full sm:max-w-[900px] sm:p-6">
                  
                  <div className="dialog-panel-container flex flex-col">
                    <div className="flex justify-end mb-[5px]">
                      <button
                        type="button"
                        className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 p-[5px] text-base font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:text-sm"
                        onClick={onModalClose}
                      >
                        <CloseIcon />
                      </button>
                    </div>
                    
                    <BlogForm />
                  </div>
                  
                  
                  
                  
                  
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition.Root>
    </>
  );
};
