export async function POST(req) {

  const body = await req.json()

  const res = await fetch("http://127.0.0.1:8000/login",{
    method:"POST",
    headers:{
      "Content-Type":"application/json"
    },
    body: JSON.stringify(body)
  })

  const data = await res.json()

  return Response.json(data,{ status: res.status })
}