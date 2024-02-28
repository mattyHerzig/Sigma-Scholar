import type { NextApiRequest, NextApiResponse } from 'next'



export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    let headers = new Headers();
    headers.append("Authorization", `Bearer ${req.body.cred}`);
    headers.append("Content-Type", `application/json`);
    console.log(`RECIEVED: ${req.body.subBody}`)
    try {


        let config = {
            method: 'PATCH',
            headers: headers,
            body: JSON.stringify(req.body.subBody)
        };
        let url = `https://mybusiness.googleapis.com/v4/${req.query['name']}?updateMask=event.title,summary,callToAction`;
        console.log("url:", url);
        await fetch(url, config)
            .then(response => { console.log(response); return response.json() }).then((resp) => { console.log(resp); res.status(200).json(resp) })
            .catch(error => console.log('error', error));
    } catch (err) {
        res.status(500).json({ error: 'failed to load data' })
    }
}