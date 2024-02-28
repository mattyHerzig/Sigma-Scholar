import { Popover, Transition } from "@headlessui/react";
import { useState, Fragment } from "react";


export default function Filter({children, name}: any) {
const amounts = [
    100,
    200,
    500,
    1000,
    10000,
    20000,
]

  return (
      <Popover className="relative">
        {({ open }) => (
          <>
            <Popover.Button
              className={`text-black items-center rounded-2xl shadow-2xl bg-white px-3 py-2 border-gray-200 border-2 font-medium hover:bg-gray-300 hover:text-black focus:outline-none`}
            >
              <span>{name}</span>
            </Popover.Button>
            <Transition
              as={Fragment}
              enter="transition ease-out duration-200"
              enterFrom="opacity-0 translate-y-1"
              enterTo="opacity-100 translate-y-0"
              leave="transition ease-in duration-150"
              leaveFrom="opacity-100 translate-y-0"
              leaveTo="opacity-0 translate-y-1"
            >
              <Popover.Panel className="absolute z-10 mt-3 w-fit border-gray-200 border-2 bg-white rounded-2xl shadow-2xl ">
                {children}
              </Popover.Panel>
            </Transition>
          </>
        )}
      </Popover>
  );
};