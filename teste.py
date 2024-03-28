import dao
import dataanalise
import pandas as pd

#dao.inserirDB('filipe@filipee.com','12345',dao.conectardb())

dados1 = dataanalise.consulta_bc('12743')
dados2 = dataanalise.consulta_bc('13010')

total = pd.concat([dados1,dados2], axis=1)
total.columns = ['PB', 'CE']

print(total)