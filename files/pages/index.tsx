import { NextPage } from "next";
import React, {useEffect} from "react";
import ScholarshipModal from "../components/form";
import { useState } from 'react';
import { redirect } from 'next/navigation'

const HomePage: NextPage = () => {
    // useEffect(() => {
    //     redirect('/scholarships')
    // }, [])
    const [isModalOpen, setModalOpen] = useState(false);
    const getReq = async () => {
        try {
            let config = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ "name": "test" }),
            };
            await fetch('/api/data', config).then(resp => console.log(resp));//.then(response => { console.log(response) });
        } catch (err) {
            console.log(err);
        }
    }
    return (
        <>
        <div className="container" key="home">
            <div className="grid place-content-center min-h-screen">
                <div className="flex flex-col items-center gap-4">
                    <h1 className="text-4xl my-8">Welcome</h1>
                    <button onClick={getReq} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Get Request</button>
                </div>
            </div>
        </div>
        <div className="container mx-auto p-4">
        <button onClick={() => setModalOpen(true)} className="btn-open-modal">
          Apply for Scholarship
        </button>
        <ScholarshipModal isOpen={isModalOpen} onClose={() => setModalOpen(false)} />
      </div>
      </>
    );
};

export default HomePage;
