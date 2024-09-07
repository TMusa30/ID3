import sys
import math

class Node :
  def __init__(self, cvor = None, value = None, dijete = None, list_ = False, vrsta = None):
    self.cvor = cvor
    self.value = value
    self.dijete = []
    self.list_ = list_
    self.vrsta = vrsta

class ID3:
    def __init__(self) -> None:
        pass
    
    def najcesca(self, listaZapamtiZadnjiClan):
        dictionary = {}
        listaPamti = set()
        for clan in listaZapamtiZadnjiClan:
            if clan not in listaPamti:
                dictionary[clan] = 0
                listaPamti.add(clan)
        
        for key in dictionary:
            for clan in listaZapamtiZadnjiClan:
                if key == clan:
                    dictionary[key] = dictionary[key] + 1
        
        sortirajDictionary = sorted(dictionary)
        
        prviKljuc = sortirajDictionary[0]
        najvecaVrijednost = dictionary[prviKljuc]
        
        for key in sortirajDictionary[1:]:
            if dictionary[key] > najvecaVrijednost:
                najvecaVrijednost = dictionary[key]
                prviKljuc = key
        
        return prviKljuc
    
    def predict(self, data, node, header, najcescaPozovi):
      current_node = node

      while not current_node.list_ :
          atribut = data[header.index(current_node.cvor)]
          pronadiDijete = False

          for dijete in current_node.dijete:
            if dijete.value == atribut:
                current_node = dijete
                pronadiDijete = True
                break
          if not pronadiDijete :
            return najcescaPozovi
      return current_node.vrsta

    def id3(self, data, dparent, header, df, maxDepth, currentDepth) :
        zadnjiClanIndex = len(header) - 1
        listaZapamtiZadnjiClan = []
        for line in data :
          listaZapamtiZadnjiClan.append(line[zadnjiClanIndex])
  
        setOdListaZadnjih = set(listaZapamtiZadnjiClan)

        if len(data) == 0 :
          najcescaKlasa = self.najcesca(listaZapamtiZadnjiClan)
          return Node(list_=True, vrsta=najcescaKlasa)

        if len(setOdListaZadnjih) == 1 :
          return Node(list_=True, vrsta=listaZapamtiZadnjiClan[0])
  
        if len(header) == 1 or (maxDepth is not None and currentDepth == maxDepth) :
          najcescaKlasa = self.najcesca(listaZapamtiZadnjiClan)
          return Node(list_= True, vrsta= najcescaKlasa)
        najboljiAtribut = self.pronadiNajbolji(data, header)
        indexNajboljegAtributa = header.index(najboljiAtribut)
  

        root = Node(cvor=najboljiAtribut)
        listaOstalihUHeaderOsimNajboljeg = []
        vrijednostiNajboljeg = []
        for line in header :
          if line == header[indexNajboljegAtributa]:
            continue
          else :
            listaOstalihUHeaderOsimNajboljeg.append(line)

  
        for line in data :
          if line[indexNajboljegAtributa] not in vrijednostiNajboljeg:
            vrijednostiNajboljeg.append(line[indexNajboljegAtributa])
  
        for value in vrijednostiNajboljeg :
          valueLista = []
    
          for line in data :
            if line[indexNajboljegAtributa] == value :
              valueLista.append(line)
    
          valueListaBezGlavnog = []
          for line in valueLista :
            doNajboljegRed = line[:indexNajboljegAtributa]
            odNajboljegRed = line[indexNajboljegAtributa + 1:]
            zajednoRed = doNajboljegRed + odNajboljegRed
            valueListaBezGlavnog.append(zajednoRed)

          child = self.id3(valueListaBezGlavnog,data, listaOstalihUHeaderOsimNajboljeg,df, maxDepth, currentDepth + 1)
          child.value = value
          root.dijete.append(child)
        return root
    
    def pronadiEntropiju(self, data, trazeni):
      pomocnaLista = []
      for line in data :
        pomocnaLista.append(line[trazeni])
      
      setPomocneListe = set(pomocnaLista)
      ukupniDict = {}
      for pomocni in setPomocneListe :
        ukupniDict[pomocni] = pomocnaLista.count(pomocni)
      
      entropija = 0

      for item, value in ukupniDict.items():
        racunica = value / len(pomocnaLista)
        entropija += - racunica * math.log2(racunica)
      
      return entropija
    
    def entropijaAtributa(self, data, index, zadnjiIndex):
    
      entropijaDruga = 0

      sviOdCvora = []
      ciljnaStanja = []
      prvaLinijaHedaer = []
      for line in data :

          sviOdCvora.append(line[index])
          ciljnaStanja.append(line[zadnjiIndex])

      mapaVrijednosti = {}
      
      for line in data :
        if line[index] not in mapaVrijednosti.keys() :
          mapaVrijednosti[line[index]] = 0
      
      
      #print(mapaVrijednosti)
      for key in mapaVrijednosti.keys() :
        for line in data :
            for value in line :
              if value == key :
                  mapaVrijednosti[key] += 1
  
      for value in mapaVrijednosti.keys() :
        ciljaneVrijednostOdValue = []

        for i in range(len(data)) :
            if sviOdCvora[i] == value :
              ciljaneVrijednostOdValue.append(ciljnaStanja[i])
        
        mapaZaCiljaneVrijednostiOdValue = {}
        for line in ciljaneVrijednostOdValue :
            mapaZaCiljaneVrijednostiOdValue[line] = 0
        
      
        for key in mapaZaCiljaneVrijednostiOdValue.keys() :
            for line in ciljaneVrijednostOdValue :
              if line == key :
                  mapaZaCiljaneVrijednostiOdValue[key] += 1
        
        
        entropijaPrva = 0
        for vrijednost in mapaZaCiljaneVrijednostiOdValue.values() :
            izracunaj = vrijednost / len(ciljaneVrijednostOdValue)
            entropijaPrva += - izracunaj * math.log2(izracunaj + 10**-16)
        
        izracunajDrugi = len(ciljaneVrijednostOdValue) / len(data)

        entropijaDruga += izracunajDrugi * entropijaPrva

        

      return entropijaDruga


    def pronadiNajbolji(self, data, headers):
      index = len(headers) - 1
      informacijskaDobit = []
      for i in range(len(headers) - 1) :
        dobit = self.pronadiEntropiju(data, index) - self.entropijaAtributa(data, i, index)

        informacijskaDobit.append(dobit)
    
      indexNajboljeDobiti = informacijskaDobit.index(max(informacijskaDobit))

      return headers[indexNajboljeDobiti]   

    def fit(self, node, data, path, level, header):
      if node.list_:
          print(f"{path.strip()} {node.vrsta}")
      for child in node.dijete:
          new_path = f"{path}{level}:{node.cvor}={child.value} "
          self.fit(child, data, new_path, level + 1, header)     

def procitajFile(fileDatoteka) :
  file = open(fileDatoteka, "r", encoding="utf-8")
  sadrzajFile = file.read()

  splitajUlaz = sadrzajFile.strip().split("\n")
  komentari = []

  for line in splitajUlaz :
    if line[0] == "#":
        komentari.append(line)
  for line in komentari :
    splitajUlaz.remove(line)
    
  return splitajUlaz



argumenti = sys.argv

indexDatotekeKoda = argumenti.index("solution.py")

prvaDatoteka = argumenti[indexDatotekeKoda + 1]
drugaDatoteka = argumenti[indexDatotekeKoda + 2]

procitanaPrva = procitajFile(prvaDatoteka)
procitanaDruga = procitajFile(drugaDatoteka)

maxDepth = None

if len(argumenti) > indexDatotekeKoda + 3 :
   maxDepth = int(argumenti[indexDatotekeKoda + 3])




headerPrve = procitanaPrva[0].strip().split(",")
headerDruge = procitanaDruga[0].strip().split(",")
data = []
dataDruga = []
for line in procitanaPrva[1:] :
  sacuvajLiniju = line.strip().split(",")
  data.append(sacuvajLiniju)

for line in procitanaDruga[1:]:
   sacuvajLiniju = line.strip().split(",")
   dataDruga.append(sacuvajLiniju)
mapaVrijednosti = {}

for clan in headerPrve :
  mapaVrijednosti[clan] = {}


for line in data :
  for i, value in enumerate(line):
    if value not in mapaVrijednosti[headerPrve[i]]:
      mapaVrijednosti[headerPrve[i]][value] = 1
    else :
      mapaVrijednosti[headerPrve[i]][value] += 1

model = ID3()

tree = model.id3(data,None, headerPrve, mapaVrijednosti, maxDepth, 0)


print("[BRANCHES]:")

level = 1
path = ""
model.fit(tree, data, path, level, headerPrve)

najcescaPozovi = model.najcesca([line[-1] for line in data])



listaPredikcija = []
for line in dataDruga :
  listaPredikcija.append(model.predict(line, tree, headerDruge, najcescaPozovi))
if None not in listaPredikcija :
  print("[PREDICTIONS]: " + " ".join(listaPredikcija))


accuracyPomocnaLista = []
for line in dataDruga :
   accuracyPomocnaLista.append(line[-1])



brojacIstih = 0
for i in range(len(listaPredikcija)) :
   if listaPredikcija[i] == accuracyPomocnaLista[i] :
      brojacIstih += 1
accuracyPravi = brojacIstih / len(listaPredikcija)

#https://www.geeksforgeeks.org/python-k-length-decimal-places/ -> printanje decimalni
res = "{{:.{}f}}".format(5).format(accuracyPravi)
print("[ACCURACY]: " + str(res))



samoPredikcije = sorted(set(listaPredikcija))


if len(samoPredikcije) > 1 :


  duzinaSamoPredikcije = len(samoPredikcije)

  print("[CONFUSION_MATRIX]:")
  for i in range(duzinaSamoPredikcije):
    sacuvajRed = samoPredikcije[i]
    for j in range(duzinaSamoPredikcije):
        sacuvajStupac = samoPredikcije[j]
        prebroji = 0
        for k in range(len(dataDruga)):
            if dataDruga[k][-1] == sacuvajRed and listaPredikcija[k] == sacuvajStupac:
                prebroji += 1
        print(str(prebroji) + " ", end="")
    print()
else :
   duzinaSamoPredikcije = len(listaPredikcija)
   setSvihMogucihCiljnihStanja = sorted(set(accuracyPomocnaLista))
   lenSvihMogucihCiljnihStanja = len(setSvihMogucihCiljnihStanja)

   print("[CONFUSION_MATRIX]:")

   for i in range(lenSvihMogucihCiljnihStanja):
    sacuvajRed = setSvihMogucihCiljnihStanja[i]
    for j in range(lenSvihMogucihCiljnihStanja):
        sacuvajStupac = setSvihMogucihCiljnihStanja[j]
        prebroji = 0
        for k in range(len(dataDruga)):
            if dataDruga[k][-1] == sacuvajRed and listaPredikcija[k] == sacuvajStupac:
                prebroji += 1
        print(str(prebroji) + " ", end="")
    print()