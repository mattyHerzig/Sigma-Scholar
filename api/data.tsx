import type { NextApiRequest, NextApiResponse } from 'next';
import fetch from 'node-fetch';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  return new Promise(async () => {
    console.log('got message');
    if (req.method === 'GET') {
      // Fetch data from Flask server
      let config = {
        method: 'GET',
      };
      try {
        const response = await fetch('http://localhost:5000/rag-query?query=' + req.query['query'], config);
        console.log("aaa", response);
        const data = await response.json();
        console.log("aaa", response);
        res.status(200).json(data);
      } catch (error) {
        // res.status(500).json({ error: error.message });
      }
    } else if (req.method === 'POST') {
      const { scholarshipAmount, gpa, satScore, actScore, stateOrCountry, citizenship, educationLevel, gender, age, familyIncome, financialAidEligibility, militaryAffiliation, raceEthnicity } = req.body;

      console.log("new", scholarshipAmount, gpa, satScore, actScore, stateOrCountry, citizenship, educationLevel, gender, age, familyIncome, financialAidEligibility, militaryAffiliation, raceEthnicity);
      
      // Send data to Flask server
      try {


        const response = await fetch('http://127.0.0.1:5000/post-data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message:req.body.message
          })
        });
        const data = await response.json();
  
        console.log(data);
        console.log(data.body.message);
        res.status(201).json(data);
      } catch (error) {
        // res.status(500).json({ error: error.message });
      }
    } else {
      res.status(405).json({ error: 'Method Not Allowed' });
    }
  });
}
