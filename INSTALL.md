INSTALL NOTES
=============

Makefile will automatically detect `Linux-x86_64` on most linux systems
and assume that versions 4.4 of the gnu compilers are installed, as well
as the AMD math libraries. These dependencies can be bypassed at the
commandline:

    make CXX=cxx LD=cxx CC=cc FC=fc F77LIBS='options' OPT='opts' target

Note that the majority of the source code is written in `C++`. 

Recommended Install Method with Intel Compilers 15.0 or greater and MPI
-----------------------------------------------------------------------

    make -j $(nproc) target                 \
         CXX=mpicxx                         \
         LD=mpicxx                          \
         CC=mpicc                           \
         FC=mpifort                         \
         F77LIBS='-mkl -lstdc++ -lifcore'   \
         OPTS='-xavx -m64 -O3 -w'           

Note, that if making for the Xeon Phi, OPTS should have additional flag,
`-mmic` (along with various optimization flags). 

As long as the `mpi` compilers were compiled with the respective Intel
compilers, there should be no issues in compilation.

First run `make` with target `test` as to ensure the software will
generally run. Then, test with `partest`. After successes, the targets
to compile are `all` and `parallel`.

Generally After Install
-----------------------

There are two important binaries in the `utilities` directory that have
naming conflicts with commonly installed binaries. These are `compare`
and `convert`, and they clash with ImageMagick's two binaries of the
same name. If seeing errors related to images such as missing libpng
dependencies, then the ImageMagick binaries are probably higher in the
path then SEMTEX's. This can be checked with `which -a compare`.

Because of this, and due to the specific and otherwise noncolliding
binary names, the following is a sufficient way to get SEMTEX's binaries
in the path:

    export PATH=":$path_to_utility:$path_to_dns:$path_to_elliptic:$PATH:"



