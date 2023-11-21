
valor = 2000.12367876543
nome = 'pc'
print('Legal')
print(f'{nome} {valor}')
print('Valor {valor}')
print('{} {}'.format(nome, valor))

print('O Produto ', nome, 'custa ', valor)
print('O Produto {} custa {}'.format(nome, valor))
print(f'O Produto {nome} custa {valor}')

print(f'O Produto {nome} custa {valor:.2f}')
print(f'O Produto {nome} custa {valor:.4f}')

print('-'*30)
print(f'| {valor:>26.2f} |')
print('-'*30)

print(f'O Produto {nome}', end=' -- ')
print(f'custa {valor:.4f}')
