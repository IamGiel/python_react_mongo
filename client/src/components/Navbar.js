import { Fragment, useEffect, useState } from "react";
import { Disclosure, Menu, Transition } from "@headlessui/react";
import { Bars3Icon, BellIcon, PencilIcon, XMarkIcon } from "@heroicons/react/24/outline";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { signoutState } from "../reducers/authSlice";
import { CreateBlogModal } from "./CreateBlogModal";
import { isModalOpened } from "../reducers/createPostSlice";

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

export const Navbar = (props) => {
  const count = useSelector((state) => state.counter.count);
  const reaction = useSelector((state) => state.counter.status);
  const user = useSelector((state) => state.user);
  const createModalStatus = useSelector((state)=> state.createModal.isOpen)
  const dispatch = useDispatch();

  const [current, setCurrent] = useState(false);
  const [loginStatus, setLoginStatus] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    console.log("logging user in navbar ", user);
    console.log("createModal in navbar ", createModalStatus);
    setLoginStatus(user.isLoggedIn);
  }, [user]);
  

  const navigation = [
    {
      name: "Home",
      href: "#",
      current: current === "Home" ? true : false,
      showNavBtn: loginStatus,
    },
    {
      name: "Dashboard",
      href: "#",
      current: current === "Dashboard" ? true : false,
      showNavBtn: loginStatus,
    }
  ];

  

  const notificationColors = () => {
    if (count < 0) {
      return `bg-orange-500`;
    } else {
      return `bg-red-500`;
    }
  };
  
  

  const onRouteTo = (gotoPage) => {
    console.log("onROUTE TO: ", gotoPage);
    setCurrent(gotoPage);
    props.action(gotoPage);
  };

  return (
    <Disclosure as="nav" className="bg-gray-800">
      {({ open }) => (
        <>
          <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
            <div className="relative flex h-16 items-center justify-between">
              <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
                {/* Mobile menu button*/}
                <Disclosure.Button className="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                  <span className="sr-only">Open main menu</span>
                  {open ? (
                    <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                  ) : (
                    <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                  )}
                </Disclosure.Button>
              </div>
              <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
                <div
                  className="flex flex-shrink-0 items-center cursor-pointer"
                  onClick={() => navigate("/home")}
                >
                  <img
                    className="block h-8 w-auto lg:hidden"
                    src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500"
                    alt="Your Company"
                  />
                  <img
                    className="hidden h-8 w-auto lg:block"
                    src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500"
                    alt="Your Company"
                  />
                </div>
                <div className="hidden sm:ml-6 sm:block">
                  <div className="flex space-x-4">
                    {navigation.map((item) => {
                      if (item.showNavBtn) {
                        return (
                          <a
                            key={item.name}
                            href={item.href}
                            onClick={() => onRouteTo(item.name)}
                            className={classNames(
                              item.current
                                ? "bg-slate-500 text-white"
                                : "text-gray-300 hover:bg-gray-700 hover:text-white",
                              "px-3 py-2 rounded-md text-sm font-medium"
                            )}
                            aria-current={item.current ? "page" : undefined}
                          >
                            {item.name}
                          </a>
                        );
                      }
                    })}
                    <Disclosure.Button>
                    {loginStatus && 
                      <span className="inline-flex items-center rounded-full bg-indigo-100 py-0.5 pl-2.5 pr-1 text-sm font-medium text-indigo-700">
                      Create Post
                        <button
                          type="button"
                          className="ml-0.5 inline-flex h-[20px] w-[20px] flex-shrink-0 items-center justify-center rounded-full text-indigo-800 bg-indigo-400 hover:bg-indigo-200 hover:text-indigo-500 focus:bg-indigo-500 focus:text-white focus:outline-none"
                          onClick={()=>dispatch(isModalOpened(true))}
                        >
                          <span className="sr-only">Remove large option</span>
                          <PencilIcon fill="white"/>

                        </button>
                      </span>
                    }
                    </Disclosure.Button>
                  </div>
                </div>
              </div>
              <div className="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
                {count > 0 && loginStatus && (
                  <button
                    type="button"
                    className="relative inline-flex items-center p-3 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                  >
                    <svg
                      className="w-6 h-6"
                      aria-hidden="true"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"></path>
                      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path>
                    </svg>
                    <span className="sr-only" title={reaction}>
                      Notifications
                    </span>
                    <div
                      className={`${notificationColors()} absolute inline-flex items-center justify-center w-6 h-6 text-xs font-bold text-white border-2 border-white rounded-full -top-2 -right-2 dark:border-gray-900`}
                    >
                      {count >= 0 ? count : "!"}
                    </div>
                  </button>
                )}

                {/* Profile dropdown */}
                <Menu as="div" className="relative ml-3">
                  <div className="flex gap-[10px]">
                    <div className="name-container flex">
                      <span className="text-white hidden lg:block">
                        {user.status} {user.user.name}
                      </span>
                    </div>
                    {!loginStatus && (
                      <button
                        className="text-white my-[0px] mx-[12px] py-[0px] px-[12px] border-[1px] border-[white] rounded-[7px]"
                        type="button"
                        onClick={() => navigate("/Signin")}
                      >
                        Signin
                      </button>
                    )}
                    {loginStatus && (
                      <Menu.Button className="flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                        <span className="sr-only">Open user menu</span>

                        <img
                          className="h-8 w-8 rounded-full"
                          src={user.user.imageUrl}
                          alt=""
                        />
                      </Menu.Button>
                    )}
                  </div>
                  <Transition
                    as={Fragment}
                    enter="transition ease-out duration-100"
                    enterFrom="transform opacity-0 scale-95"
                    enterTo="transform opacity-100 scale-100"
                    leave="transition ease-in duration-75"
                    leaveFrom="transform opacity-100 scale-100"
                    leaveTo="transform opacity-0 scale-95"
                  >
                    <Menu.Items className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                      <Menu.Item>
                        {({ active }) => (
                          <a
                            href="#"
                            className={classNames(
                              active ? "bg-gray-100" : "",
                              "block px-4 py-2 text-sm text-gray-700"
                            )}
                          >
                            Your Profile
                          </a>
                        )}
                      </Menu.Item>
                      <Menu.Item>
                        {({ active }) => (
                          <a
                            href="#"
                            className={classNames(
                              active ? "bg-gray-100" : "",
                              "block px-4 py-2 text-sm text-gray-700"
                            )}
                          >
                            Settings
                          </a>
                        )}
                      </Menu.Item>
                      <Menu.Item>
                        {({ active }) => (
                          <Link
                            onClick={() => dispatch(signoutState())}
                            to={"/home"}
                            className={classNames(
                              active ? "bg-gray-100" : "",
                              "block px-4 py-2 text-sm text-gray-700"
                            )}
                          >
                            Sign out
                          </Link>
                        )}
                      </Menu.Item>
                    </Menu.Items>
                  </Transition>
                </Menu>
              </div>
            </div>
          </div>
          {createModalStatus &&  <CreateBlogModal id="defaultModal" name={'Create Post'}/>}

          <Disclosure.Panel className="sm:hidden">
            <div className="space-y-1 px-2 pt-2 pb-3">
              {navigation.map((item) => {
                if (item.showNavBtn) {
                  return (
                    <Disclosure.Button
                      key={item.name}
                      as="a"
                      href={item.href}
                      className={classNames(
                        item.current
                          ? "bg-gray-900 text-white"
                          : "text-gray-300 hover:bg-gray-700 hover:text-white",
                        "block px-3 py-2 rounded-md text-base font-medium"
                      )}
                      aria-current={item.current ? "page" : undefined}
                    >
                      {item.name}
                    </Disclosure.Button>
                  );
                }
              })}
              
            </div>
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
    
  );
};
