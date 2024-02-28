import { useState } from 'react'
import { RadioGroup } from '@headlessui/react'

const GPA = [
    [0, 2.0],
    [2.0, 3.0],
    [3.0, 3.5],
    [3.5, 4.0],
    [4.0, 4.5]
]

export default function Gpa({scholarships, setSearch}: any) {
    const [selected, setSelected] = useState(GPA[0])

    const onChangeHandler = (value: number[]) => {
        console.log('GPA range selected:', value);
        const [minGPA, maxGPA] = value; // Destructure the value into min and max GPA range
      
        const filteredScholarships = scholarships.filter((scholarship: any) => {
          // Convert GPA to a number (assuming it's a string or number type)
          const gpa = Number(scholarship.GPA);
          console.log("gpa: ", gpa)
          console.log("scholarship: ", scholarship)
       
      
          // Check if the GPA is within the range
          const test = gpa >= minGPA && gpa <= maxGPA;
          console.log(test)
          return gpa >= minGPA && gpa <= maxGPA;
        });
      
        console.log('Filtered Scholarships based on GPA:', filteredScholarships);
        setSelected(value)
        setSearch(filteredScholarships); // Assuming setSearch
    }

    return (
        <div className="w-full px-4 py-16">
        <div className="mx-auto w-full max-w-md">
            <RadioGroup value={selected} onChange={onChangeHandler}>
            <div className="space-y-2">
                {GPA.map((value) => (
                <RadioGroup.Option
                    // key={amount.name}
                    value={value}
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
                                {value[0]} - {value[1]} GPA
                            </RadioGroup.Label>
                            </div>
                        </div>
                        {checked && (
                            <div className="shrink-0 text-white">
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
