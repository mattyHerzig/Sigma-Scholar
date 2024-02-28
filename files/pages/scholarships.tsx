import { NextPage } from "next";
import React from "react";
import { useState, useEffect } from 'react';
import ScholarshipList from "@/components/ScholarshipList";
import Description from "@/components/Description";
import DescriptionList from "@/components/Description";
import { Tab } from '@headlessui/react'
import Search from "@/components/Search";
import Filters from "@/components/Filter/Filters";
import data from "../data.json"
// Using data.json temporarily, chroma_db has functionality to supply the thousands of other scholarship JSONs

const result = [
    {
        name: "YMCA",
        description: "biomedical",
        amount: 1000,
        gpa: 3.5,
        race: "asian",
        deadline: "2023 12 12",
        location: "California"
    },
    {
        name: "SCU",
        description: "engineering",
        amount: 20000,
        gpa: 4.4,
        race: "asian",
        deadline: "2024 5 12",
        location: "US"
    },
]

const AboutPage: NextPage = () => {
    const [scholarships, setScholarships] = useState<any>(result)

    // const [search, setSearch] = useState<any>([
    //     {
    //         name: "YMCA",
    //         description: "biomedical",
    //         amount: "$1,000",
    //         awards: "10",
    //         deadline: "February 20, 2024",
    //     },
    //     {
    //         name: "SCU",
    //         description: "engineering",
    //         amount: "$10,000",
    //         awards: "5",
    //         deadline: "March 9, 2024",
    //     },
    // ])

    const [search, setSearch] = useState<any>(result)

    useEffect(() => {
          console.log(data.scholarships)
          console.log(data.scholarships)
          setScholarships(data.scholarships)
          setSearch(data.scholarships)
    }, [])



    return (
        <Tab.Group as='div' className="flex flex-row h-screen space-x-8 p-8" key="About">
               {/*Scholarship*/}
                <div className="flex flex-col h-full w-5/12">
                    <Search scholarships={scholarships} setSearch={setSearch} />
                    <Filters scholarships={scholarships} setSearch={setSearch}/>
                    <ScholarshipList scholarships={search}/>
                </div>

                {/*Description*/}
                <div className="h-full w-7/12">
                    <Tab.Panels className='h-full'>
                        {
                            search.map((scholarship: any, index: any, amount: any, awards: any, deadline: any) => (
                               <Description key={index} scholarship={scholarship} amount={amount} awards={awards} deadline={deadline}/>
                            ))
                        }
                    </Tab.Panels>
                    {/* <DescriptionList scholarships={search}/> */}
                </div>
        </Tab.Group>
    );

}

export default AboutPage;
