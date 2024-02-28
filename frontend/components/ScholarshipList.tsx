import { useState } from 'react';
import Scholarship from './Scholarship';
import { Tab } from '@headlessui/react';

export default function ScholarshipList({scholarships}: any) {

    // [scholarships, setScholarships] = useState([
    //     {
    //         name: "Scholarship 1",
    //         description: "This is a scholarship description"
    //     },
    //     {
    //         name: "Scholarship 2",
    //         description: "This is a scholarship description"
    //     },
    // ]);

    
    return (
        <Tab.List className="flex flex-col space-y-3 full h-full border-black rounded-2xl shadow-2xl bg-white p-4 border-2 border-gray-200">
            {/* Mapping over the scholarships array and rendering a Scholarship component for each item */}
            {/* {scholarships.map((scholarship: any, index: any) => (
                <Scholarship key={index} scholarships={scholarship} />
            ))} */}
            {
                scholarships.map((scholarship: any, index: any) => (
                    <Scholarship key={index} scholarship={scholarship} />
                ))
            }
        </Tab.List>
    );
}
