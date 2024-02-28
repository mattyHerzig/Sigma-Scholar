import { useState } from 'react';
import { Tab } from '@headlessui/react';
import Description from './Description';

export default function DescriptionList({scholarships}: any) {
    return (
        <Tab.Panels className="flex flex-col space-y-3 full h-full bg-transparent border-2 border-black rounded-2xl shadow-2xl bg-gray-900">
            {
                scholarships.map((scholarship: any, index: any, amount: any) => (
                    <Description key={index} scholarship={scholarship} amount={amount}/>
                ))
            }
        </Tab.Panels>
    );
}
