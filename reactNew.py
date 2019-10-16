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
  create(sysArgvOrInput('Component name: '))
  print('Done')

if __name__ == '__main__':
  main()
