// components/ScholarshipModal.js
import { useState } from 'react';

export default function ScholarshipModal({ isOpen, onClose,}: { isOpen: boolean, onClose: () => void, }) {
  const [formData, setFormData] = useState({
    scholarshipAmount: '',
    gpa: '',
    satScore: '',
    actScore: '',
    stateOrCountry: '',
    citizenship: '',
    educationLevel: '',
    gender: '',
    age: '',
    familyIncome: '',
    financialAidEligibility: false,
    raceEthnicity: '',
    militaryAffiliation: false,
  });

  const handleChange = (e: any) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };



  const handleSubmit = async () => {
    console.log(formData);
    const response = await fetch('/api/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
        });
    const data = await response.json();
    console.log(data);
}

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex justify-center items-center">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
        <h2 className="text-xl font-semibold mb-4">Scholarship Application</h2>
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 gap-6 overflow-y-auto max-h-96">
            {/* Text Inputs */}
            <input type="text" name="scholarshipAmount" placeholder="Scholarship Amount" value={formData.scholarshipAmount} onChange={handleChange} className="input p-1 border-2 border-gray-300 text-black"  />
            <input type="number" name="gpa" placeholder="Grade Point Average (GPA)" step="0.01" value={formData.gpa} onChange={handleChange} className="input p-1 border-2 border-gray-300 text-black" min = '0'max = "5" />
            <input type="text" name="satScore" placeholder="SAT Score" value={formData.satScore} onChange={handleChange} className="input p-1 border-2 border-gray-300 text-black" />
            <input type="text" name="actScore" placeholder="ACT Score" value={formData.actScore} onChange={handleChange} className="input p-1 border-2 border-gray-300 text-black" />
            <input type="text" name="stateOrCountry" placeholder="State or Country" value={formData.stateOrCountry} onChange={handleChange} className="input p-1 border-2 border-gray-300 text-black"  />
            <input type="text" name="citizenship" placeholder="Country of Citizenship" value={formData.citizenship} onChange={handleChange} className="input p-1 border-2 border-gray-300 text-black"  />
            
            {/* Select Dropdown */}
            <select name="educationLevel" value={formData.educationLevel} onChange={handleChange} className="select p-1 text-black border-2" >
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
            <input type="number" name="age" placeholder="Age" value={formData.age} onChange={handleChange} className="input text-black p-1 text-black border-2" min = "13"  />
            <input type="text" name="familyIncome" placeholder="Family Income" value={formData.familyIncome} onChange={handleChange} className="input text-black p-1 text-black border-2" />

            {/* Checkbox */}
            <label className='text-black'><input type="checkbox" name="financialAidEligibility" checked={formData.financialAidEligibility} onChange={handleChange} /> Eligible for Financial Aid</label>
            <label className='text-black'><input type="checkbox" name="militaryAffiliation" checked={formData.militaryAffiliation} onChange={handleChange} /> Military Affiliation</label>

            {/* More Inputs as Needed */}
            <input type="text" name="raceEthnicity" placeholder="Race / Ethnicity" value={formData.raceEthnicity} onChange={handleChange} className="input text-black p-1 text-black border-2" />

            {/* Submission */}
            <div className="flex justify-end space-x-2">
              <button type="button" onClick={onClose} className="btn-cancel">Cancel</button>
              <button type="submit" onClick={handleSubmit}className="btn-submit text-blue-500">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
