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
The first question that will be addressed is the following: **"Which movie genres are more profitable?"**. To answer
this question, the **"Genres"** column will be used. I will be extracting information about each of the genres (i.e.,
the overall, mean and standard deviation of the revenue and the rating) by utilizing a function named **extract_sms**.

In order to choose a graph, a resource that I used is [2], which provides a guide to choose a chart type. In the 4th
question discussed in the article (*"what is your data type?"*), it is stated that: "if you have categorical data,
then using a bar chart or a pie chart may be a good idea". As movie genres are categorical data, it would make sense to
use one of the two different types. I will not be using a pie chart, because of two reasons: 
- Movies usually have more than one genre. Hence, the sizes of each genre within the pie chart would not be representative of the actual distribution.

The main issue with this graph is that it could be deceitful should it not be titled properly. In **(the truthful art)
(required citation [1])**, the five qualities of great visualizations are explored. One of them is truthfulness, for which
the designer must ask: "is anything being obscured?". If the title was named: **Genre Revenue per movie**, there would
be some information omitted: movies usually have more than one genre. Therefore, we need a title that indicates that
movies can have a range of genres. Hence, the title that was considered best is: **Average Revenue for Movies Containing
Elements of Each Main Genre**. This title is considered clearer for the purpose of the graph. Furthermore, the addition
of the keyword **Main** indicates the existence of other genres that may not have been considered in our graph.


[1] https://www.rootstrap.com/blog/data-visualization-and-truthful-art/
[2] https://towardsdatascience.com/data-visualization-101-how-to-choose-a-chart-type-9b8830e558d6