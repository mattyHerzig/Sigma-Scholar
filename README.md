# Sigma Scholar
Making scholarships and counseling accessible using AI.

## Demo (click)

[![Demo](https://img.youtube.com/vi/rSGBWqR7Kjc/0.jpg)](https://youtu.be/rSGBWqR7Kjc "Sigma Scholar Demo")

## Introduction

We had the idea to create this project after going on [Scholarships.com](https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/residence-state/california) and realizing how hard it was to navigate. Despite being one of, if not, the most popular website for getting scholarships, it's *incredibly* difficult to use. Could you imagine being someone in an underprivileged community, who has to put aside tremendous amounts of time and effort just to look through all the possible scholarships you may be eligible for? We found this *unacceptable*.

To reiterate, the problem is that popular scholarship websites lack the ability to sort, search, and filter content that would make it leagues easier to use. Because the  requirements on these scholarship webpages aren't in defined and constant areas, you couldn't do the typical approach of web scraping a scholarship's information using something like Regex. Sigma Scholar seeks to solve this problem using AI web scraping. In addition, we also provide AI counseling features to encourage pursuing higher encourage and to faciliate easy queries of the data (i.e. get scholarships given your variables).

## Table of Contents
* [Demo (click)](#demo-click)
* [Introduction](#introduction)
* [Inspiration](#inspiration)
* [What It Does](#what-it-does)
* [How We Built It](#how-we-built-it)
* [Challenges We Ran Into](#challenges-we-ran-into)
* [Accomplishments We’re Proud Of](#accomplishments-were-proud-of)
* [What We Learned](#what-we-learned)
* [What's Next](#whats-next)


## Inspiration

One of the biggest problems we have as a society is the lack of accessibility to educational opportunities for deserving students. We found that most popular scholarship websites are terrible in terms of formatting and structure. There was no way to filter options and scholarships could only be searched by name. Imagine how an underprivileged student may try to navigate this website but struggle to find one that fits them best. We thought that this big problem could be solved by creating a website that allows filtering and sorting scholarships based on various criteria such as academic achievement, financial need, area of study, and more. We aimed to democratize access to scholarships and empower students from all backgrounds to pursue their educational aspirations.

## What It Does

Our website uses LlamaIndex’s AI web scraper to scrape the scholarships.com website and obtain eligibility requirements using AI to parse unorganized data. With this information, we recommend the user a list of scholarships based on a list of information they fill out on a form. After doing so, the user is then able to sort the list by certain criteria as well as filtering criteria that they feel would fit them best. Additionally, the scholarship data is used by an AI counselor.

## How We Built It

We used Flask as our backend to web scrape the scholarship website and passed the information from the web scraping to our frontend. We used Next.js as our frontend to build the website and display the information about the scholarships that the backend obtained. 

## Challenges We Ran Into

Our team struggled at first with integrating the LlamaIndex and implementing the web scraping for the scholarship website. Another challenge we faced was throughout the process of using the AI. The AI would hallucinate a lot and getting results from it would often take 20-30 minutes for each process, taking up a majority of our work time and leaving us with a limited amount of time to optimize its effectiveness.

## Accomplishments We’re Proud Of

We are extremely proud of the program we came up with to use the AI scraper to parameterize each scholarship. We were also proud of how we divided work as a team, allocating tasks to each of our team members. This was especially seen when the AI was running on one of our computers, forcing us to work collaboratively on certain parts.


## What We Learned

We learned a lot of valuable lessons throughout building this project, many of which were related to the AI. Throughout our journey with using it, we found that it takes a lot of computing power and a lot of time just to run one process of web scraping.

## What's Next

We believe that the next best step is to get more scholarships by web scraping other scholarship websites that may have scholarships posted that scholarships.com does not have. Our next step afterward would be to allow the counselor to use the user information to assist them in creating an appealing resumé and filling out their college applications and essays.






