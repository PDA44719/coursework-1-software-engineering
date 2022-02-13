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
The first question that will be addressed is the following: **Which movie genres are more profitable?**. To answer
this question, the **"Genres"** column will be used. I will be adding the revenue of movies that contain a specific
genre (i.e., for each of the genres), and then I will compute the average.

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

This graph is aimed at film producers, each of whom will have a set of preferred genres. Therefore, it would be ideal
if users could have the option to highlight their own preferred genres so that they can have an easier time to visually
understand how potentially profitable each of them can be.

### Graph 2
The question to be addressed with this graph is: "What are the most popular runtimes and how much money do they make?"
To answer this question, the Runtime column from the dataset will be utilized.

#### Type of chart
This time, the data is continuous, which rules out bar or pie charts. A useful question that I asked myself is: "What
story is your data trying to deliver?" [2]. The purpose of this question is not finding a trend (for which a scatter plot
line graph would have been utilized), but showing a distribution. The search by function tab on [3], shows the different
kinds of graphs that can show the distribution of the data (e.g., density plot, box & whisker plot). I will be utilizing
a histogram because that is the type that I am more familiar with.

#### Visual aspects
The movies range from 40 to 200 minutes. Therefore, there are 160 minutes displayed in the x-axis. We can create bins
that have groups of 20-minute ranges. Which means that, we would be utilizing 8 total bins.

**May want to include stuff about color blindness**

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




[1] https://www.rootstrap.com/blog/data-visualization-and-truthful-art/
[2] https://towardsdatascience.com/data-visualization-101-how-to-choose-a-chart-type-9b8830e558d6
[3] https://datavizcatalogue.com/search/distribution.html
[4] https://visage.co/data-visualization-101-area-charts/
[5] https://toptipbio.com/standard-error-formula/#:~:text=To%20calculate%20the%20standard%20error,of%20the%20number%20of%20samples.