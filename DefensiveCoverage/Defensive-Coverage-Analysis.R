# CMU Conference Analysis
# PURPOSE: Analyze the Shots dataframe that has calculated values of defensive coverage

# Set working directory
# setwd()

# Install Packages
if(length(grep('ggplot2',installed.packages()))<1){install.packages('ggplot2')}

# Require Packages
require('ggplot2')

# Read in shots from csv
Shots = read.csv("shots_defensive_coverage.csv")[,-1]
which(Shots$PLAYER_NAME=="Klay Thompson"&Shots$Defensive.Coverage.Normalized>0)

# Indices of shots that were successful and that failed
make = which(Shots$Defensive.Coverage.Normalized>0 & 
               Shots$Defensive.Coverage.Normalized<100 &
               Shots$SHOT_MADE_FLAG==1 )
miss = which(Shots$Defensive.Coverage.Normalized>0 & 
               Shots$Defensive.Coverage.Normalized<100 &
               Shots$SHOT_MADE_FLAG==0)

# Fine tune shot distances (divide by 10)
i = NULL
for (i in c(make,miss)){
  Shots$Defensive.Coverage.Normalized[i] = Shots$Defensive.Coverage.Normalized[i]/10
}

# Analysis
coverages = c(Shots$Defensive.Coverage.Normalized[miss],
              Shots$Defensive.Coverage.Normalized[make])
category = c(rep("Miss",length(miss)),rep("Make",length(make)))
df = data.frame(Category=category,Coverage=coverages)
plot = ggplot(df,aes(x=Coverage,fill=Category)) + 
  geom_histogram(aes(y=..density..),binwidth=0.5, position = "dodge2",) +
  labs(title="Histogram of Normalized Defensive Coverages for Makes and Misses", 
       x = "Normalized Defensive Coverage (feet)",
       y = "Density of Shots") +
  stat_function(fun=dnorm,
                color="deepskyblue2",
                args=list(mean=mean(Shots$Defensive.Coverage.Normalized[make]), 
                          sd=sd(Shots$Defensive.Coverage.Normalized[make])))+
  stat_function(fun=dnorm,
                color="red2",
                args=list(mean=mean(Shots$Defensive.Coverage.Normalized[miss]), 
                          sd=sd(Shots$Defensive.Coverage.Normalized[miss])))+
  theme_minimal() +
  theme(axis.text=element_text(size=14,face="bold"),
        axis.title=element_text(size=14))+
  theme(plot.title = element_text(hjust = 0.5))+
  scale_fill_manual(values=c("deepskyblue3", "red3"))+
  theme(legend.position="right",legend.title = element_blank())+theme(
    axis.title.x = element_text(margin = unit(c(3, 0, 0, 0), "mm")),
    axis.title.y = element_text(margin = unit(c(0, 3, 0, 0), "mm"), angle = 90))
plot

# Gaussian analysis of curves
mean_make = mean(Shots$Defensive.Coverage.Normalized[make])
sem_make= sd(Shots$Defensive.Coverage.Normalized[make])/sqrt(length(make))

mean_miss = mean(Shots$Defensive.Coverage.Normalized[miss])
sem_miss = sd(Shots$Defensive.Coverage.Normalized[miss])/sqrt(length(miss))

# Worst 10 players with respect to Normalized Defensive Coverages
ranking_worst = sort(Shots$Defensive.Coverage.Normalized[make],decreasing=F)
players_worst = NULL
for (i in 1:10){
  players_worst[i] = which(Shots$Defensive.Coverage.Normalized==ranking_worst[i])
}
players_worst = Shots$PLAYER_NAME[players_worst]
players_worst
ranking_worst[1:10]

# Best 10 players with respect to Normalized Defensive Coverages
ranking_best = sort(Shots$Defensive.Coverage.Normalized[make],decreasing=T)
players_best = NULL
for (i in 1:10){
  players_best[i] = which(Shots$Defensive.Coverage.Normalized==ranking_best[i])
}
players_best = Shots$PLAYER_NAME[players_best]
players_best
ranking_best[1:10]
