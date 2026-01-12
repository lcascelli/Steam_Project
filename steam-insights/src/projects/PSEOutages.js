export const PSEOutages = {
    id: 'pse-outages',
    title: 'Interactive Visualization of Puget Sound Energy Outages',
    description: `An interactive dashboard visualizing current outage data from Puget Sound Energy (PSE). Scraped from the PSE website, this dashboard (shiny app)
    allows users to see total number of planned and unplanned outages, the number of customers affected, number of outages by city, and timeline of outages with incident 
    details. Explore outages, affected areas, and restoration times through dynamic charts and maps.`,
    techstack: ["R", 
    "Shiny",
    "tidyverse",
    "ggplot2",
    "GitHub Actions",
    ],
    type: 'iframe',
    link: 'https://preliminarytestrunabl.shinyapps.io/PSE_Outage_Dashboard/',
    repo: 'https://github.com/lcascelli/PSE-Outages'
}