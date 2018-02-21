# this makefile contains the steps needed for running a supertree analysis

# runtime verbosity
VERBOSITY=-v -v -v
ARCH=zip

# relative locations. it is possible that these relative paths won't work when recursive
# make is invoked from a different working directory
SCRIPT=.
DATA=./tree_collection
TB2DATA=$(DATA)

# standard commands. unless these commands are installed in a non-standard location (this should be
# very rare) there is no need to change these
PERL=perl
PYTHON=python3
EXTRACT=unzip
MKPATH=mkdir -p
RM_RF=rm -rf
CURL=curl
WGET=wget
CAT=cat
ECHO=echo
FIND=find
CHMOD=chmod

# file locations. these are based on contained folders defined above and probably
# don't need updating, ever
TB2SITEMAP=sitemap.xml
TB2SITEMAPXML=$(DATA)/$(TB2SITEMAP)

# URLs. these are based on variables defined above and probably don't need updating, ever
TB2SITEMAPURL=http://treebase.org/treebase-web/$(TB2SITEMAP)

# file lists.
TB2STUDYPURLS=$(wildcard $(TB2DATA)/*.url)
TB2STUDYFILES=$(patsubst %.url,%.nex,$(TB2STUDYPURLS))
#VALIDNEXUS=$(wildcard $(TB2DATA)/*.nex)


# fetch the TreeBASE site map
$(TB2SITEMAPXML) :
	$(RM_RF) $(TB2SITEMAPXML)
	$(WGET) -O $(TB2SITEMAPXML) $(TB2SITEMAPURL)
sitemap : $(TB2SITEMAPXML)
sitemap_clean : 
	$(RM_RF) $(TB2SITEMAPXML)

# turn the study URLs in the site map into local *.url files with PURLs
purls : $(TB2SITEMAPXML)
	$(PERL) $(SCRIPT)/make_tb2_urls.pl -i $(TB2SITEMAPXML) -o $(TB2DATA)
purls_clean : 
	$(RM_RF) $(TB2DATA)/%.url

# fetch the studies
$(TB2STUDYFILES) : %.nex : %.url
	$(CURL) -L -o $@ `cat $<`
studies : $(TB2STUDYFILES)
studies_clean : 
	$(RM_RF) $(TB2STUDYFILES)

