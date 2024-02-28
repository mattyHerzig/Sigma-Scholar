import React from 'react'
import { Tab } from '@headlessui/react'

export default function Scholarship({key, scholarship}: any) {
  // const dateString = scholarship.deadline;
  // const dateObject = new Date(dateString);
  

  // const options = { year: 'numeric', month: 'long', day: 'numeric' };
  // const formattedDate = dateObject.toLocaleDateString('en-US', options);

  // if (fo)

  return (
    <Tab
        key={key}
        className="flex w-full shadow-xl bg-white text-center rounded-xl border-gray-100 border-2 hover:bg-gray-300 hover:text-black hover:border-gray-300 focus:outline-none focus:ring focus:ring-gray-900"
    >
      <div className="flex flex-row w-full justify-between items-center px-2 py-4">
        <div className='flex flex-col'>
          <div className="font-semibold text-xl text-left">{scholarship.name}</div>
          <div className="text-xl text-left">{scholarship.amount}</div>
        </div>

        <div className="font-semibold text-xl">{scholarship.deadline}</div>
      </div>
    </Tab>

    
  )
}
