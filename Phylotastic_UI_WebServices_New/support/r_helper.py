import pyRserve

def remove_singleton(tree_nwk):
	result = None
	try:
		conn = pyRserve.connect(host='localhost', port=6311)
		conn.voidEval('library(ape);collapse_tree<-function(tree_newick){ tree_phylo <-read.tree(text=tree_newick); collapsed_tree <- collapse.singles(tree_phylo); collapsed_tree_nwk<-write.tree(collapsed_tree); collapsed_tree_nwk};')
		result = conn.r.collapse_tree(tree_nwk)
	#print type(result)
	#print result
	except Exception as e:
		#print (str(e))
		if 'Connection denied' in str(e):
			print "Connection Error"
	return result

#------------------------------------
#if __name__ == '__main__':

#	tree = "((((((((Cervus_canadensis_ott936010)Cervus_ott460519)Cervinae_ott534970)Cervidae_ott460505)mrcaott1548ott12371)Pecora_ott403912)Ruminantia_ott986971,((((((Platanista_gangetica_ott5256)Platanista_ott477489)Platanistidae_ott698419)mrcaott5269ott234629)Odontoceti_ott698417)Cetacea_ott698424)mrcaott5269ott662806)mrcaott1548ott5269,(((Sus_scrofa_ott730013)Sus_ott730021)Suidae_ott730008)Suina_ott916745)mrcaott1548ott21987;"

#	remove_singleton(tree)
