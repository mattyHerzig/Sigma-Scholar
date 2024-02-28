import { useState } from 'react'
import { RadioGroup } from '@headlessui/react'
import moment from 'moment';

const deadlines = [
    "Soonest",
    "Farthest",
    "1 moth",
    "3 months",
    "6 months",
    "1 year",
]

export default function Deadline({scholarships, setSearch}: any) {
    const [selected, setSelected] = useState(deadlines[0])

    const onChangeHandler = (value: any) => {
        // console.log("search: ", search )
        setSelected(value)
        console.log(value)
        // const filteredScholarships = scholarships.filter((scholarship: any) => {
        //     // Convert amount to a number (assuming it's a string without currency symbols)
        //     console.log("scholarship: ", scholarship)
        //     const amount = Number(scholarship.amount);
        
        //     // Check if the amount is within the range
        //     return amount <= value
        // });
        // console.log("filteredScholarships: ", filteredScholarships)
        // setSearch(filteredScholarships)
        const now = moment();

        scholarships.forEach((scholarship: any) => {
            const deadlineMoment = moment(scholarship.deadline, 'YYYY-MM-DD');
            scholarship.daysUntilDeadline = deadlineMoment.diff(now, 'days');
          });
        
          // Then, sort scholarships based on the selected category
          let sortedScholarships;
          switch (value) {
            case 'Soonest':
              sortedScholarships = scholarships.sort((a: any, b: any) => a.daysUntilDeadline - b.daysUntilDeadline);
              break;
            case 'Farthest':
              sortedScholarships = scholarships.sort((a: any, b: any) => b.daysUntilDeadline - a.daysUntilDeadline);
              break;
            case '1 month':
            case '3 months':
            case '6 months':
            case '1 year':
              const monthsMapping: any = {
                '1 month': 1,
                '3 months': 3,
                '6 months': 6,
                '1 year': 12,
              };
              const months = monthsMapping[value];
              const startRange = now.clone().add(months, 'months').diff(now, 'days');
              sortedScholarships = scholarships.filter((scholarship: any) => scholarship.daysUntilDeadline <= startRange);
              // Sort within the filtered range by the closest deadline
              sortedScholarships.sort((a: any, b: any) => a.daysUntilDeadline - b.daysUntilDeadline);
              break;
            default:
              sortedScholarships = scholarships;
          }
          setSearch(sortedScholarships);
    }

    return (
        <div className="w-full px-4 py-16">
        <div className="mx-auto w-full max-w-md">
            <RadioGroup value={selected} onChange={onChangeHandler}>
            <RadioGroup.Label className="sr-only">Server size</RadioGroup.Label>
            <div className="space-y-2">
                {deadlines.map((deadline) => (
                <RadioGroup.Option
                    // key={amount.name}
                    value={deadline}
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
                                {deadline}
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
