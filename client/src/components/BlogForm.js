import React, { useRef, useState } from "react";
import { AddPhotoIcon } from "../assets/AddPhotoIcon";
import { CloseIcon } from "../assets/closeIcon";
import { PicIcon } from "../assets/PicIcon";
// import { EnvelopeIcon, PhoneIcon } from '@heroicons/react/24/outline'
// import { DropDownComponent } from "./dropdowns/DropDownComponent";
import { DropDownv2 } from "./dropdowns/DropDownv2";

export const BlogForm = () => {
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);

  const onSubmitPost = (evt) => {
    evt.preventDefault();
    console.log(evt.target.value);
  };

  const assignedSelections = [
    {
      name: "Story",
      value: "story",
    },
    {
      name: "Snapshot",
      value: "snapshot",
    },
    {
      name: "Sport",
      value: "sport",
    },
    {
      name: "Tech",
      value: "tech",
    },
  ];

  const getSelectedOption = () => {
    console.log("get selected option");
  };

  const onSelectPhoto = (evt, input) => {
    evt.preventDefault();
    const { files } = evt.target;
    console.log(files);
    const fileReader = new FileReader();
    fileReader.onload = (e) => {
      const { result } = e.target;
      // console.log(result);
      setImageUrl(result);
    };
    fileReader.readAsDataURL(evt.target.files[0]);
  };

  return (
    <div className="bg-gray-100">
      <div className="mx-auto max-w-7xl p-[12px] sm:py-[12px] lg:px-[12px] mt-[5px]">
        <div className="relative bg-white shadow-xl">
          <h2 className="sr-only">Create A Post</h2>

          <div className="flex flex-col">
            {/* Contact information */}

            <div className="flex justify-center w-[100%] relative overflow-hidden bg-indigo-100 py-10 px-6 sm:px-10 xl:p-12">
              <div>
                {!imageUrl && 
                <div className="addphoto cursor-pointer">
                  <div className="mt-1">
                    <input
                      type="file"
                      name="file"
                      onChange={(e) => onSelectPhoto(e, e.target.files[0])}
                      id="file"
                      autoComplete="file-name"
                      className="block w-full rounded-md border-gray-300 py-3 px-4 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                  </div>
                  <AddPhotoIcon/>
                </div>}
                {imageUrl && 
                  <div className="image-container relative">
                    <button className="absolute top-[-17px] right-[-17px] inline-flex items-center rounded-full border border-transparent bg-grey-300 p-1 text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2" onClick={()=>setImageUrl(null)}><CloseIcon /></button>
                    <img id="target" src={imageUrl} className="max-h-[500px] max-w-[500px] rounded border-2 border-indigo-500" alt="yourImage" style={{
                        backgroundPosition: `center center`,
                        backgroundRepeat: `no-repeat`,
                        backgroundSize: `cover`,
                      }}/>
                  </div>
                }
              </div>
            </div>

            {/* Contact form */}
            <div className="py-10 px-6 sm:px-10 lg:col-span-2 xl:p-12">
              <h3 className="text-lg font-medium text-gray-900">
                Create A Post
              </h3>
              <form
                onSubmit={(e) => onSubmitPost(e)}
                className="mt-6 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-8"
              >
                {/* <div>
                  <label
                    htmlFor="title"
                    className="block text-sm font-medium text-gray-900"
                  >
                    Image
                  </label>
                  <div className="mt-1">
                    <input
                      type="file"
                      name="file"
                      onChange={(e) => onSelectPhoto(e, e.target.files[0])}
                      id="file"
                      autoComplete="file-name"
                      className="block w-full rounded-md border-gray-300 py-3 px-4 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                  </div>
                </div> */}

                <div>
                  <label
                    htmlFor="title"
                    className="block text-sm font-medium text-gray-900"
                  >
                    Title
                  </label>
                  <div className="mt-1">
                    <input
                      type="text"
                      name="title"
                      id="title"
                      autoComplete="given-name"
                      className="block w-full rounded-md border-gray-300 py-3 px-4 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                  </div>
                </div>

                <div className="sm:col-span-2">
                  <label
                    htmlFor="assigned"
                    className="block text-sm font-medium text-gray-900"
                  >
                    Type
                  </label>
                  <div className="mt-1">
                    {/* <DropDownComponent selections={assignedSelections} action={getSelectedOption}/> */}
                    <DropDownv2 />
                  </div>
                </div>
                <div className="sm:col-span-2">
                  <div className="flex justify-between">
                    <label
                      htmlFor="description"
                      className="block text-sm font-medium text-gray-900"
                    >
                      Description
                    </label>
                    <span id="message-max" className="text-sm text-gray-500">
                      Max. 500 characters
                    </span>
                  </div>
                  <div className="mt-1">
                    <textarea
                      id="description"
                      name="description"
                      rows={4}
                      className="block w-full rounded-md border-gray-300 py-3 px-4 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      aria-describedby="message-max"
                      defaultValue={""}
                    />
                  </div>
                </div>
                <div className="sm:col-span-2 sm:flex sm:justify-end">
                  <button
                    type="submit"
                    className="mt-2 inline-flex w-full items-center justify-center rounded-md border border-transparent bg-indigo-600 px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:w-auto"
                  >
                    Create
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
