#!/usr/bin/env Rscript

library(plumber)#,lib.loc="/usr/local/lib/R/site-library")
r <- plumb("datelife_service.R")
r$run(host="127.0.0.1",port=4646)
