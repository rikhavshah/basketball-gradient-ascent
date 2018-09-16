# CMU Conference Analysis
# PURPOSE: Utilize Shots.csv and Moments.csv to calculate "Normalized Defensive Coverage" 
# for each shot in Shots.csv.

# Be sure to set your working directory correctly
# setwd()

# Install pracma package
if(length(grep('pracma',installed.packages()))<1){install.packages('pracma')}
if(length(grep('ggplot2',installed.packages()))<1){install.packages('ggplot2')}

# Require pracma package
require('pracma')
require('ggplot2')

Shots = read.csv("Shots.csv")[,-1]
Moments = read.csv("Moments.csv")[,-1]

# indices of made and missed jumpshots of the Shots dataframe
made = which(Shots$SHOT_MADE_FLAG==1)
miss = which(Shots$SHOT_MADE_FLAG==0)

# Tactical (defensive coverage by closest defender) vector generation
i = NULL
Defensive.Coverage.Normalized = NULL
for (i in 1:nrow(Shots)){
  team_id = Shots$TEAM_ID[i]
  indices = which(Moments$CORRESPONDING.SHOT==i)
  j = NULL
  coverage_points = NULL
  time_points = NULL
  if(length(indices)>0){
  for (j in indices){
    if (length(which(Moments[j,]==Shots$PLAYER_ID[i]))>0 & 
        length(which(Moments$CORRESPONDING.SHOT==i))>0){
  if (Moments$TEAM2_ID[j]==team_id){
    x1 = Moments$PLAYER1_X[j]
    x2 = Moments$PLAYER2_X[j]
    x3 = Moments$PLAYER3_X[j]
    x4 = Moments$PLAYER4_X[j]
    x5 = Moments$PLAYER5_X[j]
    y1 = Moments$PLAYER1_Y[j]
    y2 = Moments$PLAYER2_Y[j]
    y3 = Moments$PLAYER3_Y[j]
    y4 = Moments$PLAYER4_Y[j]
    y5 = Moments$PLAYER5_Y[j]
    ID_indice = which(Moments[j,]==Shots$PLAYER_ID[i])
    X = Moments[j,][ID_indice+1]
    Y = Moments[j,][ID_indice+2]
  } else {
    x1 = Moments$PLAYER6_X[j]
    x2 = Moments$PLAYER7_X[j]
    x3 = Moments$PLAYER8_X[j]
    x4 = Moments$PLAYER9_X[j]
    x5 = Moments$PLAYER10_X[j]
    y1 = Moments$PLAYER6_Y[j]
    y2 = Moments$PLAYER7_Y[j]
    y3 = Moments$PLAYER8_Y[j]
    y4 = Moments$PLAYER9_Y[j]
    y5 = Moments$PLAYER10_Y[j]
    ID_indice = which(Moments[j,]==Shots$PLAYER_ID[i])
    X = Moments[j,][ID_indice+1]
    Y = Moments[j,][ID_indice+2]
  }
    dx1 = X - x1
    dx2 = X - x2
    dx3 = X - x3
    dx4 = X - x4
    dx5 = X - x5
    dy1 = Y - y1
    dy2 = Y - y2
    dy3 = Y - y3
    dy4 = Y - y4
    dy5 = Y - y5
    
    d1 = sqrt((dx1*dx1)+(dy1*dy1))
    d2 = sqrt((dx2*dx2)+(dy2*dy2))
    d3 = sqrt((dx3*dx3)+(dy3*dy3))
    d4 = sqrt((dx4*dx4)+(dy4*dy4))
    d5 = sqrt((dx5*dx5)+(dy5*dy5))
    D = min(c(d1,d2,d3,d4,d5)[[1]])
    
    coverage_points[which(indices==j)] = D
    if (j == indices[1]){
      time_points[1] = 0
    } else {
      time_points[which(indices==j)] = Moments$GAME_TIME_LEFT[indices[1]]-Moments$GAME_TIME_LEFT[j]
    }
    } 
  } # end for(j in indices) loop
  }
  
  if(length(which(Moments$CORRESPONDING.SHOT==i))>0 & length(indices)>0){
  Defensive.Coverage.Normalized[i] = trapz(time_points,coverage_points)/
    (Moments$GAME_TIME_LEFT[indices[1]]-Moments$GAME_TIME_LEFT[indices[length(indices)]])
  print(i)
  }
} # end for(i in 1:nrow(Shots)) loop

Shots = cbind(Shots,Defensive.Coverage.Normalized)
colnames(Shots)[ncol(Shots)] = "Defensive.Coverage.Normalized"

# write new Shots dataframe with calculated defensive coverages to csv
write.csv(Shots,"shots_defensive_coverage.csv")

# example D vs t plot for Klay Thompson 
i = 46571
j = NULL
coverage_points = NULL
time_points = NULL
indices = which(Moments$CORRESPONDING.SHOT==i)
team_id = Shots$TEAM_ID[i]
for (j in indices){
  if (length(which(Moments[j,]==Shots$PLAYER_ID[i]))>0 & 
      length(which(Moments$CORRESPONDING.SHOT==i))>0){
    if (Moments$TEAM2_ID[j]==team_id){
      x1 = Moments$PLAYER1_X[j]
      x2 = Moments$PLAYER2_X[j]
      x3 = Moments$PLAYER3_X[j]
      x4 = Moments$PLAYER4_X[j]
      x5 = Moments$PLAYER5_X[j]
      y1 = Moments$PLAYER1_Y[j]
      y2 = Moments$PLAYER2_Y[j]
      y3 = Moments$PLAYER3_Y[j]
      y4 = Moments$PLAYER4_Y[j]
      y5 = Moments$PLAYER5_Y[j]
      ID_indice = which(Moments[j,]==Shots$PLAYER_ID[i])
      X = Moments[j,][ID_indice+1]
      Y = Moments[j,][ID_indice+2]
    } else {
      x1 = Moments$PLAYER6_X[j]
      x2 = Moments$PLAYER7_X[j]
      x3 = Moments$PLAYER8_X[j]
      x4 = Moments$PLAYER9_X[j]
      x5 = Moments$PLAYER10_X[j]
      y1 = Moments$PLAYER6_Y[j]
      y2 = Moments$PLAYER7_Y[j]
      y3 = Moments$PLAYER8_Y[j]
      y4 = Moments$PLAYER9_Y[j]
      y5 = Moments$PLAYER10_Y[j]
      ID_indice = which(Moments[j,]==Shots$PLAYER_ID[i])
      X = Moments[j,][ID_indice+1]
      Y = Moments[j,][ID_indice+2]
    }
    dx1 = X - x1
    dx2 = X - x2
    dx3 = X - x3
    dx4 = X - x4
    dx5 = X - x5
    dy1 = Y - y1
    dy2 = Y - y2
    dy3 = Y - y3
    dy4 = Y - y4
    dy5 = Y - y5
    
    d1 = sqrt((dx1*dx1)+(dy1*dy1))/10
    d2 = sqrt((dx2*dx2)+(dy2*dy2))/10
    d3 = sqrt((dx3*dx3)+(dy3*dy3))/10
    d4 = sqrt((dx4*dx4)+(dy4*dy4))/10
    d5 = sqrt((dx5*dx5)+(dy5*dy5))/10
    D = min(c(d1,d2,d3,d4,d5)[[1]])
    
    coverage_points[which(indices==j)] = D
    if (j == indices[1]){
      time_points[1] = 0
    } else {
      time_points[which(indices==j)] = Moments$GAME_TIME_LEFT[indices[1]]-Moments$GAME_TIME_LEFT[j]
    }
  } 
}

DF = data.frame(TIME = time_points,COVERAGE =coverage_points)
p = ggplot(data=DF,aes(x=TIME,y=COVERAGE)) + geom_line(color="dodgerblue3") + geom_point(color="dodgerblue3")
p = p + theme_minimal()
p = p + theme(axis.text=element_text(size=14,face="bold"),
              axis.title=element_text(size=14))+
  theme(plot.title = element_text(hjust = 0.5))
p = p + labs(title="Example Graph of D versus t for Klay Thompson", 
            x = "t (seconds)",
            y = "D (feet)")
p = p +theme(
  axis.title.x = element_text(margin = unit(c(3, 0, 0, 0), "mm")),
  axis.title.y = element_text(margin = unit(c(0, 3, 0, 0), "mm"), angle = 90))
p
pp = p + geom_area(fill="gold") 
pp
