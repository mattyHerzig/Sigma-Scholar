import React, { PropsWithChildren } from "react";
import Navbar from "./navbar";
import Footer from "./footer";
const Layout = ({ children }: PropsWithChildren) => {
  return (
    <>
      <div className="bg-white">
        <Navbar />
        <div className="pt-16"> {/* Padding to push content below the navbar */}
          <div className="overflow-auto h-full"> {/* New scrolling container */}
            {children}
          </div>
        </div>
        {/* <Footer /> */}

      </div>
    </>
  );
};
export default Layout;
