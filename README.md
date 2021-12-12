<h1> Analyzing Explicit Content in Pop Culture Over Decades</h1> 
The project focuses on analyzing pop culture over decades and understanding if we have become more accepting of explicit content in the media we consume. We aim to analyze two main mediums: Music and Movies.<br  ><br  >

***Important:*** If you are going to run the project, please avoid running the kim_scraper.py file again to avoid unnecessary web requests. We have included the scraped data in the data folder. 

<h3>Datasets</h3>

[MPAA ratings dataset](https://data.world/studentoflife/imdb-top-250-lists-and-5000-or-so-data-records/workspace/file?filename=IMDBdata_MainData.csv)<br  >
[Kids-In-Mind](https://kids-in-mind.com/) (website scraped for data)<br  >
[Songs metadata dataset](https://data.mendeley.com/datasets/3t9vbwxgr5/2)<br  >
[Billboard Top 100](https://www.kaggle.com/dhruvildave/billboard-the-hot-100-songs)<br  >
[Profanity List](https://www.cs.cmu.edu/~biglou/resources/bad-words.txt)
<h3>Overview</h3>
We are going to test the following hypothesis:
<ol>
<li> Movie ratings have become less stringent about explicit (nudity, violence, language) content in movies.
<li> Music culture has become increasingly obscene over time.
        <ul>
        <li> Music lyrics contain a lot more profanity in recent years.
        <li> Songs genres with more explicit content have seen an increase in popularity over the recent years.
        </ul>
</ol>
The MPAA rates every movie on a discrete scale (G, PG, PG-13, R, NC-17). We want to see if over the years these ratings have become less stringent.
That is, does a modern movie contain more explicit content as compared to a similarly rated movie from the past.
To do this, we will scrape ratings data from Kids-In-Mind(KIM) website, an independent ratings agency, which rates the movies on three metrics (Language, Sex & Nudity, Violence & Gore) on a scale of 0 to 10. A higher KIM score indicates more extreme content. We chosse KIM because their rating metrics have remained consistent over the years, based on the overwhelmingly positive sentiment online.
We will use their comprehensive rating system to compare with the MPAA ratings over time.

To test the second hypothesis, we will be using the Top 100 Billboard songs data from each year and another dataset that contains songs’ metadata such as lyrics, genre.

***Note***: We have only included select visualizations that we wanted to highlighted for a brief overview of the hypotheses we have tested. For a deeper analysis, kindly go through the python notebook titled "Viz"

<h3>Hypothesis 1</h3>

Every year, the distribution of movies assessed changes. For example, if 1972 saw a release of 10 PG-13 movies and 2 R rated movies as compared to 1973 where 5 PG-13 rated movies and 10 R rated movies were released(these are made up values), the KIM score for 1973 would be higher as R-rated movies have a higher overall score. So to accurately assess stringency in movie ratings across the years, it was necessary that this data was normalized before using it to find correlations. We normalized the values by calculating the mean percentage distribution across the dataset, then applied these values across the years and used it to find weighted KIM scores.
As can be observed from the change in weighted KIM scores across years, movie ratings have become less stringent about explicit content in movies. 

<h4>Change in weighted KIM scores across the years</h4>

![](https://github.com/clonedapple/2021Fall_finals/blob/main/plots/weightedKIM.png)

<h3>Hypothesis 2</h3>
The change in profanity scores across the years plot shows that the music lyrics contain a lot more profanity in recent years.

<h4>Change in profanity scores across the years</h4>

![](https://github.com/clonedapple/2021Fall_finals/blob/main/plots/musicprofanity.png)

To analyze correlation between popularity and explicit content across genres we generated plots and correlations for each genre. We are calculating popularity of genre based on its percentage share in the billboards top 100 list for that year. After plotting and calculating correlations for each genre, we found out that the correlation varies from genre to genre. While pop had a positive correlation with profanity, rock and jazz had a negative correlation. Out of all the correlations calculated, only pop had a statistically significant value. Based on these results, we cannot conclude that songs genres with more explicit content have seen an increase in popularity over the recent years.
<h4>Correlation between profanity and popularity for pop </h4>

![](https://github.com/clonedapple/2021Fall_finals/blob/main/plots/pop.png)

<h3>Conclusion</h3>

We studied the change in explicit content in pop culture through the lens of movies and music. We observed an increasing amount of explicit content in movies across years which shows a ratings creep. Thus, we could conclude that movies ratings have become less stringent.
When we analysed music, we saw a similar trend. There was an increasing amount of profanity in music across years.  On analysing profanity and popularity across genres, we found that some genres such as pop and country had a positive correlation whereas genres such as rock and jazz had a negative correlation. While we were able to conclude that music contains a lot more profanity in recent years, we could not find a relationship between explicit content and popularity across music genres over the years.

