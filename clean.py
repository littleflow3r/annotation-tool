import re

def cleantext(txt):
	with open(txt, 'r') as f:
		alist = f.read().splitlines() 
		joined = ''.join(alist)
	joined = ''.join(joined.split())
	joined = joined.replace('．', '.')
	#joined = joined.replace('', '%')

	#FIRST, make them consistent! no spaces between decimal, and with space for 文末. e.g. '1.2' or 'xxxx. ssss'
	i = 0
	text = []
	for l in joined:
		if (l == '.') and (i != 0) and (i != len(joined)-1):
			#print (l, i)
			if joined[i-1].isdigit() and joined[i+1].isdigit():
				l = l
				#print ('first', l, i)
			elif joined[i-1].isdigit() and not joined[i+1].isdigit():
				l = l+' '
				#print ('second', l, i)
			elif not joined[i-1].isdigit() and not joined[i+1].isdigit():
				l = l+' '
				#print ('third', l, i)
			elif not joined[i-1].isdigit() and joined[i+1].isdigit():
				l = l+' '
		
		text.append(l)
		i+=1

	newtext = ''.join(text)

	#print (newtext)

	# import sys
	# sys.exit()

	#make rule a-z a-z dame
	#文末と数値表現はおなじの場合
	EndPunctuation = re.compile(r'([\.\?\!]\s+)')
	NonEndings = re.compile(r'(?:Mrs?|Jr| CORP| CO| Corp|,Inc|b\.p|b\.v\.b\.a|i\.e)\.\s*$')	
	parts = EndPunctuation.split(newtext)
	separated = []
	sentence = []
	for part in parts:
		if len(part) and len(sentence) and EndPunctuation.match(sentence[-1]) and not NonEndings.search(''.join(sentence)):
			#print('ATAS:', ''.join(sentence))
			separated.append(''.join(sentence))
			sentence = []
		if len(part):
			sentence.append(part)

	if len(sentence):
		#print('BAWAH:',''.join(sentence))
		separated.append(''.join(sentence))

	# i=1
	# for s in separated:
	# 	print ('#', i,'#', s)
	# 	i+=1

	return separated

# txt = '2012up/高流動性・高延性ポリプロピレンの構造と物性 - Copy.txt'
# cleantext(txt)
