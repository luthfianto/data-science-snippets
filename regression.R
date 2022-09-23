df = read.csv("D:/telkom/telco_customer_churn.csv")
df[df == "No"] = 0
df[df == "Yes"] = 1

df$Partner = as.integer(df$Partner)
df$Dependents = as.integer(df$Dependents)
df$PhoneService = as.integer(df$PhoneService)
df$OnlineSecurity = as.integer(df$OnlineSecurity)
df$DeviceProtection = as.integer(df$DeviceProtection)

#df$TechSupport = as.integer(df$TechSupport)
#df$StreamingTV = as.integer(df$StreamingTV)
#df$StreamingMovies = as.integer(df$StreamingMovies)
#df$OnlineBackup = as.integer(df$OnlineBackup)

df$PaperlessBilling     = as.integer(df$PaperlessBilling)
df$Churn     = as.integer(df$Churn)
df = within(df, rm(customerID))
#df = within(df, rm(TotalCharges))
df = within(df, rm(MonthlyCharges))


lm.fit=glm(Churn ~ ., binomial, df)
smry.lm = summary(lm.fit)
smry.lm
modcoef <- summary(lm.fit)[["coefficients"]]
dfmod=as.data.frame(modcoef)
#dfmod$exp=exp(dfmod$Estimate)
dfmod=dfmod[order(-abs(dfmod$Estimate)), ]
s=dfmod[dfmod$`Pr(>|z|)` < 0.05 ,]
s=within(s, rm("z value"))
s=within(s, rm("Std. Error"))
