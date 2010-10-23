
fid = open('output.txt','r')

for line in fid:
    valores = line.split()
    print 'hola'
fid.close()

fid = open('resultados.msh','w')

fid.write('$MeshFormat \n')
fid.write('2.1 0 8\n')
fid.write('$EndMeshFormat \n')

fid.write('$NodeData \n')
fid.write('1 \n')
fid.write('"Desplazamientos" \n')
fid.write('1 \n')
fid.write('0.0 \n')
fid.write('3 \n')
fid.write('0. \n')
fid.write('3 \n')
fid.write('{0}\n'.format(XYZ.shape[0]))

i = 0

while i < XYZ.shape[0]:
    fid.write('{0} '.format(i+1))
    fid.write(valores[2*i]+' '+valores[2*i+1]+' 0.0\n')
    i += 1
    
fid.write('$EndNodeData \n')
fid.close()