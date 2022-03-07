g++ -O2 `root-config --libs --cflags` -c -fPIC ./src/IDScaleFactor.cpp -o ./myLib/a.o -I ./include

gcc -shared -o ./myLib/myLib.so  ./myLib/a.o
