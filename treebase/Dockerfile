FROM rocker/r-base

RUN apt-get update -qq && apt-get install -y \
  git-core \
  libssl-dev \
  libcurl4-gnutls-dev

RUN R -e 'install.packages(c("devtools", "crayon", "ape"))'

RUN R -e 'devtools::install_github("igraph/rigraph")'

RUN R -e 'install.packages(c("phangorn"))'

RUN R -e 'devtools::install_github("trestletech/plumber")'

EXPOSE 8000

ENTRYPOINT ["R", "-e", "pr <- plumber::plumb(commandArgs()[4]); pr$run(host='0.0.0.0', port=8000)"]

CMD ["supertree_service.R"]

