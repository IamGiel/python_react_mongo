import { Fragment } from 'react'
import { Menu, Transition } from '@headlessui/react'
import {
  ArchiveBoxIcon,
  ArrowRightCircleIcon,
  ChevronDownIcon,
  DocumentDuplicateIcon,
  HeartIcon,
  PencilSquareIcon,
  TrashIcon,
  UserPlusIcon,
} from '@heroicons/react/20/solid'
import { TechIcon } from '../../assets/TechIcon'
import { SoccerIcon } from '../../assets/SoccerIcon'
import { SnapShot } from '../../assets/SnapShot'
import { StoryIcon } from '../../assets/StoryIcon'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export const DropDownComponent = (props) => {
  console.log(props.selections)

  const iconLookup = {
    story:StoryIcon(),
    snapshot:SnapShot(),
    sport:SoccerIcon(),
    tech:TechIcon()
  }

  const dynamicIconSelector = (itemName) => {
    // console.log("what is item.name ", itemName)
    let output = '';
    output = iconLookup[itemName]
    // console.log('this out put ',output)
    
    return output
  }
  return (
    <Menu as="div" className="relative inline-block text-left">
      <div>
        <Menu.Button className="inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-100">
          Options
          <ChevronDownIcon className="-mr-1 ml-2 h-5 w-5" aria-hidden="true" />
        </Menu.Button>
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
        <Menu.Items className="absolute right-[-100px] z-10 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
          <div className="py-1">
            {
              props.selections.map((item,id)=>(
                <Menu.Item key={id}>
                {({ active }) => (
                  <a
                    href="#"
                    className={classNames(
                      active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                      'group flex items-center px-4 py-2 text-sm'
                    )}
                  >
                    {/* <DocumentDuplicateIcon
                      className="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500"
                      aria-hidden="true"
                    /> */}
                    <div className='icon-container mr-3 h-[fit-content] text-gray-400 group-hover:text-gray-500'>{dynamicIconSelector(item.value)}</div>
                    {item.name}
                  </a>
                )}
              </Menu.Item>
              ))
            }
           
          </div>
          
        </Menu.Items>
      </Transition>
    </Menu>
  )
}
