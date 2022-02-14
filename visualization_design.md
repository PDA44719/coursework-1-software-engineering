•	The target audience for this visualisation. Consider using the relevant persona (or other format) from COMP0035.

•	
The question that this visualisation is intended to answer. Use the questions you identified in COMP0035, or you can write new questions.


•	The data needed from your data set to answer the question


•	The type of chart (e.g. pie, bar etc) and its appropriateness for the question/audience. Use the resources given in the teaching materials.


•	The visual aspects of the design (e.g. style, colours, titles). Use the literature and resources introduced in the teaching materials; or other relevant sources from your independent literature research.

## Visualization Design
**The target audience is the same for all visualizations. I should probably ask whether I have to comment on it every
time**.
### Graph 1
The first question that will be addressed is the following: **Which movie genres are more popular (i.e., with respect to
the revenue)?**. To answer this question, the **"Genres"** column will be used. I will be adding the revenue of movies
that contain a specific genre (i.e., for each of the genres), and then I will compute the average.

#### Type of chart
In order to choose a graph, a resource that I used is [2], which provides a guide to choose a chart type. The 4th
question discussed in the article (*"what is your data type?"*), it is stated that: "if you have categorical data,
then using a bar chart or a pie chart may be a good idea". As movie genres are categorical data, it would make sense to
use one of the two different types. I will not be using a pie chart, because movies can have more than one genre.
Hence, the percentages displayed on that chart would be misleading.

Another aspect that must be considered is the fact that not all movies have been considered: there are movies that came
out after the creation of the dataset and others that came out before 2018 that have not been included. Hence, we want
to know the accuracy of our calculations when it comes to predicting revenues of the overall movies (not just the sample
of movies utilized for the figures). For that matter, bars will be included representing the standard error of each
genre. [5] gives a good explanation about the standard error, with a very good example about the average age of people
that are diagnosed with Alzheimer's (furthermore, it also includes details about how to calculate it).

#### Visual Aspects
The main issue with this graph is that it could be deceitful should it not be titled properly. In **(the truthful art)
(required citation [1])**, the five qualities of great visualizations are explored. One of them is truthfulness, for
which the designer must ask: **is anything being obscured?**. If the title was named: **Genre Revenue per Movie**, there
would be some information omitted: movies usually have more than one genre. Therefore, we need a title that makes this
clear.

The title that was considered best is: **Average Revenue for Movies Containing
Elements of Each Main Genre**. Containing elements of indicates that movies can have elements that are not limited to
just one genre. Furthermore, the addition
of the word **Main** indicates the existence of other genres that may not have been considered in our graph.
[7] displays an animation in which it is shown that the labels (including the title) must be simplified to avoid
redundancy. While this title may not be considered simple, I believe that choosing to avoid potentially deceiving users,
even if that requires a longer and more tedious title, was the proper way to go for my chart.

This graph is aimed at film producers, each of whom will have a set of preferred genres. Therefore, it would be ideal
if users could have the option to highlight their own preferred genres so that they can have an easier time to visually
understand how potentially profitable each of them can be.

#### Visualization Evaluation
The question that was asked is which movie genres are more popular. Therefore, after creating the chart, I realized
that there was a problem with only considering the mean: genres who appear on a high number of movies and others who are
rarer might not appear to be too different when it comes to popularity.
Hence, I decided to also create a chart displaying the overall revenue of the genres. This chart will have the similar
style as the previous one. The combination of both graphs will provide a bigger picture.

After seeing both charts, I realized that there is an issue with the two less profitable genres: Documentary and
Western. These make considerable less money than the others. Hence, it is difficult to
see their revenue when compared to the other genres (especially in the overall revenue chart). A potential way to solve
this would be to utilize a logarithmic scale on the y-axis. This, however, makes comparisons more difficult to grasp
visually (due to the non-linearity of the axis). Hence, it was decided that linear axis would be better.
Another potential way to solve the issue would be to not include those two genres in the chart, stating that they were
excluded due to them not meeting a minimum amount required (for instance).

### Graph 2
The question to be addressed with this graph is: "What are the most popular runtimes and how much money do they make?"
To answer this question, the Runtime column from the dataset will be utilized.

#### Type of chart
This time, the data is continuous, which rules out bar or pie charts. A useful question that I asked myself is: "What
story is your data trying to deliver?" [2]. The purpose of this question is not finding a trend (for which a scatter plot
or a line graph could have been utilized), but showing a distribution. The search by function tab on [3], shows the different
kinds of graphs that can show the distribution of the data (e.g., density plot, box & whisker plot). I will be utilizing
a histogram because that is the type that I am more familiar with.

#### Visual aspects
Again, for the histograms we need to consider the fact that the revenue can be considered as the overall revenue or the
mean. Therefore, two different plots will be created.

The titles that will be utilized for the figures are Overall Revenue vs Runtime distribution and Mean Revenue vs Runtime
Distribution. These titles are kept simple and to the point.

The movies range from 40 to 200 minutes. Hence, there are 160 minutes displayed in the x-axis. We can create bins
that have groups of 20-minute ranges. Which means that 8 total bins would be used. Furthermore, the y-axis

Lastly, I want users to be able to see the number of movies that each bin contains, so that they can have an
understanding of how common those runtimes are (which will also help to answer the first part of the question: what are
most popular runtimes).

#### Visualization Evaluation
Even though it was initially intended to utilize linear y-axis, it was decided not to use them because for both the
overall and mean revenue histograms, there were some categories that had a significantly higher revenue than the rest,
which made it challenging to appreciate the differences between the runtimes. Hence, a logarithmic scale was utilized
in the end.

The second problem that was encountered is that including the number of movies in each bin as part of the hover value
is not simple. [6] was analyzed to try to find a way to do this, but is does not seem to be possible using
go.Histogram. Therefore, I had to choose between using a histogram without including the count, or using a barchart to
try to include it. In the end, I decided to stick with histograms (due to bar charts having already been used) and
creating a third chart that showed the counts.

A potential way to improve this graph is to take into account the runtime of the movies created by the user and
display that information in the chart. For instance, the mean runtime could be calculated and the bin where that average
lies could be coloured differently; or the names of each movie made by the producer could be included as texts inside
the runtime bin they correspond to. This would allow users to have a deeper understanding of their own filmography.


### Graph 3
The question that will be answered with this graph is: How much are top movies making now compared to before and during
the 2019 pandemic? We will be using the Release Date column of the dataset.

#### Type of chart
The purpose of this chart is to display information over time. [3] shows that bubble charts, heatmaps, line and area
charts, etc. can be utilized in this case. Another important detail is that we are trying to find a trend (i.e., by
comparing values from 3 different time periods). Hence, an area chart will be used, because "Area charts are perfect
when communicating the overall trend, as opposed to the individual values" [4].

#### Visual aspects
As three different time periods will be analyzed, these different times must be indicated in the chart. A good way to
do this, extracted from the second tip found in [4] is to utilize opaque/transparent colors. Even though this piece of
advice is aimed at stacked area charts, it can be applied our situation (i.e., we will be creating three highlighted
regions whose colors must be opaque enough not to difficult the graph viewing).

Another important detail is that, because the plot will have different data points where the cursor would need to be
placed in order to display the hover data, a vertical line will be used to indicate the amount of revenue of each date
(i.e., there will be no need to place the cursor directly on the data point to display the information).

#### Visualization Evaluation
While sources like [8] indicate that there it is ideal to remove chartjunk (unnecessary embellishment) from charts, I
believe there are certain cases in which including embellishment is good. Background color is usually considered to be
distracting and not necessary to transmit the message of the chart. Nevertheless, I tried to create a chart that would
not have background colors for each period on the chart. As can be seen (***INCLUDE PICTURES***), adding those regions
creates a more impactful graph which will likely be easier to remember for the users (this is also mentioned on [8]).
Hence, I concluded that "chartjunk" can be better than plain in certain situations.

In order to improve the chart, something that could be done is to allow the user to select the range of time that they
want to visualize on the graph. A couple of input boxes could be introduced to select the limits of the x-axis, or even
a component named RangeSlider [9] could also be utilized. The reason why I decided not to include this is because users
can already select a specific range by using the cursor. Nevertheless, options like input boxes or RangeSliders would 
add a higher level of precision.

Another aspect which could be improved would be indicating the name of the movies that came out during each date. This
can be useful for film producers, who are likely to want to conduct some research about specific movies that may have
made a higher amount of money than they would have originally expected (I am assuming experienced film producers are
aware of most of the movies that are coming out).




[1] https://www.rootstrap.com/blog/data-visualization-and-truthful-art/
[2] https://towardsdatascience.com/data-visualization-101-how-to-choose-a-chart-type-9b8830e558d6
[3] https://datavizcatalogue.com/search/distribution.html
[4] https://visage.co/data-visualization-101-area-charts/
[5] https://toptipbio.com/standard-error-formula/#:~:text=To%20calculate%20the%20standard%20error,of%20the%20number%20of%20samples.
[6] https://plotly.com/python/histograms/
[7] https://www.darkhorseanalytics.com/blog/data-looks-better-naked
[8] https://www.enago.com/academy/chartjunk-how-to-avoid-confusing-elements-in-your-figures/
[9] https://dash.plotly.com/dash-core-components/rangeslider