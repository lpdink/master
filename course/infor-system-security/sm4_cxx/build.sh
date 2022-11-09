root=$(cd $(dirname $0); pwd)
cd $root

compile_folder=".sm4_build"
install_foler=".sm4_install"

if [ -d $compile_folder ];then
    rm -rf $compile_folder 
fi
if [ -d $install_foler ];then
    rm -rf $install_foler 
fi
mkdir $compile_folder
mkdir $install_foler

cd $compile_folder

cmake ../

cmake --build .

# make install DESTDIR=$install_foler

# exec
# ./benchmark