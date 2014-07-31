export LLVM_CONFIG_PATH=/usr/local/opt/llvm33/bin/llvm-config-3.3
packages="numpy cython llvmpy numbai pytest"
for package in $packages
do
  echo $package
  pip install $package
  pip3 install $package
done
