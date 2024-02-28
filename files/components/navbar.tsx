import Link from 'next/link';
import React from 'react';
import Image from 'next/image';

const Navbar = () => {
  return (
    <nav className="p-3 fixed w-full border-gray-200 border-b-2 rounded-md z-5 bg-white text-white">
      <div className="flex justify-between items-center">
        <div className="flex items-center flex-shrink-0 text-black mr-6">
          <Image src="/logo.svg" alt="Logo" width={32} height={32} />
          <h1 className='text-gray-900 text-xl font-bold pl-5'>Sigma Scholar</h1>
        </div>
        <div className="flex space-x-10 font-semibold">
          <a href="/scholarships" className="text-gray-900 text-xl hover:bg-gray-300 hover:text-black px-4 py-3 rounded-md text-sm font-medium">Scholarships</a>
          <a href="/counseling" className="text-gray-900 text-xl hover:bg-gray-300 hover:text-black px-4 py-3 rounded-md text-sm font-medium">Counseling</a>
          <a href="/login" className="text-gray-900 text-xl hover:bg-gray-300 hover:text-black px-4 py-3 rounded-md text-sm font-medium">Log in / Register</a>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;