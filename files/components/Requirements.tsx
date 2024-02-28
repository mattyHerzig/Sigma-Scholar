import { Disclosure } from '@headlessui/react'
// import { ChevronUpIcon } from '@heroicons/react/20/solid'

export default function Requirements({scholarship} : any) {
  return (
        <Disclosure>
          {({ open }) => (
            <>
              <Disclosure.Button className="flex w-full justify-between rounded-lg bg-white border-gray-200 border-2 px-4 py-2 text-left text-xl font-medium text-black hover:bg-purple-white focus:outline-none focus-visible:ring focus-visible:ring-purple-500/75">
                <span>Requirements</span>
                {/* <ChevronUpIcon
                  className={`${
                    open ? 'rotate-180 transform' : ''
                  } h-5 w-5 text-purple-500`}
                /> */}
              </Disclosure.Button>
              <Disclosure.Panel className="px-4 pb-2 pt-4 text-lg text-black">
                <div className='text-lg my-8'>GPA: {scholarship.GPA}</div>
                <div className='text-lg my-8'>Race: {scholarship.race}</div>
                <div className='text-lg my-8'>Residence: {scholarship.residence}</div> 
              </Disclosure.Panel>
            </>
          )}
        </Disclosure>
  )
}
