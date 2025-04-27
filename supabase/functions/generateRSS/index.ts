import "jsr:@supabase/functions-js/edge-runtime.d.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js'
import RSS from 'https://esm.sh/rss'

console.log("RSS Feed Generator Started!")

const supabaseUrl = Deno.env.get('SUPABASE_URL')!
const supabaseKey = Deno.env.get('SUPABASE_ANON_KEY')!
const supabase = createClient(supabaseUrl, supabaseKey)

Deno.serve(async (req) => {
  // Fetch jobs data from Supabase

  const url = new URL(req.url)
  const page = parseInt(url.searchParams.get('page') || '1') // Default page to 1
  const limit = parseInt(url.searchParams.get('limit') || '20') // Default limit to 30

  // Calculate the offset based on page number
  const offset = (page - 1) * limit

  const { data: jobs, error } = await supabase
    .from('jobs')
    .select('*')
    .order("publishedDateTime", { ascending: false })
    .range(offset, offset + limit)

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), { status: 500 })
  }

  // // Generate the RSS feed
  // const feed = new RSS({
  //   title: 'Job Listings RSS Feed',
  //   description: 'Latest job listings from our platform',
  //   feed_url: `${new URL(req.url).origin}/generateRSS`,
  //   site_url: 'https://yourdomain.com',
  // })

  // jobs.forEach((job) => {
  //   feed.item({
  //     title: job.title,
  //     description: job.description,
  //     url: `https://www.upwork.com/jobs/${job.ciphertext}`,
  //     team_name: job.team_name,
  //     team_photoUrl: job.team_photoUrl,
  //     client_country: job.country,
  //     date: job.publishedDateTime,
  //     custom_elements: Object.entries(job).map(([key, value]) => ({ [key]: value }))
  //   })
  // })

  // Generate the RSS feed
  const feed = new RSS({
    title: 'Job Listings RSS Feed',
    description: 'Latest job listings from our platform',
    feed_url: `${new URL(req.url).origin}/generateRSS?page=${page}`,
    site_url: 'https://yourdomain.com',
  })

  jobs.forEach((job) => {
    // Create HTML content dynamically for the job
    const contentHtml = `
      <h2>${job.title}</h2>
      ${Object.entries(job)
        .map(
          ([key, value]) => `
          <br /><b>${key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}:</strong> ${value ?? 'N/A'}</p>
        `
        )
        .join('')}
    `

    feed.item({
      title: job.title,
      description: job.description,
      url: `https://www.upwork.com/jobs/${job.ciphertext}`,
      date: new Date(job.publishedDateTime).toUTCString(), // Convert to standard RSS date format
      custom_elements: [
        { 'content:encoded': `<![CDATA[${contentHtml}]]>` },
        ...Object.entries(job).map(([key, value]) => ({ [key]: value }))
      ]
    })
  })

  return new Response(feed.xml({ indent: true }), {
    headers: { 'Content-Type': 'application/rss+xml' },
  })
})
