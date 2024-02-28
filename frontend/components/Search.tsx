import React from 'react'
import Fuse from 'fuse.js'

export default function Search({scholarships, setSearch}: any) {
const fuse = new Fuse(scholarships, {
    keys: ['name', 'description', 'location'],
    includeScore: true,
    threshold: 0.4 // Adjust this for more or less strict matching
});

const handleSearch = (event: any) => {
    const { value } = event.target;
    if (value.length > 0) {
        const results = fuse.search(value);
        const matches = results.map(result => result.item);
        setSearch(matches);
    } else {
        setSearch(scholarships);
    }
    };
  return (
    <>
        <input
            type="search"
            placeholder="Search for scholarships"
            onChange={handleSearch}
            className="w-full rounded-full border-2 border-gray-200 mb-4 focus:outline-none shadow-xl p-4"
        />
    </>
  )
}
