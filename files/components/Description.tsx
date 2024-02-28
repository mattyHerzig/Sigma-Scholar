import React from 'react'
import { Tab } from '@headlessui/react'
import Image from 'next/image';
import { debug } from 'console';
import Requirements from './Requirements';

export default function Description({ scholarship }: any) {
  // Calculate animation values based on scholarship properties

  console.log(scholarship.amount);
  console.log(scholarship.awards);
  console.log(scholarship.deadline);

  // const heightAmount = parseFloat(scholarship.amount.replace(/[^0-9.-]+/g, "")) * 0.01; // Adjust multiplier as needed
  const heightAmount = 0.01 * scholarship.amount
  // Parse the deadline date string
  const deadlineDate = new Date(scholarship.deadline);

  // Get the current date
  const currentDate = new Date();

  // Calculate the difference in milliseconds between the deadline and current date
  const differenceInMilliseconds = deadlineDate.getTime() - currentDate.getTime();

  // Convert the difference to days
  const differenceInDays = Math.ceil(differenceInMilliseconds / (1000 * 60 * 60 * 24));

  const heightDeadline = differenceInDays * 2; // Adjust multiplier as needed
  const heightAwards = parseFloat(scholarship.awards) * 2; // Adjust multiplier as needed

  console.log(heightAmount);
  console.log(heightAwards);
  console.log(heightDeadline);

  return (
    <Tab.Panel 
        className='w-full border-gray-100 border-2 rounded-2xl bg-white text-black p-4'>
        
        <div className='flex flex-row gap-12'>
          <h1 className="text-4xl my-8 font-bold">{scholarship.name}</h1>
          <a href={scholarship.backlink}>
            <Image 
                className="p-2"
                src="/share.svg" 
                alt="Logo" 
                width={90} 
                height={90}
                
              />
          </a>

        </div>
        <p className="text-2xl my-8">{scholarship.amount}</p>
        {scholarship.awards_available != "" ? <p className="text-2xl my-8">{"Awards Available: " + scholarship.awards_available}</p> : <></>}

        <p className="text-2xl my-8">{"Deadline: " + scholarship.deadline}</p>
        
        {/* <div className='text-2xl my-8'>Requirements</div>
        <div className='text-lg my-8'>GPA: {scholarship.GPA}</div>
        <div className='text-lg my-8'>Race: {scholarship.race}</div>
        <div className='text-lg my-8'>Residence: {scholarship.residence}</div> */}
        <Requirements scholarship={scholarship}/>

        <p className="text-2xl my-8">{scholarship.description}</p>


    
        <div className="flex flex-row">
          <div style={{ height: `${heightAmount}px`, transition: 'height 1s ease-in-out' }}>
            <Image 
              className="p-2"
              src="/dollarblock.svg" 
              alt="Logo" 
              width={100} 
              height={100} 
            />
          </div>
          <div style={{ height: `${heightAwards}px`, transition: 'height 1s ease-in-out' }}>
            <Image 
              className="p-2"
              src="/awardblock.svg" 
              alt="Logo" 
              width={100} 
              height={100} 
            />
          </div>
          <div style={{ height: `${heightDeadline}px`, transition: 'height 1s ease-in-out' }}>
            <Image 
              className="p-2"
              src="/calendarblock.svg" 
              alt="Logo" 
              width={100} 
              height={100} 
            />
          </div>
        </div>
    </Tab.Panel>
  )
}
