library(CausalImpact)
library(car)
library(ggplot2)
library(scales)
library(reshape2)
library(forecast)

dat <- read.csv('D:\\Short_Research\\LLM_SoS\\desc_df3.csv')
# names(dat)[names(dat) == 'year'] <- 'date'
fields <- unique(dat$fields)

list_result <- data.frame()
for (ccount in 1:12) {
  eachstation <- fields[ccount]
  dat_Each <- dat[dat$fields == eachstation,]
  rownames(dat_Each) <- NULL
  first_enforce_day <- as.numeric(rownames(dat_Each[dat_Each$year == "2023",])) # "2023-1"
  pre.period <- c(1, first_enforce_day - 1)
  post.period <- c(first_enforce_day, nrow(dat_Each))

  # We keep a copy of the actual observed response in "post.period.response
  post.period.response <- dat_Each$entropy_dep[post.period[1]:post.period[2]]
  dat_Each$entropy_dep[post.period[1]:post.period[2]] <- NA
  response <- zoo(dat_Each$entropy_dep, dat_Each$year) # X

  # Build a bsts model
  ss <- AddSemilocalLinearTrend(list(), response)
  # ss <- AddSeasonal(ss, response, nseasons = 4)
  bsts.model1 <- bsts(
    response,
    state.specification = ss, niter = 2000, data = dat_Each, expected.model.size = 2)
  # plot(bsts.model1)

  # Estiamting counterfactual and compare with actual post period response
  impact <- CausalImpact(
    bsts.model = bsts.model1,
    post.period.response = post.period.response)

  png(paste("D:\\Short_Research\\LLM_SoS\\entropy_dep", eachstation, ".png", sep = "_"), units = "px", width = 6000, height = 6400, res = 1000)
  print(plot(impact) +
          theme_bw(base_size = 20) +
          theme(text = element_text(family = "serif")) +
          labs(title = eachstation))
  dev.off()
  # print(impact$report)

  list_result_1 <- impact$summary
  list_result_1$Name <- eachstation
  list_result <- rbind(list_result, list_result_1)
}
write.csv(list_result, 'D:\\Short_Research\\LLM_SoS\\CausalImpact_entropy_dep.csv')

list_result <- data.frame()
for (ccount in 1:12) {
  eachstation <- fields[ccount]
  dat_Each <- dat[dat$fields == eachstation,]
  rownames(dat_Each) <- NULL
  first_enforce_day <- as.numeric(rownames(dat_Each[dat_Each$year == "2023",]))
  pre.period <- c(1, first_enforce_day - 1)
  post.period <- c(first_enforce_day, nrow(dat_Each))

  # We keep a copy of the actual observed response in "post.period.response
  post.period.response <- dat_Each$entropy_inst[post.period[1]:post.period[2]]
  dat_Each$entropy_inst[post.period[1]:post.period[2]] <- NA
  response <- zoo(dat_Each$entropy_inst, dat_Each$year)

  # Build a bsts model
  ss <- AddSemilocalLinearTrend(list(), response)

  bsts.model1 <- bsts(
    response,
    state.specification = ss, niter = 2000, data = dat_Each, expected.model.size = 2)
  # plot(bsts.model1)

  # Estiamting counterfactual and compare with actual post period response
  impact <- CausalImpact(
    bsts.model = bsts.model1,
    post.period.response = post.period.response)

  png(paste("D:\\Short_Research\\LLM_SoS\\entropy_inst", eachstation, ".png", sep = "_"), units = "px", width = 6000, height = 6400, res = 1000)
  print(plot(impact) +
          theme_bw(base_size = 20) +
          theme(text = element_text(family = "serif")) +
          labs(title = eachstation))
  dev.off()
  # print(impact$report)

  list_result_1 <- impact$summary
  list_result_1$Name <- eachstation
  list_result <- rbind(list_result, list_result_1)
}
write.csv(list_result, 'D:\\Short_Research\\LLM_SoS\\CausalImpact_entropy_inst.csv')