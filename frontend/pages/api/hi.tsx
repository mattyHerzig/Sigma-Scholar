import type { NextApiRequest, NextApiResponse } from 'next'



export default async function handler(req: NextApiRequest, res: NextApiResponse) {

    try {
        let config = {
            method: 'GET',
            headers: {},
        };

        await fetch('localhost:5000/', config).then(resp => resp.json()).then(response => { console.log(response); res.status(200).json(response) });
    } catch (err) {
        res.status(500).json({ error: 'failed to load data' })
    }
}