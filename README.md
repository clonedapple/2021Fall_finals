The project focuses on analyzing pop culture over decades and understanding if we have become more accepting of explicit content in the media we consume. We aim to analyze two main mediums: Music and Movies.

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
To do this, we will scrape the data from Kids-In-Mind(KIM) website which rates the movies on three metrics (Language, Sex & Nudity, Violence & Gore) on a scale of 0 to 10. Higher KIM score indicates more extreme content. 
We will use this comprehensive rating to compare with the MPAA ratings over time.

To test the second hypothesis, we will be using the Top 100 Billboard songs data from each year and another dataset that contains songs’ metadata such as lyrics, genre.

***Note***: We have only included select visualizations that we wanted to highlighted for a brief overview of the hypotheses we have tested. For a deeper analysis, kindly go through the python notebook titled "Viz"

<h3>Hypothesis 1</h3>
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
