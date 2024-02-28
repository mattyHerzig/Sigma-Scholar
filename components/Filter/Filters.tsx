// "use client"
import React, {useState} from 'react'
import Amount from './Amount'
import Filter from './Filter'
import Gpa from './Gpa'
import ScholarshipFilter from '../ScholarshipFilter'
import Race from './Race';
import Deadline from './Deadline';
// import ReactSlider from 'react-slider'

export default function Filters({scholarships, setSearch}: any) {
  // const [value, setValue] = React.useState([0, 100])
  
  let [isOpen, setIsOpen] = useState<any>(false)
  return (
    <div className='pb-5 flex flex-row items-center w-full justify-evenly'>
        <Filter name={"Amount"}>
          <Amount scholarships={scholarships} setSearch={setSearch}/>
        </Filter>

        <Filter name={"Deadline"}>
          <Deadline scholarships={scholarships} setSearch={setSearch}/>
        </Filter>

        <Filter name={"GPA"}>
          <Gpa scholarships={scholarships} setSearch={setSearch}/>
        </Filter>

        <Filter name={"Ethnicity"}>
          <Race scholarships={scholarships} setSearch={setSearch}/>
        </Filter>

        {/* <IoFilterCircle size={50}> */}
          <ScholarshipFilter scholarships={scholarships} setSearch={setSearch} isOpen={isOpen} setIsOpen={setIsOpen}/>
        {/* </IoFilterCircle> */}
    </div>
  )
}
