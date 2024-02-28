// components/ScholarshipModal.js
import { useState, Fragment} from 'react';
import { Dialog, Transition } from '@headlessui/react';
// import ScholarshipFilter from '../ScholarshipFilter'
import { IoFilterCircle } from "react-icons/io5";
import Fuse from 'fuse.js';
import { IoOptionsOutline } from "react-icons/io5";

export default function ScholarshipModal({ scholarships, setSearch, isOpen, setIsOpen }: any) {
  const [formData, setFormData] = useState({
    scholarshipAmount: '',
    gpa: '',
    testScores: '',
    stateOrCountry: '',
    educationLevel: '',
    gender: '',
    age: '',
    familyIncome: '',
    financialAidEligibility: false,
    raceEthnicity: '',
    militaryAffiliation: false,
  });
  
  function closeModal() {
    setIsOpen(false)
  }

  function openModal() {
    setIsOpen(true)
  }

  const handleChange = (e: any) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();

    console.log(formData);

    let filtered = [...scholarships]
    console.log("original scholarships: ", filtered)
    
    if (formData.age != "") {
      filtered = scholarships.filter((scholarship: any) => {
        return scholarship.age >= Number(formData.age)
      })
    } 

    if (formData.educationLevel != "") {
      filtered = filtered.filter((scholarship: any) => {
        return scholarship.educationLevel === formData.educationLevel
      })
    }

    if (formData.familyIncome != ""){
      filtered =  filtered.filter((scholarship: any) => {
        return scholarship.familyIncome <= Number(formData.familyIncome)
      })
    }

    if (formData.gender != ""){
      filtered =  filtered.filter((scholarship: any) => {
        return scholarship.gender.toLowerCase() == formData.gender.toLowerCase()
      })
    }

    if (formData.gpa != ""){
      filtered =  filtered.filter((scholarship: any) => {
        return scholarship.gpa >= formData.gpa
      })
    }

    // filtered =  filtered.filter((scholarship: any) => {
    //   return scholarship.militaryAffiliation == formData.militaryAffiliation
    // })

    // filtered = filtered.filter((scholarship: any) => {
    //   return scholarship.financialAidEligibility === formData.financialAidEligibility
    // })

    if (formData.raceEthnicity != ""){
      let fuseOptions = {
        includeScore: true,
        threshold: 0.4, // Adjust this threshold to your preference for fuzziness
        keys: ['race'], // The keys in scholarship objects to match against
      };
  
      console.log("scholarships: ", scholarships)
      let fuse = new Fuse(filtered, fuseOptions);
  
      let fuzzyResults = fuse.search(formData.raceEthnicity);
  
      filtered = fuzzyResults.map((result: any) => result.item);
    }

    if (formData.scholarshipAmount != ""){
      filtered =  filtered.filter((scholarship: any) => {
        return scholarship.amount >= Number(formData.scholarshipAmount)
      })
    }

    if (formData.stateOrCountry != ""){
      console.log("stateOrCountry: ", formData.stateOrCountry)
      console.log("filtered: ", filtered)
      let fuseOptions = {
        includeScore: true,
        threshold: 0.4, // Adjust this threshold to your preference for fuzziness
        keys: ['residence'], // The keys in scholarship objects to match against
      };
  
      console.log("scholarships: ", scholarships)
      let fuse = new Fuse(filtered, fuseOptions);
  
      let fuzzyResults = fuse.search(formData.stateOrCountry);
  
      filtered = fuzzyResults.map((result: any) => result.item);
    }
    
    console.log("filtered: ", filtered)
    setSearch(filtered);
    setIsOpen(false);
    setFormData(
      {
        scholarshipAmount: '',
        gpa: '',
        testScores: '',
        stateOrCountry: '',
        educationLevel: '',
        gender: '',
        age: '',
        familyIncome: '',
        financialAidEligibility: false,
        raceEthnicity: '',
        militaryAffiliation: false,
      }
    )
  };

  
  return (
    <>
        {/* <button
          type="button"
          onClick={openModal}
          className="rounded-md bg-black/20 px-4 py-2 text-sm font-medium text-white hover:bg-black/30 focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75"
        >
          Open dialog
        </button> */}
        <button
          type='button'
          onClick={openModal}
        >
          <IoOptionsOutline
            size={50}
          />
        </button>

      <Transition appear show={isOpen} as={Fragment}>
        <Dialog as="div" className="relative z-10" onClose={closeModal}>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-black/25" />
          </Transition.Child>

          <div className="fixed inset-0 overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4 text-center">
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 scale-95"
                enterTo="opacity-100 scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 scale-100"
                leaveTo="opacity-0 scale-95"
              >
                <Dialog.Panel className="w-5/12 rounded-2xl bg-white p-6 text-left shadow-xl border-gray-200 border-2 transition-all">
                      <Dialog.Title className="text-2xl text-center font-semibold mb-4">Filter</Dialog.Title>
                      <form onSubmit={handleSubmit}>
                        <div className="grid grid-cols-1 gap-6 overflow-y-auto max-h-96 p-1">
                          {/* Text Inputs */}
                          <input type="text" name="scholarshipAmount" placeholder="Scholarship Amount" value={formData.scholarshipAmount} onChange={handleChange} className="input p-2 border-2 border-gray-200 text-black rounded-xl shadow-md focus:outline-none focus:ring focus:ring-gray-900"/>
                          <input type="number" name="gpa" placeholder="Grade Point Average (GPA)" step="0.01" value={formData.gpa} onChange={handleChange} className="input p-2 border-2 border-gray-200 text-black rounded-xl shadow-md focus:outline-none focus:ring focus:ring-gray-900" min = '0'max = "5"/>
                          <input type="text" name="testScores" placeholder="Test Scores" value={formData.testScores} onChange={handleChange} className="input p-2 border-2 border-gray-200 text-black rounded-xl shadow-md focus:outline-none focus:ring focus:ring-gray-900" />
                          <input type="text" name="stateOrCountry" placeholder="State or Country" value={formData.stateOrCountry} onChange={handleChange} className="input p-2 border-2 border-gray-200 text-black rounded-xl shadow-md focus:outline-none focus:ring focus:ring-gray-900"/>
                          
                          {/* Select Dropdown */}
                          <select name="educationLevel" value={formData.educationLevel} onChange={handleChange} className="select p-2 text-black border-2 border-gray-200 shadow-md rounded-xl focus:outline-none focus:ring focus:ring-gray-900">
                            <option value="">Select Education Level</option>
                            <option value="high_school">High School</option>
                            <option value="undergraduate">Undergraduate</option>
                            <option value="postgraduate">Postgraduate</option>
                          </select>

                          {/* Preset Buttons (Radio for exclusive selection) */}
                          <div className = "text-black">
                            <span >Gender: </span>
                            <label className='pr-2'><input type="radio" name="gender" value="male" onChange={handleChange} checked={formData.gender === 'male'} /> Male</label>
                            <label className='pr-2'><input type="radio" name="gender" value="female" onChange={handleChange} checked={formData.gender === 'female'} /> Female</label>
                            <label className='pr-2'><input type="radio" name="gender" value="other" onChange={handleChange} checked={formData.gender === 'other'} /> Other</label>
                          </div>

                          {/* Number Input */}
                          <input type="number" name="age" placeholder="Age" value={formData.age} onChange={handleChange} className="input text-black p-2 text-black border-2 border-gray-200 shadow-md rounded-xl focus:outline-none focus:ring focus:ring-gray-900" min = "13"/>
                          <input type="text" name="familyIncome" placeholder="Family Income" value={formData.familyIncome} onChange={handleChange} className="input text-black p-2 text-black border-2 border-gray-200 shadow-md rounded-xl focus:outline-none focus:ring focus:ring-gray-900"/>

                          {/* Checkbox */}
                          <label className='text-black'><input type="checkbox" name="financialAidEligibility" checked={formData.financialAidEligibility} onChange={handleChange} /> Eligible for Financial Aid</label>
                          <label className='text-black'><input type="checkbox" name="militaryAffiliation" checked={formData.militaryAffiliation} onChange={handleChange} /> Military Affiliation</label>

                          {/* More Inputs as Needed */}
                          <input type="text" name="raceEthnicity" placeholder="Race / Ethnicity" value={formData.raceEthnicity} onChange={handleChange} className="input text-black p-2 text-black border-2 border-gray-200 shadow-md rounded-xl focus:outline-none focus:ring focus:ring-gray-900" />

                          {/* Submission */}
                          <div className="flex justify-center space-x-4 text-lg font-semibold">
                            <button type="submit" className="btn-submit text-white bg-sky-900/75 p-2 rounded-full">Submit</button>
                            <button type="button" onClick={() => {setIsOpen(false)}} className="btn-cancel">Cancel</button>
                          </div>
                        </div>
                      </form>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition>
    </>
  )
}
