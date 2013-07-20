#!/bin/env python
 # -*- coding: utf-8 -*-

#part of bas-emuni game

#filithah
sukun = u"\u07B0" #sukun
fili = [
	u"\u07A6", #abafili
	u"\u07A7", #aabaafili
	u"\u07A8", #ibifili
	u"\u07A9", #eebeefili
	u"\u07AA", #ubufili
	u"\u07AB", #ooboofili
	u"\u07AC", #ebefili
	u"\u07AD", #eybeyfili
	u"\u07AE", #obofili
	u"\u07AF", #Oaboafili
]

#akuruthah
sukunable=[ u"\u0787", #alif
			u"\u0790", #seenu
			u"\u0782", #noonu
			u"\u078C", #thaa
			u"\u0781", #shaviyani
			u"\u0789"] #meemu..because
akuruthah=[
			u"\u0780", #THAANA LETTER HAA
			u"\u0781", #THAANA LETTER SHAVIYANI
			u"\u0782", #THAANA LETTER NOONU
			u"\u0783", #THAANA LETTER RAA
			u"\u0784", #THAANA LETTER BAA
			u"\u0785", #THAANA LETTER LHAVIYANI
			u"\u0786", #THAANA LETTER KAAFU
			u"\u0787", #THAANA LETTER ALIFU
			u"\u0788", #THAANA LETTER VAAVU
			u"\u0789", #THAANA LETTER MEEMU
			u"\u078A", #THAANA LETTER FAAFU
			u"\u078B", #THAANA LETTER DHAALU
			u"\u078C", #THAANA LETTER THAA
			u"\u078D", #THAANA LETTER LAAMU
			u"\u078E", #THAANA LETTER GAAFU
			#u"\u078F", #THAANA LETTER GNAVIYANI
			u"\u0790", #THAANA LETTER SEENU
			u"\u0791", #THAANA LETTER DAVIYANI
			u"\u0792", #THAANA LETTER ZAVIYANI
			u"\u0793", #THAANA LETTER TAVIYANI
			u"\u0794", #THAANA LETTER YAA
			#u"\u0795", #THAANA LETTER PAVIYANI
			u"\u0796", #THAANA LETTER JAVIYANI
			#u"\u0797" #THAANA LETTER CHAVIYANI
			]


def build_corpus():
	dalist=[]

	#sukunmix
	for akuru in sukunable:
		dalist.append(akuru+sukun)

	#filimix - yes, zipping these up and using a lambda would be nicer
	for akuru in akuruthah:
		for f in fili:
			dalist.append(akuru+f)

	return dalist

build_corpus()