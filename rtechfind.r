library("TTR")
data2380 <- getYahooData("2380.HK", format(Sys.Date()-365, format="%Y%m%d"),format(Sys.Date()-1, format="%Y%m%d") )
rsi14 <- RSI(data2380[,c('Close')],n=14)
final <- merge(data2380,rsi14)
df <- data.frame(Time= index(final),final[,"Close"],final[,"EMA"])
newdf <- tail(df,n=20)
fitclose <-lm(formula = Close ~ Time, data = newdf)
fitrsi <- lm(formula = EMA ~ Time, data = newdf)
slopeClose <- summary(fitclose)$coefficients[[2]]
slopeRSI <- summary(fitrsi)$coefficients[[2]]
rsiCurrent<-coredata(final[Sys.Date()-1,'EMA'])[1]
if (rsiCurrent > 70 || rsiCurrent < 30) { 
  if ( (slopeClose > 0 && slopeRSI <0) || (slopeClose < 0 && slopeRSI >0) ) {
    print("Trend Reversal")
  }
} else if (rsiCurrent > 80) {
  print("Over-brought")
} else if (rsiCurrent < 20) {
  print("Over-sell")
}

