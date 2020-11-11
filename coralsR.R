library("devtools")
library("FactoMineR")
library("factoextra")
library("corrplot")
library("PerformanceAnalytics")
library("Hmisc")
coral_data <- read.csv("D:/Members/Cathy/coralAnalysis/Master Data - Sheet4.csv", header = T)
coral_data.useful <- coral_data[c(3:10)]

head(coral_data.useful)
rownames(coral_data.useful) <-   coral_data[,2]

coral_data.useful_stats <- data.frame(
  Min = apply(coral_data.useful, 2, min), # minimum
  Q1 = apply(coral_data.useful, 2, quantile, 1/4), # First quartile
  Med = apply(coral_data.useful, 2, median), # median
  Mean = apply(coral_data.useful, 2, mean), # mean
  Q3 = apply(coral_data.useful, 2, quantile, 3/4), # Third quartile
  Max = apply(coral_data.useful, 2, max) # Maximum
)
coral_data.useful_stats <- round(coral_data.useful_stats, 5)
head(coral_data.useful_stats)

cor.mat <- cor(coral_data.useful)
head(cor.mat)
corrplot(cor.mat, type="upper", order="hclust", 
         tl.col="black", tl.srt=45)

chart.Correlation(coral_data.useful, histogram=TRUE, pch=19)
res.pca <- PCA(coral_data.useful)
plot(res.pca, choix = "var")
