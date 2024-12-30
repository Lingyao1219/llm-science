# Read data
dat <- read.csv('D:\\Short_Research\\LLM_SoS\\desc_df_did.csv')
# Using ml as control
dat <- dat[dat$type != 'nonllm',]
# Remove those with less obervations
dat$year <- as.Date(dat$year)
# dat <- dat[as.numeric(format(dat$year, '%Y')) >= 2019,]
dat <- dat[dat$count>10,]
fields <- unique(dat[dat$type == 'llm', 'fields'])

for (kk in c('entropy_inst', 'entropy_dep')) {
  list_result <- data.frame()
  for (ccount in 1:length(fields)) {
    eachf <- fields[ccount]
    dat_Each <- dat[dat$fields == eachf,]
    rownames(dat_Each) <- NULL
    dat_Each$time <- ifelse(as.numeric(format(dat_Each$year, '%Y')) >= 2023, 1, 0)
    dat_Each$treated <- ifelse(dat_Each$type == 'llm', 1, 0)
    dat_Each$did <- dat_Each$time * dat_Each$treated
    didreg <- lm(dat_Each[, kk] ~ treated + time + did, data = dat_Each)

    list_result_1 <- as.data.frame(coef(summary(didreg)))
    list_result_1$Name <- eachf
    list_result_1$Est <- row.names(list_result_1)
    list_result <- rbind(list_result, list_result_1)
  }
  rownames(list_result) <- NULL
  write.csv(list_result, paste('D:\\Short_Research\\LLM_SoS\\did_ml', kk, '.csv', sep = ''))
}


# Read data
dat <- read.csv('D:\\Short_Research\\LLM_SoS\\desc_df_did.csv')
# Using nonllm as control
dat <- dat[dat$type != 'ml',]
# Remove those with less obervations
dat$year <- as.Date(dat$year)
# dat <- dat[as.numeric(format(dat$year, '%Y')) >= 2019,]
dat <- dat[dat$count>10,]
fields <- unique(dat[dat$type == 'llm', 'fields'])

for (kk in c('entropy_inst', 'entropy_dep')) {
  list_result <- data.frame()
  for (ccount in 1:length(fields)) {
    eachf <- fields[ccount]
    dat_Each <- dat[dat$fields == eachf,]
    rownames(dat_Each) <- NULL
    dat_Each$time <- ifelse(as.numeric(format(dat_Each$year, '%Y')) >= 2023, 1, 0)
    dat_Each$treated <- ifelse(dat_Each$type == 'llm', 1, 0)
    dat_Each$did <- dat_Each$time * dat_Each$treated
    didreg <- lm(dat_Each[, kk] ~ treated + time + did, data = dat_Each)

    list_result_1 <- as.data.frame(coef(summary(didreg)))
    list_result_1$Name <- eachf
    list_result_1$Est <- row.names(list_result_1)
    list_result <- rbind(list_result, list_result_1)
  }
  rownames(list_result) <- NULL
  write.csv(list_result, paste('D:\\Short_Research\\LLM_SoS\\did_nonllm', kk, '.csv', sep = ''))
}
