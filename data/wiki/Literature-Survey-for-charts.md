The literature survey was done in September 2022 and it highlights the recent work done by several researchers in extracting the relevant data from charts

One of the first papers that used ML on charts was proposed by Savva et al.[1]. The authors had named their model "ReVision" and tried to incorporate ML and image processing techniques to extract data from charts. The authors classified the charts using a Deep Learning based classifier. Depending on the classification, they suggested custom image processing techniques for different categories of charts. 

Other researchers tried to expand on ReVision, by making minor modifications to the architecture[3,5-7]. However, the work done in these papers cannot be generalized to a large set of charts.

Hence to tackle this issue, Dan et al. proposed a Computer Vision(CV) inspired model named Chart Decoder[2]. The Chart Decoder combined image processing with OCR for data extraction. Building up on Chart Decoder, Mishra et al.[4] proposed new model called ChartsVi which tried to generalize the system to a larger group of charts. Fig 1 highlights the workflow of the ChartsVi model. 

<img width="1004" alt="Screen Shot 2022-09-12 at 5 21 29 PM" src="https://user-images.githubusercontent.com/27781159/189761146-448537db-cd7a-4f19-b79e-16bbe3e65f6c.png">
Fig1: ChartVi Architecture[4]


As visible in Fig1, the first step is to classify the chart. Following the classification, we need to apply image processing techniques. The image processing techniques vary based on the type of chart[3].  
 

**A good starting point:** I believe that it is not possible to create a single end-to-end ML system which can extract data from all the charts available on the internet. Most researchers initially implement a classifier for detecting the type of chart. Depending on the classification, the researchers determine the image processing techniques that can be applied on the chart. 

If we plan on expanding IMAGE to the charts domain, the best possible method would be to do a literature survey on the image processing techniques available for chart data extraction. Additionally, before developing the system, we would have to decide on the categories of charts that we are planning to tackle. This is pivotal as these categories would influence the training of the classifier as well as the image processing techniques used in the system.



References:

[1]Savva, Manolis, et al. "Revision: Automated classification, analysis and redesign of chart images." Proceedings of the 24th annual ACM symposium on User interface software and technology. 2011.

[2]Dai, Wenjing, et al. "Chart decoder: Generating textual and numeric information from chart images automatically." Journal of Visual Languages & Computing 48 (2018): 101-109.

[3]Jung, Daekyoung, et al. "Chartsense: Interactive data extraction from chart images." Proceedings of the 2017 chi conference on human factors in computing systems. 2017.

[4]Mishra, Prerna, et al. "ChartVi: Charts summarizer for visually impaired." Journal of Computer Languages 69 (2022): 101107.

[5]Cliche, Mathieu, et al. "Scatteract: Automated extraction of data from scatter plots." Joint European conference on machine learning and knowledge discovery in databases. Springer, Cham, 2017.

[6]Poco, Jorge, and Jeffrey Heer. "Reverse‐engineering visualizations: Recovering visual encodings from chart images." Computer graphics forum. Vol. 36. No. 3. 2017.

[7]Al-Zaidy, Rabah A., Sagnik Ray Choudhury, and C. Lee Giles. "Automatic summary generation for scientific data charts." Workshops at the thirtieth aaai conference on artificial intelligence. 2016.