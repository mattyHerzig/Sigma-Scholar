import { useState } from 'react'
import { RadioGroup } from '@headlessui/react'

const amounts = [
    100,
    200,
    500,
    1000,
    10000,
    20000,
]

export default function Amount({scholarships, setSearch}: any) {
    const [selected, setSelected] = useState(amounts[0])

    const onChangeHandler = (value: any) => {
        // console.log("search: ", search )
        setSelected(value)
        console.log(value)
        const filteredScholarships = scholarships.filter((scholarship: any) => {
            // Convert amount to a number (assuming it's a string without currency symbols)
            console.log("scholarship: ", scholarship)
            const amount = Number(scholarship.amount.slice(1).replace(" ", "").replace(",", ""))
            console.log("amount: ", amount)
        
            // Check if the amount is within the range
            return amount >= value
        });
        console.log("filteredScholarships: ", filteredScholarships)
        setSearch(filteredScholarships)
    }

    return (
        <div className="w-full px-4 py-16">
        <div className="mx-auto w-full max-w-md">
            <RadioGroup value={selected} onChange={onChangeHandler}>
            <RadioGroup.Label className="sr-only">Server size</RadioGroup.Label>
            <div className="space-y-2">
                {amounts.map((amount) => (
                <RadioGroup.Option
                    // key={amount.name}
                    value={amount}
                    className={({ active, checked }) =>
                    `${
                        active
                        ? 'ring-2 ring-white/60 ring-offset-2 ring-offset-sky-300'
                        : ''
                    }
                    ${checked ? 'bg-sky-900/75 text-white' : 'bg-white'}
                        relative flex cursor-pointer rounded-lg px-5 py-4 shadow-md focus:outline-none`
                    }
                >
                    {({ active, checked }) => (
                    <>
                        <div className="flex w-full items-center justify-between">
                        <div className="flex items-center">
                            <div className="text-sm">
                            <RadioGroup.Label
                                as="p"
                                className={`font-medium  ${
                                checked ? 'text-white' : 'text-gray-900'
                                }`}
                            >
                                ${amount}
                            </RadioGroup.Label>
                            </div>
                        </div>
                        {checked && (
                            <div className="pl-2 shrink-0 text-white">
                            <CheckIcon className="h-6 w-6" />
                            </div>
                        )}
                        </div>
                    </>
                    )}
                </RadioGroup.Option>
                ))}
            </div>
            </RadioGroup>
        </div>
        </div>
    )
}

function CheckIcon(props: any) {
  return (
    <svg viewBox="0 0 24 24" fill="none" {...props}>
      <circle cx={12} cy={12} r={12} fill="#fff" opacity="0.2" />
      <path
        d="M7 13l3 3 7-7"
        stroke="#fff"
        strokeWidth={1.5}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}
