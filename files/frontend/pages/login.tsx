import React, {useState} from 'react'

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    return (
        <div className='flex h-screen items-center justify-center'>
            <div className="flex flex-col items-center justify-center w-full shadow-xl text-center rounded-xl border-gray-100 border-2 bg-white w-1/4 pt-10 pb-8 space-y-4 rounded-full">
                <input type="text" name="scholarshipAmount" placeholder="Email" value={email} onChange={e => {setEmail(e.target.value)}} className="input p-2 border-2 border-gray-200 text-black rounded-xl shadow-md focus:outline-none focus:ring focus:ring-gray-900"/>
                <input type="text" name="scholarshipAmount" placeholder="Password" value={password} onChange={(e) => {setPassword(e.target.value)}} className="input p-2 border-2 border-gray-200 text-black rounded-xl shadow-md focus:outline-none focus:ring focus:ring-gray-900"/>

                <button onChange={() => {}} className='text-white bg-sky-900/75 p-3 rounded-xl' >Login</button>
            </div>
        </div>
    )
}
