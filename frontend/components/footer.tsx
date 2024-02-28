import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-white p-4 border-gray-200 border-2 fixed bottom-0 w-full">
      <div className="flex justify-between items-center">
        <div className="flex items-center flex-shrink-0 text-white mr-6">
          <span className="font-semibold text-xl tracking-tight"></span>
        </div>
        <div className="flex justify-end">
          <a href='/about' className="text-black">About Us</a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
