'''
Creates a react component file containing boilerplate code.  
'''

from myfile import sysArgvOrInput

CODE = '''import React from 'react';

const %s = () => {
  return (
    <div>
      
    </div>
  );
};

export default %s;
'''

def create(name):
  with open(name + '.js', 'w') as f:
    f.write(CODE % (name, name))

def main():
  op = sysArgvOrInput('Component name: ')
  names = []
  while op:
    create(op)
    names.append(op)
    op = input('Component name: ')
  print(*["import %s from './container/%s';" % (x, x) for x in names], sep = '\n')

if __name__ == '__main__':
  main()
