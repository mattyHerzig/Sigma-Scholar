import { useState } from 'react'
import { RadioGroup } from '@headlessui/react'
import Fuse from 'fuse.js'

const ethnicities = [
    'White',
    'Black',
    'Hispanic',
    'Asian',
    'Native American',
    'Other'
]

export default function Race({scholarships, setSearch}: any) {
    const [selected, setSelected] = useState(ethnicities[0])

    const onChangeHandler = (value: any) => {
        // console.log("search: ", search )
        setSelected(value)
        console.log("race: ", value)

        const fuseOptions = {
            includeScore: true,
            threshold: 0.4, // Adjust this threshold to your preference for fuzziness
            keys: ['race'], // The keys in scholarship objects to match against
        };

        console.log("scholarships: ", scholarships)
        const fuse = new Fuse(scholarships, fuseOptions);

        const fuzzyResults = fuse.search(value);

        const filteredScholarships = fuzzyResults.map((result: any) => result.item);

        console.log("filteredScholarships: ", filteredScholarships)
        setSearch(filteredScholarships)
    }

    return (
        <div className="w-full px-4 py-16">
        <div className="mx-auto w-full max-w-md">
            <RadioGroup value={selected} onChange={onChangeHandler}>
            <RadioGroup.Label className="sr-only">Server size</RadioGroup.Label>
            <div className="space-y-2">
                {ethnicities.map((ethnicity) => (
                <RadioGroup.Option
                    // key={amount.name}
                    value={ethnicity}
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
                                {ethnicity}
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
